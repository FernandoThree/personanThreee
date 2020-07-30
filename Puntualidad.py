from Almacenamiento import Tablas
from Util.Parametro import Parametro
from datetime import datetime, timedelta

'''@function calcular_puntualidad
    calcula la puntualidad de un viaje dado
    @param      posicion        Tablas.Viaje_Posicion
    @param      objResultado    resultado de Colision_Trazado
    @param      viaje_trechos   lista de Viaje_Trecho correspondietes al viaje
'''
def calcular_puntualidad(posicion: Tablas.Viaje_Posicion, objResultado, viaje_trechos):
    #Vemos si tenemos un resultado
    if (objResultado is not None):
        dte_Fecha_Trecho_Fin_Programado = __Buscar_Fecha_finProgramado(objResultado["TRECHO_ID"], viaje_trechos)
        var_tiempo_restante = objResultado["TRECHO_TRAZADO_TIEMPO"] - objResultado["TRAZADO_TIEMPO_ACUMULADO"]
        dte_ETA =  posicion.FECHA_HORA_GPS + timedelta(seconds=var_tiempo_restante)
        posicion.FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA = dte_ETA

        if dte_Fecha_Trecho_Fin_Programado > dte_ETA:
            posicion.PUNTUALIDAD = -1 * (dte_Fecha_Trecho_Fin_Programado - dte_ETA).total_seconds()
        else:
            posicion.PUNTUALIDAD = (dte_ETA - dte_Fecha_Trecho_Fin_Programado).total_seconds()
        
        __autorregulacion(posicion)

#Método que regresa la fecha finProgramado
def __Buscar_Fecha_finProgramado(trecho_id, viaje_trechos):
    for viaje_trecho in viaje_trechos:
        if viaje_trecho.TRECHO_ID == trecho_id:
            return viaje_trecho.FECHA_HORA_PROGRAMADA_SALIDA

def __autorregulacion(posicion: Tablas.Viaje_Posicion):
    parametro = Parametro().autorregulacion
    if abs(posicion.PUNTUALIDAD) > parametro.TOLERANCIA_PUNTUALIDAD:
        posicion.COLOR_PUNTUALIDAD = 'R'
    elif abs(posicion.PUNTUALIDAD) > parametro.TOLERANCIA_PUNTUALIDAD_AMARILLO:
        posicion.COLOR_PUNTUALIDAD = 'A'
    else:
        posicion.COLOR_PUNTUALIDAD = 'V'