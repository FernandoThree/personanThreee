import requests
import json
import datetime
import timedelta
import sys
from Autoregulacion.Acceso import Acceso
import base64
import sys


class MensajesSerialIOX:

    def getUserID(self):
        myAcceso = Acceso()
        return myAcceso.getUserID()

    # Mensajes MIME o Serial
    def sendMessage(self, mensajeTxt, bus, usuario):
        myAcceso = Acceso()
        command = '\xa1'
        checksum1 = b'\x00'
        checksum2 = b'\x00'

        cadenaB = bytes(command, "utf-8") + \
            bytes([len(mensajeTxt)]) + bytes(mensajeTxt, "utf-8")

        checksum1 = (sum(cadenaB[1:]) & 0xFF)
        #nvCad usada para el checksum2
        nvCad = b""
        i = 2
        for element in cadenaB[1:]:
            subA = cadenaB[1:i]
            nvCad += subA
            i += 1

        checksum2 = (sum(nvCad) & 0xFF)
        cadenaA = cadenaB + bytes([checksum1]) + bytes([checksum2])
        b64 = base64.b64encode(cadenaA[1:])

        reqNvoMensaje = {
            'method': 'Add',
            'params': {
                'typeName': 'TextMessage',
                'credentials': myAcceso.getCrede(),
                'entity': {
                    'activeFrom': '0001-01-01',
                    'activeTo': '9999-12-31T23:59:59.999Z',
                    'isDirectionToVehicle': True,
                    'messageContent': {
                        'data': str(b64).replace("b'", "").replace("'", ""),
                        'channel': 1,
                        'isAcknowledgeRequired': True,
                        'contentType': 'SerialIox'
                    },
                    'user': {'id': usuario},
                    'device': {'id': bus}
                }
            }
        }
        data = myAcceso.getElement(reqNvoMensaje)
        if 'error' in data:
            print(data.json(), file=sys.stderr)
        return data.json()

    # Mensaje Abierto MIME/Serial
    def sendTextMessage(self, mensajeTxt, bus, usuario):
        return self.sendMessage("#|TEX_X1|" + str(datetime.datetime.now())[0:19].replace(' ', 'T') + "|5|1|1|2|1000|" + mensajeTxt + "|#", bus, usuario)

    # Mensajes GARMIN
    def sendMessageGarmin(self, mensajeTxt, bus, usuario):
        myAcceso = Acceso()
        reqNvoMensaje = {
            'method': 'Add',
            'params': {
                'typeName': 'TextMessage',
                'credentials': myAcceso.getCrede(),
                'entity': {
                    'activeFrom': '0001-01-01',
                    'activeTo': '9999-12-31T23:59:59.999Z',
                    'isDirectionToVehicle': True,
                    'messageContent': {
                        'message': mensajeTxt,
                        'urgent': True,
                        'contentType': 'Normal'
                    },
                    'user': {'id': usuario},
                    'device': {'id': bus}
                }
            }
        }
        data = myAcceso.getElement(reqNvoMensaje)
        if 'error' in data:
            print(data.json(), file=sys.stderr)
        return data.json()

    # Mensaje Abierto GARMIN
    def sendTextMessageGarmin(self, mensajeTxt, bus, usuario):
        return self.sendMessageGarmin("#|TEX_X1|" + str(datetime.datetime.now())[0:19].replace(' ', 'T') + "|5|1|1|2|1000|" + mensajeTxt + "|#", bus, usuario)

    def getDevices(self):
        myAcceso = Acceso()
        ahora = datetime.datetime.utcnow()
        reqDevices = {
            'method': 'Get',
            'params': {
                'typeName': 'Device',
                'credentials': myAcceso.getCrede()
            }
        }
        diccionario = {}
        respDevices = myAcceso.getElement(reqDevices)
        if respDevices.status_code == 200:
            if 'error' in respDevices.json():
                print(respDevices.json(), file=sys.stderr)
                return None
            else:
                for x in respDevices.json()['result']:
                    #if x['devicePlans'] is not None and len(x['devicePlans']) > 0 and x['serialNumber'] != '000-000-0000':
                    if x['serialNumber'] != '000-000-0000':
                        diccionario[x['id']] = {
                            "eco": x['name'],
                            "diasSinConexion": None,
                            "fechaUltConexion": None,
                            "serialNumber": x['serialNumber']
                        }
            #Inicio Status Info
            reqLg = {
                'method': 'Get',
                'params': {
                    'typeName': 'DeviceStatusInfo',
                    'credentials': myAcceso.getCrede()
                }
            }
            respLg = myAcceso.getElement(reqLg)
            if respLg.status_code == 200:
                if 'error' in respLg.json():
                    print(respLg.json(), file=sys.stderr)
                    return diccionario
                for stDev in respLg.json()['result']:
                    diccionario[stDev['device']['id']]['diasSinConexion'] = (
                        ahora - datetime.datetime.strptime(stDev['dateTime'], '%Y-%m-%dT%H:%M:%S.%fZ')).days
                    diccionario[stDev['device']['id']]['diasSinConexion'] = diccionario[stDev['device']['id']
                                                                                        ]['diasSinConexion'] if diccionario[stDev['device']['id']]['diasSinConexion'] > 0 else 0
                    diccionario[stDev['device']['id']
                                ]['fechaUltConexion'] = stDev['dateTime']
                    if 'latitude' in stDev and 'longitude' in stDev:
                        diccionario[stDev['device']['id']
                                    ]['lat'] = stDev['latitude']
                        diccionario[stDev['device']['id']
                                    ]['lon'] = stDev['longitude']
            del respLg
        return diccionario

    def getTextMessages(self, bus, minutos=30):
        myAcceso = Acceso()
        reqMessages = {
            'method': 'Get',
            'params': {
                'typeName': 'TextMessage',
                'search':  {
                    'fromDate':  str(datetime.datetime.today() - timedelta.Timedelta(minutes=minutos))[0:19].replace(' ', 'T'),
                    'DeviceSearch': {
                            'id': bus
                    }
                },
                'credentials': myAcceso.getCrede()
            }
        }
        data = myAcceso.getElement(reqMessages)
        if data.status_code != 200 or 'error' in data:
            print(data, file=sys.stderr)
            return {}
        mensajesTexto = {}
        for x in data.json()['result']:
            try:
                if "#|TEX_E1" in str(base64.b64decode(x['messageContent']['data'])) or "#|TEX_X1" in str(base64.b64decode(x['messageContent']['data'])):
                    sp = str(base64.b64decode(
                        x['messageContent']['data'])).split('|')
                    temp = {}
                    temp['msj'] = sp[2] if "TEX_E1" in sp[1] else sp[8]
                    temp['enviado'] = x['sent']
                    temp['entregado'] = None if 'delivered' not in x else x['delivered']
                    temp['estado'] = 'pnd' if 'delivered' not in x else 'ok'
                    temp['toDevice'] = x['isDirectionToVehicle']
                    mensajesTexto[x['id']] = temp
            except:
                continue
        return mensajesTexto

    def getFullTextMessages(self, minutos=30, bus=None):
        myAcceso = Acceso()
        if bus == None:
            reqMessages = {
                'method': 'Get',
                'params': {
                    'typeName': 'TextMessage',
                    'search':  {
                        'fromDate':  str(datetime.datetime.today() - timedelta.Timedelta(minutes=minutos))[0:19].replace(' ', 'T')
                    },
                    'credentials': myAcceso.getCrede()
                }
            }
        else:
            reqMessages = {
                'method': 'Get',
                'params': {
                    'typeName': 'TextMessage',
                    'search':  {
                        'fromDate':  str(datetime.datetime.today() - timedelta.Timedelta(minutes=minutos))[0:19].replace(' ', 'T'),
                        'DeviceSearch': {
                                'id': bus
                        }
                    },
                    'credentials': myAcceso.getCrede()
                }
            }
        data = myAcceso.getElement(reqMessages)
        if data.status_code != 200 or 'error' in data:
            print(data, file=sys.stderr)
            return {}
        mensajesTexto = {}
        for x in data.json()['result']:
            temp = {}
            try:
                if "#" in str(base64.b64decode(x['messageContent']['data'])):
                    temp['msj'] = "#" + \
                        str(base64.b64decode(x['messageContent']['data'])).split(
                            '#')[1]+"#"
                else:
                    temp['msj'] = str(base64.b64decode(
                        x['messageContent']['data']))
            except:
                pass
            temp['enviado'] = x['sent']
            temp['entregado'] = None if 'delivered' not in x else x['delivered']
            temp['estado'] = 'pnd' if 'delivered' not in x else 'ok'
            temp['toDevice'] = x['isDirectionToVehicle']
            mensajesTexto[x['id']] = temp
        return mensajesTexto
