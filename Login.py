import requests
import json
import datetime
import timedelta
import os
import sys
from google.cloud import datastore

class Login:
    _clientDS = datastore.Client()
     
    def getAuthorized(self):
        query = self._clientDS.query(kind=os.environ['ACL_SERVICE'])
        query.add_filter('MCSERVICE', '=', os.environ['MCSERVICE'])
        # Obtenemos los resultados
        items = query.fetch()
        resultado_DS = None
        for item in items:
            resultado_DS = item
        return str(resultado_DS['AUTHORIZED']) if str(resultado_DS['AUTHORIZED']).endswith(',') else str(resultado_DS['AUTHORIZED']) + ','
    
    def isAuthorized(self, email):
        return self.getAuthorized().find(str(email) + ',') >= 0