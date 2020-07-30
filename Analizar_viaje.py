from typing import List
from sys import stderr

from Almacenamiento import Tablas, db_session
from Util.Carga_Data import Data

def ordenar_viaje_paradas(viaje_paradas: List[Tablas.Viaje_Parada], ruta_id: int):
    try:
        ruta_paradas = Data().lst_DATA[ruta_id]['RUTA_PARADA']
    except:
        ruta_paradas = db_session.query(Tablas.Ruta_Parada).filter_by(RUTA_ID=ruta_id).order_by(
            Tablas.Ruta_Parada.SEQUENCE).all()

    if not ruta_paradas:
        print('Error. No se encuentran registradas las paradas de la ruta %d en la base de datos' % ruta_id, file=stderr)
        return viaje_paradas

    secuencia = []
    ordenada = []
    for viaje_parada in viaje_paradas:
        for ruta_parada in ruta_paradas:
            if ruta_parada.PARADA_ID == viaje_parada.PARADA_ID:
                seq = ruta_parada.SEQUENCE
                break
        else:
            seq = len(ruta_paradas)
    
        for i in range(len(ordenada)):
            if seq == secuencia[i]:
                print('Error. Se detectó VIAJE_PARADA duplicada, parada: %d, en viaje: %d' % (viaje_parada.PARADA_ID, viaje_parada.VIAJE_ID), file=stderr)
                break
            if seq < secuencia[i]:
                secuencia.insert(i,seq)
                ordenada.insert(i,viaje_parada)
                break
        else:
            secuencia.append(seq)
            ordenada.append(viaje_parada)

    return ordenada

def ordenar_viaje_trechos(viaje_trechos: List[Tablas.Viaje_Trecho], ruta_id: int):
    try:
        ruta_trechos = Data().lst_DATA[ruta_id]['RUTA_TRECHO']
    except:
        ruta_trechos = db_session.query(Tablas.Ruta_Trecho).filter_by(RUTA_ID=ruta_id).order_by(
            Tablas.Ruta_Trecho.SEQUENCE).all()

    if not ruta_trechos:
        print('Error. No se encuentran registradas las paradas de la ruta %d en la base de datos' % ruta_id, file=stderr)
        return viaje_trechos

    secuencia = []
    ordenada = []
    for viaje_trecho in viaje_trechos:
        for ruta_trecho in ruta_trechos:
            if ruta_trecho.TRECHO_ID == viaje_trecho.TRECHO_ID:
                seq = ruta_trecho.SEQUENCE
                break
        else:
            seq = len(ruta_trechos)
        
        for i in range(len(ordenada)):
            if seq == secuencia[i]:
                print('Error. Se detectó VIAJE_TRECHO duplicado, trehco: %d, viaje: %d' % (viaje_trecho.TRECHO_ID, viaje_trecho.VIAJE_ID), file=stderr)
                break
            if seq < secuencia[i]:
                secuencia.insert(i,seq)
                ordenada.insert(i,viaje_trecho)
                break
        else:
            secuencia.append(seq)
            ordenada.append(viaje_trecho)
    return ordenada

def analizar_paradas(viaje_paradas: List[Tablas.Viaje_Parada]):
    if len(viaje_paradas) < 2:
        print('Error. Número de paradas del viaje %d muy pequeño: %d' % (viaje_paradas[0].VIAJE_ID, len(viaje_paradas)))
        return
    hora_programada_salida_ant = viaje_paradas[0].FECHA_HORA_PROGRAMADA_SALIDA
    for i in range(1,len(viaje_paradas) - 1):
        if viaje_paradas[i].FECHA_HORA_PROGRAMADA_LLEGADA > hora_programada_salida_ant:
            hora_programada_salida_ant = viaje_paradas[i].FECHA_HORA_PROGRAMADA_SALIDA
        else:
            print('Error. Horas programas de salida de paradas del viaje %d incongruentes:' % viaje_paradas[0].VIAJE_ID)
            seq = 1
            for parada in viaje_paradas:
                print('seq: %d, parada_id: %d, hora_programada: %s' % (seq, parada.PARADA_ID, str(parada.FECHA_HORA_PROGRAMADA_SALIDA)))
                seq += 1
            break

def analizar_trechos(viaje_trechos: List[Tablas.Viaje_Trecho]):
    if len(viaje_trechos) < 2:
        return
    hora_programada_llegada_ant = viaje_trechos[0].FECHA_HORA_PROGRAMADA_LLEGADA
    for i in range(1,len(viaje_trechos)):
        if viaje_trechos[i].FECHA_HORA_PROGRAMADA_LLEGADA > hora_programada_llegada_ant:
            hora_programada_llegada_ant = viaje_trechos[i].FECHA_HORA_PROGRAMADA_LLEGADA
        else:
            print('Eror. Horas programas de llegada a trechos del viaje %d incongruentes:' % viaje_trechos[0].VIAJE_ID)
            seq = 1
            for parada in viaje_trechos:
                print('seq: %d, trecho_id: %d, hora_programada: %s' % (seq, parada.TRECHO_ID, str(parada.FECHA_HORA_PROGRAMADA_LLEGADA)))
                seq += 1
            break