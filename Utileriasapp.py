#REEMPLAZA DE UNA LISTA Y PPONE LA FECHAMAXIMA DE OTRA LISTA (SE CAMBIO PERO SE QUEDA EL CODIGO .. SI COSTO UN PEDITO)
def ReeplazaFechaViaje(listViajeTrecho,_listParainsertarViajes,ERPCOCORRIDAID):
    maxfecha = listViajeTrecho[-1].get('FECHA_HORA_PROGRAMADA_LLEGADA')
    for dicviajes in _listParainsertarViajes:
        if dicviajes.get('ERPCO_CORRIDA_ID') == str(ERPCOCORRIDAID):
            dicviajes['FECHA_HORA_PROGRAMADA_LLEGADA'] = maxfecha
    return _listParainsertarViajes



