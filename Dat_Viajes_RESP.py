import datetime
import sys
#Almacenamiento
from Almacenamiento import Tablas, Tablas_Erpco, db_session
from sqlalchemy.orm import aliased
from sqlalchemy.sql import exists,func

class DatERPCO:
    def creaviajes(self):
        self.CreaViajesCatalogos()

    #Compara ERPCO CORRIDA, CON SAE_RUTA_DETALLE
    def creadatos(self,listaobjetosERPCOCORRIDA,listaobjetosSAE_RUTA_DETALLE):
        dicEstaERPCO_RUTA_ID = {}
        for OBJETOTABLA in listaobjetosERPCOCORRIDA:
            dicERPCOCORRIDA = OBJETOTABLA.__dict__
            RUTA_ID = dicERPCOCORRIDA.get("RUTA_ID")
            AUTOBUS_ID = dicERPCOCORRIDA.get("AUTOBUS_ID")
            CONDUCTOR_ID = 0
            FECHA_HORA_PROGRAMADA_SALIDA = dicERPCOCORRIDA.get("FECHORSAL") #str(dicERPCOCORRIDA.get("FECHORSAL")).replace(' ', 'T')
            FECHA_HORA_REAL_SALIDA = str(dicERPCOCORRIDA.get("FECCORRIDA")) + str(dicERPCOCORRIDA.get("HORACORRIDA"))[13:7]  #str(dicERPCOCORRIDA.get("FECHORSAL")).replace(' ', 'T')
            FECHA_HORA_PROGRAMADA_LLEGADA = dicERPCOCORRIDA.get("FECHORLLE") #str(dicERPCOCORRIDA.get("FECHORSAL")).replace(' ', 'T')
            FECHA_HORA_REAL_LLEGADA = dicERPCOCORRIDA.get("FECHORLLE") #str(dicERPCOCORRIDA.get("FECHORSAL")).replace(' ', 'T')
            ZONA_HORARIA_ID = 0
            VIAJE_STATUS_ID = 1
            FECHA_ACTUALIZACION = str(datetime.datetime.today())[0:19] #str(datetime.datetime.today())[0:19].replace(' ', 'T')
            ERPCO_CORRIDA_ID = dicERPCOCORRIDA.get("CORRIDA_ID")
            ULTIMO_VIAJE_POSICION_ID = 0

            # Buscamos si existe esta Ruta en SAE_RUTA_DETALLE
            for objSAE_RUTA_DETALLE in listaobjetosSAE_RUTA_DETALLE:
                dicSAE_RUTA_DETALLE = objSAE_RUTA_DETALLE.__dict__
                FK_ERPCO_RUTA_ID = dicSAE_RUTA_DETALLE.get("FK_ERPCO_RUTA_ID")
                ESTA = 0
                if FK_ERPCO_RUTA_ID == RUTA_ID:
                    ESTA = 1
                    FK_RUTA = dicSAE_RUTA_DETALLE["FK_RUTA_ID"]
                    dicEstaERPCO_RUTA_ID[str(ERPCO_CORRIDA_ID)] = {
                        "RUTA_ID": str(RUTA_ID),
                        "AUTOBUS_ID": str(AUTOBUS_ID),
                        "CONDUCTOR_ID": str(CONDUCTOR_ID),
                        "FECHA_HORA_PROGRAMADA_SALIDA": str(FECHA_HORA_PROGRAMADA_SALIDA),
                        "FECHA_HORA_REAL_SALIDA": str(FECHA_HORA_REAL_SALIDA),
                        "FECHA_HORA_PROGRAMADA_LLEGADA": str(FECHA_HORA_PROGRAMADA_LLEGADA),
                        "FECHA_HORA_REAL_LLEGADA": str(FECHA_HORA_REAL_LLEGADA),
                        "ZONA_HORARIA_ID": str(ZONA_HORARIA_ID),
                        "VIAJE_STATUS_ID": str(VIAJE_STATUS_ID),
                        "FECHA_ACTUALIZACION": str(FECHA_ACTUALIZACION),
                        "ERPCO_CORRIDA_ID": str(ERPCO_CORRIDA_ID),
                        "ULTIMO_VIAJE_POSICION_ID" : str(ULTIMO_VIAJE_POSICION_ID),
                        "Estatus": str('1'),
                        "ID_RUTA":FK_RUTA
                    }
                    break

            if ESTA == 0:
                FK_RUTA = 0
                dicEstaERPCO_RUTA_ID[str(ERPCO_CORRIDA_ID)] = {
                    "RUTA_ID": str(RUTA_ID),
                    "AUTOBUS_ID": str(AUTOBUS_ID),
                    "CONDUCTOR_ID": str(CONDUCTOR_ID),
                    "FECHA_HORA_PROGRAMADA_SALIDA": str(FECHA_HORA_PROGRAMADA_SALIDA),
                    "FECHA_HORA_REAL_SALIDA": str(FECHA_HORA_REAL_SALIDA),
                    "FECHA_HORA_PROGRAMADA_LLEGADA": str(FECHA_HORA_PROGRAMADA_LLEGADA),
                    "FECHA_HORA_REAL_LLEGADA": str(FECHA_HORA_REAL_LLEGADA),
                    "ZONA_HORARIA_ID": str(ZONA_HORARIA_ID),
                    "VIAJE_STATUS_ID": str(VIAJE_STATUS_ID),
                    "FECHA_ACTUALIZACION": str(FECHA_ACTUALIZACION),
                    "ERPCO_CORRIDA_ID": str(ERPCO_CORRIDA_ID),
                    "ULTIMO_VIAJE_POSICION_ID": str(ULTIMO_VIAJE_POSICION_ID),
                    "Estatus": str('0'),
                    "ID_RUTA": str('0')
                }
        return dicEstaERPCO_RUTA_ID

        # Realiza la siguiente validación RUTA
    #Compara La RUTA
    def comparaviajesRUTA(self, dic, listaobjetosRUTA):

            ListaConviajesValidados = []
            dicEstaERPCO_RUTA_ID = {}
            for objSAE_RUTA in listaobjetosRUTA:
                dicSAE_RUTA = objSAE_RUTA.__dict__
                ID_RUTA = dicSAE_RUTA.get("ID")
                # and v['ID_RUTA'] == str(ID_RUTA)
                dicSinRuta = {k: v for k, v in dic.items() if v['Estatus'] == '1' and v['ID_RUTA'] == ID_RUTA }
                if len(dicSinRuta) > 0:
                    for key,valor in dicSinRuta.items():
                        ListaConviajesValidados.append(valor)
            return ListaConviajesValidados
    #Creamos Lista de directorios de latabla viajes
    def CrealistadedirectoriosTablaViajes(self,listaobjetosVIAJES):
        # Guardo en una sola lista los objetos para poder buscar en un solo lote.
        DictaobjetosVIAJESNuevoformato = {}
        for OBJViajes in listaobjetosVIAJES:
            dicViajes = OBJViajes.__dict__
            FK_RUTA = str(dicViajes.get("FK_RUTA"))
            if FK_RUTA == 'None':
                FK_RUTA = '0'
            AUTOBUS_ID = str(dicViajes.get("AUTOBUS_ID"))
            if AUTOBUS_ID == 'None':
                AUTOBUS_ID = '0'
            CONDUCTOR_ID = str(dicViajes.get("CONDUCTOR_ID"))
            if CONDUCTOR_ID == 'None':
                CONDUCTOR_ID = '0'
            FECHA_HORA_PROGRAMADA_SALIDA = str(dicViajes.get("FECHA_HORA_PROGRAMADA_SALIDA"))
            if FECHA_HORA_PROGRAMADA_SALIDA == 'None':
                FECHA_HORA_PROGRAMADA_SALIDA = '1900-01-01T00:00:00.000'

            FECHA_HORA_REAL_SALIDA = str(dicViajes.get("FECHA_HORA_REAL_SALIDA"))
            if FECHA_HORA_REAL_SALIDA == 'None':
                FECHA_HORA_REAL_SALIDA = '1900-01-01T00:00:00.000'
            FECHA_HORA_PROGRAMADA_LLEGADA = str(dicViajes.get("FECHA_HORA_PROGRAMADA_LLEGADA"))
            if FECHA_HORA_PROGRAMADA_LLEGADA == 'None':
                FECHA_HORA_PROGRAMADA_LLEGADA = '1900-01-01T00:00:00.000'
            FECHA_HORA_REAL_LLEGADA = str(dicViajes.get("FECHA_HORA_REAL_LLEGADA"))
            if FECHA_HORA_REAL_LLEGADA == 'None':
                FECHA_HORA_REAL_LLEGADA = '1900-01-01T00:00:00.000'
            ZONA_HORARIA_ID = str(dicViajes.get("ZONA_HORARIA_ID"))
            if ZONA_HORARIA_ID == 'None':
                ZONA_HORARIA_ID = '0'
            VIAJE_STATUS_ID = str(dicViajes.get("VIAJE_STATUS_ID"))
            if VIAJE_STATUS_ID == 'None':
                VIAJE_STATUS_ID = '0'
            FECHA_ACTUALIZACION = str(dicViajes.get("FECHA_ACTUALIZACION"))
            if FECHA_ACTUALIZACION == 'None':
                FECHA_ACTUALIZACION = '1900-01-01T00:00:00.000'
            ERPCO_CORRIDA_ID = str(dicViajes.get("ERPCO_CORRIDA_ID"))
            if ERPCO_CORRIDA_ID == 'None':
                ERPCO_CORRIDA_ID = '0'
            ULTIMO_VIAJE_POSICION_ID = str(dicViajes.get("ULTIMO_VIAJE_POSICION_ID"))
            if ULTIMO_VIAJE_POSICION_ID == 'None':
                ULTIMO_VIAJE_POSICION_ID = '0'

            DictaobjetosVIAJESNuevoformato[str(ERPCO_CORRIDA_ID)] = {
                "RUTA_ID": str(FK_RUTA),
                "AUTOBUS_ID": str(AUTOBUS_ID),
                "CONDUCTOR_ID": str(CONDUCTOR_ID),
                "FECHA_HORA_PROGRAMADA_SALIDA": str(FECHA_HORA_PROGRAMADA_SALIDA),
                "FECHA_HORA_REAL_SALIDA": str(FECHA_HORA_REAL_SALIDA),
                "FECHA_HORA_PROGRAMADA_LLEGADA": str(FECHA_HORA_PROGRAMADA_LLEGADA),
                "FECHA_HORA_REAL_LLEGADA": str(FECHA_HORA_REAL_LLEGADA),
                "ZONA_HORARIA_ID": str(ZONA_HORARIA_ID),
                "VIAJE_STATUS_ID": str(VIAJE_STATUS_ID),
                "FECHA_ACTUALIZACION": str(FECHA_ACTUALIZACION),
                "ERPCO_CORRIDA_ID": str(ERPCO_CORRIDA_ID),
                "ULTIMO_VIAJE_POSICION_ID": str(ULTIMO_VIAJE_POSICION_ID)
            }
        return DictaobjetosVIAJESNuevoformato
    #Compara los viajes de Erpco en la tabla de Vaijes SAE
    def ComparaviajesERPCOSAE(self,ListaConviajesValidados,listaobjetosVIAJES):
        ListaDiferentes = []
        listParaguardarViajes = []
        listParaactualizarViajes = []
        DictaobjetosVIAJESNuevoformato = self.CrealistadedirectoriosTablaViajes(listaobjetosVIAJES)
        cuantos = len(DictaobjetosVIAJESNuevoformato)
        #Pregunto por cada registro de los viajes validos de ERPCO si se encuentran en el Lote de viajes
        for objViajesValido in ListaConviajesValidados:
            #for key,valor in objViajesValido.items():
                #if key == 'ERPCO_CORRIDA_ID':
                    #ERPCO_CORRIDA_ID = valor
                dicViajeComparar = {k: v for k, v in DictaobjetosVIAJESNuevoformato.items() if v['ERPCO_CORRIDA_ID'] == str(objViajesValido.get("ERPCO_CORRIDA_ID"))}
                #Validamos si esta con el tamaño del resultado.
                if len(dicViajeComparar) > 0:
                    #si esta, Comparamos los campos para buscar diferencias
                    dicdiferencias = {k: v for k, v in dicViajeComparar.items() if  v['AUTOBUS_ID'] != str(objViajesValido.get("AUTOBUS_ID"))
                                                                                or v['CONDUCTOR_ID'] != str(objViajesValido.get("CONDUCTOR_ID"))
                                                                                or v['FECHA_HORA_REAL_SALIDA'] != str(objViajesValido.get("FECHA_HORA_REAL_SALIDA"))}
                    if len(dicdiferencias) > 0:
                        listParaactualizarViajes.append(objViajesValido)
                else:
                    #si no esta lo guardamos en una lista para posteriormente guardarlos todos
                    listParaguardarViajes.append(objViajesValido)
        if len(listParaguardarViajes) > 0:
            self.insertadatosViajes(listParaguardarViajes)
        if len(listParaactualizarViajes) > 0:
            self.insertadatosViajes(listParaactualizarViajes)
   #*********************************************************************************
    #Crea el catalogo de Buses
    def CreaViajesCatalogos(self):
        #Variables
        EstaBus = False
        CORRIDA_ID_TABLA_VIAJE  = None
        ViajeValido =True
        _EntraaguardarLista = False
        #CREAMOS EL ALIAS DE CADA BD
        TblAutobus = aliased(Tablas.Autobus)
        #Creamos Los Diccionarios para trabajar
        DicEC_ECT = {}
        _DictAutobus = {}
        _DicAutobus = {}
        #Creamos Listas Con Resultados Finales
        _ArrResultadoBuses = []
        _ArrEC_ECT = []
        _listParaactualizarViajes = []
        _listParainsertarViajes = []
        _listViajePadada = []
        _listViajeTrecho = []
        _listCatConductores = []
        _listCatAutobuses = []


        #Creamos arreglo con join ERPCO_CORRIDA y ERPO_CORRIDA_TRAMO
        _listEC_ECT = \
            db_session.query(Tablas_Erpco.ERPCO_CORRIDA.CORRIDA_ID,
                             Tablas_Erpco.ERPCO_CORRIDA.RUTA_ID,
                             Tablas_Erpco.ERPCO_CORRIDA_TRAMO.AUTOBUS_ID,
                             Tablas_Erpco.ERPCO_CORRIDA.AUTOBUS_ID,
                             Tablas_Erpco.ERPCO_CORRIDA_TRAMO.CONDUCTOR1_ID,
                             Tablas_Erpco.ERPCO_CORRIDA.FECHORSAL,
                             Tablas_Erpco.SAE_RUTA_DETALLE.FK_RUTA_ID). \
                filter_by(CORRIDA_ID=Tablas_Erpco.ERPCO_CORRIDA_TRAMO.CORRIDA_ID,
                          RUTA_ID=Tablas_Erpco.SAE_RUTA_DETALLE.FK_ERPCO_RUTA_ID
                          ). \
                group_by(
                Tablas_Erpco.ERPCO_CORRIDA.CORRIDA_ID,
                Tablas_Erpco.ERPCO_CORRIDA.RUTA_ID,
                Tablas_Erpco.ERPCO_CORRIDA_TRAMO.AUTOBUS_ID,
                Tablas_Erpco.ERPCO_CORRIDA.AUTOBUS_ID,
                Tablas_Erpco.ERPCO_CORRIDA_TRAMO.CONDUCTOR1_ID,
                Tablas_Erpco.ERPCO_CORRIDA.FECHORSAL,
                Tablas_Erpco.SAE_RUTA_DETALLE.FK_ERPCO_RUTA_ID,
                Tablas_Erpco.SAE_RUTA_DETALLE.FK_RUTA_ID
            ).all()

        valores = len(_listEC_ECT)
        #Buscamos si el Autobus esta en las tabls de SAE si no esta lo insertamos
        for datos in _listEC_ECT:
            ViajeValido = True
            DicEC_ECT = dict(zip('abcdefgh', datos))
            testdato = DicEC_ECT.get('a')
            if _EntraaguardarLista == False or  DicEC_ECT.get('a') != ERPCOCORRIDAID:
                EstaBus = False
                EstaConductor = False
                ERPCOCORRIDAID = DicEC_ECT.get('a')
                NombreAutobus = DicEC_ECT.get('c')
                IdErpcoAutobus = DicEC_ECT.get('d')
                Numempleado = DicEC_ECT.get('e')
                FECHORSAL = DicEC_ECT.get('f')
                FKSALIDARUTAID =  DicEC_ECT.get('g')

                stmt = exists().where(Tablas.Autobus.NUMECONOMICO == NombreAutobus)
                for NUMECONOMICO, in db_session.query(Tablas.Autobus.NUMECONOMICO).filter(stmt):
                        EstaBus = True
                        if NUMECONOMICO == NombreAutobus:
                            break
                # Buscamos si el Conductor esta en las tabls de SAE si no esta lo insertamos
                stmt2 = exists().where(Tablas.Conductor.NUMEMPLEADO == Numempleado)
                for NUMECONOMICO, in db_session.query(Tablas.Conductor.NUMEMPLEADO).filter(stmt2):
                    EstaConductor = True
                    if NUMECONOMICO == Numempleado:
                        break



                 #BUSCAMOS SI ESTA LA RUTA DEL VIAJE EN RUTA
                stmt3 = exists().where(Tablas.Ruta.ID == FKSALIDARUTAID)
                for _FKERPCORUTAID, in db_session.query(Tablas.Ruta.ID).filter(stmt3):
                        EstaRutaERPCO = True
                        if _FKERPCORUTAID == FKSALIDARUTAID:
                            break
                # BUSCAMOS SI EL VIAJE EXISTE EN LA TABLA VIAJES
                stmt4 = exists().where(Tablas.Viaje.ERPCO_CORRIDA_ID == ERPCOCORRIDAID)

                for _AUTOBUS_ID_VIAJE,\
                    CORRIDA_ID_TABLA_VIAJE,\
                    _FECHORSAL_VIAJE,\
                    _CONDUCTOR_ID_TAB_VIAJE,\
                        in db_session.query(Tablas.Viaje.AUTOBUS_ID,
                                            Tablas.Viaje.ERPCO_CORRIDA_ID,
                                            Tablas.Viaje.FECHA_HORA_PROGRAMADA_SALIDA,
                                            Tablas.Viaje.CONDUCTOR_ID).\
                            filter(stmt4):
                    break
                if CORRIDA_ID_TABLA_VIAJE == None and EstaRutaERPCO == True:
                    DicActualizaViajes = {
                        'RUTA_ID': str(_FKERPCORUTAID),
                        'AUTOBUS_ID': str(IdErpcoAutobus),
                        'CONDUCTOR_ID': str(Numempleado),
                        'FECHA_HORA_PROGRAMADA_SALIDA': str(FECHORSAL).replace(' ','T'),
                        'FECHA_HORA_REAL_SALIDA': str(FECHORSAL).replace(' ','T'),
                        'FECHA_HORA_PROGRAMADA_LLEGADA': str('1900-01-01T00:00:00'),
                        'FECHA_HORA_REAL_LLEGADA': str('1900-01-01T00:00:00'),
                        'ZONA_HORARIA_ID': str(7),
                        'VIAJE_STATUS_ID': str(1),
                        'FECHA_ACTUALIZACION': str(str(datetime.datetime.today())[0:19].replace(' ','T')),
                        'ERPCO_CORRIDA_ID': str(ERPCOCORRIDAID),
                        'ULTIMO_VIAJE_POSICION_ID': str(0)
                    }
                    if IdErpcoAutobus != None and Numempleado != None:
                        ViajeValido = False
                        _listParainsertarViajes.append(DicActualizaViajes)
                    #Buscamos los valores de RUTA_PARADA
                    _listRutaParada = \
                        db_session.query(Tablas.Ruta_Parada.RUTA_ID,
                                         Tablas.Ruta_Parada.PARADA_ID
                                         ). \
                            filter_by(RUTA_ID=_FKERPCORUTAID
                                      ).all()
                    for datos in _listRutaParada:
                        DicRutaParada = dict(zip('ab', datos))
                        PARADAID = DicRutaParada.get('b')
                        DicVIAJEPARADA = {
                            'VIAJE_ID': str(ERPCOCORRIDAID),
                            'PARADA_ID': str(PARADAID),
                            'FECHA_HORA_PROGRAMADA_LLEGADA':  str('1900-01-01T00:00:00'),
                            'FECHA_HORA_REAL_LLEGADA':  str('1900-01-01T00:00:00'),
                            'FECHA_HORA_PROGRAMADA_SALIDA': str('1900-01-01T00:00:00'),
                            'FECHA_HORA_REAL_SALIDA': str('1900-01-01T00:00:00'),
                            'ZONA_HORARIA_ID': str(7)
                        }
                        if ViajeValido:
                            _listViajePadada.append(DicVIAJEPARADA)
                    # Buscamos los valores de RUTA_TRECHO
                    _listRutaTrecho = \
                        db_session.query(Tablas.Ruta_Trecho.RUTA_ID,
                                         Tablas.Ruta_Trecho.TRECHO_ID,
                                         Tablas.Trecho_Trazado.ID,
                                         Tablas.Trecho_Trazado.PRIORIDAD,
                                         Tablas.Trecho_Trazado.DISTANCIA,
                                         Tablas.Trecho_Trazado.TIEMPO
                                         ). \
                            filter_by(RUTA_ID=_FKERPCORUTAID,
                                      TRECHO_ID = Tablas.Trecho_Trazado.TRECHO_ID
                                      ).\
                            order_by(Tablas.Ruta_Trecho.TRECHO_ID).all()
                    primeravuelta = 1
                    format = '%Y-%m-%dT%H:%M:%S'
                    for datos in _listRutaTrecho:
                        DicRutaTrecho = dict(zip('abcdef', datos))
                        TRECHOID = DicRutaTrecho.get('a')
                        TRECHO_TRAZADO_ID = DicRutaTrecho.get('c')
                        TIEMPOSEG = DicRutaTrecho.get('f')
                        if primeravuelta == 1:
                            fechainicio = str(FECHORSAL)
                            FECHORSAL =FECHORSAL + datetime.timedelta(seconds=TIEMPOSEG)
                            dtfechafin = FECHORSAL
                        else:
                            fechainicio = str(dtfechafin)
                            FECHORSAL = FECHORSAL + datetime.timedelta(seconds=TIEMPOSEG)
                            dtfechafin = FECHORSAL
                        DicVIAJETRECHO = {
                            'VIAJE_ID': str(ERPCOCORRIDAID),
                            'TRECHO_ID': str(TRECHOID),
                            'TRECHO_TRAZADO_ID': str(TRECHO_TRAZADO_ID),
                            'FECHA_HORA_PROGRAMADA_LLEGADA': str(fechainicio).replace(' ','T'),
                            'FECHA_HORA_REAL_LLEGADA': str('1900-01-01T00:00:00'),
                            'FECHA_HORA_PROGRAMADA_SALIDA': str(dtfechafin).replace(' ','T'),
                            'FECHA_HORA_REAL_SALIDA': str('1900-01-01T00:00:00')
                        }
                        if ViajeValido:
                            _listViajeTrecho.append(DicVIAJETRECHO)
                            primeravuelta += 1
                            _EntraaguardarLista = True

                elif  CORRIDA_ID_TABLA_VIAJE != None :
                    if CORRIDA_ID_TABLA_VIAJE == ERPCOCORRIDAID and  (_AUTOBUS_ID_VIAJE != IdErpcoAutobus or _CONDUCTOR_ID_TAB_VIAJE != Numempleado or _FECHORSAL_VIAJE != FECHORSAL):
                        DicActualizaViajes = {
                            'RUTA_ID': str(_FKERPCORUTAID),
                            'AUTOBUS_ID': str(IdErpcoAutobus),
                            'CONDUCTOR_ID': str(Numempleado),
                            'FECHA_HORA_PROGRAMADA_SALIDA': str(FECHORSAL),
                            'FECHA_HORA_REAL_SALIDA': str(FECHORSAL),
                            'FECHA_HORA_PROGRAMADA_LLEGADA': str('1900-01-01T00:00:00'),
                            'FECHA_HORA_REAL_LLEGADA': str('1900-01-01T00:00:00'),
                            'ZONA_HORARIA_ID': str(0),
                            'VIAJE_STATUS_ID': str(1),
                            'FECHA_ACTUALIZACION': str(str(datetime.datetime.today())[0:19]),
                            'ERPCO_CORRIDA_ID': str(ERPCOCORRIDAID),
                            'ULTIMO_VIAJE_POSICION_ID': str(0)
                        }
                        _listParainsertarViajes.append(DicActualizaViajes)
                        _EntraaguardarLista = True

                if EstaBus == False or EstaConductor == False :
                    if EstaBus == False:
                        if NombreAutobus != None and IdErpcoAutobus != None:
                            DicInsert = {
                            'DESCRIPTION': 'Autobus',
                            'ACTIVE': '1',
                            'NUMECONOMICO': str(NombreAutobus),
                            'ID_NUM_ERPCO': str(IdErpcoAutobus)
                        }
                            _listCatAutobuses.append(DicInsert)
                    if EstaConductor == False:
                        if Numempleado != None:
                            DicInsertConductor = {
                            'NAME': '',
                            'ACTIVE': '1',
                            'NUMEMPLEADO': str(Numempleado)
                        }
                            _listCatConductores.append(DicInsertConductor)

        self.insertadatosViajes(_listParainsertarViajes,_listViajePadada,_listViajeTrecho,_listCatConductores,_listCatAutobuses)
    #METODO QUE SE ENCARGA DE INSERTAR LOS BUSES SI NO SE ENCUENTRAN EN EL CATALOGO.
    def Creaautobuses(self,_listEC_ECT):
        #Creamos Listas Con Resultados Finales
        _listParainsertarViajes = []
        _listViajePadada = []
        _listViajeTrecho = []
        _listCatConductores = []
        _listCatAutobuses = []

        for datos in _listEC_ECT:
            ViajeValido = True
            DicEC_ECT = dict(zip('abcdefgh', datos))
            testdato = DicEC_ECT.get('a')
            EstaBus = False
            EstaConductor = False
            ERPCOCORRIDAID = DicEC_ECT.get('a')
            NombreAutobus = DicEC_ECT.get('c')
            IdErpcoAutobus = DicEC_ECT.get('d')
            Numempleado = DicEC_ECT.get('e')
            FECHORSAL = DicEC_ECT.get('f')
            FKSALIDARUTAID = DicEC_ECT.get('g')
            stmt = exists().where(Tablas.Autobus.NUMECONOMICO == NombreAutobus)
            for NUMECONOMICO, in db_session.query(Tablas.Autobus.NUMECONOMICO).filter(stmt):
                EstaBus = True
                if NUMECONOMICO == NombreAutobus:
                     break
            # Buscamos si el Conductor esta en las tabls de SAE si no esta lo insertamos
            stmt2 = exists().where(Tablas.Conductor.NUMEMPLEADO == Numempleado)
            for NUMECONOMICO, in db_session.query(Tablas.Conductor.NUMEMPLEADO).filter(stmt2):
                EstaConductor = True
                if NUMECONOMICO == Numempleado:
                    break
            if EstaBus == False or EstaConductor == False:
                if EstaBus == False:
                    if NombreAutobus != None and IdErpcoAutobus != None:
                        DicInsert = {
                            'DESCRIPTION': 'Autobus',
                            'ACTIVE': '1',
                            'NUMECONOMICO': str(NombreAutobus),
                            'ID_NUM_ERPCO': str(IdErpcoAutobus)
                        }
                        _listCatAutobuses.append(DicInsert)
                if EstaConductor == False:
                    if Numempleado != None:
                        DicInsertConductor = {
                            'NAME': '',
                            'ACTIVE': '1',
                            'NUMEMPLEADO': str(Numempleado)
                        }
                        _listCatConductores.append(DicInsertConductor)

        self.insertadatosViajes(_listParainsertarViajes, _listViajePadada, _listViajeTrecho, _listCatConductores,_listCatAutobuses)
    #METODO PARA INSERTAR DATOS
    def insertadatosViajes(self,listParainsertarViajes,listViajeParada,listViajeTrecho,_listCatConductores,_listCatAutobuses):
        if len(listParainsertarViajes) > 0 or len(listViajeParada) > 0 or len(listViajeTrecho) > 0 or len(_listCatConductores) > 0 or len(_listCatAutobuses) > 0:
            try:
                if len(_listCatAutobuses) > 0:
                    Insertabus = Tablas.Autobus.insert_many(_listCatAutobuses)
                if len(_listCatConductores) > 0:
                    Insertabus = Tablas.Conductor.insert_many(_listCatConductores)
                if len(listParainsertarViajes) > 0:
                    LOGRECORD = Tablas.Viaje.insert_many(listParainsertarViajes)
                if len(listViajeParada) > 0:
                    LOGRECORD = Tablas.Viaje_Parada.insert_many(listViajeParada)
                if len(listViajeTrecho) > 0:
                    LOGRECORD = Tablas.Viaje_Trecho.insert_many(listViajeTrecho)

            except:
                print("Unexpected error-->>: ", sys.exc_info()[0], file=sys.stderr)































