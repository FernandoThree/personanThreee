from sqlalchemy import Column, Integer, VARCHAR, NCHAR, DateTime, CHAR, Float
from sqlalchemy.exc import SQLAlchemyError
import datetime
from Almacenamiento import db_session, Base
from Almacenamiento.Tablas import Tabla

class Siiab_Detalle_Gps(Base,Tabla):
    __tablename__        = 'SIIAB_DETALLE_GPS'
    PK_ID                = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    SIVA_POBLACION_ID    = Column(Integer)                
    FK_SIIAB_SERVIDOR_ID = Column(Integer)                   
    LATITUD              = Column(Integer)      
    NS                   = Column(CHAR(1)) 
    LONGITUD             = Column(Integer)       
    WE                   = Column(CHAR(1)) 
    TIPOGPS              = Column(CHAR(1))      

    def __init__(self, 
        PK_ID               : int = None,
        SIVA_POBLACION_ID   : int = None,
        FK_SIIAB_SERVIDOR_ID: int = None,
        LATITUD             : int = None,
        NS                  : str = None,
        LONGITUD            : int = None,
        WE                  : str = None,
        TIPOGPS             : str = None
    ):
        self.PK_ID                = PK_ID               
        self.SIVA_POBLACION_ID    = SIVA_POBLACION_ID   
        self.FK_SIIAB_SERVIDOR_ID = FK_SIIAB_SERVIDOR_ID
        self.LATITUD              = LATITUD             
        self.NS                   = NS                  
        self.LONGITUD             = LONGITUD            
        self.WE                   = WE                  
        self.TIPOGPS              = TIPOGPS             

class Siiab_Marca(Base,Tabla):
    __tablename__        = 'SIIAB_MARCA'
    PK_ID                = Column(VARCHAR(2), primary_key = True, autoincrement = False)   #Not Identity
    DESCRIPCION          = Column(VARCHAR(50))    
    STATUS               = Column(Integer)
    FECHA_ACTUALIZACION  = Column(DateTime, default = datetime.datetime.utcnow)            

    def __init__(self, 
        PK_ID              : str = None,
        DESCRIPCION        : str = None,
        STATUS             : int = None,
        FECHA_ACTUALIZACION: datetime.datetime = None
    ):
        self.PK_ID               = PK_ID              
        self.DESCRIPCION         = DESCRIPCION        
        self.STATUS              = STATUS             
        self.FECHA_ACTUALIZACION = FECHA_ACTUALIZACION

class Siiab_Poblacion(Base,Tabla):
    __tablename__        = 'SIIAB_POBLACION'
    PK_ID                = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    SIVA_IDPOB           = Column(Integer)     
    DESCRIPCION          = Column(VARCHAR(50))      
    CLAVE                = Column(VARCHAR(10))
    STATUS               = Column(Integer) 
    FECHA_ACTUALIZACION  = Column(DateTime, default = datetime.datetime.utcnow)              
    FK_SIIAB_SERVIDOR_ID = Column(Integer)               

    def __init__(self, 
        PK_ID               : int = None,
        SIVA_IDPOB          : int = None,
        DESCRIPCION         : str = None,
        CLAVE               : str = None,
        STATUS              : int = None,
        FECHA_ACTUALIZACION : datetime.datetime = None,
        FK_SIIAB_SERVIDOR_ID: int = None
    ):
        self.PK_ID                = PK_ID               
        self.SIVA_IDPOB           = SIVA_IDPOB          
        self.DESCRIPCION          = DESCRIPCION         
        self.CLAVE                = CLAVE               
        self.STATUS               = STATUS              
        self.FECHA_ACTUALIZACION  = FECHA_ACTUALIZACION 
        self.FK_SIIAB_SERVIDOR_ID = FK_SIIAB_SERVIDOR_ID

class Siiab_Region(Base,Tabla):
    __tablename__        = 'SIIAB_REGION'
    PK_ID                = Column(VARCHAR(2), primary_key = True, autoincrement = False)   #Not Identity
    DESCRIPCION          = Column(VARCHAR(50))
    STATUS               = Column(Integer)
    FECHA_ACTUALIZACION  = Column(DateTime, default = datetime.datetime.utcnow)
    
    def __init__(self, 
        PK_ID              : str = None,
        DESCRIPCION        : str = None,
        STATUS             : int = None,
        FECHA_ACTUALIZACION: datetime.datetime = None
    ):
        self.PK_ID               = PK_ID              
        self.DESCRIPCION         = DESCRIPCION        
        self.STATUS              = STATUS             
        self.FECHA_ACTUALIZACION = FECHA_ACTUALIZACION

class Siiab_Secuencia(Base,Tabla):
    __tablename__         = 'SIIAB_SECUENCIA'
    PK_ID                 = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    FK_SIIAB_REGION_ID    = Column(VARCHAR(2))           
    FK_SIIAB_MARCA_ID     = Column(VARCHAR(2))          
    FK_SIIAB_ZONA_ID      = Column(VARCHAR(3))         
    FK_SIIAB_SERVICIO_ID  = Column(Integer)             
    AUTOBUS               = Column(VARCHAR(10))
    VERSION               = Column(Integer)
    STATUS                = Column(Integer)

    def __init__(self,
        PK_ID               : int = None,
        FK_SIIAB_REGION_ID  : str = None,
        FK_SIIAB_MARCA_ID   : str = None,
        FK_SIIAB_ZONA_ID    : str = None,
        FK_SIIAB_SERVICIO_ID: int = None,
        AUTOBUS             : str = None,
        VERSION             : int = None,
        STATUS              : int = None
    ):
        self.PK_ID                = PK_ID               
        self.FK_SIIAB_REGION_ID   = FK_SIIAB_REGION_ID  
        self.FK_SIIAB_MARCA_ID    = FK_SIIAB_MARCA_ID   
        self.FK_SIIAB_ZONA_ID     = FK_SIIAB_ZONA_ID    
        self.FK_SIIAB_SERVICIO_ID = FK_SIIAB_SERVICIO_ID
        self.AUTOBUS              = AUTOBUS             
        self.VERSION              = VERSION             
        self.STATUS               = STATUS              

class Siiab_Secuencia_Detalle(Base,Tabla):
    __tablename__         = 'SIIAB_SECUENCIA_DETALLE'
    PK_ID                 = Column(VARCHAR(2), primary_key = True, autoincrement = False)   #Not Identity
    FK_SIIAB_SECUENCIA_ID = Column(Integer)                   
    ORDEN                 = Column(Integer)   
    FECHA_HORA            = Column(DateTime, default = datetime.datetime.utcnow)        
    NUMERO_TRAMO          = Column(Integer)          
    ORIGEN                = Column(Integer)    
    DESTINO               = Column(Integer)     
    VIA                   = Column(Integer) 
    OPERADOR_1            = Column(Integer)        
    OPERADOR_2            = Column(Integer)        
    STATUS                = Column(Integer)    
    POBLACION_ACTUAL      = Column(Integer)              

    def __init__(self, 
        PK_ID                : str = None,
        FK_SIIAB_SECUENCIA_ID: int = None,
        ORDEN                : int = None,
        FECHA_HORA           : datetime.datetime = None,
        NUMERO_TRAMO         : int = None,
        ORIGEN               : int = None,
        DESTINO              : int = None,
        VIA                  : int = None,
        OPERADOR_1           : int = None,
        OPERADOR_2           : int = None,
        STATUS               : int = None,
        POBLACION_ACTUAL     : int = None
    ):
        self.PK_ID                = PK_ID               
        self.FK_SIIAB_SECUENCIA_ID = FK_SIIAB_SECUENCIA_ID
        self.ORDEN                = ORDEN               
        self.FECHA_HORA           = FECHA_HORA          
        self.NUMERO_TRAMO         = NUMERO_TRAMO        
        self.ORIGEN               = ORIGEN              
        self.DESTINO              = DESTINO             
        self.VIA                  = VIA                 
        self.OPERADOR_1           = OPERADOR_1          
        self.OPERADOR_2           = OPERADOR_2          
        self.STATUS               = STATUS              
        self.POBLACION_ACTUAL     = POBLACION_ACTUAL    

class Siiab_Servicio(Base,Tabla):
    __tablename__        = 'SIIAB_SERVICIO'
    PK_ID                = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    DESCRIPCION          = Column(VARCHAR(50))
    DESCRIPCION_LARGA    = Column(VARCHAR(1024))
    STATUS               = Column(Integer)
    FECHA_ACTUALIZACION  = Column(DateTime, default = datetime.datetime.utcnow)

    def __init__(self, 
        PK_ID              : int = None,
        DESCRIPCION        : str = None,
        DESCRIPCION_LARGA  : str = None,
        STATUS             : int = None,
        FECHA_ACTUALIZACION: datetime.datetime = None
    ):
        self.PK_ID               = PK_ID              
        self.DESCRIPCION         = DESCRIPCION        
        self.DESCRIPCION_LARGA   = DESCRIPCION_LARGA  
        self.STATUS              = STATUS             
        self.FECHA_ACTUALIZACION = FECHA_ACTUALIZACION

class Siiab_Servidor(Base,Tabla):
    __tablename__             = 'SIIAB_SERVIDOR'
    PK_ID                     = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    DESCRIPCION               = Column(VARCHAR(50))     
    FK_SIIAB_SERVIDOR_TIPO_ID = Column(Integer)                     
    FK_SIIAB_SISTEMA_ID       = Column(Integer)             
    FK_REGION_ID              = Column(Integer)         
    FK_REGION_MARCA_ID        = Column(Integer)             
    FK_REGION_ZONA            = Column(VARCHAR(10))         
    SERVIDOR                  = Column(VARCHAR(50))     
    BASE_DATOS                = Column(VARCHAR(50))     
    STATUS                    = Column(Integer) 

    def __init__(self, 
        PK_ID                    : int = None,
        DESCRIPCION              : str = None,
        FK_SIIAB_SERVIDOR_TIPO_ID: int = None,
        FK_SIIAB_SISTEMA_ID      : int = None,
        FK_REGION_ID             : int = None,
        FK_REGION_MARCA_ID       : int = None,
        FK_REGION_ZONA           : str = None,
        SERVIDOR                 : str = None,
        BASE_DATOS               : str = None,
        STATUS                   : int = None
    ):
        self.PK_ID                     = PK_ID                    
        self.DESCRIPCION               = DESCRIPCION              
        self.FK_SIIAB_SERVIDOR_TIPO_ID = FK_SIIAB_SERVIDOR_TIPO_ID
        self.FK_SIIAB_SISTEMA_ID       = FK_SIIAB_SISTEMA_ID      
        self.FK_REGION_ID              = FK_REGION_ID             
        self.FK_REGION_MARCA_ID        = FK_REGION_MARCA_ID       
        self.FK_REGION_ZONA            = FK_REGION_ZONA           
        self.SERVIDOR                  = SERVIDOR                 
        self.BASE_DATOS                = BASE_DATOS               
        self.STATUS                    = STATUS                   

class Siiab_Servidor_Ip_Aut(Base,Tabla):
    __tablename__        = 'SIIAB_SERVIDOR_IP_AUT'
    PK_ID                = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    DESCRIPCION          = Column(VARCHAR(100))
    SERVIDOR             = Column(VARCHAR(100))    
    STATUS               = Column(Integer)

    def __init__(self, 
        PK_ID      : int = None,
        DESCRIPCION: str = None,
        SERVIDOR   : str = None,
        STATUS     : int = None
    ):
        self.PK_ID       = PK_ID      
        self.DESCRIPCION = DESCRIPCION
        self.SERVIDOR    = SERVIDOR   
        self.STATUS      = STATUS     

class Siiab_Servidor_Tipo(Base,Tabla):
    __tablename__        = 'SIIAB_SERVIDOR_TIPO'
    PK_ID                = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    DESCRIPTION          = Column(VARCHAR(50))
    STATUS               = Column(Integer)

    def __init__(self,
        PK_ID      : int = None,
        DESCRIPTION: str = None,
        STATUS     : int = None
    ):
        self.PK_ID       = PK_ID      
        self.DESCRIPTION = DESCRIPTION
        self.STATUS      = STATUS     

class Siiab_Sistema(Base,Tabla):
    __tablename__        = 'SIIAB_SISTEMA'
    PK_ID                = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    DESCRIPTION          = Column(VARCHAR(50))
    STATUS               = Column(Integer)

    def __init__(self,
        PK_ID      : int = None,
        DESCRIPTION: str = None,
        STATUS     : int = None
    ):
        self.PK_ID       = PK_ID      
        self.DESCRIPTION = DESCRIPTION
        self.STATUS      = STATUS     

class Siiab_Tramo(Base,Tabla):
    __tablename__         = 'SIIAB_TRAMO'
    PK_ID                 = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    NOMBRE                = Column(VARCHAR(100))
    NUMERO_TRAMO          = Column(Integer)      
    FK_SIIAB_REGION_ID    = Column(VARCHAR(2))            
    FK_SIIAB_MARCA_ID     = Column(VARCHAR(2))           
    FK_SIIAB_ZONA_ID      = Column(VARCHAR(3))          
    FK_SIIAB_SERVICIO_ID  = Column(Integer)              
    STATUS                = Column(Integer)
    FECHA_ACTUALIZACION   = Column(DateTime, default = datetime.datetime.utcnow)             
    FK_SIIAB_SERVIDOR_ID  = Column(Integer)              
    
    def __init__(self,
        PK_ID               : int = None,
        NOMBRE              : str = None,
        NUMERO_TRAMO        : int = None,
        FK_SIIAB_REGION_ID  : str = None,
        FK_SIIAB_MARCA_ID   : str = None,
        FK_SIIAB_ZONA_ID    : str = None,
        FK_SIIAB_SERVICIO_ID: int = None,
        STATUS              : int = None,
        FECHA_ACTUALIZACION : datetime.datetime = None,
        FK_SIIAB_SERVIDOR_ID: int = None
    ):
        self.PK_ID                = PK_ID               
        self.NOMBRE               = NOMBRE              
        self.NUMERO_TRAMO         = NUMERO_TRAMO        
        self.FK_SIIAB_REGION_ID   = FK_SIIAB_REGION_ID  
        self.FK_SIIAB_MARCA_ID    = FK_SIIAB_MARCA_ID   
        self.FK_SIIAB_ZONA_ID     = FK_SIIAB_ZONA_ID    
        self.FK_SIIAB_SERVICIO_ID = FK_SIIAB_SERVICIO_ID
        self.STATUS               = STATUS              
        self.FECHA_ACTUALIZACION  = FECHA_ACTUALIZACION 
        self.FK_SIIAB_SERVIDOR_ID = FK_SIIAB_SERVIDOR_ID
    
class Siiab_Tramo_Detalle(Base,Tabla):
    __tablename__                   = 'SIIAB_TRAMO_DETALLE'
    PK_ID                           = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    NUMERO_TRAMO                    = Column(Integer)
    SECUENCIA                       = Column(Integer)
    KILOMETROS                      = Column(Float)
    FK_SIIAB_POBLACION_SIVA_IDPOB   = Column(Integer)
    FK_SIIAB_SERVIDOR_ID            = Column(Integer)

    def __init__(self,
        PK_ID                        : int = None,
        NUMERO_TRAMO                 : int = None,
        SECUENCIA                    : int = None,
        KILOMETROS                   : float = None,
        FK_SIIAB_POBLACION_SIVA_IDPOB: int = None,
        FK_SIIAB_SERVIDOR_ID         : int = None
    ):
        self.PK_ID                         = PK_ID                        
        self.NUMERO_TRAMO                  = NUMERO_TRAMO                 
        self.SECUENCIA                     = SECUENCIA                    
        self.KILOMETROS                    = KILOMETROS                   
        self.FK_SIIAB_POBLACION_SIVA_IDPOB = FK_SIIAB_POBLACION_SIVA_IDPOB
        self.FK_SIIAB_SERVIDOR_ID          = FK_SIIAB_SERVIDOR_ID         

class Siiab_Zona(Base,Tabla):
    __tablename__       = 'SIIAB_ZONA'
    PK_ID               = Column(VARCHAR(3), primary_key = True, autoincrement = False)   #Not Identity
    DESCRIPCION         = Column(VARCHAR(50))
    STATUS              = Column(Integer)
    FECHA_ACTUALIZACION = Column(DateTime, default = datetime.datetime.utcnow)

    def __init__(self,
        PK_ID              : str = None,
        DESCRIPCION        : str = None,
        STATUS             : int = None,
        FECHA_ACTUALIZACION: datetime.datetime = None
    ):
        self.PK_ID               = PK_ID              
        self.DESCRIPCION         = DESCRIPCION        
        self.STATUS              = STATUS             
        self.FECHA_ACTUALIZACION = FECHA_ACTUALIZACION