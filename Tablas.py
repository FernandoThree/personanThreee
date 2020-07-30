from sqlalchemy import Column, Integer, String, DateTime, NVARCHAR, NCHAR, VARCHAR, Float, BIGINT, Time
from sqlalchemy.dialects.mssql import TINYINT, BIT
from sqlalchemy.exc import SQLAlchemyError
import datetime
from enum import Enum
from Almacenamiento import db_session, Base
import sys
"""@function update
    envía los cambios realizados en los objetos mapeados hacia la base de datos
"""
def update():
    db_session.commit()

"""@class Tabla
    Clase base para el mapeo de tablas de la base de datos, define métodos comunes.
    Sus métodos de clase sólo pueden ser llamados por una subclase que herede también 
    de la clase Base.
"""
class Tabla():
    def __repr__(self):
        return self.__dict__

    def __str__(self):
        d = dict(self.__dict__)
        del d['_sa_instance_state']
        return str(d)
    
    """@method add
        agrega el objeto actual en la base de datos
    """
    def add(self):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError as e:
            print('add: SQLAlchemyError: ', str(e), self,file=sys.stderr)
            raise Exception('error de insercion')

    """@method delete
        elimina el objeto actual de la base de datos
    """
    def delete(self):
        try:
            db_session.delete(self)
            db_session.commit()
        except SQLAlchemyError as e:
            print('delete, SQLAlchemyError: ', e, self,file=sys.stderr)
            raise Exception('error de borrado')

    """@method update
        actuliza el objeto actual en la base de datos
        @param      entity(dict)        especificación de columnas
    """
    def update(self, entity: dict):
        for key, value in entity.items():
            setattr(self, key, value)
        db_session.commit()

    """@classmethod get
        recupera el registro de la base de datos correspondiente a la 
        llave principal pasada como parámetro
        @param      key                 valor de llave primaria

        return      [TableClas]         registro correspondiente
    """
    @classmethod
    def get(cls, key):
        return db_session.query(cls).get(key)

    """@classmethod insert
        crea una instancia de [TableClass], la escribe en la base de datos
        y la devuevle.
            INSERT INTO [TABLE] ...
        @param      entity(dict)        especificación de columnas

        @return [TableClass]
    """
    @classmethod
    def insert(cls, entity: dict):
        try:
            _entity = cls(**entity)
            db_session.add(_entity)
            db_session.commit()
            return _entity
        except SQLAlchemyError as e:
            print('insert: SQLAlchemyError: ', e, entity,file=sys.stderr)
            return None

    """@classmethod insert_many
        crea una instancia de [TableClass] en la base de datos
        por cada uno de los registros que se le pasan.
        Recibe una lista de diccionarios que contienen los registos a insertar.
            INSERT INTO [TABLE] ... VALUES ...
        @param      entities        especificación de columnas
    """    
    @classmethod
    def insert_many(cls, entities):
        if isinstance(entities, list) or isinstance(entities, tuple):
            db_session.bulk_insert_mappings(cls, entities)
            db_session.commit()

    """@classmethod update_many
        actualiza en la base de datos los registros pasados como parámetro,
        Recibe una lista de diccionarios con los registros a actualizar,
        es necesario que la llave primaria esté indicada.        
        @param      entities        especificación de columnas
    """        
    @classmethod
    def update_many(cls, entities):
        if isinstance(entities, list) or isinstance(entities, tuple):
            db_session.bulk_update_mappings(cls, entities)
            db_session.commit()

    """@classmethod extracts
        primeramente aplica una consulta SQL para recuperar el primer 
        registro que coincida con los filtros pasados como parámetro:
            SELECT TOP(1) FROM [TABLE] WHERE ... LIMIT 1
        si lo encontró entonces aplica una sentenca SQL para borrarlo
            DELETE FROM [TABLE] WHERE ...
        @param      entity(dict)    especificación de columnas

        @return     [TableClass]    el registro borrado
    """
    @classmethod
    def extract(cls, entity: dict):
        try:
            _entity = db_session.query(cls).filter_by(**entity).first()
            db_session.delete(_entity)
            db_session.commit()
            return _entity
        except SQLAlchemyError as e:
            print('extract: SQLAlchemyError: ', e, entity,file=sys.stderr)
            return None

    """@classmethod extracts
        borra todos los registros indicados en una lista o un diccioario
            DELETE FROM [TABLE] WHERE ...
        @param      entity(dict)    especificación de columnas

        @return     [TableClass]    el registro borrado
    """
    @classmethod
    def extract_many(cls, entities):
        if isinstance(entities, list) or isinstance(entities, tuple):
            for entity in entities:
                try:
                    _entity = cls.query_one(entity)
                    db_session.delete(_entity)
                except SQLAlchemyError as e:
                    print('extract_many: SQLAlchemyError: ', e, entity,file=sys.stderr)
            db_session.commit()
        else:
            for key in entities:
                try:
                    _entity = cls.get(key)
                    db_session.delete(_entity)
                except SQLAlchemyError as e:
                    print('extract_many: SQLAlchemyError: ', e, key)
            db_session.commit()

    """@classmethod query_one
        devuelve el primer resultado de aplicar una sentencia SQL:
        SELECT TOP(1) FROM [TABLE] WHERE ...
        aplicando los filtros pasados como parámetros
        @param  entity(dict)    especificación de columnas

        @return [TableClass]    
    """
    @classmethod
    def query_one(cls, entity: dict):
        try:
            return db_session.query(cls).filter_by(**entity).first()
        except SQLAlchemyError as e:
            print('query_one: SQLAlchemyError: ', e, entity,file=sys.stderr)
            return None

    """@classmethod query
        devuelve el resultado de aplicar una sentencia SQL:
            SELECT * FROM [TABLE] WHERE ...
        aplicando los filtros recibidos como parametros 
        @param  entity(dict)   especificación de columnas

        @return     list([TableClass])
    """
    @classmethod
    def query_all(cls, entity: dict):
        try :
            result = db_session.query(cls).filter_by(**entity).all()   #list
            return result
        except SQLAlchemyError as e:
            print('query_all: SQLAlchemyError: ', e, entity,file=sys.stderr)
            return None


class Autobus(Base,Tabla):
    __tablename__ = 'AUTOBUS'
    ID          = Column(Integer, primary_key = True)   #Identity by default
    DESCRIPTION = Column(VARCHAR(50))
    ACTIVE      = Column(Integer)
    NUMECONOMICO = Column(VARCHAR(50))
    ID_NUM_ERPCO = Column(VARCHAR(50))

    def __init__(self,
                ID: int = None,
                DESCRIPTION: str = None,
                ACTIVE: int = None,
                NUMECONOMICO: str = None,
                ID_NUM_ERPCO: str = None
                ):
        self.ID          = ID
        self.DESCRIPTION = DESCRIPTION
        self.ACTIVE      = ACTIVE
        self.NUMECONOMICO = NUMECONOMICO
        self.ID_NUM_ERPCO = ID_NUM_ERPCO

class Clima_Tipo(Base,Tabla):
    __tablename__ = 'CLIMA_TIPO'
    ID          = Column(Integer, primary_key = True)   #Identity by default
    DESCRIPTION = Column(NCHAR(50))
    ACTIVE      = Column(Integer)

    def __init__(self, ID: int  = None, DESCRIPTION: str = None, ACTIVE: int = None):
        self.ID          = ID
        self.DESCRIPTION = DESCRIPTION
        self.ACTIVE      = ACTIVE

class Color(Base, Tabla):
    __tablename__ = 'COLOR'
    ID          = Column(Integer, primary_key = True)   #Identity by default
    NAME        = Column(NCHAR(50))
    VALUE       = Column(NCHAR(10))
    ACTIVE      = Column(Integer)

    def __init__(self, ID: int  = None, NAME: str = None, VALUE: str = None, ACTIVE: int = None):
        self.ID          = ID
        self.NAME        = NAME
        self.VALUE       = VALUE
        self.ACTIVE      = ACTIVE

    class Color_enum(Enum):
        NEGRO       = 1
        BLANCO      = 2
        ROJO        = 3
        VERDE       = 4
        AZUL        = 5
        AMARILLO    = 6
        CIAN        = 7
        MAGENTA     = 8
        MORADO      = 9
        MARINO      = 10
        TURQUESA    = 11
        LIMA        = 12
        FUCSIA      = 13
        NARANJA     = 14

class Conductor(Base, Tabla):
    __tablename__ = 'CONDUCTOR'
    ID          = Column(Integer, primary_key = True)   #Identity by default
    NAME        = Column(NCHAR(50))
    ACTIVE      = Column(Integer)
    NUMEMPLEADO = Column(NCHAR(100))

    def __init__(self, ID: int = None, NAME: str = None, ACTIVE: int = None, NUMEMPLEADO: str = None):
        self.ID          = ID
        self.NAME        = NAME
        self.ACTIVE      = ACTIVE
        self.NUMEMPLEADO = NUMEMPLEADO

class Evento(Base, Tabla):
    __tablename__ = 'EVENTO'
    ID              = Column(Integer, primary_key = True)   #Identity by default
    EVENTO_TIPO_ID  = Column(Integer)
    HORA_EVENTO     = Column(Integer)
    DIA_EVENTO      = Column(Integer)
    MES_EVENTO      = Column(Integer)
    AÑO_EVENTO      = Column(Integer)
    PARADA_ID       = Column(Integer)
    TRECHO_ID       = Column(Integer)

    def __init__(
        self, ID:       int = None, 
        EVENTO_TIPO_ID: int = None, 
        HORA_EVENTO:    int = None, 
        DIA_EVENTO:     int = None,
        MES_EVENTO:     int = None, 
        AÑO_EVENTO:     int = None, 
        PARADA_ID:      int = None, 
        TRECHO_ID:      int = None):
        self.ID             = ID
        self.EVENTO_TIPO_ID = EVENTO_TIPO_ID
        self.HORA_EVENTO    = HORA_EVENTO
        self.DIA_EVENTO     = DIA_EVENTO
        self.MES_EVENTO     = MES_EVENTO
        self.AÑO_EVENTO     = AÑO_EVENTO
        self.PARADA_ID      = PARADA_ID
        self.TRECHO_ID      = TRECHO_ID

class Evento_Tipo(Base, Tabla):
    __tablename__ = 'EVENTO_TIPO'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    DESCRIPTION   = Column(NCHAR(50))
    ACTIVE        = Column(Integer)

    class enum(Enum):
        VIAJE       = 1
        MENSAJE     = 2
        SISTEMA     = 3
        PRIORITARIO = 4
        OTRO        = 5

    def __init__(self, ID: int = None, DESCRIPTION: String = None, ACTIVE: int = None):
        self.ID           = ID
        self.DESCRIPTION  = DESCRIPTION
        self.ACTIVE       = ACTIVE

class Evento_Viaje(Base, Tabla):
    __tablename__ = 'EVENTO_VIAJE'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    EVENTO_ID     = Column(Integer)
    VIAJE_ID      = Column(Integer)
    SEQUENCE      = Column(Integer)

    def __init__(self, ID: int = None, EVENTO_ID: int = None, VIAJE_ID: int = None, SEQUENCE: int = None):
        self.ID        = ID        
        self.EVENTO_ID = EVENTO_ID
        self.VIAJE_ID  = VIAJE_ID 
        self.SEQUENCE  = SEQUENCE 

class Log(Base, Tabla):
    __tablename__ = 'LOG'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    LOG_TYPE_ID   = Column(Integer)
    DATE          = Column(DateTime, default=datetime.datetime.utcnow)
    HEADER        = Column(NVARCHAR(None))
    DETAIL        = Column(NVARCHAR(None))
    USER_ID       = Column(Integer)
    TABLE_NAME    = Column(NCHAR(50))
    TABLE_PK_ID   = Column(Integer)
    APPLICATION   = Column(NVARCHAR(None))
    CONTROLLER    = Column(NVARCHAR(None))
    FUNCTIONS     = Column(NVARCHAR(None))
    QUERY         = Column(NVARCHAR(None))
    ACTIVE        = Column(Integer)

    def __init__(self, 
        ID         :int = None,
        LOG_TYPE_ID:int = None,
        DATE       :datetime.datetime = None,
        HEADER     :str = None,
        DETAIL     :str = None,
        USER_ID    :int = None,
        TABLE_NAME :str = None,
        TABLE_PK_ID:int = None,
        APPLICATION:str = None,
        CONTROLLER :str = None,
        FUNCTIONS  :str = None,
        QUERY      :str = None,
        ACTIVE     :int = None        
    ):
        self.ID          = ID         
        self.LOG_TYPE_ID = LOG_TYPE_ID
        self.DATE        = DATE       
        self.HEADER      = HEADER     
        self.DETAIL      = DETAIL     
        self.USER_ID     = USER_ID    
        self.TABLE_NAME  = TABLE_NAME 
        self.TABLE_PK_ID = TABLE_PK_ID
        self.APPLICATION = APPLICATION
        self.CONTROLLER  = CONTROLLER 
        self.FUNCTIONS   = FUNCTIONS  
        self.QUERY       = QUERY      
        self.ACTIVE      = ACTIVE     

class Log_Type(Base, Tabla):
    __tablename__ = 'LOG_TYPE'
    ID          = Column(Integer, primary_key = True)   #Identity by default
    NAME        = Column(NCHAR(50))
    CODE        = Column(NCHAR(50))
    ACTIVE      = Column(Integer)

    def __init__(self, 
        ID    : int = None,
        NAME  : str = None,
        CODE  : str = None,
        ACTIVE: int = None
    ):
        self.ID     = ID    
        self.NAME   = NAME  
        self.CODE   = CODE  
        self.ACTIVE = ACTIVE

class Multiruta(Base, Tabla):
    __tablename__ = 'MULTIRUTA'
    ID          = Column(Integer, primary_key = True)   #Identity by default
    NAME        = Column(NCHAR(50))
    ACTIVE      = Column(Integer)
    COLOR_ID    = Column(Integer)

    def __init__(self, 
        ID      : int = None,
        NAME    : str = None,
        ACTIVE  : int = None,
        COLOR_ID: int = None
    ):
        self.ID       = ID    
        self.NAME     = NAME  
        self.ACTIVE   = ACTIVE
        self.COLOR_ID = COLOR_ID

class Multiruta_Ruta(Base, Tabla):
    __tablename__ = 'MULTIRUTA_RUTA'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    MULTIRUTA_ID  = Column(Integer)
    RUTA_ID       = Column(Integer)

    def __init__(self, 
        ID          : int = None,
        MULTIRUTA_ID: int = None,
        RUTA_ID     : int = None
    ):
        self.ID           = ID    
        self.MULTIRUTA_ID = MULTIRUTA_ID
        self.RUTA_ID      = RUTA_ID

class Parada(Base, Tabla):
    __tablename__ = 'PARADA'
    ID              = Column(Integer, primary_key = True)   #Identity by default
    NAME            = Column(NCHAR(50))          
    ACTIVE          = Column(Integer)
    COLOR_ID        = Column(Integer)  
    PARADA_TIPO_ID  = Column(Integer)        
    ZONA_HORARIA_ID = Column(Integer)

    def __init__(self, 
        ID             : int = None,
        NAME           : str = None,
        ACTIVE         : int = None,
        COLOR_ID       : int = None,
        PARADA_TIPO_ID : int = None,
        ZONA_HORARIA_ID: int = None
    ):
        self.ID             = ID            
        self.NAME           = NAME          
        self.ACTIVE         = ACTIVE        
        self.COLOR_ID       = COLOR_ID      
        self.PARADA_TIPO_ID = PARADA_TIPO_ID
        self.ZONA_HORARIA_ID= ZONA_HORARIA_ID 

class Viaje_Autoregulacion(Base, Tabla):
    __tablename__                               = 'VIAJE_AUTOREGULACION'
    ID                                          = Column(Integer, primary_key = True)   #Identity by default
    AUTOBUS                                     = Column(VARCHAR(20))
    ULTIMA_CONEXION_GPS                         = Column(DateTime)
    VIAJE_AUTOBUS_ADELANTE                      = Column(VARCHAR(10))
    VIAJE_COLOR_FRECUENCIA_ADELANTE             = Column(VARCHAR(2))
    VIAJE_ID_ADELANTE                           = Column(Integer)
    VIAJE_FREC_ATRAS                            = Column(Integer)
    VIAJE_FREC_ATRAS_PROGRAMADA                 = Column(Integer)
    VIAJE_AUTOBUS_ATRAS                         = Column(VARCHAR(10))
    VIAJE_COLOR_FRECUENCIA_ATRAS                = Column(VARCHAR(2))
    VIAJE_ID_ATRAS                              = Column(Integer)
    FREC_TOLERANCIA_AMARILLO                    = Column(Integer)
    FREC_TOLERANCIA_ROJO                        = Column(Integer)
    PARADA_ID_ULTIMA                            = Column(Integer)
    COLISION_PARADA_ULTIMA_HORA                 = Column(DateTime)
    DISTANCIA_PARADA_ULTIMA                     = Column(Integer)
    FECHA_ACTUALIZACION                         = Column(DateTime)
    LAT                                         = Column(Float)
    LON                                         = Column(Float) 
    VEL                                         = Column(Float)
    DISTANCIA_RECORRIDA_TOTAL                   = Column(Float)
    TRECHO_ACTUAL_ID                            = Column(Integer)
    TRECHO_TRAZADO_ACTUAL_ID                    = Column(Integer)
    TRECHO_TRAZADO_DISTANCIA_RECORRIDA_PARCIAL  = Column(Float)
    RUTA_ID                                     = Column(Integer)
    VIAJE_ID                                    = Column(Integer)
    VIAJE_STATUS_ID                             = Column(Integer)
    VIAJE_ULTIMA_POSICION_ID                    = Column(Integer)
    VIAJE_SALIDA_REAL                           = Column(DateTime)
    VIAJE_PUNTUALIDAD                           = Column(Integer)
    VIAJE_COLOR_PUNTUALIDAD                     = Column(VARCHAR(100))
    VIAJE_PUNTUALIDAD_TOLERANCIA_AMARILLO       = Column(Integer)
    VIAJE_PUNTUALIDAD_TOLERANCIA_ROJO           = Column(Integer)
    VIAJE_FREC_ADELANTE                         = Column(Integer)
    VIAJE_FREC_ADELANTE_PROGRAMADA              = Column(DateTime)
    MENSAJE                                     = Column(VARCHAR(2048))
    ENVIADO                                     = Column(Integer)
    def __init__(self,
      	ID                                          : int = None, 
        AUTOBUS                                     : str = None,
        ULTIMA_CONEXION_GPS                         : datetime.datetime = None, 
        VIAJE_AUTOBUS_ADELANTE                      : str  = None,
        VIAJE_COLOR_FRECUENCIA_ADELANTE             : str  = None,
        VIAJE_ID_ADELANTE                           : int  = None,
        VIAJE_FREC_ATRAS                            : int  = None,
        VIAJE_FREC_ATRAS_PROGRAMADA                 : int  = None,
        VIAJE_AUTOBUS_ATRAS                         : str  = None,
        VIAJE_COLOR_FRECUENCIA_ATRAS                : str  = None,
        VIAJE_ID_ATRAS                              : int  = None,
        FREC_TOLERANCIA_AMARILLO                    : int  = None,
        FREC_TOLERANCIA_ROJO                        : int  = None,
        PARADA_ID_ULTIMA                            : int  = None,
        COLISION_PARADA_ULTIMA_HORA                 : datetime.datetime  = None,
        DISTANCIA_PARADA_ULTIMA                     : int  = None,
        FECHA_ACTUALIZACION                         : datetime.datetime  = None,
        LAT                                         : float = None,
        LON                                         : float = None,
        VEL                                         : float = None,
        DISTANCIA_RECORRIDA_TOTAL                   : float = None,
        TRECHO_ACTUAL_ID                            : int = None,
        TRECHO_TRAZADO_ACTUAL_ID                    : int = None,
        TRECHO_TRAZADO_DISTANCIA_RECORRIDA_PARCIAL  : float = None,
        RUTA_ID                                     : int = None,
        VIAJE_ID                                    : int = None,
        VIAJE_STATUS_ID                             : int = None,
        VIAJE_ULTIMA_POSICION_ID                    : int = None,
        VIAJE_SALIDA_REAL                           : datetime.datetime  = None,
        VIAJE_PUNTUALIDAD                           : int = None,
        VIAJE_COLOR_PUNTUALIDAD                     : str  = None, 
        VIAJE_PUNTUALIDAD_TOLERANCIA_AMARILLO       : int  = None,
        VIAJE_PUNTUALIDAD_TOLERANCIA_ROJO           : int  = None,
        VIAJE_FREC_ADELANTE                         : int  = None,
        VIAJE_FREC_ADELANTE_PROGRAMADA              : datetime.datetime  = None,
        MENSAJE                                     : str  = None,
        ENVIADO                                     : int  = None
    ):
        self.ID                                          = ID
        self.AUTOBUS                                     = AUTOBUS
        self.ULTIMA_CONEXION_GPS                         = ULTIMA_CONEXION_GPS
        self.VIAJE_AUTOBUS_ADELANTE                      = VIAJE_AUTOBUS_ADELANTE
        self.VIAJE_COLOR_FRECUENCIA_ADELANTE             = VIAJE_COLOR_FRECUENCIA_ADELANTE
        self.VIAJE_ID_ADELANTE                           = VIAJE_ID_ADELANTE
        self.VIAJE_FREC_ATRAS                            = VIAJE_FREC_ATRAS
        self.VIAJE_FREC_ATRAS_PROGRAMADA                 = VIAJE_FREC_ATRAS_PROGRAMADA
        self.VIAJE_AUTOBUS_ATRAS                         = VIAJE_AUTOBUS_ATRAS
        self.VIAJE_COLOR_FRECUENCIA_ATRAS                = VIAJE_COLOR_FRECUENCIA_ATRAS
        self.VIAJE_ID_ATRAS                              = VIAJE_ID_ATRAS
        self.FREC_TOLERANCIA_AMARILLO                    = FREC_TOLERANCIA_AMARILLO
        self.FREC_TOLERANCIA_ROJO                        = FREC_TOLERANCIA_ROJO
        self.PARADA_ID_ULTIMA                            = PARADA_ID_ULTIMA
        self.COLISION_PARADA_ULTIMA_HORA                 = COLISION_PARADA_ULTIMA_HORA
        self.DISTANCIA_PARADA_ULTIMA                     = DISTANCIA_PARADA_ULTIMA
        self.FECHA_ACTUALIZACION                         = FECHA_ACTUALIZACION
        self.LAT                                         = LAT
        self.LON                                         = LON
        self.VEL                                         = VEL
        self.DISTANCIA_RECORRIDA_TOTAL                   = DISTANCIA_RECORRIDA_TOTAL
        self.TRECHO_ACTUAL_ID                            = TRECHO_ACTUAL_ID
        self.TRECHO_TRAZADO_ACTUAL_ID                    = TRECHO_TRAZADO_ACTUAL_ID
        self.TRECHO_TRAZADO_DISTANCIA_RECORRIDA_PARCIAL  = TRECHO_TRAZADO_DISTANCIA_RECORRIDA_PARCIAL
        self.RUTA_ID                                     = RUTA_ID  
        self.VIAJE_ID                                    = VIAJE_ID
        self.VIAJE_STATUS_ID                             = VIAJE_STATUS_ID
        self.VIAJE_ULTIMA_POSICION_ID                    = VIAJE_ULTIMA_POSICION_ID
        self.VIAJE_SALIDA_REAL                           = VIAJE_SALIDA_REAL
        self.VIAJE_PUNTUALIDAD                           = VIAJE_PUNTUALIDAD
        self.VIAJE_COLOR_PUNTUALIDAD                     = VIAJE_COLOR_PUNTUALIDAD
        self.VIAJE_PUNTUALIDAD_TOLERANCIA_AMARILLO       = VIAJE_PUNTUALIDAD_TOLERANCIA_AMARILLO
        self.VIAJE_PUNTUALIDAD_TOLERANCIA_ROJO           = VIAJE_PUNTUALIDAD_TOLERANCIA_ROJO
        self.VIAJE_FREC_ADELANTE                         = VIAJE_FREC_ADELANTE
        self.VIAJE_FREC_ADELANTE_PROGRAMADA              = VIAJE_FREC_ADELANTE_PROGRAMADA
        self.MENSAJE                                     = MENSAJE
        self.ENVIADO                                     = ENVIADO

class Parada_Poligono(Base, Tabla):
    __tablename__ = 'PARADA_POLIGONO'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    PARADA_ID     = Column(Integer)      
    SEQUENCE      = Column(Integer)      
    ACTIVE        = Column(Integer)  
    LATITUD       = Column(Float)  
    LONGITUD      = Column(Float)      

    def __init__(self, 
        ID       : int = None,
        PARADA_ID: int = None,
        SEQUENCE : int = None,
        ACTIVE   : int = None,
        LATITUD  : float = None,
        LONGITUD : float = None
    ):
        self.ID        = ID       
        self.PARADA_ID = PARADA_ID
        self.SEQUENCE  = SEQUENCE 
        self.ACTIVE    = ACTIVE   
        self.LATITUD   = LATITUD  
        self.LONGITUD  = LONGITUD 
    
class Parada_Tipo(Base, Tabla):
    __tablename__ = 'PARADA_TIPO'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    DESCRIPTION   = Column(NCHAR(50))     
    ACTIVE        = Column(Integer)

    def __init__(self, 
        ID         : int = None,
        DESCRIPTION: str = None,
        ACTIVE     : int = None
    ):
        self.ID          = ID         ,
        self.DESCRIPTION = DESCRIPTION,
        self.ACTIVE      = ACTIVE
    
class Ruta(Base, Tabla):
    __tablename__ = 'RUTA'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    NAME          = Column(NCHAR(50))
    ACTIVE        = Column(Integer)
    COLOR_ID      = Column(Integer)    
    PARADA_INI    = Column(Integer)    
    PARADA_FIN    = Column(Integer)    
    DISTANCIA     = Column(Float)    
    TIEMPO        = Column(Integer)
    ENTRENADO     = Column(Integer)

    def __init__(self, 
        ID        : int = None,
        NAME      : str = None,
        ACTIVE    : int = None,
        COLOR_ID  : int = None,
        PARADA_INI: int = None,
        PARADA_FIN: int = None,
        DISTANCIA : float = None,
        TIEMPO    : int = None,
        ENTRENADO : int = None
    ):
        self.ID         = ID        
        self.NAME       = NAME      
        self.ACTIVE     = ACTIVE    
        self.COLOR_ID   = COLOR_ID  
        self.PARADA_INI = PARADA_INI
        self.PARADA_FIN = PARADA_FIN
        self.DISTANCIA  = DISTANCIA 
        self.TIEMPO     = TIEMPO
        self.ENTRENADO  = ENTRENADO

class Ruta_Parada(Base, Tabla):
    __tablename__ = 'RUTA_PARADA'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    RUTA_ID       = Column(Integer)
    PARADA_ID     = Column(Integer)    
    SEQUENCE      = Column(Integer)
    ESTANCIA      = Column(Integer)

    def __init__(self, 
        ID       : int = None,
        RUTA_ID  : int = None,
        PARADA_ID: int = None,
        SEQUENCE : int = None,
        ESTANCIA : int = None
    ):
        self.ID        = ID       
        self.RUTA_ID   = RUTA_ID  
        self.PARADA_ID = PARADA_ID
        self.SEQUENCE  = SEQUENCE
        self.ESTANCIA  = ESTANCIA

class Ruta_Trecho(Base, Tabla):
    __tablename__ = 'RUTA_TRECHO'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    RUTA_ID       = Column(Integer)
    TRECHO_ID     = Column(Integer)    
    SEQUENCE      = Column(Integer)    
    
    def __init__(self, 
        ID       : int = None,
        RUTA_ID  : int = None,
        TRECHO_ID: int = None,
        SEQUENCE : int = None
    ):
        self.ID        = ID       
        self.RUTA_ID   = RUTA_ID  
        self.TRECHO_ID = TRECHO_ID
        self.SEQUENCE  = SEQUENCE

class Trazado(Base, Tabla):
    __tablename__     = 'TRAZADO'
    ID                = Column(Integer, primary_key = True)   #Identity by default
    TRECHO_TRAZADO_ID = Column(Integer) 
    SEQUENCE          = Column(Integer)
    LATITUD           = Column(Integer)
    LONGITUD          = Column(Integer)
    DISTANCIA_ACUMULADA = Column(Float)
    TIEMPO_ACUMULADO  = Column(Integer)

    def __init__(self, 
        ID               : int = None,
        TRECHO_TRAZADO_ID: int = None,
        SEQUENCE         : int = None,
        LATITUD          : int = None,
        LONGITUD         : int = None,
        DISTANCIA_ACUMULADA: float = None,
        TIEMPO_ACUMULADO : int = None
    ):
        self.ID                = ID               ,
        self.TRECHO_TRAZADO_ID = TRECHO_TRAZADO_ID,
        self.SEQUENCE          = SEQUENCE         ,
        self.LATITUD           = LATITUD          ,
        self.LONGITUD          = LONGITUD         ,
        self.DISTANCIA_ACUMULADA = DISTANCIA_ACUMULADA,
        self.TIEMPO_ACUMULADO  = TIEMPO_ACUMULADO

class Trecho(Base, Tabla):
    __tablename__  = 'TRECHO'
    ID             = Column(Integer, primary_key = True)   #Identity by default
    NAME           = Column(NCHAR(50))
    ACTIVE         = Column(Integer)
    COLOR_ID       = Column(Integer)    
    PARADA_INI     = Column(Integer)    
    PARADA_FIN     = Column(Integer)    
    TRECHO_TIPO_ID = Column(Integer)
    ENTRENADO      = Column(Integer)

    def __init__(self, 
        ID            : int = None,
        NAME          : int = None,
        ACTIVE        : int = None,
        COLOR_ID      : int = None,
        PARADA_INI    : int = None,
        PARADA_FIN    : int = None,
        TRECHO_TIPO_ID: int = None,
        ENTRENADO     : int = None
    ):
        self.ID             = ID            
        self.NAME           = NAME          
        self.ACTIVE         = ACTIVE        
        self.COLOR_ID       = COLOR_ID      
        self.PARADA_INI     = PARADA_INI    
        self.PARADA_FIN     = PARADA_FIN    
        self.TRECHO_TIPO_ID = TRECHO_TIPO_ID
        self.ENTRENADO      = ENTRENADO

class Trecho_Tiempo_Estad(Base, Tabla):
    __tablename__     = 'TRECHO_TIEMPO_ESTAD'
    ID                = Column(Integer, primary_key = True)   #Identity by default
    TRECHO_ID         = Column(Integer)       
    TIEMPO            = Column(Integer)    
    HORA              = Column(Integer)  
    DIA               = Column(Integer) 
    MES               = Column(Integer) 
    AÑO               = Column(Integer) 
    TIPO_DIA          = Column(Integer)      
    TIPO_CLIMA        = Column(Integer)        
    TRECHO_TRAZADO_ID = Column(Integer)               

    def __init__(self, 
        ID               : int = None,
        TRECHO_ID        : int = None,
        TIEMPO           : int = None,
        HORA             : int = None,
        DIA              : int = None,
        MES              : int = None,
        AÑO              : int = None,
        TIPO_DIA         : int = None,
        TIPO_CLIMA       : int = None,
        TRECHO_TRAZADO_ID: int = None
    ):
        self.ID                = ID               
        self.TRECHO_ID         = TRECHO_ID        
        self.TIEMPO            = TIEMPO           
        self.HORA              = HORA             
        self.DIA               = DIA              
        self.MES               = MES              
        self.AÑO               = AÑO              
        self.TIPO_DIA          = TIPO_DIA         
        self.TIPO_CLIMA        = TIPO_CLIMA       
        self.TRECHO_TRAZADO_ID = TRECHO_TRAZADO_ID

class Trecho_Tipo(Base, Tabla):
    __tablename__ = 'TRECHO_TIPO'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    DESCRIPTION   = Column(NCHAR(50))
    ACTIVE        = Column(Integer) 

    def __init__(self, 
        ID         : int = None,
        DESCRIPTION: str = None,
        ACTIVE     : int = None
    ):
        self.ID          = ID          
        self.DESCRIPTION = DESCRIPTION 
        self.ACTIVE      = ACTIVE      
    
    class Trecho_Tipo_enum(Enum):
        INDIVIDUAL = 1
        COMPARTIDO = 2

class Trecho_Trazado(Base, Tabla):
    __tablename__ = 'TRECHO_TRAZADO'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    NAME          = Column(NCHAR(50))
    TRECHO_ID     = Column(Integer)     
    PRIORIDAD     = Column(Integer)     
    DISTANCIA     = Column(Integer)     
    TIEMPO        = Column(Integer)
    ACTIVE        = Column(Integer)

    def __init__(self, 
        ID       : int = None,
        NAME     : str = None,
        TRECHO_ID: int = None,
        PRIORIDAD: int = None,
        DISTANCIA: int = None,
        TIEMPO   : int = None,
        ACTIVE   : int = None
    ):
        self.ID        = ID       
        self.NAME      = NAME     
        self.TRECHO_ID = TRECHO_ID
        self.PRIORIDAD = PRIORIDAD
        self.DISTANCIA = DISTANCIA
        self.TIEMPO    = TIEMPO
        self.ACTIVE    = ACTIVE

class Viaje(Base, Tabla):
    __tablename__                 = 'VIAJE'
    ID                            = Column(Integer, primary_key = True)   #Identity by default
    RUTA_ID                       = Column(Integer)
    AUTOBUS_ID                    = Column(Integer)  
    CONDUCTOR_ID                  = Column(Integer)    
    FECHA_HORA_PROGRAMADA_SALIDA  = Column(DateTime, default=datetime.datetime.utcnow)                    
    FECHA_HORA_REAL_SALIDA        = Column(DateTime, default=datetime.datetime.utcnow)              
    FECHA_HORA_PROGRAMADA_LLEGADA = Column(DateTime, default=datetime.datetime.utcnow)                     
    FECHA_HORA_REAL_LLEGADA       = Column(DateTime, default=datetime.datetime.utcnow)               
    ZONA_HORARIA_ID               = Column(Integer)       
    VIAJE_STATUS_ID               = Column(Integer)       
    FECHA_ACTUALIZACION           = Column(DateTime, default=datetime.datetime.utcnow)           
    ERPCO_CORRIDA_ID              = Column(Integer)        
    ULTIMO_VIAJE_POSICION_ID      = Column(Integer)                

    def __init__(self, 
        ID                           : int = None,
        RUTA_ID                      : int = None,
        AUTOBUS_ID                   : int = None,
        CONDUCTOR_ID                 : int = None,
        FECHA_HORA_PROGRAMADA_SALIDA : datetime.datetime = None,
        FECHA_HORA_REAL_SALIDA       : datetime.datetime = None,
        FECHA_HORA_PROGRAMADA_LLEGADA: datetime.datetime = None,
        FECHA_HORA_REAL_LLEGADA      : datetime.datetime = None,
        ZONA_HORARIA_ID              : int = None,
        VIAJE_STATUS_ID              : int = None,
        FECHA_ACTUALIZACION          : datetime.datetime = None,
        ERPCO_CORRIDA_ID             : int = None,
        ULTIMO_VIAJE_POSICION_ID     : int = None
    ):
        self.ID                            = ID                           
        self.RUTA_ID                       = RUTA_ID                      
        self.AUTOBUS_ID                    = AUTOBUS_ID                   
        self.CONDUCTOR_ID                  = CONDUCTOR_ID                 
        self.FECHA_HORA_PROGRAMADA_SALIDA  = FECHA_HORA_PROGRAMADA_SALIDA 
        self.FECHA_HORA_REAL_SALIDA        = FECHA_HORA_REAL_SALIDA       
        self.FECHA_HORA_PROGRAMADA_LLEGADA = FECHA_HORA_PROGRAMADA_LLEGADA
        self.FECHA_HORA_REAL_LLEGADA       = FECHA_HORA_REAL_LLEGADA      
        self.ZONA_HORARIA_ID               = ZONA_HORARIA_ID              
        self.VIAJE_STATUS_ID               = VIAJE_STATUS_ID              
        self.FECHA_ACTUALIZACION           = FECHA_ACTUALIZACION          
        self.ERPCO_CORRIDA_ID              = ERPCO_CORRIDA_ID             
        self.ULTIMO_VIAJE_POSICION_ID      = ULTIMO_VIAJE_POSICION_ID     
    
class Viaje_Parada(Base, Tabla):
    __tablename__                 = 'VIAJE_PARADA'
    ID                            = Column(Integer, primary_key = True)   #Identity by default
    VIAJE_ID                      = Column(Integer)
    PARADA_ID                     = Column(Integer) 
    FECHA_HORA_PROGRAMADA_LLEGADA = Column(DateTime, default=datetime.datetime.utcnow)                     
    FECHA_HORA_REAL_LLEGADA       = Column(DateTime, default=datetime.datetime.utcnow)               
    FECHA_HORA_PROGRAMADA_SALIDA  = Column(DateTime, default=datetime.datetime.utcnow)                    
    FECHA_HORA_REAL_SALIDA        = Column(DateTime, default=datetime.datetime.utcnow)              
    ZONA_HORARIA_ID               = Column(Integer)       

    def __init__(self, 
        ID                           : int = None,
        VIAJE_ID                     : int = None,
        PARADA_ID                    : int = None,
        FECHA_HORA_PROGRAMADA_LLEGADA: datetime.datetime = None,
        FECHA_HORA_REAL_LLEGADA      : datetime.datetime = None,
        FECHA_HORA_PROGRAMADA_SALIDA : datetime.datetime = None,
        FECHA_HORA_REAL_SALIDA       : datetime.datetime = None,
        ZONA_HORARIA_ID              : int = None
    ):
        self.ID                            = ID                           
        self.VIAJE_ID                      = VIAJE_ID                     
        self.PARADA_ID                     = PARADA_ID                    
        self.FECHA_HORA_PROGRAMADA_LLEGADA = FECHA_HORA_PROGRAMADA_LLEGADA
        self.FECHA_HORA_REAL_LLEGADA       = FECHA_HORA_REAL_LLEGADA      
        self.FECHA_HORA_PROGRAMADA_SALIDA  = FECHA_HORA_PROGRAMADA_SALIDA 
        self.FECHA_HORA_REAL_SALIDA        = FECHA_HORA_REAL_SALIDA       
        self.ZONA_HORARIA_ID               = ZONA_HORARIA_ID              

class Viaje_Posicion(Base, Tabla):
    __tablename__                        = 'VIAJE_POSICION'
    ID                                   = Column(Integer, primary_key = True)   #Identity by default
    VIAJE_ID                             = Column(Integer)    
    SEQUENCE                             = Column(Integer)    
    FECHA_HORA_PROCESAMIENTO             = Column(DateTime, default=datetime.datetime.utcnow)                    
    FECHA_HORA_GPS                       = Column(DateTime, default=datetime.datetime.utcnow)          
    VELOCIDAD                            = Column(Integer)     
    DISTANCIA                            = Column(Float)     
    PORCENTAJE_AVANCE_RUTA               = Column(Float)                  
    PORCENTAJE_AVANCE_TRECHO             = Column(Float)                    
    LATITUD                              = Column(Integer)   
    LONGITUD                             = Column(Integer)    
    TRECHO_ANTERIOR_ID                   = Column(Integer)              
    TRECHO_ACTUAL_ID                     = Column(Integer)            
    TRECHO_SIGUIENTE_ID                  = Column(Integer)               
    PARADA_ANTERIOR_ID                   = Column(Integer)              
    PARADA_SIGUIENTE_ID                  = Column(Integer)               
    FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA = Column(DateTime, default=datetime.datetime.utcnow)                                
    ULTIMO_EVENTO_ID                     = Column(Integer)            
    PUNTUALIDAD                          = Column(Integer)       
    FRECUENCIA_ATRAS                     = Column(Integer)            
    FRECUENCIA_ADELANTE                  = Column(Integer)               
    DISTANCIA_ATRAS                      = Column(Integer)           
    DISTANCIA_ADELANTE                   = Column(Integer)              
    VIAJE_ATRAS_ID                       = Column(Integer)          
    VIAJE_ADELANTE_ID                    = Column(Integer)             
    CLIMA_TIPO_ID                        = Column(Integer)         
    COLOR_PUNTUALIDAD                    = Column(NCHAR(1))
    COLOR_FRECUENCIA_ADELANTE            = Column(NCHAR(1))
    COLOR_FRECUENCIA_ATRAS               = Column(NCHAR(1))
    COLOR_STATUS                         = Column(NCHAR(10))
    VIAJE_STATUS_RECORRIDO_ID            = Column(Integer)

    def __init__(self, 
        ID                                  : int = None,
        VIAJE_ID                            : int = None,
        SEQUENCE                            : int = None,
        FECHA_HORA_PROCESAMIENTO            : datetime.datetime = None,
        FECHA_HORA_GPS                      : datetime.datetime = None,
        VELOCIDAD                           : int = None,
        DISTANCIA                           : float = None,
        PORCENTAJE_AVANCE_RUTA              : float = None,
        PORCENTAJE_AVANCE_TRECHO            : float = None,
        LATITUD                             : int = None,
        LONGITUD                            : int = None,
        TRECHO_ANTERIOR_ID                  : int = None,
        TRECHO_ACTUAL_ID                    : int = None,
        TRECHO_SIGUIENTE_ID                 : int = None,
        PARADA_ANTERIOR_ID                  : int = None,
        PARADA_SIGUIENTE_ID                 : int = None,
        FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA: datetime.datetime = None,
        ULTIMO_EVENTO_ID                    : int = None,
        PUNTUALIDAD                         : int = None,
        FRECUENCIA_ATRAS                    : int = None,
        FRECUENCIA_ADELANTE                 : int = None,
        DISTANCIA_ATRAS                     : int = None,
        DISTANCIA_ADELANTE                  : int = None,
        VIAJE_ATRAS_ID                      : int = None,
        VIAJE_ADELANTE_ID                   : int = None,
        CLIMA_TIPO_ID                       : int = None,
        COLOR_PUNTUALIDAD                   : str = None,
        COLOR_FRECUENCIA_ADELANTE           : str = None,
        COLOR_FRECUENCIA_ATRAS              : str = None,
        COLOR_STATUS                        : str = None,
        VIAJE_STATUS_RECORRIDO_ID           : int = None,
    ):
        self.ID                                   = ID                                  
        self.VIAJE_ID                             = VIAJE_ID                            
        self.SEQUENCE                             = SEQUENCE                            
        self.FECHA_HORA_PROCESAMIENTO             = FECHA_HORA_PROCESAMIENTO            
        self.FECHA_HORA_GPS                       = FECHA_HORA_GPS                      
        self.VELOCIDAD                            = VELOCIDAD                           
        self.DISTANCIA                            = DISTANCIA                           
        self.PORCENTAJE_AVANCE_RUTA               = PORCENTAJE_AVANCE_RUTA              
        self.PORCENTAJE_AVANCE_TRECHO             = PORCENTAJE_AVANCE_TRECHO            
        self.LATITUD                              = LATITUD                             
        self.LONGITUD                             = LONGITUD                            
        self.TRECHO_ANTERIOR_ID                   = TRECHO_ANTERIOR_ID                  
        self.TRECHO_ACTUAL_ID                     = TRECHO_ACTUAL_ID                    
        self.TRECHO_SIGUIENTE_ID                  = TRECHO_SIGUIENTE_ID                 
        self.PARADA_ANTERIOR_ID                   = PARADA_ANTERIOR_ID                  
        self.PARADA_SIGUIENTE_ID                  = PARADA_SIGUIENTE_ID                 
        self.FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA = FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA
        self.ULTIMO_EVENTO_ID                     = ULTIMO_EVENTO_ID                    
        self.PUNTUALIDAD                          = PUNTUALIDAD                         
        self.FRECUENCIA_ATRAS                     = FRECUENCIA_ATRAS                    
        self.FRECUENCIA_ADELANTE                  = FRECUENCIA_ADELANTE                 
        self.DISTANCIA_ATRAS                      = DISTANCIA_ATRAS                     
        self.DISTANCIA_ADELANTE                   = DISTANCIA_ADELANTE                  
        self.VIAJE_ATRAS_ID                       = VIAJE_ATRAS_ID                      
        self.VIAJE_ADELANTE_ID                    = VIAJE_ADELANTE_ID                   
        self.CLIMA_TIPO_ID                        = CLIMA_TIPO_ID                       
        self.COLOR_PUNTUALIDAD                    = COLOR_PUNTUALIDAD        
        self.COLOR_FRECUENCIA_ADELANTE            = COLOR_FRECUENCIA_ADELANTE
        self.COLOR_FRECUENCIA_ATRAS               = COLOR_FRECUENCIA_ATRAS   
        self.COLOR_STATUS                         = COLOR_STATUS             
        self.VIAJE_STATUS_RECORRIDO_ID            = VIAJE_STATUS_RECORRIDO_ID


class Viaje_Status(Base, Tabla):
    __tablename__ = 'VIAJE_STATUS'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    NAME          = Column(NCHAR(50))
    ACTIVE        = Column(Integer)

    def __init__(self, 
        ID    : int = None,
        NAME  : str = None,
        ACTIVE: int = None
    ):
        self.ID     = ID     
        self.NAME   = NAME  
        self.ACTIVE = ACTIVE             

    class enum(Enum):
        PROGRAMADO = 1
        EN_VIAJE   = 2
        TERMINADO  = 3
        CANCELADO  = 4
        CANCELADO_DATOS = 5
        DESENROLAMIENTO = 6

class Viaje_Status_Recorrido(Base, Tabla):
    __tablename__ = 'VIAJE_STATUS_RECORRIDO'
    ID            = Column(Integer, primary_key = True) #Identity by default
    NAME          = Column(NCHAR(50))
    CLAVE         = Column(NCHAR(10))
    ACTIVE        = Column(Integer)

    def __init__(self,
        ID    : int = None,
        NAME  : str = None,
        CLAVE : str = None,
        ACTIVE: int = None
    ):
        self.ID     = ID    
        self.NAME   = NAME  
        self.CLAVE  = CLAVE 
        self.ACTIVE = ACTIVE

    # no cambiar el orden, el nombre original es la clave y el alias el nombre completo
    class enum(Enum):
         OK = 1
         SC = 2
         FR = 3
         OR = 4
         CONECTADO     = 1 
         SIN_CONEXION  = 2
         FUERA_DE_RUTA = 3
         OTRO          = 4


class Viaje_Trecho(Base, Tabla):
    __tablename__                 = 'VIAJE_TRECHO'
    ID                            = Column(Integer, primary_key = True)   #Identity by default
    VIAJE_ID                      = Column(Integer)
    TRECHO_ID                     = Column(Integer) 
    TRECHO_TRAZADO_ID             = Column(Integer)         
    FECHA_HORA_PROGRAMADA_LLEGADA = Column(DateTime, default=datetime.datetime.utcnow)                      
    FECHA_HORA_REAL_LLEGADA       = Column(DateTime, default=datetime.datetime.utcnow)               
    FECHA_HORA_PROGRAMADA_SALIDA  = Column(DateTime, default=datetime.datetime.utcnow)                    
    FECHA_HORA_REAL_SALIDA        = Column(DateTime, default=datetime.datetime.utcnow)              

    def __init__(self, 
        ID                           : int = None,
        VIAJE_ID                     : int = None,
        TRECHO_ID                    : int = None,
        TRECHO_TRAZADO_ID            : int = None,
        FECHA_HORA_PROGRAMADA_LLEGADA: datetime.datetime = None,
        FECHA_HORA_REAL_LLEGADA      : datetime.datetime = None,
        FECHA_HORA_PROGRAMADA_SALIDA : datetime.datetime = None,
        FECHA_HORA_REAL_SALIDA       : datetime.datetime = None
    ):
        self.ID                            = ID                           
        self.VIAJE_ID                      = VIAJE_ID                     
        self.TRECHO_ID                     = TRECHO_ID                    
        self.TRECHO_TRAZADO_ID             = TRECHO_TRAZADO_ID            
        self.FECHA_HORA_PROGRAMADA_LLEGADA = FECHA_HORA_PROGRAMADA_LLEGADA
        self.FECHA_HORA_REAL_LLEGADA       = FECHA_HORA_REAL_LLEGADA      
        self.FECHA_HORA_PROGRAMADA_SALIDA  = FECHA_HORA_PROGRAMADA_SALIDA 
        self.FECHA_HORA_REAL_SALIDA        = FECHA_HORA_REAL_SALIDA       

class Zona_Horaria(Base, Tabla):
    __tablename__ = 'ZONA_HORARIA'
    ID            = Column(Integer, primary_key = True)   #Identity by default
    NAME          = Column(NCHAR(50))
    HORA          = Column(Integer)
    ACTIVE        = Column(Integer)  

    def __init__(self, 
        ID    : int = None,
        NAME  : str = None,
        HORA  : int = None,
        ACTIVE: int = None
    ):
        self.ID     = ID    
        self.NAME   = NAME  
        self.HORA   = HORA  
        self.ACTIVE = ACTIVE

class Hst_Geotab_Logrecord(Base,Tabla):
    __tablename__ = 'HST_GEOTAB_LOGRECORD'
    PK_ID                 = Column(Integer, primary_key = True)   #dummy primary key
    AUTOBUS               = Column(VARCHAR(20))  
    LATITUD               = Column(Float)  
    LONGITUD              = Column(Float)   
    FECHA_ACTUALIZACION   = Column(DateTime, default =  datetime.datetime.utcnow)              
    FECHA_REGISTRO_GEOTAB = Column(DateTime)                
    VERSION               = Column(BIGINT)  
    DISTANCIA             = Column(Float)    
    VELOCIDAD             = Column(Float)    
    FECHA_REPLICA         = Column(DateTime)        

    def __init__(self, 
        PK_ID                 : int = None,
        AUTOBUS               : str = None,
        LATITUD               : float = None,
        LONGITUD              : float = None,
        FECHA_ACTUALIZACION   : datetime.datetime = None,
        FECHA_REGISTRO_GEOTAB : datetime.datetime = None,
        VERSION               : int = None,
        DISTANCIA             : float = None,
        VELOCIDAD             : float = None,
        FECHA_REPLICA         : datetime.datetime = None
    ):
        self.PK_ID                 = PK_ID                
        self.AUTOBUS               = AUTOBUS              
        self.LATITUD               = LATITUD              
        self.LONGITUD              = LONGITUD             
        self.FECHA_ACTUALIZACION   = FECHA_ACTUALIZACION  
        self.FECHA_REGISTRO_GEOTAB = FECHA_REGISTRO_GEOTAB
        self.VERSION               = VERSION              
        self.DISTANCIA             = DISTANCIA            
        self.VELOCIDAD             = VELOCIDAD            
        self.FECHA_REPLICA         = FECHA_REPLICA

class Colision(Base,Tabla):
    __tablename__         = 'COLISION'
    PK_ID                 = Column(Integer, primary_key = True)   #dummy primary key
    AUTOBUS               = Column(VARCHAR(20))  
    PARADA_ID             = Column(Integer)
    FECHA_INICIO          = Column(DateTime)
    FECHA_FIN             = Column(DateTime)
    VELOCIDAD_PROMEDIO    = Column(Float)
    DISTANCIA             = Column(Float)
    DURACION              = Column(Integer)
    VELOCIDAD_MAX         = Column(Integer)
    NUMERO_LOCALIZACIONES = Column(Integer)
    VIAJE_ID              = Column(Integer)
    COLISION_ACTIVA       = Column(BIT)

    def __init__(self,
        PK_ID                 : int = None,
        AUTOBUS               : str = None,
        PARADA_ID             : int = None,
        FECHA_INICIO          : datetime.datetime = None,
        FECHA_FIN             : datetime.datetime = None,
        VELOCIDAD_PROMEDIO    : float = None,
        DISTANCIA             : float = None,
        DURACION              : int = None,
        VELOCIDAD_MAX         : int = None,
        NUMERO_LOCALIZACIONES : int = None,
        VIAJE_ID              : int = None,
        COLISION_ACTIVA       : int = None
    ):
        self.PK_ID                 = PK_ID                
        self.AUTOBUS               = AUTOBUS              
        self.PARADA_ID             = PARADA_ID            
        self.FECHA_INICIO          = FECHA_INICIO         
        self.FECHA_FIN             = FECHA_FIN            
        self.VELOCIDAD_PROMEDIO    = VELOCIDAD_PROMEDIO   
        self.DISTANCIA             = DISTANCIA            
        self.DURACION              = DURACION             
        self.VELOCIDAD_MAX         = VELOCIDAD_MAX        
        self.NUMERO_LOCALIZACIONES = NUMERO_LOCALIZACIONES
        self.VIAJE_ID              = VIAJE_ID
        self.COLISION_ACTIVA       = COLISION_ACTIVA

class Sae_Rec_Mensajes_Txt(Base,Tabla):
    __tablename__ = 'SAE_REC_MENSAJES_TXT'
    MSJ           = Column(NVARCHAR(120))
    SENDER        = Column(NVARCHAR(120))
    AUTOBUS       = Column(NVARCHAR(5))
    ENVIADO       = Column(DateTime)
    ENTREGADO     = Column(DateTime)
    ESTADO        = Column(TINYINT)
    TO_AUTOBUS    = Column(BIT)
    ID_SUPLY      = Column(BIGINT, primary_key = True, autoincrement = False)

    def __init__(self,
        ID_SUPLY   : int,
        MSJ        : str,
        SENDER     : str,
        AUTOBUS    : str,
        ENVIADO    : datetime.datetime,
        ENTREGADO  : datetime.datetime,
        ESTADO     : int = None,
        TO_AUTOBUS : int = None
    ):
        self.MSJ        = MSJ       
        self.SENDER     = SENDER    
        self.AUTOBUS    = AUTOBUS   
        self.ENVIADO    = ENVIADO   
        self.ENTREGADO  = ENTREGADO 
        self.ESTADO     = ESTADO    
        self.TO_AUTOBUS = TO_AUTOBUS
        self.ID_SUPLY   = ID_SUPLY  

class Sae_Parametro(Base,Tabla):
    __tablename__ = 'SAE_PARAMETRO'
    LLAVE         = Column(NCHAR(128), primary_key = True, autoincrement = False)
    VALOR         = Column(NCHAR(1024))
    ACTIVE        = Column(Integer)

    def __init__(self,
        LLAVE : str, 
        VALOR : str,
        ACTIVE: int = None

    ):
        self.LLAVE  = LLAVE 
        self.VALOR  = VALOR 
        self.ACTIVE = ACTIVE

class Sae_Parametro_Autorregulacion(Base, Tabla):
    __tablename__ = 'SAE_PARAMETRO_AUTORREGULACION'
    PK_ID                           = Column(Integer, primary_key = True)
    NOMBRE                          = Column(VARCHAR(50))
    HORA_INICIO                     = Column(Time(7))
    HORA_FIN                        = Column(Time(7))
    TOLERANCIA_PUNTUALIDAD          = Column(Integer)
    FRECUENCIA                      = Column(Integer)
    TOLERANCIA_FRECUENCIA           = Column(Integer)
    TOLERANCIA_SALIDA_TERMINAL      = Column(Integer)
    STATUS                          = Column(Integer)
    TOLERANCIA_PUNTUALIDAD_AMARILLO = Column(Integer)
    TOLERANCIA_FRECUENCIA_AMARILLO  = Column(Integer)
    VIGENCIA_MENSAJE_MINUTOS        = Column(Integer)

    def __init__(self,
        PK_ID                          : int = None,
        NOMBRE                         : str = None,
        HORA_INICIO                    : datetime.time = None,
        HORA_FIN                       : datetime.time = None,
        TOLERANCIA_PUNTUALIDAD         : int = None,
        FRECUENCIA                     : int = None,
        TOLERANCIA_FRECUENCIA          : int = None,
        TOLERANCIA_SALIDA_TERMINAL     : int = None,
        STATUS                         : int = None,
        TOLERANCIA_PUNTUALIDAD_AMARILLO: int = None,
        TOLERANCIA_FRECUENCIA_AMARILLO : int = None,
        VIGENCIA_MENSAJE_MINUTOS       : int = None
    ):
        self.PK_ID                           = PK_ID                          
        self.NOMBRE                          = NOMBRE                         
        self.HORA_INICIO                     = HORA_INICIO                    
        self.HORA_FIN                        = HORA_FIN                       
        self.TOLERANCIA_PUNTUALIDAD          = TOLERANCIA_PUNTUALIDAD         
        self.FRECUENCIA                      = FRECUENCIA                     
        self.TOLERANCIA_FRECUENCIA           = TOLERANCIA_FRECUENCIA          
        self.TOLERANCIA_SALIDA_TERMINAL      = TOLERANCIA_SALIDA_TERMINAL     
        self.STATUS                          = STATUS                         
        self.TOLERANCIA_PUNTUALIDAD_AMARILLO = TOLERANCIA_PUNTUALIDAD_AMARILLO
        self.TOLERANCIA_FRECUENCIA_AMARILLO  = TOLERANCIA_FRECUENCIA_AMARILLO 
        self.VIGENCIA_MENSAJE_MINUTOS        = VIGENCIA_MENSAJE_MINUTOS       

class Hst_Monitoreo_Mensajes(Base, Tabla):
    __tablename__ = 'HST_MONITOREO_MENSAJES'
    PK_ID  = Column(BIGINT, primary_key=True)  # dummy primary key, not identity
    GEOTAB_ID  = Column(Integer)
    FECHA_ENVIO  = Column(DateTime)
    AUTOBUS  = Column(VARCHAR(50))
    FECHA_ENTREGA  = Column(DateTime)
    TEXTO_MENSAJE  = Column(VARCHAR(500))
    ESTATUS  = Column(Integer)
    SERVIDOR_A_VEHICULO  = Column(Integer)
    FECHA_ENVIO_MENSAJE  = Column(DateTime)
    CLAVE_CONDUCTOR  = Column(VARCHAR(10))
    CLAVE_POBLACION_ORIGEN  = Column(VARCHAR(5))
    CLAVE_POBLACION_DESTINO  = Column(VARCHAR(5))
    CLAVE_POBLACION_VIA  = Column(VARCHAR(50))
    CLAVE_POBLACION_ACTUAL  = Column(VARCHAR(50))
    LATITUD_ACTUAL  = Column(VARCHAR(10))
    LONGITUD_ACTUAL  = Column(VARCHAR(10))
    FECHORA_PROGRAMADA_APERTURA_VIAJE  = Column(DateTime)
    FECHORA_VIAJE  = Column(DateTime)
    PUNTUALIDAD_ACTUALIDAD_AUTOBUS  = Column(Integer)
    TOLERANCIA_PUNTUALIDAD_AMARILLO  = Column(Integer)
    TOLERANCIA_PUNTUALIDAD_ROJO  = Column(Integer)
    FRECUENCIA_TEORICA_AUTOBUS_ATRAS  = Column(Integer)
    FRECUENCIA_TEORICA_AUTOBUS_ADELANTE  = Column(Integer)
    TOLERANCIA_FRECUENCIA_AMARILLO  = Column(Integer)
    TOLERANCIA_FRECUENCIA_ROJO  = Column(Integer)
    AUTOBUS_ATRAS  = Column(VARCHAR(10))
    TIEMPO_AUTOBUS_ATRAS  = Column(Integer)
    AUTOBUS_ADELANTE  = Column(VARCHAR(10))
    TIEMPO_AUTOBUS_ADELANTE  = Column(Integer)
    FECHA_HORA_DE_SALIDA_PROGRAMADA  = Column(DateTime)
    CLAVE_POBLACION_ULTIMA_GEOCERCA_CRUZADA = Column(VARCHAR(10))
    FECHA_HORA_DE_ULTIMA_GEOCERCA_CRUZADA  = Column(DateTime)
    VIGENCIA_DEL_MENSAJE_EN_MINUTOS  = Column(Integer)
    ID_MENSAJE  = Column(BIGINT)
    PRIORIDAD  = Column(Integer)
    REQUIERE_RESPUESTA  = Column(Integer)
    TIPO_RESPUESTA  = Column(Integer)
    TIEMPO_VIGENCIA_MENSAJE_MIN  = Column(Integer)
    MENSAJE_ABIERTO = Column(VARCHAR(20))
    TIPO_MENSAJE  = Column(BIGINT) 
    ID_MENSAJE_RESPUESTA  = Column(Integer)
    TOTAL_COLUMNAS = Column(Integer)

    def __init__(self,
            PK_ID                   : int = None,
            GEOTAB_ID               : int = None,
            FECHA_ENVIO             : datetime.datetime = None,
            AUTOBUS                 : str = None,
            FECHA_ENTREGA           : datetime.datetime = None,
            TEXTO_MENSAJE           : str = None,
            ESTATUS                 : int = None,
            SERVIDOR_A_VEHICULO     : int = None,
            FECHA_ENVIO_MENSAJE     : datetime.datetime = None,
            CLAVE_CONDUCTOR         : str = None,
            CLAVE_POBLACION_ORIGEN  : str = None,
            CLAVE_POBLACION_DESTINO : str = None,
            CLAVE_POBLACION_VIA     : str = None,
            CLAVE_POBLACION_ACTUAL  : str = None,
            LATITUD_ACTUAL          : str = None,
            LONGITUD_ACTUAL         : str = None,
            FECHORA_PROGRAMADA_APERTURA_VIAJE   : datetime.datetime = None,
            FECHORA_VIAJE           : datetime.datetime = None,
            PUNTUALIDAD_ACTUALIDAD_AUTOBUS  : int = None,
            TOLERANCIA_PUNTUALIDAD_AMARILLO : int = None,
            TOLERANCIA_PUNTUALIDAD_ROJO     : int = None,
            FRECUENCIA_TEORICA_AUTOBUS_ATRAS    : int = None,
            FRECUENCIA_TEORICA_AUTOBUS_ADELANTE : int = None,
            TOLERANCIA_FRECUENCIA_AMARILLO      : int = None,
            TOLERANCIA_FRECUENCIA_ROJO          : int = None,
            AUTOBUS_ATRAS                       : str = None,
            TIEMPO_AUTOBUS_ATRAS                : int = None,
            AUTOBUS_ADELANTE                    : str = None,
            TIEMPO_AUTOBUS_ADELANTE             : int = None,
            FECHA_HORA_DE_SALIDA_PROGRAMADA     : datetime.datetime = None,
            CLAVE_POBLACION_ULTIMA_GEOCERCA_CRUZADA : str = None,
            FECHA_HORA_DE_ULTIMA_GEOCERCA_CRUZADA   : datetime.datetime = None,
            VIGENCIA_DEL_MENSAJE_EN_MINUTOS         : int = None,
            ID_MENSAJE              : int = None,
            PRIORIDAD               : int = None,
            REQUIERE_RESPUESTA      : int = None,
            TIPO_RESPUESTA          : int = None,
            TIEMPO_VIGENCIA_MENSAJE_MIN     : int = None,
            MENSAJE_ABIERTO         : str = None,
            TIPO_MENSAJE            : str = None, 
            ID_MENSAJE_RESPUESTA    : int = None,
            TOTAL_COLUMNAS          : int = None
        ):
            self.PK_ID = PK_ID
            self.GEOTAB_ID = GEOTAB_ID
            self.FECHA_ENVIO = FECHA_ENVIO
            self.AUTOBUS = AUTOBUS
            self.FECHA_ENTREGA = FECHA_ENTREGA
            self.TEXTO_MENSAJE = TEXTO_MENSAJE
            self.ESTATUS = ESTATUS
            self.SERVIDOR_A_VEHICULO = SERVIDOR_A_VEHICULO
            self.FECHA_ENVIO_MENSAJE = FECHA_ENVIO_MENSAJE
            self.CLAVE_CONDUCTOR = CLAVE_CONDUCTOR
            self.CLAVE_POBLACION_ORIGEN = CLAVE_POBLACION_ORIGEN
            self.CLAVE_POBLACION_DESTINO = CLAVE_POBLACION_DESTINO
            self.CLAVE_POBLACION_VIA = CLAVE_POBLACION_VIA
            self.CLAVE_POBLACION_ACTUAL = CLAVE_POBLACION_ACTUAL
            self.LATITUD_ACTUAL = LATITUD_ACTUAL
            self.LONGITUD_ACTUAL = LONGITUD_ACTUAL 
            self.FECHORA_PROGRAMADA_APERTURA_VIAJE = FECHORA_PROGRAMADA_APERTURA_VIAJE
            self.FECHORA_VIAJE = FECHORA_VIAJE
            self.PUNTUALIDAD_ACTUALIDAD_AUTOBUS = PUNTUALIDAD_ACTUALIDAD_AUTOBUS
            self.TOLERANCIA_PUNTUALIDAD_AMARILLO = TOLERANCIA_PUNTUALIDAD_AMARILLO
            self.TOLERANCIA_PUNTUALIDAD_ROJO = TOLERANCIA_PUNTUALIDAD_ROJO
            self.FRECUENCIA_TEORICA_AUTOBUS_ATRAS = FRECUENCIA_TEORICA_AUTOBUS_ATRAS
            self.FRECUENCIA_TEORICA_AUTOBUS_ADELANTE = FRECUENCIA_TEORICA_AUTOBUS_ADELANTE
            self.TOLERANCIA_FRECUENCIA_AMARILLO = TOLERANCIA_FRECUENCIA_AMARILLO
            self.TOLERANCIA_FRECUENCIA_ROJO = TOLERANCIA_FRECUENCIA_ROJO
            self.AUTOBUS_ATRAS = AUTOBUS_ATRAS
            self.TIEMPO_AUTOBUS_ATRAS = TIEMPO_AUTOBUS_ATRAS
            self.AUTOBUS_ADELANTE = AUTOBUS_ADELANTE
            self.TIEMPO_AUTOBUS_ADELANTE = TIEMPO_AUTOBUS_ADELANTE
            self.FECHA_HORA_DE_SALIDA_PROGRAMADA = FECHA_HORA_DE_SALIDA_PROGRAMADA
            self.CLAVE_POBLACION_ULTIMA_GEOCERCA_CRUZADA = CLAVE_POBLACION_ULTIMA_GEOCERCA_CRUZADA
            self.FECHA_HORA_DE_ULTIMA_GEOCERCA_CRUZADA = FECHA_HORA_DE_ULTIMA_GEOCERCA_CRUZADA
            self.VIGENCIA_DEL_MENSAJE_EN_MINUTOS = VIGENCIA_DEL_MENSAJE_EN_MINUTOS
            self.ID_MENSAJE =  ID_MENSAJE
            self.PRIORIDAD = PRIORIDAD
            self.REQUIERE_RESPUESTA = REQUIERE_RESPUESTA
            self.TIPO_RESPUESTA = TIPO_RESPUESTA
            self.TIEMPO_VIGENCIA_MENSAJE_MIN = TIEMPO_VIGENCIA_MENSAJE_MIN
            self.MENSAJE_ABIERTO = MENSAJE_ABIERTO
            self.TIPO_MENSAJE = TIPO_MENSAJE
            self.ID_MENSAJE_RESPUESTA = ID_MENSAJE_RESPUESTA
            self.TOTAL_COLUMNAS = TOTAL_COLUMNAS 