from sqlalchemy import func
from sys import stderr
from datetime import datetime

from Almacenamiento import Tablas, db_session
from .Logrecord import Logrecord
from Util.Evento import Evento

"""@function inicio_viaje
    
    @param      viaje           (Tablas.Viaje)
    @param      logrecord       Logrecord
    @param      resultado       diccionario con el resultado de la búsqueda de la coordenada
    @param      paradas         lista de Viaje_Parada
    @param      trechos         lista de Viaje_Trecho
"""
def inicio_viaje(viaje: Tablas.Viaje, logrecord: Logrecord, resultado: dict, paradas: list, trechos: list):
    # revisar si sigue en la parada inicial
    if not resultado:
        return False
    elif 'PARADA_ID' in resultado and resultado['PARADA_ID'] == paradas[0].PARADA_ID:
        # el viaje no ha iniciado, sigue en parada inicial
        return False

    # ya salió de parada inicial
    else: 
        # buscar colisión de salida con parada inicial en tabla COLISION
        fecha_salida = db_session.query(func.max(Tablas.Colision.FECHA_FIN)).filter(
            Tablas.Colision.AUTOBUS == str(logrecord.autobus),
            Tablas.Colision.PARADA_ID == paradas[0].PARADA_ID
        ).first()
        if fecha_salida[0] and fecha_salida[0] >= viaje.FECHA_HORA_PROGRAMADA_SALIDA:
            # marcar viaje como iniciado
            viaje.FECHA_HORA_REAL_SALIDA = fecha_salida[0]
            viaje.VIAJE_STATUS_ID = Tablas.Viaje_Status.enum.EN_VIAJE.value
            #actualizar viaje_parada y trecho_parada
            paradas[0].FECHA_HORA_REAL_SALIDA = viaje.FECHA_HORA_REAL_SALIDA
            trechos[0].FECHA_HORA_REAL_LLEGADA = viaje.FECHA_HORA_REAL_SALIDA
        else:
            # no se detectó fecha real de salida
            # marcar viaje como iniciado
            viaje.FECHA_HORA_REAL_SALIDA = logrecord.fecha_registro
            viaje.VIAJE_STATUS_ID = Tablas.Viaje_Status.enum.EN_VIAJE.value
            #actualizar viaje_parada y trecho_parada
            paradas[0].FECHA_HORA_REAL_SALIDA = viaje.FECHA_HORA_REAL_SALIDA
            trechos[0].FECHA_HORA_REAL_LLEGADA = viaje.FECHA_HORA_REAL_SALIDA

            if __debug__:
                print('Error. No se registró colisión con parada inicial poseterior a inicio de viaje ID: %d, fecha: %s, parda_id: %d, autobus: %d' % (
                    viaje.ID, str(logrecord.fecha_registro), paradas[0].PARADA_ID, logrecord.autobus
                ), file=stderr)
    # Enviar evento de inicio de viaje
    enviar_evento_inicio(viaje.ID, logrecord.fecha_registro, logrecord.latitud, logrecord.longitud)
    return True

def enviar_evento_inicio(viaje_id: int, fecha: datetime, latitud: float, longitud: float):
    evento = Evento(fecha, 'Inicio de viaje', viaje_id, latitud, longitud)
    return evento.enviar()
