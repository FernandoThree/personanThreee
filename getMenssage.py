import mygeotab as mg
import getpass 

class recepMenssage:
    # Definimos una clase para usar API en la recepción de mensajes
"""    BORRALO ****************************************************************************
{"credentials": {"database": "saeado", "sessionId": "1066324154464238471758", "userName": " test.idt@mobilityado.com"}, 
    "path": "my89.geotab.com", "securityToken":
     {"database": "saeado", "sessionId": "1066324156444238471758", "userName": "test.idt@mobilityado.com"}}
""" 
    def crdmg(self):
        # input() instead of raw_input() in Python 3
        database = raw_input(“Database: ”)
        username = raw_input(“Username: ”)
        password = getpass.getpass(“Password: ”)
        api = mg.API(database=database, username=username, password=password)
        api.authenticate()
        password = None

        # After saving password, password is set to none, but session_id is set to authenticate calls
        print(api.credentials.password == None)
        print(api.credentials.session_id == None)
