from datetime import datetime

class Logrecord():
    def __init__(self, logrecord: dict):
        self.autobus = int(logrecord['Autobus'])
        self.region = int(logrecord['Region']) 
        self.fecha_registro = datetime.strptime(logrecord['fecharegistro'], '%Y-%m-%dT%H:%M:%S')
        self.latitud = float(logrecord['latitud'])
        self.longitud = float(logrecord['longitud'])
        self.velocidad = float(logrecord['Velocidad'])