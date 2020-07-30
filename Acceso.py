import requests
import json
import datetime
import timedelta
import os
import sys
from google.cloud import datastore

class Acceso:
    _URL = os.environ['URL_MGT']
    _HEADERS = json.loads(os.environ['HDRS_MGT'])
    _LOGIN_DATA = json.loads(os.environ['LGIN_DATA'])
    _clientDS = datastore.Client()
    _resultado_DS = None
    #Ultimo: 5821133378405638863
    #Caducado: 7179171805771627354
    _crede = None
    _generar_crede = False
    _user_id = None
    #_FILE_TO_SAVE = "codetx/cred.txt"
    def __init__(self):
        self.getCredDS()
        if self._crede is None or not 'path' in self._crede:
            self.getCrede(True)
        else:
            self._URL = self._URL if (self._crede['path'] == 'ThisServer') else 'https://' + self._crede['path'] + '/apiv1/'
    
    @property
    def HEADERS(self):
        return self._HEADERS
    
    @property
    def URL(self):
        return self._URL

    def getCrede(self, nuevo = False):
        if self._crede is None or nuevo:
            response = requests.post(os.environ['URL_MGT'],data=json.dumps(self._LOGIN_DATA),headers=self._HEADERS)
            if 'error' in response.json():
                print('>', 'ERROR getCrede', '<', sep=('-')*15, file=sys.stderr)
                print(response.json(), file=sys.stderr)
                print('>', ' END-ERROR ', '<',  sep=('-')*15, file=sys.stderr)
            if response.status_code == 200:
                result = response.json()['result']
                print('>', 'NUEVO SESSION ID', '<', sep=('-')*15, file=sys.stderr)
                print(result, file=sys.stderr)
                print('>', ' E N D ', '<', sep=('-')*15, file=sys.stderr)
                self._crede =  result
                self._URL = self._URL if (result['path'] == 'ThisServer') else 'https://' + result['path'] + '/apiv1/'
                self.setCredDS()
        return self._crede['credentials']

    def getElement(self,reqElement):
        respElement = requests.post(self._URL,data=json.dumps(reqElement),headers=self._HEADERS)
        if 'error' in respElement.json() and not self._generar_crede:
            print('>', 'ERROR getElement', '<', sep=('-')*15, file=sys.stderr)
            print(json.dumps(respElement.json()), file=sys.stderr)
            print('>', 'END-ERROR', '<', sep=('-')*15, file=sys.stderr)
            reqElement['params']['credentials'] = self.getCrede(True)
            self._generar_crede = True
            return self.getElement(reqElement)
        elif self._generar_crede:
            self._generar_crede = False
        return respElement

    def getUserID(self):
        reqUsers  = { 
            'method' : 'Get', 
            'params': {
                'typeName':'User', 
                'search' : {
                    'name' : self._LOGIN_DATA['params']['userName']
                },
                'credentials': self.getCrede()
            }
        }
        respuesta = 'b0'
        respUsers = self.getElement(reqUsers)
        if respUsers.status_code != 200 or 'error' in respUsers:
            print(respUsers,file=sys.stderr)
            print(respUsers.json(), file=sys.stderr)
        else:
            for x in respUsers.json()['result']:
                respuesta=x['id']
                break

        #print(respUsers)
        #print(respUsers.json())
        return respuesta
        #return respUsers.json()


    def getCredDS(self):
        query = self._clientDS.query(kind=os.environ['KIND_DS'])
        query.add_filter('MCSERVICE', '=', os.environ['MCSERVICE'])
        # Obtenemos los resultados
        items = query.fetch()
        self._resultado_DS = None
        for item in items:
            self._resultado_DS = item
        self._crede = json.loads(self._resultado_DS['CREDENT'])
    
    def setCredDS(self):
        self._resultado_DS.update({'CREDENT':json.dumps(self._crede)})
        self._clientDS.put(self._resultado_DS)
        