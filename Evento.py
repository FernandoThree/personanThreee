import requests
from datetime import datetime
from sys import stderr

from Almacenamiento.Tablas import Evento_Tipo
from .Seguridad import generar_fecha_sha256
from .Parametro import Parametro

''' class Evento
    Contiene los datos para definir un evento que se enviará al collector y este a su vez lo registrará en la base de datos.

    El método `enviar` debe ser llamada una vez que se ha iniciado sesión con la base de datos
'''
class Evento():
    def __init__(self, 
        fecha: datetime, 
        descripcion: str, 
        viaje_id: int,
        latitud: float, 
        longitud: float, 
        tipo:int = Evento_Tipo.enum.VIAJE.value, 
        mostrar: int = 1
    ):
        self.tipo        = tipo
        self.fecha       = fecha
        self.descripcion = descripcion
        self.mostrar     = mostrar
        self.viaje_id    = viaje_id
        self.metadata    = 'https://maps.google.com/?q=%f,%f' % (latitud, longitud)

    def __str__(self):
        return 'Fecha: %s, descripción: %s, viaje_id: %d, tipo: %d, mostrar: %d' % (str(self.fecha), self.descripcion, self.viaje_id, self.tipo, self.mostrar)

    def enviar(self):
        token = generar_fecha_sha256()
        hed   = {'Authorization': 'Bearer ' + token}
        json  = {'EVENTO': [{
            'EVENTO_TIPO_ID': self.tipo,
            'EVENTO_FECHA'  : self.fecha.strftime('%Y-%m-%dT%H:%M:%S'),
            'DESCRIPCION'   : self.descripcion,
            'METADATA'      : self.metadata,
            'MOSTRAR_EN_SINOPTICO': self.mostrar,
            'VIAJE_ID'      : str(self.viaje_id) if self.viaje_id else 'null'
        }]}
        try:
            respuesta = requests.post(Parametro().collector_event_url, json = json, headers = hed, timeout = 5)
            if respuesta.status_code != 200:
                print('Error, status %d. Ocurrió un error al enviar el evento a collector.' % respuesta.status_code, self, file=stderr)
            return respuesta
        except requests.exceptions.Timeout:
            print('Error al enviar Evento. Collector demora demasiado en responder', file=stderr)
        
        return None



