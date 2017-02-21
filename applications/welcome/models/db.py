db = DAL("sqlite://storage.sqlite")

db.define_table('GardenInfo',
                Field('DateTime','datetime',requires=IS_DATETIME(format='%d/%m/%Y %H:%M:%S'),default=request.now),
                Field('SoilMoisture'),
                Field('AirHumidity'),
                Field('Temperature'),
                Field('RelayStatus', 'text'))
