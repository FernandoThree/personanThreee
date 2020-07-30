from sqlalchemy import func, or_
from datetime import datetime, date, timedelta
from typing import List
import sys

from Almacenamiento import Tablas, db_session
from Colision.Colision_Trazado import colision_parada, distancia_parada
from Util.Carga_Data import Data
from Util.Parametro import Parametro
from Math_geo.Point import Point
from Math_geo.Polygon import Polygon

def parada_colision():
    # recuperar último HST_GEOTAB_LOGRECORD analizado
    param_hstgeotab = Tablas.Sae_Parametro.get('mod-colision-last-hstgeotab-id')

    # recuperar histórico desde el último analizado
    logrecords = db_session.query(Tablas.Hst_Geotab_Logrecord).filter(
        Tablas.Hst_Geotab_Logrecord.PK_ID > int(param_hstgeotab.VALOR)
    ).order_by(
        Tablas.Hst_Geotab_Logrecord.AUTOBUS,
        Tablas.Hst_Geotab_Logrecord.FECHA_REGISTRO_GEOTAB
    ).all()

    if __debug__:
        print('Info. Logrecords cargados, registros por analizar: %d' % len(logrecords), file=sys.stderr)
    # recuperar colisiones activas, debe haber como máximo una colisión activa por autobús
    colisiones_activas = Tablas.Colision.query_all({'COLISION_ACTIVA':1})

    # recuperar poligonos de las paradas
    d_poligonos = {}
    for parada_id, parada_poligonos in Data().dic_ParadaPoligono.items():
        vertices = [Point(latitude=parada_poligono.LATITUD, longitude=parada_poligono.LONGITUD) for parada_poligono in parada_poligonos]
        if vertices:
            poligono = Polygon(vertices)
            d_poligonos[parada_id] = poligono

    # revisar colisiones
    autobus_ant = None
    colision = None
    for logrecord in logrecords:
        # actualizar id de último logrecord analizado
        if logrecord.PK_ID > int(param_hstgeotab.VALOR):
            param_hstgeotab.VALOR = str(logrecord.PK_ID)
        # ver si hay colisión activa
        if logrecord.AUTOBUS != autobus_ant:
            autobus_ant = logrecord.AUTOBUS
            colision = buscar_colision_activa(logrecord.AUTOBUS, colisiones_activas)
        
        if colision:
            # ignorar registros anteriores a colisión activa TODO: reivsar si es necesario actualizar colisiones anteriores a la activa
            if colision and logrecord.FECHA_REGISTRO_GEOTAB < colision.FECHA_INICIO:
                continue
        
            # revisar si sigue en misma parada
            if colision.PARADA_ID in d_poligonos:
                if colision_parada(colision.PARADA_ID, logrecord.LATITUD, logrecord.LONGITUD):
                    # actualizar colisión activa
                    if logrecord.FECHA_REGISTRO_GEOTAB > colision.FECHA_FIN:
                        colision.FECHA_FIN = logrecord.FECHA_REGISTRO_GEOTAB
                        colision.DURACION = (colision.FECHA_FIN - colision.FECHA_INICIO).total_seconds()
                
                    colision.VELOCIDAD_PROMEDIO = (colision.VELOCIDAD_PROMEDIO * colision.NUMERO_LOCALIZACIONES + logrecord.VELOCIDAD) / (
                        colision.NUMERO_LOCALIZACIONES + 1)
                    colision.VELOCIDAD_MAX = max(colision.VELOCIDAD_MAX, logrecord.VELOCIDAD)
                    colision.NUMERO_LOCALIZACIONES += 1

                    continue
                else:
                    # marcar colisión como inactiva
                    colision.COLISION_ACTIVA = 0
                # Tablas.update()
            else:
                print('Error. Parada %d registrada en la colisión %d no se encuentra en la base de datos, se marca la colisión como inactiva'
                    % (colision.PARADA_ID, colision.ID), file=sys.stderr)
                colision.COLISION_ACTIVA = 0
                # Tablas.update()

        # revisar colisión con paradas
        for parada_id, poligono in d_poligonos.items():
            # if distancia_parada(parada_id, logrecord.LATITUD, logrecord.LONGITUD) > 400:
            #     continue
            if poligono.in_polygon(Point(logrecord.LATITUD, logrecord.LONGITUD)):
                colision = Tablas.Colision(
                    AUTOBUS               = logrecord.AUTOBUS,
                    PARADA_ID             = parada_id,
                    FECHA_INICIO          = logrecord.FECHA_REGISTRO_GEOTAB,
                    FECHA_FIN             = logrecord.FECHA_REGISTRO_GEOTAB,
                    VELOCIDAD_PROMEDIO    = logrecord.VELOCIDAD,
                    DISTANCIA             = logrecord.DISTANCIA,
                    DURACION              = 0,
                    VELOCIDAD_MAX         = logrecord.VELOCIDAD,
                    NUMERO_LOCALIZACIONES = 1,
                    COLISION_ACTIVA       = 1
                )

                # buscar viaje
                viaje_id = db_session.query(Tablas.Viaje.ID).filter(
                    Tablas.Viaje.AUTOBUS_ID == int(logrecord.AUTOBUS),
                    or_(
                        Tablas.Viaje.VIAJE_STATUS_ID == Tablas.Viaje_Status.enum.EN_VIAJE.value,
                        Tablas.Viaje.VIAJE_STATUS_ID == Tablas.Viaje_Status.enum.DESENROLAMIENTO.value
                    )
                ).first()
                if not viaje_id:
                    viaje_id = db_session.query(Tablas.Viaje.ID).filter(
                        Tablas.Viaje.AUTOBUS_ID == int(logrecord.AUTOBUS),
                        Tablas.Viaje.FECHA_HORA_PROGRAMADA_SALIDA < logrecord.FECHA_REGISTRO_GEOTAB,
                        Tablas.Viaje.FECHA_HORA_PROGRAMADA_LLEGADA > logrecord.FECHA_REGISTRO_GEOTAB
                    ).first()                    

                if viaje_id:
                    colision.VIAJE_ID = viaje_id.ID
                
                colision.add()
                break

    Tablas.update()

def buscar_colision_activa(autobus: str, colisiones_activas: List[Tablas.Colision]) -> Tablas.Colision:
    for colision in colisiones_activas:
        if autobus == colision.AUTOBUS:
            return colision
    return None


def Trayecto():
    # 1.- se obtienen paradas-poligono antes que otros datos
    # Todas las paradas activas
    lstParadas =  db_session.query(Tablas.Parada.ID,
                                Tablas.Parada.NAME).filter_by(ACTIVE = 1).order_by(Tablas.Parada.ID).all()
    # Hash Table con todo los poligonos cargados en Memoria
    dicPoligonos = {}   # diccionario poligonal

    for parada in lstParadas:       # Con las paradas se obtienen las coordenadas por orden de parada
        hstVertice = []             # Lista de vertices de parada
        objPoligono = None
        lstVertices = db_session.query(Tablas.Parada_Poligono.LATITUD, Tablas.Parada_Poligono.LONGITUD,
                                        Tablas.Parada_Poligono.PARADA_ID,
                                        Tablas.Parada_Poligono.SEQUENCE).filter_by(ACTIVE = 1,
                                            PARADA_ID = parada.ID).order_by(Tablas.Parada_Poligono.SEQUENCE).all()
        #Cargamos la lista de vertice del poligono
        for vertice in lstVertices:       # Se arma el diccionario de paradas y poligonos de paradas
            punto = Point(vertice.LATITUD, vertice.LONGITUD)
            hstVertice.append(punto)

        #Necesitamos al menos 3 puntos para crear un poligono
        if(len(hstVertice) > 2):
            #Cargamos el poligono con base a la lista de vertices
            objPoligono = Polygon(hstVertice)

            #Agregamos el poligono
            dicPoligonos[parada.ID] = {"PARADA": parada, "POLIGONO":objPoligono}    # Se agrega diccionario a otro diccionario

    # 2. se Obtiene los autobuses 
    lstAutobus = db_session.query(Tablas.Hst_Geotab_Logrecord.AUTOBUS).distinct().all()

    for xAutobus in lstAutobus:
        if __debug__:
            print('Eco Autobús:', xAutobus.AUTOBUS, sep=(':='))
        listColisionesHistorica = []    # Lista de colisiones hst_geotab ...
        dicColisionesActivas = {}       # Diccionario de Colisiones de la lista ...
        HstLocalizacion = []            # Lista del historico de localizaciones ...

        # Obtenemos la fecha máxima de colision (última), por autobús
        fechaMax = db_session.query(Tablas.Colision.AUTOBUS, func.max(Tablas.Colision.FECHA_FIN)).\
                    filter(Tablas.Colision.AUTOBUS == xAutobus.AUTOBUS).group_by(Tablas.Colision.AUTOBUS).all()

        if fechaMax:
            for dayMax in fechaMax:
                fechaIni = dayMax[1]
        else:
            if __debug__:
                print("ECO BUS", xAutobus.AUTOBUS, sep=(":"))
            # En caso de que no haya resgistros del autobus en colision, obtengo la fecha minima de Hst_Geotab y de ahi empieza...
            # espero solo funcione para las pruebas o para el inicio, después de eso, nunca más vuelva a entrar.
            fechaMaxH = db_session.query(Tablas.Hst_Geotab_Logrecord.AUTOBUS,\
                            func.max(Tablas.Hst_Geotab_Logrecord.FECHA_REGISTRO_GEOTAB)).\
                            filter(Tablas.Hst_Geotab_Logrecord.AUTOBUS == xAutobus.AUTOBUS).\
                            group_by(Tablas.Hst_Geotab_Logrecord.AUTOBUS).all()
            
            for DayMax in fechaMaxH:
                if __debug__:
                    print('fecha maxima', DayMax[1] - timedelta(days=1), sep=(': '))

                fechaIni = DayMax[1] - timedelta(days=1)
        
        # Se obtienen todas las colisiones existentes en la tabla de GEOTAB,
        #   Tablas.Hst_Geotab_Logrecord.FECHA_REGISTRO_GEOTAB < fechaFin
        HstLocalizacion = db_session.query(Tablas.Hst_Geotab_Logrecord.LATITUD, Tablas.Hst_Geotab_Logrecord.LONGITUD,
                                    Tablas.Hst_Geotab_Logrecord.AUTOBUS, Tablas.Hst_Geotab_Logrecord.PK_ID,
                                    Tablas.Hst_Geotab_Logrecord.FECHA_REGISTRO_GEOTAB, Tablas.Hst_Geotab_Logrecord.VELOCIDAD,
                                    Tablas.Hst_Geotab_Logrecord.DISTANCIA).filter(Tablas.Hst_Geotab_Logrecord.AUTOBUS == xAutobus.AUTOBUS,
                                                                                Tablas.Hst_Geotab_Logrecord.FECHA_REGISTRO_GEOTAB > fechaIni).order_by(
                                                                                            Tablas.Hst_Geotab_Logrecord.PK_ID,
                                                                                            Tablas.Hst_Geotab_Logrecord.FECHA_REGISTRO_GEOTAB).distinct().all()

        # Se consulta tabla de colision para traer colision por fecha y autobus ("hoy vacia"); faltta traer la modificación a la ultima colision
        if __debug__:
            print('REGISTROS', len(HstLocalizacion), sep=('=:'))
        for objLocalizacion in HstLocalizacion:
            ptoColision = Point(objLocalizacion.LATITUD, objLocalizacion.LONGITUD)
            #Vamos a iterar cada Parada
            for idParada in dicPoligonos:
                parada = dicPoligonos[idParada]["PARADA"]
                objPoligono = dicPoligonos[idParada]["POLIGONO"]
                if objPoligono.in_polygon(ptoColision):
                    #Preguntamos si ya tenemos una colsión en proceso con esa parada
                    if(idParada in dicColisionesActivas) :
                        #Actulizamos las fecha de SALIDA
                        dicColisionesActivas[idParada]["SALIDA"] = objLocalizacion
                        dicColisionesActivas[idParada]["CONTADOR"] += 1
                    else:
                        # No tenemos activa de esta parada, vamos a crearla
                        dicColisionesActivas[idParada] = {"PARADA_ID": idParada, "PARADA": parada,
                                                        "POLIGONO": objPoligono, "ENTRADA": objLocalizacion,
                                                        "SALIDA": objLocalizacion, "CONTADOR": 1}
                else:
                    # No tenemos colision con el poligono
                    # Vamos  a preguntar si teniamos colision activa.
                    if (idParada in dicColisionesActivas):
                        # Teniamos una colision activa, pero ya, lo mandamos al diccionario historico, para su
                        # Almacenamiento
                        listColisionesHistorica.append(dicColisionesActivas[idParada])
                        # Limpiamos la colsiones activas
                        del dicColisionesActivas[idParada]

        # Mostramos las colisiones detectadas
        # AQUI RECOMIENDO QUE GUARDES LA INFORMACION EN LA BASE DE DATOS
        for objColision in listColisionesHistorica:
            # vamos a buscar el id del viaje; 
            IdViaje = db_session.query(Tablas.Viaje.ID).filter(\
                Tablas.Viaje.VIAJE_STATUS_ID != 1,
                Tablas.Ruta_Parada.RUTA_ID == Tablas.Viaje.RUTA_ID,
                Tablas.Parada.ID == Tablas.Ruta_Parada.PARADA_ID,
                Tablas.Parada.ACTIVE == 1,
                Tablas.Viaje.AUTOBUS_ID == xAutobus.AUTOBUS,
                Tablas.Ruta_Parada.PARADA_ID == objColision['PARADA_ID'],
                Tablas.Viaje.FECHA_HORA_PROGRAMADA_SALIDA <= objColision['ENTRADA'][4],
                Tablas.Viaje.FECHA_HORA_PROGRAMADA_LLEGADA >= objColision['SALIDA'][4]).all()
                    #func.dateadd(Tablas.Viaje.FECHA_HORA_PROGRAMADA_LLEGADA, timedelta(minutes=15), Interval()) >= objColision['SALIDA'][4]).all()

            if IdViaje:
                for vId in IdViaje:
                    Id_Viaje = vId[0]
            else:
                Id_Viaje = None

            TDura =  objColision['SALIDA'][4] - objColision['ENTRADA'][4]
            if __debug__:
                print('Tiempo duración', TDura, sep=('=: '))
            #constructor
            ColisionDetec = Tablas.Colision(AUTOBUS=str(objLocalizacion.AUTOBUS), PARADA_ID=objColision['PARADA_ID'],
                                FECHA_INICIO=objColision['ENTRADA'][4], FECHA_FIN=objColision['SALIDA'][4],
                                VELOCIDAD_PROMEDIO=objLocalizacion.VELOCIDAD, DISTANCIA=objLocalizacion.DISTANCIA, DURACION=TDura.seconds, 
                                VELOCIDAD_MAX=objLocalizacion.VELOCIDAD, NUMERO_LOCALIZACIONES=objColision['CONTADOR'], 
                                VIAJE_ID=Id_Viaje) 
            #insertar objerto
            ColisionDetec.add()
            Id_Viaje = None    # se limpia por no contaminar el siguiente registro, si no trae numero de viaje
            '''
            ********* ---------- Campos de la tabla --------------- **************
            PK_ID, 
            AUTOBUS, PARADA_ID, FECHA_INICIO, FECHA_FIN, VELOCIDAD_PROMEDIO, 
            DISTANCIA, DURACION, VELOCIDAD_MAX, NUMERO_LOCALIZACIONES
            ***************** -------- COLISION ---------------- ********************
            objColision['PARADA_ID'], objLocalizacion.AUTOBUS
            '''
        
