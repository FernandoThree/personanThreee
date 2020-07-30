import datetime
import sys
import operator

from Almacenamiento import Tablas, Ejecutor, db_session
from Util.Carga_Data import Data
from .Utileriasapp import ReeplazaFechaViaje
from .Carga_Datos import Cargar_Datos

class DatERPCO:
    def creaviajes(self):
        #Creamos Listas Con Resultados Finales
        _listParainsertarViajes = []
        _listViajePadada = []
        _listViajeTrecho = []
        _listCatConductores = []
        _listCatAutobuses = []

        #CARGAMOS LOS DATOS DE LAS TABLAS A UTILIZAR
        _listEC_ECT,_list_Autobus, _list_Conductor,_list_ViajesSAE, IDTABLAVIAJE = Cargar_Datos()

        #CREA LOS CATALOGOS DE AUTOBUS Y CONDUCTORReeplazaFechaViaje
        _listCatAutobuses,_listCatConductores = self.Creaautobuses(_listEC_ECT,_list_Autobus,_list_Conductor)
        #COMIENZA BARRIDO DE VIAJES
        for datos in _listEC_ECT:
            Numempleado = datos.CONDUCTOR1_ID if datos.CONDUCTOR1_ID else 0

             #BUSCAMOS SI ESTA LA RUTA DEL VIAJE EN RUTA
            if not datos.FK_RUTA_ID in Data().lst_DATA:
                continue

            # BUSCAMOS SI EL VIAJE EXISTE EN LA TABLA VIAJES
            for _viaje in _list_ViajesSAE:
                if _viaje.ERPCO_CORRIDA_ID == datos.CORRIDA_ID:
                    viaje = _viaje
                    break
            else:
                viaje = None

            if viaje is None or (
                viaje.VIAJE_STATUS_ID in {3,4,5}
                and viaje.FECHA_HORA_PROGRAMADA_SALIDA != datos.FECHORSAL
                and viaje.AUTOBUS_ID != datos.AUTOBUS_ID
            ):
                if viaje is not None and viaje.VIAJE_STATUS_ID == 1:
                    self.Eliminaviajes(viaje)

                # Crear VIAJE, VIAJE_PARADA y VIAJE_TRECHO
                IDTABLAVIAJE += 1
                ID_VIAJE = IDTABLAVIAJE
                DicActualizaViajes = {
                    'ID': str(ID_VIAJE),
                    'RUTA_ID': str(datos.FK_RUTA_ID),
                    'AUTOBUS_ID': str(datos.AUTOBUS_ID),
                    'CONDUCTOR_ID': str(Numempleado),
                    'FECHA_HORA_PROGRAMADA_SALIDA': str(datos.FECHORSAL).replace(' ','T'),
                    'FECHA_HORA_REAL_SALIDA': str(datos.FECHORSAL).replace(' ','T'),
                    'FECHA_HORA_PROGRAMADA_LLEGADA': str(datos.FECHORLLE).replace(' ','T'),
                    'FECHA_HORA_REAL_LLEGADA': str(datos.FECHORLLE).replace(' ','T'),
                    'ZONA_HORARIA_ID': str(7),
                    'VIAJE_STATUS_ID': str(1),
                    'FECHA_ACTUALIZACION': str(str(datetime.datetime.today())[0:19].replace(' ','T')),
                    'ERPCO_CORRIDA_ID': str(datos.CORRIDA_ID),
                    'ULTIMO_VIAJE_POSICION_ID': str(0)
                }

                _listViajeParadaClon, _listViajeTrechoClon = self.CreaViajeParadaViajeTrecho(datos.FK_RUTA_ID, datos.FECHORSAL, ID_VIAJE)
                _listViajePadada.extend(_listViajeParadaClon)
                _listViajeTrecho.extend(_listViajeTrechoClon)

                DicActualizaViajes['FECHA_HORA_PROGRAMADA_LLEGADA'] = _listViajeParadaClon[-1]['FECHA_HORA_PROGRAMADA_LLEGADA']
                DicActualizaViajes['FECHA_HORA_REAL_LLEGADA'] = _listViajeParadaClon[-1]['FECHA_HORA_PROGRAMADA_LLEGADA']
                _listParainsertarViajes.append(DicActualizaViajes)

        self.insertadatosViajes(_listParainsertarViajes, _listViajePadada, _listViajeTrecho,
                                            _listCatConductores,
                                            _listCatAutobuses)
        if __debug__:
            for viaje in _listParainsertarViajes:
                print(viaje,file=sys.stderr)
        return _listParainsertarViajes

    #METODO QUE SE ENCARGA DE INSERTAR LOS BUSES SI NO SE ENCUENTRAN EN EL CATALOGO.
    def Creaautobuses(self,_listEC_ECT,_list_Autobus,_list_Conductor):
        #Creamos Listas Con Resultados Finales
        _listCatConductores = []
        _listCatAutobuses = []
        #Cargamos datos de los catalogos de Autobuses y Conductores.
        for datos in _listEC_ECT:
            IdErpcoAutobus = datos.AUTOBUS_ID
            Numempleado = datos.CONDUCTOR1_ID

            #Busca si esta el bus en el catalogo
            for datosautobus in _list_Autobus:
                if str(datosautobus.NUMECONOMICO).strip() == str(IdErpcoAutobus).strip():
                    break
            else:
                if  IdErpcoAutobus != None:
                    DicInsert = {
                        'DESCRIPTION': 'Autobus',
                        'ACTIVE': '1',
                        'NUMECONOMICO': str(IdErpcoAutobus),
                        'ID_NUM_ERPCO': str(IdErpcoAutobus)
                    }
                    _listCatAutobuses.append(DicInsert)

            #Busca si esta el conductor en el catalogo
            if Numempleado is not None:
                for datosconductores in _list_Conductor:
                    if str(datosconductores.NUMEMPLEADO).strip() == str(Numempleado).strip():
                        break
                else:
                    if Numempleado is None or Numempleado == '':
                        Numempleado = 1
                    DicInsertConductor = {
                            'NAME': '',
                            'ACTIVE': '1',
                            'NUMEMPLEADO': str(Numempleado)
                        }
                    _listCatConductores.append(DicInsertConductor)

        return _listCatAutobuses,_listCatConductores

    #METODO QUE SE ENCARGA DE LLENAR LAS LISTAS PARA QUE SE GUARDEN LOS DATOS DE VIAJE_PARADA Y VIAJE_TRECHO
    def CreaViajeParadaViajeTrecho(self, _FKERPCORUTAID, FECHORSAL, ID_VIAJE):
        # Recuperar listas de ruta_paradas y ruta_trechos
        data = Data()
        _list_ruta_parada = data.lst_DATA[_FKERPCORUTAID]['RUTA_PARADA']
        _list_ruta_trechos = data.lst_DATA[_FKERPCORUTAID]['RUTA_TRECHO']
        # Creamos el diccionario Trazados_trechos con el id de trecho definido tomando el trazado con mayor prioridad
        dictTRECHO_TRAZADO = {}
        dic_trecho_trazado = data.lst_DATA[_FKERPCORUTAID]['TRECHO_TRAZADO']
        for trecho_id, list_trecho_trazado in dic_trecho_trazado.items():
            for trecho_trazado in list_trecho_trazado:
                if (not trecho_id in dictTRECHO_TRAZADO) or trecho_trazado.PRIORIDAD > dictTRECHO_TRAZADO[trecho_id].PRIORIDAD:
                    dictTRECHO_TRAZADO[trecho_id] = trecho_trazado

        # armar fechas programadas
        _listViajePadada = []
        _listViajeTrecho = []

        fecha_act = FECHORSAL
        # Primera parada
        DicVIAJEPARADA = {
            'VIAJE_ID': str(ID_VIAJE),
            'PARADA_ID': str(_list_ruta_parada[0].PARADA_ID),
            'FECHA_HORA_PROGRAMADA_LLEGADA': str('1900-01-01T00:00:00'),
            'FECHA_HORA_REAL_LLEGADA': str('1900-01-01T00:00:00'),
            'FECHA_HORA_PROGRAMADA_SALIDA': str(fecha_act).replace(' ', 'T'),
            'FECHA_HORA_REAL_SALIDA': str(fecha_act).replace(' ', 'T'),
            'ZONA_HORARIA_ID': str(7)
        }
        _listViajePadada.append(DicVIAJEPARADA)

        # Todos los trechos, y desde segunda parada hasta última
        for i in range(len(_list_ruta_trechos)):
            trecho_id = _list_ruta_trechos[i].TRECHO_ID
            trecho_trazado = dictTRECHO_TRAZADO[trecho_id]

            fecha_ant = fecha_act 
            fecha_act += datetime.timedelta(seconds = trecho_trazado.TIEMPO) 

            DicVIAJETRECHO = {
                'VIAJE_ID': str(ID_VIAJE),
                'TRECHO_ID': str(_list_ruta_trechos[i].TRECHO_ID),
                'TRECHO_TRAZADO_ID': str(trecho_trazado.ID),
                'FECHA_HORA_PROGRAMADA_LLEGADA': str(fecha_ant).replace(' ', 'T'),
                'FECHA_HORA_REAL_LLEGADA': str(fecha_ant).replace(' ', 'T'),
                'FECHA_HORA_PROGRAMADA_SALIDA': str(fecha_act).replace(' ', 'T'),
                'FECHA_HORA_REAL_SALIDA': str(fecha_act).replace(' ', 'T')
            }
            _listViajeTrecho.append(DicVIAJETRECHO)
            
            fecha_ant = fecha_act
            if _list_ruta_parada[i+1].ESTANCIA > 0:
                fecha_act += datetime.timedelta(seconds = _list_ruta_parada[i+1].ESTANCIA)

            DicVIAJEPARADA = {
                'VIAJE_ID': str(ID_VIAJE),
                'PARADA_ID': str(_list_ruta_parada[i+1].PARADA_ID),
                'FECHA_HORA_PROGRAMADA_LLEGADA': str(fecha_ant).replace(' ', 'T'),
                'FECHA_HORA_REAL_LLEGADA': str(fecha_ant).replace(' ', 'T'),
                'FECHA_HORA_PROGRAMADA_SALIDA': str(fecha_act).replace(' ', 'T'),
                'FECHA_HORA_REAL_SALIDA': str(fecha_act).replace(' ', 'T'),
                'ZONA_HORARIA_ID': str(7)
            }            
            _listViajePadada.append(DicVIAJEPARADA)

            # Quitar fecha salida última parada
            _listViajePadada[-1]['FECHA_HORA_PROGRAMADA_SALIDA'] = str('1900-01-01T00:00:00')
            _listViajePadada[-1]['FECHA_HORA_REAL_SALIDA'] = str('1900-01-01T00:00:00')

        return _listViajePadada,_listViajeTrecho

    # METODO QUE SE ENCARGA DE ELIMINAR RASTRO DE VIAJES CAMBIADOS POR ERPCO.
    def Eliminaviajes(self, viaje: Tablas.Viaje):
        Tablas.Viaje_Trecho.__table__.delete().where(Tablas.Viaje_Trecho.VIAJE_ID == viaje.ID)
        Tablas.Viaje_Parada.__table__.delete().where(Tablas.Viaje_Parada.VIAJE_ID == viaje.ID)
        viaje.delete()
    
    #METODO PARA INSERTAR DATOS
    def insertadatosViajes(self,listParainsertarViajes,listViajeParada,listViajeTrecho,_listCatConductores,_listCatAutobuses):
        if len(_listCatAutobuses) > 0:
            Tablas.Autobus.insert_many(_listCatAutobuses)
        if len(_listCatConductores) > 0:
            Tablas.Conductor.insert_many(_listCatConductores)
        if len(listParainsertarViajes) > 0:
            Tablas.Viaje.insert_many(listParainsertarViajes)
        if len(listViajeParada) > 0:
            Tablas.Viaje_Parada.insert_many(listViajeParada)
        if len(listViajeTrecho) > 0:
            Tablas.Viaje_Trecho.insert_many(listViajeTrecho)