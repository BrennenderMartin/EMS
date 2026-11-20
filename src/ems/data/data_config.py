from enum import Enum

class time_type(Enum):
    YEAR = "year"
    MONTH = "month"

class data_types(Enum):
    OIL_DATA = "oil_data"
    WEATHER_DATA = "weather_data"

    # STANDART TYPES
    DATE = "date"

    # FIELD TYPES
    TAVG = "tavg" # average temp
    SSUM = "ssum" # sun hours 
    WAVG = "wavg" # average wind
    PUSD = "pusd" # oil price in usd

# data_type, path -> csv filename, data field type, collum name
csv_field_config: dict[tuple[data_types, str], dict[str, dict[data_types, str]]] = {
    (data_types.WEATHER_DATA, "./src/ems/data/wetterdaten"): {
        "City_Wetter_2013.csv": { data_types.DATE: "Datum", data_types.TAVG: "Tmit", data_types.WAVG: "Rges", data_types.SSUM: "Sges"},
        "City_Wetter_2014.csv": { data_types.DATE: "Datum", data_types.TAVG: "Tmit", data_types.WAVG: "Rges", data_types.SSUM: "Sges"},
        "City_Wetter_2015.csv": { data_types.DATE: "Datum", data_types.TAVG: "Tmit", data_types.WAVG: "Rges", data_types.SSUM: "Sges"},
        "City_Wetter_2016.csv": { data_types.DATE: "Datum", data_types.TAVG: "Tmit", data_types.WAVG: "Rges", data_types.SSUM: "Sges"},
        "City_Wetter_2017.csv": { data_types.DATE: "Datum", data_types.TAVG: "Tmit", data_types.WAVG: "Rges", data_types.SSUM: "Sges"},
        "City_Wetter_2018.csv": { data_types.DATE: "Datum", data_types.TAVG: "Tmit", data_types.WAVG: "Rges", data_types.SSUM: "Sges"},
        "City_Wetter_2019.csv": { data_types.DATE: "Datum", data_types.TAVG: "Tmit", data_types.WAVG: "Rges", data_types.SSUM: "Sges"},
        "City_Wetter_2020.csv": { data_types.DATE: "Datum", data_types.TAVG: "Tmit", data_types.WAVG: "Rges", data_types.SSUM: "Sges"},
        "City_Wetter_2021.csv": { data_types.DATE: "Datum", data_types.TAVG: "Tmit", data_types.WAVG: "Rges", data_types.SSUM: "Sges"},
        "City_Wetter_2022.csv": { data_types.DATE: "Datum", data_types.TAVG: "Tmit", data_types.WAVG: "Rges", data_types.SSUM: "Sges"},
        "City_Wetter_2023.csv": { data_types.DATE: "Datum", data_types.TAVG: "Tmit", data_types.WAVG: "Rges", data_types.SSUM: "Sges"},
        "City_Wetter_2024.csv": { data_types.DATE: "Datum", data_types.TAVG: "Tmit", data_types.WAVG: "Rges", data_types.SSUM: "Sges"},
    }
}