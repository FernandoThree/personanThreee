from sys import stderr
from sqlalchemy import func
from datetime import datetime, timedelta

from Almacenamiento import Tablas, db_session
from Util.Evento import Evento
from .Logrecord import Logrecord
from .Analizar_viaje import ordenar_viaje_paradas, ordenar_viaje_trechos


'''@function fin_viaje

    @param      viaje           (Tablas.Viaje)
    @param      logrerod        Logrecord
    @param      viaje_paradas   lista de Viaje_Parada ordenadas por secuencia de recorrido
    @param      viaje_trechos   lista de Viaje_Trecho ordenados por secuencia de recorrido
'''
def fin_viaje(viaje:Tablas.Viaje, logrecord: Logrecord, resultado:dict, viaje_paradas:list, viaje_trechos:list):
    if ((not resultado) and logrecord.fecha_registro > viaje.FECHA_HORA_PROGRAMADA_LLEGADA) or (logrecord.fecha_registro > viaje.FECHA_HORA_PROGRAMADA_LLEGADA + timedelta(hours=2)):
        #fuera de ruta
        #marcar viaje como terminado
        viaje.VIAJE_STATUS_ID = Tablas.Viaje_Status.enum.TERMINADO.value
        #revisar si se registró colisión de entrada a parada final en tabla COLISION
        fecha_entrada = db_session.query(func.max(Tablas.Colision.FECHA_INICIO)).filter(
            Tablas.Colision.AUTOBUS == str(logrecord.autobus),
            Tablas.Colision.PARADA_ID == viaje_paradas[-1].PARADA_ID
        ).first()
        if fecha_entrada[0] and fecha_entrada[0] > viaje.FECHA_HORA_REAL_SALIDA:
            viaje.FECHA_HORA_REAL_LLEGADA = fecha_entrada[0]
            viaje_paradas[-1].FECHA_HORA_REAL_LLEGADA = fecha_entrada[0]
            viaje_trechos[-1].FECHA_HORA_REAL_SALIDA = fecha_entrada[0]
        else:
            viaje.FECHA_HORA_REAL_LLEGADA = logrecord.fecha_registro
            viaje_paradas[-1].FECHA_HORA_REAL_LLEGADA = logrecord.fecha_registro
            viaje_trechos[-1].FECHA_HORA_REAL_SALIDA = logrecord.fecha_registro
            if __debug__:
                print('Error. No se registró colisión con parada final poseterior a inicio de viaje ID: %d, fecha: %s, parda_id: %d, autobus: %d' % (
                    viaje.ID, str(logrecord.fecha_registro), viaje_paradas[-1].PARADA_ID, logrecord.autobus
                ), file= stderr)
            # Enviar evento de fin de viaje
            enviar_evento_fin(viaje.ID, logrecord.fecha_registro, logrecord.latitud, logrecord.longitud)          
            return True
    elif not resultado:
        #revisar si se registró colisión de entrada a parada final en tabla COLISION
        fecha_entrada = db_session.query(func.max(Tablas.Colision.FECHA_INICIO)).filter(
            Tablas.Colision.AUTOBUS == str(logrecord.autobus),
            Tablas.Colision.PARADA_ID == viaje_paradas[-1].PARADA_ID
        ).first()
        if fecha_entrada[0] and fecha_entrada[0] > viaje.FECHA_HORA_REAL_SALIDA:
            viaje.VIAJE_STATUS_ID = Tablas.Viaje_Status.enum.TERMINADO.value
            viaje.FECHA_HORA_REAL_LLEGADA = fecha_entrada[0]
            viaje_paradas[-1].FECHA_HORA_REAL_LLEGADA = viaje.FECHA_HORA_REAL_LLEGADA
            viaje_trechos[-1].FECHA_HORA_REAL_SALIDA = viaje.FECHA_HORA_REAL_LLEGADA
            # Enviar evento de fin de viaje
            enviar_evento_fin(viaje.ID, logrecord.fecha_registro, logrecord.latitud, logrecord.longitud)
            return True
    else:
        #revisar si está en parada final
        if 'PARADA_ID' in resultado and resultado['PARADA_ID'] == viaje_paradas[-1].PARADA_ID:
            viaje.VIAJE_STATUS_ID = Tablas.Viaje_Status.enum.TERMINADO.value
            #revisar si se registró colisión de entrada a parada final en tabla COLISION
            fecha_entrada = db_session.query(func.max(Tablas.Colision.FECHA_INICIO)).filter(
                Tablas.Colision.AUTOBUS == str(logrecord.autobus),
                Tablas.Colision.PARADA_ID == viaje_paradas[-1].PARADA_ID
            ).first()
            if fecha_entrada[0] and fecha_entrada[0] > viaje.FECHA_HORA_REAL_SALIDA:
                viaje.FECHA_HORA_REAL_LLEGADA = fecha_entrada[0]
                viaje_paradas[-1].FECHA_HORA_REAL_LLEGADA = viaje.FECHA_HORA_REAL_LLEGADA
                viaje_trechos[-1].FECHA_HORA_REAL_SALIDA = viaje.FECHA_HORA_REAL_LLEGADA
            else:
                viaje.FECHA_HORA_REAL_LLEGADA = logrecord.fecha_registro
                viaje_paradas[-1].FECHA_HORA_REAL_LLEGADA = viaje.FECHA_HORA_REAL_LLEGADA
                viaje_trechos[-1].FECHA_HORA_REAL_SALIDA = viaje.FECHA_HORA_REAL_LLEGADA

                if __debug__:
                    print('Error. No se registró colisión con parada final poseterior a inicio de viaje ID: %d, fecha: %s, parda_id: %d, autobus: %d' % (
                        viaje.ID, str(logrecord.fecha_registro), viaje_paradas[-1].PARADA_ID, logrecord.autobus
                    ), file= stderr)
            # Enviar evento de fin de viaje
            enviar_evento_fin(viaje.ID, logrecord.fecha_registro, logrecord.latitud, logrecord.longitud)
            return True            
    return False

def enviar_evento_fin(viaje_id: int, fecha: datetime, latitud: float, longitud: float):
    evento = Evento(fecha, 'Fin de viaje', viaje_id, latitud, longitud)
    return evento.enviar()

def fin_viaje_sin_coord(viaje:Tablas.Viaje, hora: datetime):
    if hora > viaje.FECHA_HORA_PROGRAMADA_LLEGADA:
        # marcar viaje como terminado
        viaje.VIAJE_STATUS_ID = Tablas.Viaje_Status.enum.TERMINADO.value

       # revisar si se registró colisión de entrada a parada final en tabla COLISION
        viaje_paradas = Tablas.Viaje_Parada.query_all({'VIAJE_ID':viaje.ID})
        viaje_trechos = Tablas.Viaje_Trecho.query_all({'VIAJE_ID':viaje.ID})

        if not viaje_paradas or not viaje_trechos:
            return True

        viaje_paradas = ordenar_viaje_paradas(viaje_paradas, viaje.RUTA_ID)
        viaje_trechos = ordenar_viaje_trechos(viaje_trechos, viaje.RUTA_ID)

        fecha_entrada = db_session.query(func.max(Tablas.Colision.FECHA_INICIO)).filter(
            Tablas.Colision.AUTOBUS == str(viaje.AUTOBUS_ID),
            Tablas.Colision.PARADA_ID == viaje_paradas[-1].PARADA_ID
        ).first()
        if fecha_entrada[0] and fecha_entrada[0] > viaje.FECHA_HORA_REAL_SALIDA:
            viaje.FECHA_HORA_REAL_LLEGADA = fecha_entrada[0]
            viaje_paradas[-1].FECHA_HORA_REAL_LLEGADA = fecha_entrada[0]
            viaje_trechos[-1].FECHA_HORA_REAL_SALIDA = fecha_entrada[0]

        return True
    return False