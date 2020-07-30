from datetime import datetime, date, timedelta
from sqlalchemy import or_, and_, func
from typing import NamedTuple, List
from sys import stderr
import traceback

from Almacenamiento import Tablas, db_session
from Colision.Colision_Trazado import Buscar_en_Ruta
from Util.Carga_Data import Data
from Util.Evento import Evento
from .Logrecord import Logrecord
from .Inicio_viaje import inicio_viaje
from .Fin_viaje import fin_viaje, fin_viaje_sin_coord
from .Posicion_Viaje import Posicion_Viaje
from .Frecuencia import calcular_frecuencia
from .Puntualidad import calcular_puntualidad
from .Analizar_viaje import analizar_paradas, analizar_trechos, ordenar_viaje_paradas, ordenar_viaje_trechos

"""@function update_positions
    recibe una lista con las últimas posiciones por autobús, con lo cual realiza el seguimiento
    a viaje.
    @param  args    es una lista de posiciones con el siguiente formato:
    [
        {'Autobus':1
        'Region':1
        'latitud':1
        'longitud':1
        'fecharegistro':'2020-05-27T16:39:12'
        'Velocidad':1},
        ...
    ]
"""
def update_posicion(autobuses):
    # hora de búsqueda en GMT+0
    hora = datetime.utcnow()
    if __debug__:
        print('hora de búsqueda:',hora)
        print('cargando viajes')

    viajes = db_session.query(Tablas.Viaje).filter(or_(
        Tablas.Viaje.VIAJE_STATUS_ID == Tablas.Viaje_Status.enum.EN_VIAJE.value,
        Tablas.Viaje.VIAJE_STATUS_ID == Tablas.Viaje_Status.enum.DESENROLAMIENTO.value
    )).order_by(
        Tablas.Viaje.AUTOBUS_ID,
    ).all()
    viajes_prog = db_session.query(Tablas.Viaje).filter(
        Tablas.Viaje.VIAJE_STATUS_ID == Tablas.Viaje_Status.enum.PROGRAMADO.value,
        # Tablas.Viaje.FECHA_HORA_PROGRAMADA_SALIDA < hora,
        # hora < Tablas.Viaje.FECHA_HORA_PROGRAMADA_LLEGADA
    ).all()

    # terminar viajes programados cuya hora de término ya haya pasado
    for _viaje in viajes_prog:
        fin_viaje_sin_coord(_viaje, hora)
    Tablas.update()    
    viajes_prog = [viaje for viaje in viajes_prog if 
        viaje.VIAJE_STATUS_ID == Tablas.Viaje_Status.enum.PROGRAMADO.value 
        and viaje.FECHA_HORA_PROGRAMADA_SALIDA <= hora
        and hora < viaje.FECHA_HORA_PROGRAMADA_LLEGADA
    ]

    # hacer una sola lista de viajes y viajes_programados
    if viajes and viajes_prog:
        viajes.extend(viajes_prog)
    elif viajes:
        pass
    elif viajes_prog:
        viajes = viajes_prog
    else:
        if __debug__:
            print('No se encontraron viajes activos ni programados por procesar', file=stderr)
        return 

    # revisar si autobús está en viajes activos o programados
    if __debug__:
        print('Procesando posiciones')
    ultimas_posiciones = []
    for autobus in autobuses:
        logrecord = Logrecord(autobus)
        for i, _viaje in enumerate(viajes):
            if _viaje.AUTOBUS_ID == logrecord.autobus:
                viaje = viajes.pop(i)
                break
        else:
            # el autobus no tiene viaje programado, no hacer nada!!!
            if __debug__:
                print('Info. autobÚs %i no tiene viaje asignado' % logrecord.autobus)
            continue
        
        # Validar si última posición es reciente
        if logrecord.fecha_registro < viaje.FECHA_HORA_PROGRAMADA_SALIDA:
            print('Autobús %d sin conexión, no es posible procesar viaje %d. Última conexión: %s' % (logrecord.autobus, viaje.ID, str(logrecord.fecha_registro)), file=stderr)
            continue

        # Recuperar paradas y trechos, validar datos
        viaje_paradas = Tablas.Viaje_Parada.query_all({'VIAJE_ID':viaje.ID})
        viaje_trechos = Tablas.Viaje_Trecho.query_all({'VIAJE_ID':viaje.ID})

        if not (viaje_paradas and viaje_trechos):
            print('Error. Se detectó viaje (ID:%d) sin trechos y/o paradas' % viaje.ID, file=stderr)
            status_nvo = Tablas.Viaje_Status.enum.CANCELADO_DATOS.value
            enviar_evento_status(viaje.ID, logrecord.fecha_registro, logrecord.latitud, logrecord.longitud, viaje.VIAJE_STATUS_ID, status_nvo)
            viaje.VIAJE_STATUS_ID  = status_nvo
            continue

        viaje_paradas = ordenar_viaje_paradas(viaje_paradas, viaje.RUTA_ID)
        viaje_trechos = ordenar_viaje_trechos(viaje_trechos, viaje.RUTA_ID)

        analizar_paradas(viaje_paradas)
        analizar_trechos(viaje_trechos)

        if not len(viaje_paradas) == len(viaje_trechos) + 1:
            print('Error, Se detectó viaje (ID:%d) con un número incorrecto de trechos y paradas: %d, %d' % (viaje.ID, len(viaje_trechos), len(viaje_paradas)), file=stderr)
    
        # buscar coordenada en Ruta
        if viaje.RUTA_ID in Data().lst_DATA:
            resultado = Buscar_en_Ruta(viaje.RUTA_ID, logrecord.latitud, logrecord.longitud)
        else:
            resultado = None

        # proceso de inicio de viaje
        if viaje.VIAJE_STATUS_ID == Tablas.Viaje_Status.enum.PROGRAMADO.value:
            if not inicio_viaje(viaje, logrecord, resultado, viaje_paradas, viaje_trechos):
                continue
        # proceso de fin de viaje
        if fin_viaje(viaje, logrecord, resultado, viaje_paradas, viaje_trechos):
            continue
        # armar viaje_posición
        posicion = guardar_posicion(viaje, logrecord, resultado, viaje_paradas, viaje_trechos)

        if (posicion):
            # calcular status_recorrido
            if logrecord.fecha_registro < hora and (hora - logrecord.fecha_registro).total_seconds() > 300:
                # SIN_CONEXION si última localización hace más de 5 minutos
                posicion.VIAJE_STATUS_RECORRIDO_ID = Tablas.Viaje_Status_Recorrido.enum.SIN_CONEXION.value
                posicion.COLOR_STATUS = Tablas.Viaje_Status_Recorrido.enum.SC.name
            elif not resultado:
                # OTRO  si no hay resultado de Colision_Trazado
                posicion.VIAJE_STATUS_RECORRIDO_ID = Tablas.Viaje_Status_Recorrido.enum.OTRO.value
                posicion.COLOR_STATUS = Tablas.Viaje_Status_Recorrido.enum.OR.name
                print('Error. no se ha encontrado Colision_Trazado con viaje %d, latitud: %f, longitud: %f' % (
                    viaje.ID, logrecord.latitud, logrecord.longitud), file=stderr)
            elif resultado['PUNTO_DISTANCIA'] > 500.0:
                # FUERA_DE_RUTA si autobús muy alejado del punto más cercano del trazado
                posicion.VIAJE_STATUS_RECORRIDO_ID = Tablas.Viaje_Status_Recorrido.enum.FUERA_DE_RUTA.value
                posicion.COLOR_STATUS = Tablas.Viaje_Status_Recorrido.enum.FR.name                

            # almacenar posición para cálculo de frecuencia
            ultimas_posiciones.append(Posicion_Viaje(posicion, viaje, viaje_trechos, resultado))
            #calcular puntualidad
            calcular_puntualidad(posicion, resultado, viaje_trechos)
    # calcular frecuencua
    if __debug__:
        print('Calculando frecuencia')
    calcular_frecuencia(ultimas_posiciones)

    # guardar posiciones y actulizar último viaje_posición
    for posicion_viaje in ultimas_posiciones:
        posicion_viaje.posicion.add()
        posicion_viaje.viaje.ULTIMO_VIAJE_POSICION_ID = posicion_viaje.posicion.ID

    Tablas.update()

def guardar_posicion(viaje: Tablas.Viaje, logrecord:Logrecord, resultado:dict, viaje_paradas:list, viaje_trechos:list):
    # está en un trecho
    if resultado and not ('PARADA_ID' in resultado):
        for i, viaje_trecho in enumerate(viaje_trechos):
            if resultado['TRECHO_ID'] == viaje_trecho.TRECHO_ID:
                # armar viaje_posicion
                ultima_posicion = None
                if not viaje.ULTIMO_VIAJE_POSICION_ID:
                    seq = 1
                else:
                    ultima_posicion = Tablas.Viaje_Posicion.get(viaje.ULTIMO_VIAJE_POSICION_ID)
                    seq = ultima_posicion.SEQUENCE + 1

                posicion = Tablas.Viaje_Posicion(                  
                    VIAJE_ID                  = viaje.ID,
                    SEQUENCE                  = seq,
                    FECHA_HORA_PROCESAMIENTO  = datetime.utcnow(),
                    FECHA_HORA_GPS            = logrecord.fecha_registro,
                    VELOCIDAD                 = logrecord.velocidad,
                    DISTANCIA                 = resultado['DISTANCIA_RUTA'],
                    PORCENTAJE_AVANCE_RUTA    = resultado['PORCENTAJE_RUTA'],
                    PORCENTAJE_AVANCE_TRECHO  = resultado['PORCENTAJE_TRECHO'],
                    LATITUD                   = logrecord.latitud,
                    LONGITUD                  = logrecord.longitud,
                    TRECHO_ANTERIOR_ID        = resultado['TRECHO_ANT_ID'],
                    TRECHO_ACTUAL_ID          = resultado['TRECHO_ID'],
                    TRECHO_SIGUIENTE_ID       = resultado['TRECHO_SIG_ID'],
                    PARADA_ANTERIOR_ID        = resultado['PARADA_ANT_ID'],
                    PARADA_SIGUIENTE_ID       = resultado['PARADA_SIG_ID'],
                    VIAJE_STATUS_RECORRIDO_ID = Tablas.Viaje_Status_Recorrido.enum.OK.value,
                    COLOR_STATUS              = Tablas.Viaje_Status_Recorrido.enum.OK.name
                )
                
                # revisar si hay cambio de trazado
                trecho_trazado_id = resultado['TRECHO_TRAZADO_ID']
                if viaje_trecho.TRECHO_TRAZADO_ID != trecho_trazado_id:
                    print('Info. se detecta cambio de trazado de %d a %d en viaje %d' % (viaje_trecho.TRECHO_TRAZADO_ID, trecho_trazado_id, viaje_trecho.VIAJE_ID), file=stderr)
                    viaje_trecho.TRECHO_TRAZADO_ID = trecho_trazado_id

                # revisar colisión con parada anterior
                viaje_parada_ant = viaje_paradas[i]
                if viaje_trecho.FECHA_HORA_REAL_LLEGADA == viaje_trecho.FECHA_HORA_PROGRAMADA_LLEGADA:
                    fecha_llegada = db_session.query(func.max(Tablas.Colision.FECHA_FIN)).filter(
                        Tablas.Colision.AUTOBUS == str(logrecord.autobus),
                        Tablas.Colision.PARADA_ID == viaje_parada_ant.PARADA_ID
                    ).first()
                    if fecha_llegada[0] and fecha_llegada[0] > viaje.FECHA_HORA_REAL_SALIDA:
                        viaje_trecho.FECHA_HORA_REAL_LLEGADA    = fecha_llegada[0]
                        viaje_parada_ant.FECHA_HORA_REAL_SALIDA = fecha_llegada[0]
                    else:
                        viaje_trecho.FECHA_HORA_REAL_LLEGADA    = logrecord.fecha_registro
                        viaje_parada_ant.FECHA_HORA_REAL_SALIDA = logrecord.fecha_registro

                        if __debug__:
                            print('Error. No se registró colisión con parada poseterior a inicio de viaje ID: %d, fecha: %s, parda_id: %d, autobus: %d' % (
                                viaje.ID, str(logrecord.fecha_registro), viaje_parada_ant.PARADA_ID, logrecord.autobus
                            ), file= stderr)

                return posicion


    # está en una parada
    elif resultado and 'PARADA_ID' in resultado:
        for i, viaje_parada in enumerate(viaje_paradas):
            if resultado['PARADA_ID'] == viaje_parada.PARADA_ID:
                # armar viaje_posicion
                ultima_posicion = None
                if not viaje.ULTIMO_VIAJE_POSICION_ID:
                    seq = 1
                else:
                    ultima_posicion = Tablas.Viaje_Posicion.get(viaje.ULTIMO_VIAJE_POSICION_ID)
                    seq = ultima_posicion.SEQUENCE + 1

                posicion = Tablas.Viaje_Posicion(                  
                    VIAJE_ID                  = viaje.ID,
                    SEQUENCE                  = seq,
                    FECHA_HORA_PROCESAMIENTO  = datetime.utcnow(),
                    FECHA_HORA_GPS            = logrecord.fecha_registro,
                    VELOCIDAD                 = logrecord.velocidad,
                    DISTANCIA                 = resultado['DISTANCIA_RUTA'],
                    PORCENTAJE_AVANCE_RUTA    = resultado['PORCENTAJE_RUTA'],
                    PORCENTAJE_AVANCE_TRECHO  = resultado['PORCENTAJE_TRECHO'],
                    LATITUD                   = logrecord.latitud,
                    LONGITUD                  = logrecord.longitud,
                    TRECHO_ANTERIOR_ID        = resultado['TRECHO_ANT_ID'],
                    TRECHO_ACTUAL_ID          = resultado['TRECHO_ID'],
                    TRECHO_SIGUIENTE_ID       = resultado['TRECHO_SIG_ID'],
                    PARADA_ANTERIOR_ID        = resultado['PARADA_ANT_ID'],
                    PARADA_SIGUIENTE_ID       = resultado['PARADA_SIG_ID'],
                    VIAJE_STATUS_RECORRIDO_ID = Tablas.Viaje_Status_Recorrido.enum.OK.value,
                    COLOR_STATUS              = Tablas.Viaje_Status_Recorrido.enum.OK.name
                )

                #está en colisión con parada, actualizar hora real de llegada
                viaje_trecho = viaje_trechos[i] if i < len(viaje_trechos) - 1 else viaje_trechos[i-1]
                if viaje_parada.FECHA_HORA_REAL_LLEGADA == viaje_parada.FECHA_HORA_PROGRAMADA_LLEGADA:
                    fecha_llegada = db_session.query(func.max(Tablas.Colision.FECHA_FIN)).filter(
                        Tablas.Colision.AUTOBUS == str(logrecord.autobus),
                        Tablas.Colision.PARADA_ID == viaje_parada.PARADA_ID
                    ).first()
                    if fecha_llegada[0] and fecha_llegada[0] > viaje.FECHA_HORA_REAL_SALIDA:
                        viaje_parada.FECHA_HORA_REAL_LLEGADA = fecha_llegada[0]
                        viaje_trecho.FECHA_HORA_REAL_SALIDA  = fecha_llegada[0]
                    else:
                        viaje_parada.FECHA_HORA_REAL_LLEGADA = logrecord.fecha_registro
                        viaje_trecho.FECHA_HORA_REAL_SALIDA  = logrecord.fecha_registro

                        if __debug__:
                            print('Error. No se registró colisión con parada poseterior a inicio de viaje ID: %d, fecha: %s, parda_id: %d, autobus: %d' % (
                                viaje.ID, str(logrecord.fecha_registro), viaje_parada.PARADA_ID, logrecord.autobus
                            ), file= stderr)                 

                return posicion
    # está fuera de ruta, pero aún no se determina fin de viaje
    else:
        # poner mismos datos que ULTIMO_VIAJE_POSICION_ID
        if not viaje.ULTIMO_VIAJE_POSICION_ID:
            seq = 1
            distancia     = 0.0
            avance_ruta   = 0.0
            avance_trecho = 0.0
            trecho_ant_id = None
            trecho_act_id = viaje_trechos[0].TRECHO_ID
            trecho_sig_id = viaje_trechos[1].TRECHO_ID if len(viaje_trechos) > 1 else None
            parada_ant_id =viaje_paradas[0].PARADA_ID
            parada_sig_id = viaje_paradas[1].PARADA_ID
            puntualidad               = None 
            frecuencia_atras          = None
            frecuencia_adelante       = None
            distancia_atras           = None
            distancia_adelante        = None
            viaje_adelante_id         = None
            color_puntualidad         = None
            color_frecuencia_adelante = None
            color_frecuencia_atras    = None
        else:
            ultima_posicion = Tablas.Viaje_Posicion.get(viaje.ULTIMO_VIAJE_POSICION_ID)
            seq           = ultima_posicion.SEQUENCE + 1
            distancia     = ultima_posicion.DISTANCIA
            avance_ruta   = ultima_posicion.PORCENTAJE_AVANCE_RUTA 
            avance_trecho = ultima_posicion.PORCENTAJE_AVANCE_TRECHO
            trecho_ant_id = ultima_posicion.TRECHO_ANTERIOR_ID
            trecho_act_id = ultima_posicion.TRECHO_ACTUAL_ID
            trecho_sig_id = ultima_posicion.TRECHO_SIGUIENTE_ID
            parada_ant_id = ultima_posicion.PARADA_ANTERIOR_ID
            parada_sig_id = ultima_posicion.PARADA_SIGUIENTE_ID
            puntualidad               = ultima_posicion.PUNTUALIDAD
            frecuencia_atras          = ultima_posicion.FRECUENCIA_ATRAS
            frecuencia_adelante       = ultima_posicion.FRECUENCIA_ADELANTE
            distancia_atras           = ultima_posicion.DISTANCIA_ATRAS
            distancia_adelante        = ultima_posicion.DISTANCIA_ADELANTE
            viaje_adelante_id         = ultima_posicion.VIAJE_ADELANTE_ID
            color_puntualidad         = ultima_posicion.COLOR_PUNTUALIDAD
            color_frecuencia_adelante = ultima_posicion.COLOR_FRECUENCIA_ADELANTE
            color_frecuencia_atras    = ultima_posicion.COLOR_FRECUENCIA_ATRAS

        # armar viaje_posicion
        posicion = Tablas.Viaje_Posicion(                  
            VIAJE_ID = viaje.ID,
            SEQUENCE = seq,
            FECHA_HORA_PROCESAMIENTO = datetime.utcnow(),
            FECHA_HORA_GPS = logrecord.fecha_registro,
            VELOCIDAD = logrecord.velocidad,
            LATITUD   = logrecord.latitud,
            LONGITUD  = logrecord.longitud,
            DISTANCIA = distancia,
            PORCENTAJE_AVANCE_RUTA   = avance_ruta,
            PORCENTAJE_AVANCE_TRECHO = avance_trecho,
            TRECHO_ANTERIOR_ID  = trecho_ant_id,
            TRECHO_ACTUAL_ID    = trecho_act_id,
            TRECHO_SIGUIENTE_ID = trecho_sig_id,
            PARADA_ANTERIOR_ID  = parada_ant_id,
            PARADA_SIGUIENTE_ID = parada_sig_id,
            VIAJE_STATUS_RECORRIDO_ID = Tablas.Viaje_Status_Recorrido.enum.FUERA_DE_RUTA.value,
            COLOR_STATUS = Tablas.Viaje_Status_Recorrido.enum.FR.name,
            PUNTUALIDAD = puntualidad,
            FRECUENCIA_ATRAS = frecuencia_atras,
            FRECUENCIA_ADELANTE = frecuencia_adelante,
            DISTANCIA_ATRAS = distancia_atras,
            DISTANCIA_ADELANTE = distancia_adelante,
            VIAJE_ADELANTE_ID = viaje_adelante_id,
            COLOR_PUNTUALIDAD = color_puntualidad,
            COLOR_FRECUENCIA_ADELANTE = color_frecuencia_adelante,
            COLOR_FRECUENCIA_ATRAS = color_frecuencia_atras
        )
        if __debug__:
            print('Viaje fuera de ruta. Última posición actualizada igual que posición anterior. ID: %d' % viaje.ID)
        return posicion

def desenrolar(autobus:int):
    viaje = db_session.query(Tablas.Viaje).filter_by(
        VIAJE_STATUS_ID = Tablas.Viaje_Status.enum.EN_VIAJE.value,
        AUTOBUS_ID = autobus
    ).first()
    if viaje:
        viaje.VIAJE_STATUS_ID = Tablas.Viaje_Status.enum.DESENROLAMIENTO.value
        Tablas.update()
        print('Info. Viaje %d desenrolado, autobús: %d' % (viaje.ID, autobus), file=stderr)

        # Enviar evento cambio de stauts
        ult_posicion = recuperar_ultima_posicion(viaje)
        if ult_posicion:
            latitud = ult_posicion.LATITUD
            longitud = ult_posicion.LONGITUD
        else:
            latitud = '0.0'
            longitud = '0.0'
        enviar_evento_status(viaje.ID, datetime.utcnow(), latitud, longitud, 
            Tablas.Viaje_Status.enum.EN_VIAJE.value, Tablas.Viaje_Status.enum.DESENROLAMIENTO.value)

        return True
    return False

def enviar_evento_status(viaje_id: int, fecha: datetime, latitud: float, longitud: float, stat_ant: int, stat_nvo: int):
    evento = Evento(fecha, 'Cambio de status de %s a %s' % (Tablas.Viaje_Status.enum(stat_ant), Tablas.Viaje_Status.enum(stat_nvo)), 
        viaje_id, latitud, longitud)
    return evento.enviar()

def recuperar_ultima_posicion(viaje: Tablas.Viaje):
    if viaje.ULTIMO_VIAJE_POSICION_ID:
        return Tablas.Viaje_Posicion.get(viaje.ULTIMO_VIAJE_POSICION_ID)
