from app-sae-15-almacenamiento-cliente import Tablas, init_db, end_db

#iniciar sesión base de datos
init_db()

#constructor
autobus1 = Tablas.Autobus(DESCRIPTION= 'ejemplo constructor', ACTIVE= 1)

#constructor con diccionario
d = {
    'DESCRIPTION': 'ejemplo diccionario',
    'ACTIVE': 1
    }
autobus2 = Tablas.Autobus(**d)

#insertar objerto
autobus1.add()
autobus2.add()

#crear objeto e insertarlo en la base de datos
d={
    'DESCRIPTION': 'ejemplo insercion',
    'ACTIVE': 1
}
autobus3 = Tablas.Autobus.insert(d)

#recuperar un objeto de la base de datos (SELECT TOP(1) FROM ... WHERE ...)
d={
    'DESCRIPTION': 'ejemplo insercion',
}
autobus = Tablas.Autobus.query_one(d)
print(autobus)

#recuperar lista de objetos (SELECT * FROM ... WHERE ...)
d={
    'DESCRIPTION': 'ejemplo actualizar1'
}
query = Tablas.Autobus.query_all(d)
if(query):
    for autobus in query:
        print(autobus)


#borar un objeto mapeado
autobus3.delete()

#borrar un registo que no está mapeado
d={
    'DESCRIPTION': 'ejemplo actualizar1',
}
autobus = Tablas.Autobus.extract(d)

#actualizar un objeto afectando sus atributos
autobus1.DESCRIPTION = 'ejemplo actualizar1'
autobus1.ACTIVE       = 0
Tablas.update()

#actualizar un objeto desde un diccionario
d={
    'DESCRIPTION': 'ejemplo actualizar2',
    'ACTIVE': 1
}
autobus2.update(d)

#insertar varios registros
l = (
    {
        'PK_ID'                 : 1,
        'AUTOBUS'               : 'prueba1',
        'LATITUD'               : 1.0,
        'LONGITUD'              : 1.0,           
        'FECHA_ACTUALIZACION'   : '2020-05-08 15:10:04.967',
        'FECHA_REGISTRO_GEOTAB' : '2020-05-08 15:10:04.967',
        'VERSION'               : 1,
        'DISTANCIA'             : 4.1,
        'VELOCIDAD'             : 1.2,
        'FECHA_REPLICA'         : '2020-05-08 15:10:04.967',
    },

    {
        'PK_ID'                 : 2,
        'AUTOBUS'               : 'prueba1',
        'LATITUD'               : 1.0,
        'LONGITUD'              : 1.0,           
        'FECHA_ACTUALIZACION'   : '2020-05-08 15:10:04.967',
        'FECHA_REGISTRO_GEOTAB' : '2020-05-08 15:10:04.967',
        'VERSION'               : 1,
        'DISTANCIA'             : 4.1,
        'VELOCIDAD'             : 1.2,
        'FECHA_REPLICA'         : '2020-05-08 15:10:04.967',
    },

    {
        'PK_ID'                 : 3,
        'AUTOBUS'               : 'prueba1',
        'LATITUD'               : 1.0,
        'LONGITUD'              : 1.0,           
        'FECHA_ACTUALIZACION'   : '2020-05-08 15:10:04.967',
        'FECHA_REGISTRO_GEOTAB' : '2020-05-08 15:10:04.967',
        'VERSION'               : 1,
        'DISTANCIA'             : 4.1,
        'VELOCIDAD'             : 1.2,
        'FECHA_REPLICA'         : '2020-05-08 15:10:04.967',
    }
)

geo = Tablas.Hst_Geotab_Logrecord.insert_many(l)


#finalizar sesión base de datos
end_db()