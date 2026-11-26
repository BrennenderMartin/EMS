from collections import defaultdict
from ems.database.crud import (
    add_oil_entry,
    add_weather_entry,
    get_oil_entry,
    get_weather_entry
)
from pandas import (
    DataFrame,
    read_csv,
    to_datetime,
    Series,
    to_numeric
)
from datetime import datetime
from dateutil.relativedelta import relativedelta

from ems.data.data_config import (
    data_types,
    csv_field_config,
    time_type
)

class DataLoader:
    def __init__(self, start_date: dict[time_type, int], end_date: dict[time_type, int]) -> None:
        self.start_date = start_date
        self.end_date = end_date

    def load_to_database(self) -> bool:
        print(f"{self.start_date[time_type.MONTH]}.{self.start_date[time_type.YEAR]} -> {self.end_date[time_type.MONTH]}.{self.end_date[time_type.YEAR]}", end=" ")
        curr_date = datetime(year=self.start_date[time_type.YEAR], month=self.start_date[time_type.MONTH], day=1)
        stats_count: int = 0
        while curr_date != datetime(year=self.end_date[time_type.YEAR], month=self.end_date[time_type.MONTH], day=1):
            extracted: dict[data_types, dict[datetime, dict[data_types, list[float]]]] = defaultdict(
                lambda: defaultdict(lambda: defaultdict(list))
            )
            for (data_type, path, time_format, sep), dataset in csv_field_config.items():
                for csv_dataset, field_data in dataset.items():
                    data: DataFrame = read_csv(f"{path}/{csv_dataset}", sep=sep)
                    data[field_data[data_types.DATE]] = to_datetime(data[field_data[data_types.DATE]], format=time_format)

                    sel_rows = data[
                        (data[field_data[data_types.DATE]].dt.month == curr_date.month) & (data[field_data[data_types.DATE]].dt.year == curr_date.year)
                    ]
                    if len(sel_rows) == 0: continue
                    stats_count += len(sel_rows)

                    match data_type:
                        case data_types.WEATHER_DATA:
                            for weather_data_type in [data_types.SSUM, data_types.TAVG, data_types.WAVG]:
                                extracted[data_type][curr_date][weather_data_type].append(round(to_numeric(sel_rows[field_data[weather_data_type]].str.replace(",", "."), errors="coerce").mean(), 2))
                        case data_types.OIL_DATA:
                            extracted[data_type][curr_date][data_types.PUSD].append(round(sel_rows[field_data[data_types.PUSD]].mean(), 2))

                        case _: pass

                match data_type:
                    case data_types.WEATHER_DATA:
                        add_weather_entry(
                            timestamp={time_type.YEAR: curr_date.year, time_type.MONTH: curr_date.month},
                            wAvg=round(Series(extracted[data_types.WEATHER_DATA][curr_date][data_types.WAVG]).mean(), 2),
                            tAvg=round(Series(extracted[data_types.WEATHER_DATA][curr_date][data_types.TAVG]).mean(), 2),
                            sSum=round(Series(extracted[data_types.WEATHER_DATA][curr_date][data_types.SSUM]).mean(), 2)
                        )
                    case data_types.OIL_DATA:
                        add_oil_entry(
                            timestamp={time_type.YEAR: curr_date.year, time_type.MONTH: curr_date.month},
                            pUSD=round(Series(extracted[data_types.OIL_DATA][curr_date][data_types.PUSD]).mean(), 2)
                        )
                    case _: pass

            curr_date = curr_date + relativedelta(months=1)
        print(f"finished with {stats_count} rows used")
        return True

    def get_data_for_date(self, date: dict[time_type, int]) -> dict[data_types, dict[data_types, float | None]]:
        oil_data, weather_data = get_oil_entry(date), get_weather_entry(date)
        return {
            data_types.OIL_DATA: {
                data_types.PUSD: oil_data.pUSD
            },
            data_types.WEATHER_DATA: {
                data_types.WAVG: weather_data.wAvg,
                data_types.TAVG: weather_data.tAvg,
                data_types.SSUM: weather_data.sSum
            }
        }


if __name__ == "__main__":
    dataloader = DataLoader(start_date={time_type.YEAR: 2015, time_type.MONTH: 1}, end_date={time_type.YEAR: 2024, time_type.MONTH: 12})
    dataloader.load_to_database()