from sqlalchemy import Column, Integer, VARCHAR, NCHAR, DateTime, NVARCHAR, CHAR
from sqlalchemy.exc import SQLAlchemyError
import datetime
from Almacenamiento import db_session, Base
from Almacenamiento.Tablas import Tabla

class Menu(Base,Tabla):
    __tablename__ = 'SAE_MENU'
    PK_ID         = Column(Integer, primary_key = True)   #Identity by default
    NAME          = Column(VARCHAR(50))
    ACTIVE        = Column(Integer)

    def __init__(self, 
        PK_ID : int = None,
        NAME  : str = None,
        ACTIVE: int = None
    ):
        self.PK_ID  = PK_ID 
        self.NAME   = NAME  
        self.ACTIVE = ACTIVE

class Menu_Build(Base,Tabla):
    __tablename__  = 'SAE_MENU_BUILD'
    PK_ID          = Column(Integer, primary_key = True)   #Identity by default
    TYPE_USER_ID   = Column(Integer)         
    MENU_ID        = Column(Integer) 
    MENU_OPTION_ID = Column(Integer)         
    ACTIVE         = Column(Integer) 

    def __init__(self, 
        PK_ID         : int = None,
        TYPE_USER_ID  : int = None,
        MENU_ID       : int = None,
        MENU_OPTION_ID: int = None,
        ACTIVE        : int = None
    ):
        self.PK_ID          = PK_ID         
        self.TYPE_USER_ID   = TYPE_USER_ID  
        self.MENU_ID        = MENU_ID       
        self.MENU_OPTION_ID = MENU_OPTION_ID
        self.ACTIVE         = ACTIVE        

class Menu_Build_Profile(Base,Tabla):
    __tablename__       = 'SAE_MENU_BUILD_PROFILE'
    PK_ID               = Column(Integer, primary_key = True)   #Identity by default
    SECURITY_PROFILE_ID = Column(Integer)            
    MENU_ID             = Column(Integer)
    ACTIVE              = Column(Integer)

    def __init__(self, 
        PK_ID              : int = None,
        SECURITY_PROFILE_ID: int = None,
        MENU_ID            : int = None,
        ACTIVE             : int = None
    ):
        self.PK_ID               = PK_ID              
        self.SECURITY_PROFILE_ID = SECURITY_PROFILE_ID
        self.MENU_ID             = MENU_ID            
        self.ACTIVE              = ACTIVE             

class Menu_Option(Base,Tabla):
    __tablename__ = 'SAE_MENU_OPTION'
    PK_ID         = Column(Integer, primary_key = True)   #Identity by default
    NAME          = Column(NCHAR(100))
    DESCRIPTION   = Column(NCHAR(100))
    URL           = Column(NCHAR(100))
    COMAND        = Column(NCHAR(100))
    ACTIVE        = Column(Integer)

    def __init__(self, 
        PK_ID      : int = None,
        NAME       : str = None,
        DESCRIPTION: str = None,
        URL        : str = None,
        COMAND     : str = None,
        ACTIVE     : int = None
    ):
        self.PK_ID       = PK_ID      
        self.NAME        = NAME       
        self.DESCRIPTION = DESCRIPTION
        self.URL         = URL        
        self.COMAND      = COMAND     
        self.ACTIVE      = ACTIVE

class Security_Profile(Base,Tabla):
    __tablename__ = 'SAE_SECURITY_PROFILE'
    PK_ID         = Column(Integer, primary_key = True)   #Identity by default
    NAME          = Column(NCHAR(10))
    ACTIVE        = Column(Integer)

    def __init__(self, 
        PK_ID : int = None,
        NAME  : int = None,
        ACTIVE: int = None
    ):
        self.PK_ID  = PK_ID 
        self.NAME   = NAME  
        self.ACTIVE = ACTIVE

class Security_Profile_User(Base,Tabla):
    __tablename__       = 'SAE_SECURITY_PROFILE_USER'
    PK_ID               = Column(Integer, primary_key = True)   #Identity by default
    SECURITY_PROFILE_ID = Column(Integer)
    SECURITY_USER_ID    = Column(Integer)

    def __init__(self, 
        PK_ID              : int = None,
        SECURITY_PROFILE_ID: int = None,
        SECURITY_USER_ID   : int = None
    ):
        self.PK_ID               = PK_ID              
        self.SECURITY_PROFILE_ID = SECURITY_PROFILE_ID
        self.SECURITY_USER_ID    = SECURITY_USER_ID   

class Securuty_User(Base,Tabla):
    __tablename__    = 'SAE_SECURITY_USER'
    PK_ID            = Column(Integer, primary_key = True)   #Identity by default
    CLAVE            = Column(NVARCHAR(10))                
    LOGIN            = Column(NCHAR(10))
    PASSWORD         = Column(NCHAR(10))    
    ACTIVE_DIRECTORY = Column(Integer)            
    NAME             = Column(CHAR(10))
    LAST_NAME        = Column(CHAR(100))    
    EMAIL            = Column(CHAR(100))
    ACTIVE           = Column(Integer)

    def __init__(self, 
        PK_ID           : int = None,
        CLAVE           : str = None,
        LOGIN           : str = None,
        PASSWORD        : str = None,
        ACTIVE_DIRECTORY: int = None,
        NAME            : str = None,
        LAST_NAME       : str = None,
        EMAIL           : str = None,
        ACTIVE          : int = None
    ):
        self.PK_ID            = PK_ID           
        self.CLAVE            = CLAVE           
        self.LOGIN            = LOGIN           
        self.PASSWORD         = PASSWORD        
        self.ACTIVE_DIRECTORY = ACTIVE_DIRECTORY
        self.NAME             = NAME            
        self.LAST_NAME        = LAST_NAME       
        self.EMAIL            = EMAIL           
        self.ACTIVE           = ACTIVE          

class Type_User(Base,Tabla):
    __tablename__ = 'SAE_TYPE_USER'
    PK_ID         = Column(Integer, primary_key = True)   #Identity by default
    NAME          = Column(NCHAR(50))
    ACTIVE        = Column(Integer)

    def __init__(self, 
        PK_ID : int = None,
        NAME  : str = None,
        ACTIVE: int = None
    ):
        self.PK_ID  = PK_ID 
        self.NAME   = NAME  
        self.ACTIVE = ACTIVE