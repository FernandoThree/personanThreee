from sys import stderr
from Almacenamiento import db_session
from Almacenamiento.Tablas import Ruta, Ruta_Parada, Ruta_Trecho, Trecho, Parada, Parada_Poligono, Trecho_Trazado, Trazado

'''@class Data 
    Singleton para almacenar información de rutas, trechos, trecho_trazados y trazados
    Debe ser inicializada después de iniciar la sesión con la base de datos (Almacenamiento.init_db)
'''
class Data():
    class __Data():
        def __init__(self):
            # Obtenemos datos de rutas, trechos, trecho_trazados, trazdos, paradas y parada_poligonos
            self.lst_Rutas         = Ruta.query_all({'ENTRENADO': 1})
            self.lst_Trechos       = Trecho.query_all({'ENTRENADO': 1, 'ACTIVE': 1})
            self.lst_TrechoTrazado = Trecho_Trazado.query_all({'ACTIVE':1})
            self.lst_Trazado       = db_session.query(Trazado).order_by(Trazado.TRECHO_TRAZADO_ID, Trazado.SEQUENCE).all()
            self.lst_Parada        = Parada.query_all({'ACTIVE': 1}) 
            # Desasociar datos de la sesión con base de datos
            for ruta in self.lst_Rutas:
                db_session.expunge(ruta)
            for trecho in self.lst_Trechos:
                db_session.expunge(trecho)
            for trecho_trazado in self.lst_TrechoTrazado:
                db_session.expunge(trecho_trazado)
            for trazado in self.lst_Trazado:
                db_session.expunge(trazado)
            for parada in self.lst_Parada:
                db_session.expunge(parada)
            
            # Guardar polígonos de las paradas indizados por PARADA_ID
            self.dic_ParadaPoligono = {}
            for parada in self.lst_Parada:
                lst_ParadaPoligono = db_session.query(Parada_Poligono).filter_by(PARADA_ID = parada.ID).order_by(
                    Parada_Poligono.SEQUENCE).all()
                # Desasociar datos de la sesión con base de datos
                for parada_poligono in lst_ParadaPoligono:
                    db_session.expunge(parada_poligono)
                
                self.dic_ParadaPoligono[parada.ID] = lst_ParadaPoligono

            #Iteramos en busca de las Rutas_Paradas y Rutas_Trechos
            self.lst_DATA = {}
            for ruta in self.lst_Rutas:
                lst_RutaParada  =db_session.query(Ruta_Parada).filter_by(RUTA_ID=ruta.ID).order_by(
                    Ruta_Parada.SEQUENCE).all()

                lst_RutaTrecho = db_session.query(Ruta_Trecho).filter_by(RUTA_ID=ruta.ID).order_by(
                    Ruta_Trecho.SEQUENCE).all()
                # Desasociar datos de la sesión con base de datos
                for ruta_parada in lst_RutaParada:
                    db_session.expunge(ruta_parada)
                for ruta_trecho in lst_RutaTrecho:
                    db_session.expunge(ruta_trecho)


                #Iteramos en busca de los trechos
                dic_TrechoTrazado = {}
                dic_Trazado = {}
                for ruta_trecho in lst_RutaTrecho:                    
                    lst_TrechoTrazado = [trecho_trazado for trecho_trazado in self.lst_TrechoTrazado if trecho_trazado.TRECHO_ID == ruta_trecho.TRECHO_ID]
                    dic_TrechoTrazado[ruta_trecho.TRECHO_ID] = lst_TrechoTrazado

                    for trecho_trazado in lst_TrechoTrazado:
                        lst_Trazado = [trazado for trazado in self.lst_Trazado if trazado.TRECHO_TRAZADO_ID == trecho_trazado.ID]
                        dic_Trazado[trecho_trazado.ID] = lst_Trazado

                #Guardamos la información de la ruta
                self.lst_DATA[ruta.ID] = {
                    "RUTA": ruta, 
                    "RUTA_PARADA": lst_RutaParada,
                    "RUTA_TRECHO": lst_RutaTrecho,
                    "TRECHO_TRAZADO": dic_TrechoTrazado,
                    "TRAZADO": dic_Trazado
                }        


    instancia = None

    def __init__(self):
        if (not hasattr(Data, 'instancia')) or Data.instancia is None:
            Data.instancia = Data.__Data()
            if __debug__:
                print('** Se ha cargado Data', file=stderr)

    def __str__(self):
        return repr(self.instancia) + repr(self)

    def __getattr__(self, name):
        try:
            return getattr(self.instancia, name)
        except:
            Data.reload()
            return getattr(self.instancia, name)

    @classmethod
    def reload(cls):
        try:
            del cls.instancia
        except:
            print('Data.instancia ha sido borrada previamente', file=stderr)
        cls.instancia = Data.__Data()