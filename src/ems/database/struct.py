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
    tAvg = FloatField(null=True) # average temp (in C°)
    sSum = FloatField(null=True) # sum of sun-hours
    wAvg = FloatField(null=True) # average wind speed (km/h)

class OilData(BaseModel):
    entry = IntegerField(primary_key=True)
    timestamp = DateField(formats=["%Y-%m"]) # year + month
    # DATA FIELDS
    pUSD = FloatField(null=True) # price in USD


def build() -> SqliteDatabase:
    db.connect()
    db.create_tables([WeatherData, OilData]) # type: ignore

    return db