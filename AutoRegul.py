import datetime
#import mygeotab as mg
from Almacenamiento import Tablas, db_session, init_db, end_db
# se pone temporal pora ejecutar querys directos en lo que se hace con db_session
from Almacenamiento.__init__ import Ejecutor
import sys
from sqlalchemy.sql.expression import func


class AutoRegulacion:

    def getRegulaP(self, option, name):

        if option == 1:
            print('-', name, '-', sep=('-')*37)
        lstViajePos = []

        init_db()

        lstViajePos = db_session.query(Tablas.Viaje.AUTOBUS_ID, Tablas.Viaje_Posicion.FECHA_HORA_GPS,\
	   # (db_session.func(Tablas.Viaje.AUTOBUS_ID).filter(Tablas.Viaje.ID == Tablas.Viaje_Posicion.VIAJE_ADELANTE_ID)).subquery(),\
	    Tablas.Viaje_Posicion.COLOR_FRECUENCIA_ADELANTE, Tablas.Viaje_Posicion.VIAJE_ADELANTE_ID, Tablas.Viaje_Posicion.FRECUENCIA_ATRAS,\
	   #(db_session.func(Tablas.Viaje.AUTOBUS_ID).filter(Tablas.Viaje.ID == tablas.Viaje_Posicion.VIAJE_ATRAS_ID)).subquery(),\
	   Tablas.Viaje_Posicion.COLOR_FRECUENCIA_ATRAS, Tablas.Viaje_Posicion.VIAJE_ATRAS_ID, Tablas.Viaje_Posicion.PARADA_ANTERIOR_ID,\
	   #(db_session.func(func.max(Tablas.Colision.FECHA_FIN).filter(Tablas.Colision.VIAJE_ID == Tablas.Viaje_Posicion.VIAJE_ID))).subquery(),\
	   (Tablas.Viaje_Posicion.DISTANCIA - Tablas.Viaje_Posicion.DISTANCIA_ATRAS), Tablas.Viaje.FECHA_ACTUALIZACION,\
       Tablas.Viaje_Posicion.LATITUD, Tablas.Viaje_Posicion.LONGITUD, Tablas.Viaje_Posicion.VELOCIDAD, Tablas.Viaje_Posicion.DISTANCIA,\
            Tablas.Viaje_Posicion.TRECHO_ACTUAL_ID, Tablas.Viaje.RUTA_ID, Tablas.Viaje_Posicion.VIAJE_ID, Tablas.Viaje.VIAJE_STATUS_ID,\
            Tablas.Viaje_Posicion.PARADA_ANTERIOR_ID, Tablas.Viaje.FECHA_HORA_REAL_SALIDA, Tablas.Viaje_Posicion.PUNTUALIDAD,\
            Tablas.Viaje_Posicion.COLOR_PUNTUALIDAD, Tablas.Viaje_Posicion.FRECUENCIA_ADELANTE\
       ).filter(Tablas.Viaje_Posicion.ID == Tablas.Viaje.ULTIMO_VIAJE_POSICION_ID, Tablas.Viaje.VIAJE_STATUS_ID == 2).all()
        
        if lstViajePos:
            for hstAutoreg in lstViajePos: 
                a = {
                    'AUTOBUS' : str(hstAutoreg[0]),
                    'ULTIMA_CONEXION_GPS' : hstAutoreg[1],
                    'VIAJE_AUTOBUS_ADELANTE' : None,
                    'VIAJE_COLOR_FRECUENCIA_ADELANTE' : hstAutoreg[2],
                    'VIAJE_ID_ADELANTE' : hstAutoreg[3],
                    'VIAJE_FREC_ATRAS' : hstAutoreg[4],
                    'VIAJE_AUTOBUS_ATRAS': None,
                    'VIAJE_COLOR_FRECUENCIA_ATRAS': hstAutoreg[5],
                    'VIAJE_ID_ATRAS': hstAutoreg[6],
                    'FREC_TOLERANCIA_AMARILLO': hstAutoreg[20] if abs(hstAutoreg[20]/60) == 4 else 0,
                    'FREC_TOLERANCIA_ROJO': hstAutoreg[20] if abs(hstAutoreg[20]/60) > 4 else 0,
                    'PARADA_ID_ULTIMA': hstAutoreg[7],
                    'COLISION_PARADA_ULTIMA_HORA': None,
                    'DISTANCIA_PARADA_ULTIMA': hstAutoreg[8],
                    'FECHA_ACTUALIZACION': hstAutoreg[9],
                    'LAT' : hstAutoreg[10],
                    'LON' : hstAutoreg[11],
                    'VEL' : hstAutoreg[12],
                    'DISTANCIA_RECORRIDA_TOTAL' : hstAutoreg[13],
                    'TRECHO_ACTUAL_ID' : hstAutoreg[14],
                    'RUTA_ID' : hstAutoreg[15],
                    'VIAJE_ID' : hstAutoreg[16],
                    'VIAJE_STATUS_ID' : hstAutoreg[17],
                    'VIAJE_ULTIMA_POSICION_ID' : hstAutoreg[18],
                    'VIAJE_SALIDA_REAL' : hstAutoreg[19],
                    'VIAJE_PUNTUALIDAD' : hstAutoreg[20],
                    'VIAJE_COLOR_PUNTUALIDAD' : hstAutoreg[21],
                    'VIAJE_FREC_ADELANTE' : hstAutoreg[22],
                    'ENVIADO' : 1
                    }

                # Se traen todos los datos de viaje Posicion, y los de otras tablas se inicia en estas líneas para ir las
                # cambiando e insertar los datos lo más completos posibles.
                
                # Viaje Autobus Front
                VAF = db_session.query(Tablas.Viaje.AUTOBUS_ID).filter(Tablas.Viaje.ID == hstAutoreg[3]).all()
                if VAF:
                    for af in VAF:
                        #a = a[:2]+(af[0],)+a[2:]
                        a['VIAJE_AUTOBUS_ADELANTE'] = af[0]
                
                # Viaje Autobus Back
                VAB = db_session.query(Tablas.Viaje.AUTOBUS_ID).filter(Tablas.Viaje.ID == hstAutoreg[6]).all()
                if VAB:
                    for ab in VAB:
                        a['VIAJE_AUTOBUS_ATRAS'] = ab[0]

                # Colision Parada Última HORA
                CUH = db_session.query(func.max(Tablas.Colision.FECHA_FIN)).filter(Tablas.Colision.VIAJE_ID == hstAutoreg[16]).all()
                if CUH:
                    for cf in CUH:
                        a['COLISION_PARADA_ULTIMA_HORA'] = cf[0]

                Auto_regulacion = Tablas.Viaje_Autoregulacion(**a)

                rgtAuto = Auto_regulacion.add()
                
                if rgtAuto:
                    print('Error al insertar...')
                
        mnsjTxt = "Resulto bien..."

        end_db()

        return mnsjTxt

    def getAutobus(self, option, name):
        lstBus = []     # Lista de autobuses
        if option == 2:
            print('-', name, '-', sep=('-')*37)
            
        init_db()
        
        # obtiene los autobuses de la parada 
        '''
        lstBus = db_session.query(Tablas.Viaje.AUTOBUS_ID, Tablas.Viaje.FECHA_ACTUALIZACION,\
                                Tablas.Viaje.CONDUCTOR_ID, Tablas.Viaje.RUTA_ID, Tablas.Viaje.ID,\
                                Tablas.Viaje.ZONA_HORARIA_ID, Tablas.Viaje.VIAJE_STATUS_ID,\
                                Tablas.Viaje.FECHA_HORA_REAL_SALIDA, Tablas.Viaje.ERPCO_CORRIDA_ID,\
                                Tablas.Viaje.FECHA_HORA_REAL_LLEGADA, Tablas.Viaje.ULTIMO_VIAJE_POSICION_ID).distinct().all()
        '''
        lstBus = db_session.query(Tablas.Hst_Monitoreo_Mensajes.AUTOBUS, Tablas.Hst_Monitoreo_Mensajes.FECHA_ENVIO,\
            Tablas.Hst_Monitoreo_Mensajes.PUNTUALIDAD_ACTUALIDAD_AUTOBUS, Tablas.Hst_Monitoreo_Mensajes.TOLERANCIA_PUNTUALIDAD_AMARILLO,\
                Tablas.Hst_Monitoreo_Mensajes.TOLERANCIA_PUNTUALIDAD_ROJO, Tablas.Hst_Monitoreo_Mensajes.FRECUENCIA_TEORICA_AUTOBUS_ATRAS,
                    Tablas.Hst_Monitoreo_Mensajes.FRECUENCIA_TEORICA_AUTOBUS_ADELANTE, Tablas.Hst_Monitoreo_Mensajes.TOLERANCIA_FRECUENCIA_AMARILLO,\
                        Tablas.Hst_Monitoreo_Mensajes.TOLERANCIA_FRECUENCIA_ROJO, Tablas.Hst_Monitoreo_Mensajes.AUTOBUS_ATRAS,\
                            Tablas.Hst_Monitoreo_Mensajes.TIEMPO_AUTOBUS_ATRAS, Tablas.Hst_Monitoreo_Mensajes.AUTOBUS_ADELANTE,\
                                Tablas.Hst_Monitoreo_Mensajes.TIEMPO_AUTOBUS_ADELANTE, Tablas.Hst_Monitoreo_Mensajes.FECHA_HORA_DE_SALIDA_PROGRAMADA,\
                                  Tablas.Hst_Monitoreo_Mensajes.CLAVE_POBLACION_ORIGEN, Tablas.Hst_Monitoreo_Mensajes.CLAVE_POBLACION_DESTINO,\
                                      Tablas.Hst_Monitoreo_Mensajes.CLAVE_POBLACION_ULTIMA_GEOCERCA_CRUZADA,\
                                          Tablas.Hst_Monitoreo_Mensajes.FECHA_HORA_DE_ULTIMA_GEOCERCA_CRUZADA,\
                                              Tablas.Hst_Monitoreo_Mensajes.VIGENCIA_DEL_MENSAJE_EN_MINUTOS).limit(10)
        for bus in lstBus:
            lstDatos = ('#|AUT_X3|' + str(datetime.datetime.today())[0:19].replace(' ','T') + '|' + str(bus.AUTOBUS) + '|' \
                        + str(bus.FECHA_ENVIO)[11:19] + str(bus.PUNTUALIDAD_ACTUALIDAD_AUTOBUS) + str(bus.TOLERANCIA_PUNTUALIDAD_AMARILLO) +\
                        '|' + str(bus.TOLERANCIA_PUNTUALIDAD_ROJO) + '|' + str(bus.FRECUENCIA_TEORICA_AUTOBUS_ATRAS) + '|' +\
                        str(bus.FRECUENCIA_TEORICA_AUTOBUS_ADELANTE) + '|' + str(bus.TOLERANCIA_FRECUENCIA_AMARILLO) + '|' +\
                        str(bus.TOLERANCIA_FRECUENCIA_ROJO) + '|' + str(bus.AUTOBUS_ATRAS) + '|' + str(bus.TIEMPO_AUTOBUS_ATRAS) + '|' +\
                        str(bus.AUTOBUS_ADELANTE) + '|' + str(bus.TIEMPO_AUTOBUS_ADELANTE) + '|' + str(bus.FECHA_HORA_DE_SALIDA_PROGRAMADA) + '|' +\
                        str(bus.CLAVE_POBLACION_ORIGEN) + '|' + str(bus.CLAVE_POBLACION_DESTINO) + '|' + str(bus.CLAVE_POBLACION_ULTIMA_GEOCERCA_CRUZADA) + '|' +\
                        str(bus.CLAVE_POBLACION_ULTIMA_GEOCERCA_CRUZADA) + '|' + str(bus.FECHA_HORA_DE_ULTIMA_GEOCERCA_CRUZADA) + '|' +\
                        str(bus.VIGENCIA_DEL_MENSAJE_EN_MINUTOS) + '|# ')

            print(lstDatos)

        mnsjTxt = "Resulto bueno..."
        end_db()

        return mnsjTxt
