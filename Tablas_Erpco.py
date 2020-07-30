from sqlalchemy import Column, Integer, VARCHAR, NCHAR, DateTime
from sqlalchemy.exc import SQLAlchemyError
import datetime
from Almacenamiento import db_session, Base
from Almacenamiento.Tablas import Tabla

#ERPCO_CLASE_SERVICIO
class Erpco_Clase_Servicio(Base,Tabla):
    __tablename__ = 'ERPCO_CLASE_SERVICIO'
    CLASESERVICIO_ID = Column(Integer, primary_key = True)   #Identity by default
    DESCCLASESERV    = Column(VARCHAR(50))
    STATUS           = Column(Integer)
    CVECLASESERV     = Column(VARCHAR(10))
    RAZONSOCIAL      = Column(VARCHAR(50))

    def __init__(self, 
        CLASESERVICIO_ID: int = None,
        DESCCLASESERV   : str = None,
        STATUS          : int = None,
        CVECLASESERV    : str = None,
        RAZONSOCIAL     : str = None
    ):
        self.CLASESERVICIO_ID = CLASESERVICIO_ID
        self.DESCCLASESERV    = DESCCLASESERV   
        self.STATUS           = STATUS          
        self.CVECLASESERV     = CVECLASESERV    
        self.RAZONSOCIAL      = RAZONSOCIAL     
#ERPCO_CORRIDA
class ERPCO_CORRIDA(Base,Tabla):
    __tablename__     = 'ERPCO_CORRIDA'
    CORRIDA_ID        = Column(Integer, primary_key = True)      
    FECCORRIDA        = Column(DateTime, primary_key = True)      
    HORACORRIDA       = Column(DateTime, primary_key = True)      
    STATUS            = Column(Integer)  
    FECHORSAL = Column(DateTime, default=datetime.datetime.utcnow)
    FECHORLLE = Column(DateTime, default=datetime.datetime.utcnow)
    FECHORLLEREAL = Column(DateTime, default=datetime.datetime.utcnow)
    FECHORSALREAL = Column(DateTime, default=datetime.datetime.utcnow)
    FECHORACT = Column(DateTime, default=datetime.datetime.utcnow)
    KILOMETROS        = Column(Integer)      
    AUTOBUS_ID        = Column(Integer)      
    CLASESERVICIO_ID  = Column(Integer)              
    REGION_ID         = Column(Integer)      
    MARCA_ID          = Column(Integer)      
    RUTA_ID           = Column(Integer)  
    STATUSVENTA = Column(NCHAR(50))
    ORIGEN_ID         = Column(Integer)      
    DESTINO_ID        = Column(Integer)      
    DIAGRAMAAUTOBUS_ID= Column(Integer)              
    NCONDS            = Column(Integer)  
    ESCONDSVAR        = Column(Integer)      
    TIPOROLCTRL_ID    = Column(Integer)          

    def __init__(self, 
        CORRIDA_ID        : int = None,
        FECCORRIDA        : datetime.datetime = None,
        HORACORRIDA       : datetime.datetime = None,
        STATUS            : int = None,
        FECHORSAL         : datetime.datetime = None,
        FECHORLLE         : datetime.datetime = None,
        FECHORLLEREAL     : datetime.datetime = None,
        FECHORSALREAL     : datetime.datetime = None,
        FECHORACT         : datetime.datetime = None,
        KILOMETROS        : int = None,
        AUTOBUS_ID        : int = None,
        CLASESERVICIO_ID  : int = None,
        REGION_ID         : int = None,
        MARCA_ID          : int = None,
        RUTA_ID           : int = None,
        STATUSVENTA       : str = None,
        ORIGEN_ID         : int = None,
        DESTINO_ID        : int = None,
        DIAGRAMAAUTOBUS_ID: int = None,
        NCONDS            : int = None,
        ESCONDSVAR        : int = None,
        TIPOROLCTRL_ID    : int = None
    ):
        self.CORRIDA_ID         = CORRIDA_ID        
        self.FECCORRIDA         = FECCORRIDA        
        self.HORACORRIDA        = HORACORRIDA       
        self.STATUS             = STATUS            
        self.FECHORSAL          = FECHORSAL         
        self.FECHORLLE          = FECHORLLE         
        self.FECHORLLEREAL      = FECHORLLEREAL     
        self.FECHORSALREAL      = FECHORSALREAL     
        self.FECHORACT          = FECHORACT         
        self.KILOMETROS         = KILOMETROS        
        self.AUTOBUS_ID         = AUTOBUS_ID        
        self.CLASESERVICIO_ID   = CLASESERVICIO_ID  
        self.REGION_ID          = REGION_ID         
        self.MARCA_ID           = MARCA_ID          
        self.RUTA_ID            = RUTA_ID           
        self.STATUSVENTA        = STATUSVENTA       
        self.ORIGEN_ID          = ORIGEN_ID         
        self.DESTINO_ID         = DESTINO_ID        
        self.DIAGRAMAAUTOBUS_ID = DIAGRAMAAUTOBUS_ID
        self.NCONDS             = NCONDS            
        self.ESCONDSVAR         = ESCONDSVAR        
        self.TIPOROLCTRL_ID     = TIPOROLCTRL_ID    
#ERPCO_CORRIDA_TRAMO
class ERPCO_CORRIDA_TRAMO(Base,Tabla):
    __tablename__ = 'ERPCO_CORRIDA_TRAMO'
    TRAMOCORRIDA_ID = Column(Integer, primary_key=True)
    CORRIDA_ID = Column(Integer)
    FECCORRIDA = Column(DateTime, default=datetime.datetime.utcnow)
    HORACORRIDA = Column(DateTime, default=datetime.datetime.utcnow)
    STATUS = Column(Integer)
    SECUENCIA = Column(Integer)
    FECHORSAL = Column(DateTime, default=datetime.datetime.utcnow)
    FECHORSALREAL = Column(DateTime, default=datetime.datetime.utcnow)
    TRECORRIDO = Column(DateTime, default=datetime.datetime.utcnow)
    TRECORRIDOREAL = Column(DateTime, default=datetime.datetime.utcnow)
    TESTANCIA = Column(DateTime, default=datetime.datetime.utcnow)
    TESTANCIAREAL = Column(DateTime, default=datetime.datetime.utcnow)
    FECHORACT = Column(DateTime, default=datetime.datetime.utcnow)
    ESTACONFIRMADO = Column(Integer)
    KMSPAGOCONDUCTOR = Column(Integer)
    AUTOBUS_ID = Column(Integer)
    TRAMO_ID = Column(Integer)
    CONDUCTOR1_ID = Column(Integer)
    CONDUCTOR2_ID = Column(Integer)

    def __init__(self,
                 TRAMOCORRIDA_ID 					    : int = None,
                 CORRIDA_ID 					    : int = None,
                 FECCORRIDA  						: datetime = None,
                 HORACORRIDA  						: datetime = None,
                 STATUS 					    : int = None,
                 SECUENCIA 					    : int = None,
                 FECHORSAL 						: datetime = None,
                 FECHORSALREAL  						: datetime = None,
                 TRECORRIDO  						: datetime = None,
                 TRECORRIDOREAL  						: datetime = None,
                 TESTANCIA  						: datetime = None,
                 TESTANCIAREAL  						: datetime = None,
                 FECHORACT  						: datetime = None,
                 ESTACONFIRMADO 					    : int = None,
                 KMSPAGOCONDUCTOR 					    : int = None,
                 AUTOBUS_ID 					    : int = None,
                 TRAMO_ID 					    : int = None,
                 CONDUCTOR1_ID 					    : int = None,
                 CONDUCTOR2_ID 					    : int = None

    ):
        self.TRAMOCORRIDA_ID = TRAMOCORRIDA_ID
        self.CORRIDA_ID = CORRIDA_ID
        self.FECCORRIDA = FECCORRIDA
        self.HORACORRIDA = HORACORRIDA
        self.STATUS = STATUS
        self.SECUENCIA = SECUENCIA
        self.FECHORSAL = FECHORSAL
        self.FECHORSALREAL = FECHORSALREAL
        self.TRECORRIDO = TRECORRIDO
        self.TRECORRIDOREAL = TRECORRIDOREAL
        self.TESTANCIA = TESTANCIA
        self.TESTANCIAREAL = TESTANCIAREAL
        self.FECHORACT = FECHORACT
        self.ESTACONFIRMADO = ESTACONFIRMADO
        self.KMSPAGOCONDUCTOR = KMSPAGOCONDUCTOR
        self.AUTOBUS_ID = AUTOBUS_ID
        self.TRAMO_ID = TRAMO_ID
        self.CONDUCTOR1_ID = CONDUCTOR1_ID
        self.CONDUCTOR2_ID = CONDUCTOR2_ID

#SAE_RUTA_DETALLE
class SAE_RUTA_DETALLE(Base,Tabla):
    __tablename__ =  "SAE_RUTA_DETALLE"
    PK_ID = Column(Integer, primary_key=True)
    FK_ERPCO_RUTA_ID = Column(Integer)
    FK_RUTA_ID = Column(Integer)
    FK_GSI_RUTA_SIIAB = Column(Integer)
    FK_ERPCO_PARADA_INICIO_ID = Column(Integer)
    FK_ERPCO_PARADA_FIN_ID = Column(Integer)


    def __init__(self,
                 PK_ID: int = None,
                 FK_ERPCO_RUTA_ID: int = None,
                 FK_RUTA_ID: int = None,
                 FK_GSI_RUTA_SIIAB: int = None,
                 FK_ERPCO_PARADA_INICIO_ID: int = None,
                 FK_ERPCO_PARADA_FIN_ID: int = None
                 ):
                    self.PK_ID = PK_ID
                    self.FK_ERPCO_RUTA_ID = FK_ERPCO_RUTA_ID
                    self.FK_RUTA_ID = FK_RUTA_ID
                    self.FK_GSI_RUTA_SIIAB = FK_GSI_RUTA_SIIAB
                    self.FK_ERPCO_PARADA_INICIO_ID = FK_ERPCO_PARADA_INICIO_ID
                    self.FK_ERPCO_PARADA_FIN_ID = FK_ERPCO_PARADA_FIN_ID
#ERPCO_RUTA
class ERPCO_RUTA(Base,Tabla):
    __tablename__ = "ERPCO_RUTA"
    RUTA_ID = Column(Integer, primary_key=True)
    NOMBRUTA = Column(NCHAR(50))
    STATUS = Column(Integer)
    CLASESERVICIO_ID = Column(Integer)
    ORIGEN_ID = Column(Integer)
    DESTINO_ID = Column(Integer)
    RUTACTRL_ID = Column(Integer)

    def __init__(self,
        RUTA_ID: int = None,
        NOMBRUTA: str = None,
        STATUS: int = None,
        CLASESERVICIO_ID: int = None,
        ORIGEN_ID  : int = None,
        DESTINO_ID : int = None,
        RUTACTRL_ID: int = None,
    ):
        self.RUTA_ID = RUTA_ID
        self.NOMBRUTA = NOMBRUTA
        self.STATUS = STATUS
        self.CLASESERVICIO_ID = CLASESERVICIO_ID
        self.ORIGEN_ID   = ORIGEN_ID                 
        self.DESTINO_ID  = DESTINO_ID                
        self.RUTACTRL_ID = RUTACTRL_ID
#ERPCO_MARCA
class Erpco_Marca(Base,Tabla):
    __tablename__    = 'ERPCO_MARCA'
    MARCA_ID         = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    CVEMARCA         = Column(VARCHAR(10))
    STATUS           = Column(Integer)
    NOMBMARCA        = Column(VARCHAR(50))
    RAZONSABREVOCIAL = Column(VARCHAR(6))

    def __init__(self, 
        MARCA_ID        : int = None,
        CVEMARCA        : str = None,
        STATUS          : int = None,
        NOMBMARCA       : str = None,
        RAZONSABREVOCIAL: str = None
    ):
        self.MARCA_ID         = MARCA_ID              
        self.CVEMARCA         = CVEMARCA              
        self.STATUS           = STATUS                
        self.NOMBMARCA        = NOMBMARCA             
        self.RAZONSABREVOCIAL = RAZONSABREVOCIAL 
#ERPCO_REGION
class Erpco_Region(Base,Tabla):
    __tablename__ = 'ERPCO_REGION'
    REGION_ID     = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    CVEREGION     = Column(VARCHAR(10))
    STATUS        = Column(Integer)
    NOMBREGION    = Column(VARCHAR(50))

    def __init__(self, 
        REGION_ID : int = None,
        CVEREGION : str = None,
        STATUS    : int = None,
        NOMBREGION: str = None,
    ):
        self.REGION_ID  = REGION_ID 
        self.CVEREGION  = CVEREGION 
        self.STATUS     = STATUS    
        self.NOMBREGION = NOMBREGION