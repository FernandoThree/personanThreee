from Almacenamiento.Tablas import Sae_Parametro, Sae_Parametro_Autorregulacion
from sys import stderr

'''@ class Parametro
    Singleton para almacenar los parámetros usados por el servicio viajes, obtenidos de la base datos,
    el constructor debe ser llamado una vez que se ha iniciado sesión con la base de datos
'''
class Parametro():
    class __Parametro():
        def __init__(self):
            self.collector_url       = Sae_Parametro.get('collector-JsonGPS-get-url').VALOR.rstrip()
            self.collector_event_url = Sae_Parametro.get('collector-EventInsert-post-url').VALOR.rstrip()
            self.autorregulacion     = Sae_Parametro_Autorregulacion.get(1)

    instancia = None

    def __init__(self):
        if not Parametro.instancia:
            Parametro.instancia = Parametro.__Parametro()

    def __str__(self):
        return repr(self.instancia) + repr(self)

    def __getattr__(self, name):
        try:
            return getattr(self.instancia, name)
        except:
            Parametro.reload()
            return getattr(self.instancia, name)

    @classmethod
    def reload(cls):
        try:
            del cls.instancia
        except:
            print('Parametro.instancia ha sido borrada previamente', file=stderr)
        cls.instancia = Parametro.__Parametro()