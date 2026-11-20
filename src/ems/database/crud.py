from ems.database.struct import (
    build,
    OilData,
    WeatherData
)
from ems.data.data_config import (
    time_type
)

from datetime import datetime

db = build()

def add_weather_entry(timestamp: dict[time_type, int], tAvg: float, sSum: float, wAvg: float) -> WeatherData:
    return WeatherData.create( # type: ignore
        timestamp=datetime(year=timestamp[time_type.YEAR], month=timestamp[time_type.MONTH], day=1),
        entry=WeatherData.select().count() + 1, # type: ignore
        tAvg=tAvg,
        sSum=sSum,
        wAvg=wAvg
    )

def add_oil_entry(timestamp: dict[time_type, int], pUSD: float) -> OilData:
    return OilData.create( # type: ignore
        timestamp=datetime(year=timestamp[time_type.YEAR], month=timestamp[time_type.MONTH], day=1),
        entry=OilData.select().count() + 1, # type: ignore
        pUSD=pUSD
    )

def get_weather_entry(timestamp: dict[time_type, int]) -> WeatherData:
    return WeatherData.get( # type: ignore
        WeatherData.timestamp.year == timestamp[time_type.YEAR], # type:ignore
        WeatherData.timestamp.month == timestamp[time_type.MONTH] # type: ignore
    )

def get_oil_entry(timestamp: dict[time_type, int]) -> OilData:
    return OilData.get( # type: ignore
        OilData.timestamp.year == timestamp[time_type.YEAR], # type: ignore
        OilData.timestamp.month == timestamp[time_type.MONTH] # type: ignore
    )


if __name__ == "__main__":
    add_weather_entry(timestamp={time_type.YEAR: 2026, time_type.MONTH: 5}, tAvg=5.2, sSum=6.3, wAvg=4.6)
    print(get_weather_entry(timestamp={time_type.YEAR: 2026, time_type.MONTH: 5}).wAvg)

