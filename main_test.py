from Autoregulacion.Mensajes import MensajesSerialIOX
from Autoregulacion.Login import Login
from Autoregulacion.AutoRegul import AutoRegulacion
import datetime
import base64
import time
import sys
import random

d = {}

def getDato(dato, sub):
    return dato[1][sub]

def getDato2(dato):
    return dato[1]['entregado']

if __name__ == '__main__':
    print('-', ' > BEGIN < ', '-', sep=('-')*38)
    mensajes = MensajesSerialIOX()
    mns_Txt = AutoRegulacion()
    bus = 'b38'
    usuario = mensajes.getUserID()
    if len(sys.argv) > 1:
        if str(sys.argv[1]) == "1":
            viaje = "2020-03-05T13:59:00"
            trama = ""
            i = 0
            for i in range(1, 51):
                #i +=1
                trama = "#|TEX_X1|{}T{}|{}|1|1|2|1000|MSJ {}|#".format(str(
                    datetime.datetime.now().date()), str(datetime.datetime.now().time())[0:8], i, i)
                # print(divmod(i,5))
                if(divmod(i, 5)[1] == 0):
                    print(trama, file=sys.stdout)
                    res = mensajes.sendMessage(trama, bus, usuario)
                    print(res, file=sys.stdout)
                    #time.sleep(1)
                frecAdelante = random.randrange(7, 17)
                punt = random.randrange(-6, 6)
                frecAtras = random.randrange(7, 17)
                trama2 = "#|AUT_X3|{}T{}|{}|3|4|12|12|3|4|1073716|{}|1073714|{}|{}|AXO|CTR|CTR|2020-03-05T14:10:46|15|#".format(
                    str(datetime.datetime.now().date()), str(datetime.datetime.now().time())[0:8], punt, frecAtras, frecAdelante, viaje)
                print(trama2, file=sys.stdout)
                res2 = mensajes.sendMessage(trama2, bus, usuario)
                print(res2, file=sys.stdout)
                #time.sleep(1)
        elif str(sys.argv[1]) == "2":
            #Todos los mensajes sin importar SerialIOX, Garmin, etc, ni categoría (comando o trama SAE)
            datos = mensajes.getFullTextMessages(minutos=720, bus=bus)
            toBus = 0
            toServ = 0
            for x in datos:
                print(str(x) + '->' + str(datos[x]))
                if(datos[x]['toDevice']):
                    toBus += 1
                else:
                    toServ += 1
            print('To Bus: ' + str(toBus) + ', To Server: ' + str(toServ))
        elif str(sys.argv[1]) == "3":
            #Obtiene información básica de las unidades
            diccionario = mensajes.getDevices()
            dic2 = sorted(diccionario.items(),
                          key=lambda kv: kv[1]['eco'], reverse=True)
            #diccionario.sort(key=lambda x: x[0]['name'], reverse=False)
            for x in dic2:
                print(str(x[0]) + ' -> ' + str(x[1]))
        elif str(sys.argv[1]) == "4":
            #Obtiene solo mensajes de Texto (Abiertos y Predefinidos)
            diccionario = mensajes.getTextMessages(bus=bus, minutos=1440)
            dic2 = sorted(diccionario.items(),
                          key=lambda kv: getDato2(kv), reverse=True)
            for x in dic2:
                print(str(x) + '->' + str(x[1]['enviado']), file=sys.stdout)
        elif str(sys.argv[1]) == "5":
            #Envio de mensaje
            mensaje = "Msj Prueba 03 PLAAAAAAT"
            resp = mensajes.sendTextMessage(mensaje, bus, usuario)
            print(resp, file=sys.stdout)
        elif str(sys.argv[1]) == "6":
            #Envio de mensaje
            mensaje = "Msj Prueba Garmin 001"
            resp = mensajes.sendTextMessageGarmin(mensaje, bus, usuario)
            print(resp, file=sys.stdout)
        elif str(sys.argv[1]) == "7":
            iduser = mensajes.getUserID()
            print(iduser)
            #for x in usuarios['result']:
            #    for y in x:
            #        print(str(y) + ' -q> ' + str(x[y]))
        elif str(sys.argv[1]) == '8':
            print(datetime.datetime.utcnow())
            MsjTxt = mns_Txt.getRegulaP(1, "Table_Position")
            print(MsjTxt)
            MsjTxt = mns_Txt.getAutobus(2, "Trama_TRX")
            print(MsjTxt)
            
    print(datetime.datetime.utcnow())
    print('-', ' >  E N D < ', '-', sep=('-')*38)
