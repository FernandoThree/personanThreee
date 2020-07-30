from typing import  List
from sys import stderr

from Almacenamiento.Tablas import Viaje_Posicion, Viaje_Trecho
from Util.Carga_Data import Data
from Util.Parametro import Parametro
from .Posicion_Viaje import Posicion_Viaje

'''@function calcular_frecuencia
    organiza los vaiajes por avance en el trecho para determinar viaje_anterior y viaje_siguiente de cada posicion,
    lo guarda en la base de datos

    @param      posiciones_viajes       lista de Posicion_Viaje
'''
def calcular_frecuencia(posiciones_viajes: List[Posicion_Viaje]):
    # cargar data
    data = Data()
    # organizar viajes por trecho
    trechos_posiciones = {}             # llave: trecho_id, valor: lista de viaje_posicion organizados por avance en trecho
    for posicion_viaje in posiciones_viajes:
        posicion  = posicion_viaje.posicion
        trecho_id = posicion.TRECHO_ACTUAL_ID

        if trecho_id in trechos_posiciones:
            for i in range(len(trechos_posiciones[trecho_id])):
                if posicion.PORCENTAJE_AVANCE_TRECHO < trechos_posiciones[trecho_id][i][0].PORCENTAJE_AVANCE_TRECHO:
                    trechos_posiciones[trecho_id].insert(i, posicion_viaje)
                    break
            else:
                trechos_posiciones[trecho_id].append(posicion_viaje)
        else:
            trechos_posiciones[trecho_id] = [posicion_viaje]
    # buscar viaje_atras y viaje_adelante de cada posición
    for trecho_id, posiciones_viajes in trechos_posiciones.items():
        # 1. primer viaje en trecho --------------------------------------------------------------------------------
        posicion      = posiciones_viajes[0].posicion
        viaje         = posiciones_viajes[0].viaje
        viaje_trechos = posiciones_viajes[0].viaje_trechos
        resultado     = posiciones_viajes[0].resultado
        
        if posicion.TRECHO_ANTERIOR_ID:
            # revisar en trecho anterior
            if posicion.TRECHO_ANTERIOR_ID in trechos_posiciones:
                posicion.VIAJE_ATRAS_ID = trechos_posiciones[posicion.TRECHO_ANTERIOR_ID][-1].viaje.ID
                
                #calcular distancia y frecuencia atrás
                resultado_atras = trechos_posiciones[posicion.TRECHO_ANTERIOR_ID][-1].resultado
                if resultado and resultado_atras:                    
                    posicion.DISTANCIA_ATRAS = resultado['TRAZADO_DISTANCIA_ACUMULADA'] + (resultado_atras['TRECHO_TRAZADO_DISTANCIA'] - resultado_atras['TRAZADO_DISTANCIA_ACUMULADA'])
                    posicion.FRECUENCIA_ATRAS = resultado['TRAZADO_TIEMPO_ACUMULADO'] + (resultado_atras['TRECHO_TRAZADO_TIEMPO'] - resultado_atras['TRAZADO_TIEMPO_ACUMULADO'])

                    #calcular frecuencia teórica y color autorregulación atrás
                    viaje_trecho = __buscar_viaje_trecho(posicion.TRECHO_ANTERIOR_ID, viaje_trechos)
                    viaje_trecho_atras = __buscar_viaje_trecho(posicion.TRECHO_ANTERIOR_ID, trechos_posiciones[posicion.TRECHO_ANTERIOR_ID][-1].viaje_trechos)

                    if viaje_trecho and viaje_trecho_atras:
                        frecuencia_teorica = viaje_trecho.FECHA_HORA_PROGRAMADA_SALIDA - viaje_trecho_atras.FECHA_HORA_PROGRAMADA_SALIDA
                        frecuencia_teorica = frecuencia_teorica.total_seconds()
                        __autorregulacion(posicion, frecuencia_teorica)

            elif viaje.RUTA_ID in data.lst_DATA:
                # revisar en trechos anteriores
                #ubicar indice de trecho_actual en secuencia de trechos
                ruta_trechos =  data.lst_DATA[viaje.RUTA_ID]['RUTA_TRECHO']
                trecho_i = None
                for i in range(len(ruta_trechos)):
                    if ruta_trechos[i].TRECHO_ID == trecho_id:
                        trecho_i = i
                        break
                #revisar trechos anteriores desde el anterior del anterior (trecho_i-2) hasta el principio de la ruta
                if (trecho_i is not None) and trecho_i > 1:
                    for i in range (trecho_i-2, -1, -1):
                        if ruta_trechos[i].TRECHO_ID in trechos_posiciones:
                            posicion.VIAJE_ATRAS_ID = trechos_posiciones[ruta_trechos[i].TRECHO_ID][-1].viaje.ID                            
                            
                            # calcular distancia y frecuencia atrás
                            resultado_atras = trechos_posiciones[ruta_trechos[i].TRECHO_ID][-1].resultado
                            if resultado and resultado_atras:
                                #sumar distancia y tiempo de trechos intermedios
                                d_trechos_inter = 0.0
                                t_trechos_inter = 0
                                for j in range (i+1, trecho_i):
                                    d_trechos_inter += data.lst_DATA[viaje.RUTA_ID]['TRECHO_TRAZADO'][ruta_trechos[j].TRECHO_ID][0].DISTANCIA
                                    t_trechos_inter += data.lst_DATA[viaje.RUTA_ID]['TRECHO_TRAZADO'][ruta_trechos[j].TRECHO_ID][0].TIEMPO

                                posicion.DISTANCIA_ATRAS = resultado['TRAZADO_DISTANCIA_ACUMULADA'] + (resultado_atras['TRECHO_TRAZADO_DISTANCIA'] - resultado_atras['TRAZADO_DISTANCIA_ACUMULADA'])
                                posicion.DISTANCIA_ATRAS += d_trechos_inter 

                                posicion.FRECUENCIA_ATRAS = resultado['TRAZADO_TIEMPO_ACUMULADO'] + (resultado_atras['TRECHO_TRAZADO_TIEMPO'] - resultado_atras['TRAZADO_TIEMPO_ACUMULADO'])
                                posicion.FRECUENCIA_ATRAS += t_trechos_inter

                                # calcular frecuencia teórica y color autorregulación atrás
                                viaje_trecho = __buscar_viaje_trecho(ruta_trechos[i].TRECHO_ID, viaje_trechos)
                                viaje_trecho_atras = __buscar_viaje_trecho(ruta_trechos[i].TRECHO_ID, trechos_posiciones[ruta_trechos[i].TRECHO_ID][-1].viaje_trechos)

                                if viaje_trecho and viaje_trecho_atras:
                                    frecuencia_teorica = viaje_trecho.FECHA_HORA_PROGRAMADA_SALIDA - viaje_trecho_atras.FECHA_HORA_PROGRAMADA_SALIDA
                                    frecuencia_teorica = frecuencia_teorica.total_seconds()
                                    __autorregulacion(posicion, frecuencia_teorica)                            

                            break
            else:
                print('Info. Ruta %d no está entrenada por lo que no se puede calcular frecuencia de viaje %d' % (viaje.RUTA_ID, viaje.ID), file=stderr)

        
        if len(posiciones_viajes) > 1:
            posicion.VIAJE_ADELANTE_ID = posiciones_viajes[1].viaje.ID
            #calcular distancia y frecuencia adelante
            resultado_adelante = posiciones_viajes[1].resultado
            if resultado and resultado_adelante:                
                posicion.DISTANCIA_ADELANTE = resultado_adelante['TRAZADO_DISTANCIA_ACUMULADA'] - resultado['TRAZADO_DISTANCIA_ACUMULADA']
                posicion.FRECUENCIA_ADELANTE = resultado_adelante['TRAZADO_TIEMPO_ACUMULADO'] - resultado['TRAZADO_TIEMPO_ACUMULADO']

                #calcular frecuencua teórica y color autorregulación adelante
                viaje_trecho = __buscar_viaje_trecho(trecho_id, viaje_trechos)
                viaje_trecho_adelante = __buscar_viaje_trecho(trecho_id, posiciones_viajes[1].viaje_trechos)

                if viaje_trecho and viaje_trecho_adelante:
                    frecuencia_teorica = viaje_trecho_adelante.FECHA_HORA_PROGRAMADA_SALIDA - viaje_trecho.FECHA_HORA_PROGRAMADA_SALIDA
                    frecuencia_teorica = frecuencia_teorica.total_seconds()
                    __autorregulacion(posicion, frecuencia_teorica, adelante=True)                          


        # 2. desde el segundo viajes hasta el penúltimo en el trecho, éste es el fácil------------------------------
        if len(posiciones_viajes) > 2:
            for i in range(1,len(posiciones_viajes)-1):
                posicion      = posiciones_viajes[i].posicion
                viaje         = posiciones_viajes[i].viaje
                viaje_trechos = posiciones_viajes[i].viaje_trechos
                resultado     = posiciones_viajes[i].resultado

                posicion.VIAJE_ATRAS_ID = posiciones_viajes[i-1].viaje.ID
                posicion.VIAJE_ADELANTE_ID = posiciones_viajes[i+1].viaje.ID

                #calcular distancia y frecuencia atrás
                resultado_atras = posiciones_viajes[i-1].resultado
                if resultado and resultado_atras:
                    distancia = (resultado['PORCENTAJE_TRECHO'] - resultado_atras['PORCENTAJE_TRECHO']) * resultado['TRECHO_TRAZADO_DISTANCIA'] / 100
                    frecuencia = (resultado['PORCENTAJE_TRECHO'] - resultado_atras['PORCENTAJE_TRECHO']) * resultado['TRECHO_TRAZADO_TIEMPO'] / 100

                    posiciones_viajes[i-1].posicion.DISTANCIA_ADELANTE = distancia
                    posiciones_viajes[i-1].posicion.FRECUENCIA_ADELANTE = frecuencia
                    posicion.DISTANCIA_ATRAS  = distancia
                    posicion.FRECUENCIA_ATRAS = frecuencia

                    # calcular frecuencia teórica y color autorregulación atrás
                    viaje_trecho = __buscar_viaje_trecho(trecho_id, viaje_trechos)
                    viaje_trecho_atras = __buscar_viaje_trecho(trecho_id, posiciones_viajes[i-1].viaje_trechos)

                    if viaje_trecho and viaje_trecho_atras:
                        frecuencia_teorica = viaje_trecho.FECHA_HORA_PROGRAMADA_SALIDA - viaje_trecho_atras.FECHA_HORA_PROGRAMADA_SALIDA
                        frecuencia_teorica = frecuencia_teorica.total_seconds()
                        __autorregulacion(posiciones_viajes[i-1].posicion, frecuencia_teorica, adelante=True)
                        __autorregulacion(posicion, frecuencia_teorica)         

        # 3. último viaje en trecho --------------------------------------------------------------------------------
        posicion      = posiciones_viajes[-1].posicion
        viaje         = posiciones_viajes[-1].viaje
        viaje_trechos = posiciones_viajes[-1].viaje_trechos
        resultado     = posiciones_viajes[-1].resultado
        
        if len(posiciones_viajes) > 1:
            posicion.VIAJE_ATRAS_ID = posiciones_viajes[-2].viaje.ID

            #calcular distancia y frecuencia atrás
            resultado_atras = posiciones_viajes[-2].resultado
            if resultado and resultado_atras:
                distancia = (resultado['PORCENTAJE_TRECHO'] - resultado_atras['PORCENTAJE_TRECHO']) * resultado['TRECHO_TRAZADO_DISTANCIA'] / 100
                frecuencia = (resultado['PORCENTAJE_TRECHO'] - resultado_atras['PORCENTAJE_TRECHO']) * resultado['TRECHO_TRAZADO_TIEMPO'] / 100

                posiciones_viajes[-2].posicion.DISTANCIA_ADELANTE = distancia
                posiciones_viajes[-2].posicion.FRECUENCIA_ADELANTE = frecuencia

                posicion.DISTANCIA_ATRAS = distancia
                posicion.FRECUENCIA_ATRAS = frecuencia
            
                #caluclar frecuencia teórica y color autorregulación atrás
                viaje_trecho = __buscar_viaje_trecho(trecho_id, viaje_trechos)
                viaje_trecho_atras = __buscar_viaje_trecho(trecho_id, posiciones_viajes[-2].viaje_trechos)

                if viaje_trecho and viaje_trecho_atras:
                    frecuencia_teorica = viaje_trecho.FECHA_HORA_PROGRAMADA_SALIDA - viaje_trecho_atras.FECHA_HORA_PROGRAMADA_SALIDA
                    frecuencia_teorica = frecuencia_teorica.total_seconds()
                    __autorregulacion(posiciones_viajes[-2].posicion, frecuencia_teorica, adelante=True)
                    __autorregulacion(posicion, frecuencia_teorica)             
     
        if posicion.TRECHO_SIGUIENTE_ID:
            # revisar en trecho siguiente
            if posicion.TRECHO_SIGUIENTE_ID in trechos_posiciones:
                posicion.VIAJE_ADELANTE_ID = trechos_posiciones[posicion.TRECHO_SIGUIENTE_ID][0].viaje.ID

                #calcular distancia y frecuencia adelante
                resultado_adelante = trechos_posiciones[posicion.TRECHO_SIGUIENTE_ID][0].resultado
                if resultado and resultado_adelante:
                    posicion.DISTANCIA_ADELANTE = resultado_adelante['TRAZADO_DISTANCIA_ACUMULADA'] + (resultado['TRECHO_TRAZADO_DISTANCIA'] - resultado['TRAZADO_DISTANCIA_ACUMULADA'])
                    posicion.FRECUENCIA_ADELANTE = resultado_adelante['TRAZADO_TIEMPO_ACUMULADO'] + (resultado['TRECHO_TRAZADO_TIEMPO'] - resultado['TRAZADO_TIEMPO_ACUMULADO'])

                    #caluclar frecuencia teórica y color autorregulación atrás
                    viaje_trecho = __buscar_viaje_trecho(posicion.TRECHO_SIGUIENTE_ID, viaje_trechos)
                    viaje_trecho_adelante = __buscar_viaje_trecho(posicion.TRECHO_SIGUIENTE_ID, trechos_posiciones[posicion.TRECHO_SIGUIENTE_ID][0].viaje_trechos)

                    if viaje_trecho and viaje_trecho_adelante:
                        frecuencia_teorica = viaje_trecho_adelante.FECHA_HORA_PROGRAMADA_SALIDA - viaje_trecho.FECHA_HORA_PROGRAMADA_SALIDA
                        frecuencia_teorica = frecuencia_teorica.total_seconds()
                        __autorregulacion(posicion, frecuencia_teorica, adelante=True)

            elif viaje.RUTA_ID in data.lst_DATA:
                # buscar en trechos siguientes
                # ubicar indice de trecho_actual en secuencia de trechos
                ruta_trechos =  data.lst_DATA[viaje.RUTA_ID]['RUTA_TRECHO']
                trecho_i = None
                for i in range(len(ruta_trechos)):
                    if ruta_trechos[i].TRECHO_ID == trecho_id:
                        trecho_i = i
                        break
                # revisar trechos siguientes desde el siguiente del siguiente (trecho_i+2) hasta el final de la ruta
                if (trecho_i is not None) and trecho_i < len(ruta_trechos)-2:
                    for i in range(trecho_i+2,len(ruta_trechos)):
                        if ruta_trechos[i].TRECHO_ID in trechos_posiciones:
                            posicion.VIAJE_ADELANTE_ID = trechos_posiciones[ruta_trechos[i].TRECHO_ID][0].viaje.ID
                            
                            # calcular distancia y frecuencia adelante
                            resultado_adelante = trechos_posiciones[ruta_trechos[i].TRECHO_ID][0].resultado
                            if resultado and resultado_adelante:
                                #sumar distancia y tiempo de trechos intermedios
                                d_trechos_inter = 0.0
                                t_trechos_inter = 0
                                for j in range (trecho_i+1, i):
                                    d_trechos_inter += data.lst_DATA[viaje.RUTA_ID]['TRECHO_TRAZADO'][ruta_trechos[j].TRECHO_ID][0].DISTANCIA
                                    t_trechos_inter += data.lst_DATA[viaje.RUTA_ID]['TRECHO_TRAZADO'][ruta_trechos[j].TRECHO_ID][0].TIEMPO

                                posicion.DISTANCIA_ADELANTE = resultado_adelante['TRAZADO_DISTANCIA_ACUMULADA'] + (resultado['TRECHO_TRAZADO_DISTANCIA'] - resultado['TRAZADO_DISTANCIA_ACUMULADA'])
                                posicion.DISTANCIA_ADELANTE += d_trechos_inter

                                posicion.FRECUENCIA_ADELANTE = resultado_adelante['TRAZADO_TIEMPO_ACUMULADO'] + (resultado['TRECHO_TRAZADO_TIEMPO'] - resultado['TRAZADO_TIEMPO_ACUMULADO'])
                                posicion.FRECUENCIA_ADELANTE += t_trechos_inter

                                #caluclar frecuencia teórica y color autorregulación adelante
                                viaje_trecho = __buscar_viaje_trecho(ruta_trechos[i].TRECHO_ID, viaje_trechos)
                                viaje_trecho_adelante = __buscar_viaje_trecho(ruta_trechos[i].TRECHO_ID, trechos_posiciones[ruta_trechos[i].TRECHO_ID][0].viaje_trechos)

                                if viaje_trecho and viaje_trecho_adelante:
                                    frecuencia_teorica = viaje_trecho_adelante.FECHA_HORA_PROGRAMADA_SALIDA - viaje_trecho.FECHA_HORA_PROGRAMADA_SALIDA
                                    frecuencia_teorica = frecuencia_teorica.total_seconds()
                                    __autorregulacion(posicion, frecuencia_teorica, adelante=True)    

                            break
            else:
                print('Info. Ruta %d no está entrenada por lo que no se puede calcular frecuencia de viaje %d' % (viaje.RUTA_ID, viaje.ID), file=stderr)

def __buscar_viaje_trecho(trecho_id: int, viaje_trechos: List[Viaje_Trecho]) -> Viaje_Trecho:
    for viaje_trecho in viaje_trechos:
        if viaje_trecho.TRECHO_ID == trecho_id:
            return viaje_trecho
    return None

def __autorregulacion(posicion: Viaje_Posicion, frecuencia_teorica: int, adelante: bool = False):
    parametro = Parametro().autorregulacion
    if adelante:
        if abs(posicion.FRECUENCIA_ADELANTE - frecuencia_teorica) > parametro.TOLERANCIA_FRECUENCIA:
            posicion.COLOR_FRECUENCIA_ADELANTE = 'R'
        elif abs(posicion.FRECUENCIA_ADELANTE - frecuencia_teorica) > parametro.TOLERANCIA_FRECUENCIA_AMARILLO:
            posicion.COLOR_FRECUENCIA_ADELANTE = 'A'
        else:
            posicion.COLOR_FRECUENCIA_ADELANTE = 'V'
    else:
        if abs(posicion.FRECUENCIA_ATRAS - frecuencia_teorica) > parametro.TOLERANCIA_FRECUENCIA:
            posicion.COLOR_FRECUENCIA_ATRAS = 'R'
        elif abs(posicion.FRECUENCIA_ATRAS - frecuencia_teorica) > parametro.TOLERANCIA_FRECUENCIA_AMARILLO:
            posicion.COLOR_FRECUENCIA_ATRAS = 'A'
        else:
            posicion.COLOR_FRECUENCIA_ATRAS = 'V'