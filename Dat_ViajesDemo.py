from Almacenamiento import Tablas, Tablas_Erpco

class DatERPCO:
    def creaviajes(self):
        self.creadatos()

    def creadatos(self):
        dicpeticionERPCOCORRIDA={'RUTA_ID': '3722'}
        dicpeticionSAE_RUTA_DETALLE = {}
        dicpeticionRUTA = {}

        listaobjetosERPCOCORRIDA = Tablas_Erpco.ERPCO_CORRIDA.query_all(dicpeticionERPCOCORRIDA)
        listaobjetosSAE_RUTA_DETALLE = Tablas_Erpco.SAE_RUTA_DETALLE.query_all(dicpeticionSAE_RUTA_DETALLE)
        listaobjetosRUTA = Tablas.Ruta.query_all(dicpeticionRUTA)

        self.compruebaRUTAS(listaobjetosERPCOCORRIDA, listaobjetosSAE_RUTA_DETALLE,listaobjetosRUTA)
    def compruebaRUTAS(self,listaobjetosERPCOCORRIDA,listaobjetosSAE_RUTA_DETALLE,listaobjetosRUTA):
        ListViajes = []
        dicViajes = {}
        existevalor = 0
        #Barre datos ERPCO_CORRIDA y los convierte en DIICCIONARIOS
        for OBJETOTABLA in listaobjetosERPCOCORRIDA:
            dicERPCOCORRIDA = OBJETOTABLA.__dict__
            for llaveEC,valorEC in dicERPCOCORRIDA.items():
                if llaveEC == "RUTA_ID":
                    varvalorEC = valorEC
                    #Buscamos si existe esta Ruta en SAE_RUTA_DETALLE
                    for objSAE_RUTA_DETALLE  in listaobjetosSAE_RUTA_DETALLE :
                        dicSAE_RUTA_DETALLE  = objSAE_RUTA_DETALLE.__dict__
                        for llaveSRD, valorSRD in dicSAE_RUTA_DETALLE.items():
                            if llaveSRD == "FK_ERPCO_RUTA_ID":
                                if valorSRD == varvalorEC:
                                    existevalor = 1
                                    FK_RUTA = dicSAE_RUTA_DETALLE["FK_SALIDA_RUTA_ID"]


                                    # Buscamos si existe esta Ruta en RUTA
                                    for obj_RUTA in listaobjetosRUTA:
                                        dic_RUTA = obj_RUTA.__dict__
                                        for llaveR, valorR in dic_RUTA.items():
                                            if llaveR == "ID":
                                                if valorR == FK_RUTA:
                                                    existevalor = 1

                                                    if existevalor == 1:
                                                        dicViajes  = {
                                                            "CORRIDA_ID": str(dicERPCOCORRIDA["CORRIDA_ID"]),
                                                            "RUTA_ID": str(dicERPCOCORRIDA["RUTA_ID"])
                                                    }
                                                    ListViajes.append(dicViajes)
        return 1











