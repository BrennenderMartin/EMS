from peewee import (
    SqliteDatabase,
    DateField,
    IntegerField,
    FloatField,
    Model,
)

#! ToDo: Add env value for that
db = SqliteDatabase("./src/EMS/data/database.db")

class BaseModel(Model):
    class Meta:
        database = db

class WeatherData(BaseModel):
    entry = IntegerField(primary_key=True)
    timestamp = DateField(formats=["%Y-%m"]) # year + month
    # DATA FIELDS
    tAvg = FloatField() # average temp (in C°)
    sSum = FloatField() # sum of sun-hours
    wAvg = FloatField() # average wind speed (km/h)

class OilData(BaseModel):
    entry = IntegerField(primary_key=True)
    timestamp = DateField(formats=["%Y-%m"]) # year + month
    # DATA FIELDS
    pUSD = FloatField() # price in USD


def build() -> SqliteDatabase:
    db.connect()
    db.create_tables([WeatherData, OilData])

    return db