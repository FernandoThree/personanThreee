from datetime import datetime, timedelta
from sqlalchemy import func, and_
from Almacenamiento import Tablas, Tablas_Erpco, db_session, Ejecutor

def Cargar_Datos():
    IDTABLAVIAJE = 0

    #Trae el ID en el que se quedó la tabla
    StrQuery = " select IDENT_CURRENT( 'Viaje' )  "
    result = db_session.execute(StrQuery)
    if result.returns_rows:
        for row in result:
            for value in row.values():
                IDTABLAVIAJE = int(value)
                break
            break

    #Creamos arreglo con join ERPCO_CORRIDA y ERPO_CORRIDA_TRAMO
    _listEC_ECT = db_session.query(
        Tablas_Erpco.ERPCO_CORRIDA.CORRIDA_ID,
        Tablas_Erpco.ERPCO_CORRIDA.ORIGEN_ID,
        Tablas_Erpco.ERPCO_CORRIDA.DESTINO_ID,
        Tablas_Erpco.ERPCO_CORRIDA.AUTOBUS_ID,
        Tablas_Erpco.ERPCO_CORRIDA_TRAMO.CONDUCTOR1_ID,
        Tablas_Erpco.ERPCO_CORRIDA.FECHORSAL,
        Tablas_Erpco.ERPCO_CORRIDA.FECHORLLE,
        Tablas_Erpco.SAE_RUTA_DETALLE.FK_RUTA_ID
    ).filter_by(
        CORRIDA_ID = Tablas_Erpco.ERPCO_CORRIDA_TRAMO.CORRIDA_ID,
        ORIGEN_ID  = Tablas_Erpco.SAE_RUTA_DETALLE.FK_ERPCO_PARADA_INICIO_ID,
        DESTINO_ID = Tablas_Erpco.SAE_RUTA_DETALLE.FK_ERPCO_PARADA_FIN_ID,
        AUTOBUS_ID = Tablas_Erpco.ERPCO_CORRIDA_TRAMO.AUTOBUS_ID
    ).distinct().all()
    #Carga datos de el BUS
    _list_Autobus = db_session.query(Tablas.Autobus).all()
    #Carga datos de los Conductores
    _list_Conductor = db_session.query(Tablas.Conductor).all()
    #Carga Datos de los viajes de SAE ya insertados
    sbqry = db_session.query(
        Tablas.Viaje.ERPCO_CORRIDA_ID, func.max(Tablas.Viaje.FECHA_ACTUALIZACION).label('FECHA_ACTUALIZACION')
    ).group_by(Tablas.Viaje.ERPCO_CORRIDA_ID).subquery()

    _list_ViajesSAE = Tablas.Viaje.query.join(sbqry, and_(
        Tablas.Viaje.ERPCO_CORRIDA_ID == sbqry.c.ERPCO_CORRIDA_ID, Tablas.Viaje.FECHA_ACTUALIZACION == sbqry.c.FECHA_ACTUALIZACION
    )).all()

    return  _listEC_ECT,_list_Autobus, _list_Conductor,_list_ViajesSAE, IDTABLAVIAJE
