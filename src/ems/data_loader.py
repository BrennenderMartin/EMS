from collections import defaultdict
from ems.database.crud import (
    add_oil_entry,
    add_weather_entry
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
        curr_date = datetime(year=self.start_date[time_type.YEAR], month=self.start_date[time_type.MONTH], day=1)
        while curr_date != datetime(year=self.end_date[time_type.YEAR], month=self.end_date[time_type.MONTH], day=1):
            print(f"{curr_date.strftime("%d/%m/%Y")}", end=" ")
            extracted: dict[data_types, dict[datetime, dict[data_types, list[float]]]] = defaultdict(
                lambda: defaultdict(lambda: defaultdict(list))
            )
            stats_count: int = 0
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
                            extracted[data_type][curr_date][data_types.WAVG].append(round(to_numeric(sel_rows[field_data[data_types.WAVG]].str.replace(",", "."), errors="coerce").mean(), 2))
                            extracted[data_type][curr_date][data_types.SSUM].append(round(to_numeric(sel_rows[field_data[data_types.SSUM]].str.replace(",", "."), errors="coerce").mean(), 2))
                            extracted[data_type][curr_date][data_types.TAVG].append(round(to_numeric(sel_rows[field_data[data_types.TAVG]].str.replace(",", "."), errors="coerce").mean(), 2))
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

            print(f"-> {stats_count} rows used")

            curr_date = curr_date + relativedelta(months=1)
        return True


if __name__ == "__main__":
    dataloader = DataLoader(start_date={time_type.YEAR: 1900, time_type.MONTH: 1}, end_date={time_type.YEAR: 2026, time_type.MONTH: 12})
    dataloader.load_to_database()