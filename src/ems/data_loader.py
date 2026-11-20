from ems.database.crud import (
    add_oil_entry,
    add_weather_entry
)
from pandas import (
    DataFrame,
    read_csv,
    to_datetime
)
from datetime import datetime

from ems.data.data_config import (
    data_types,
    csv_field_config
)

class DataLoader:
    def __init__(self, start_date: datetime, end_date: datetime) -> None:
        self.start_date = start_date
        self.end_date = end_date

    def load_to_database(self) -> bool:
        extracted: dict[data_types, dict[datetime, dict[data_types, int | float]]] = dict()
        curr_date = self.start_date
        for (data_type, path), dataset in csv_field_config.items():
            for csv_dataset, field_data in dataset.items():
                data: DataFrame = read_csv(f"{path}/{csv_dataset}", sep=";")
                data[field_data[data_types.DATE]] = to_datetime(data[field_data[data_types.DATE]], format=r"%d.%m.%Y")

                sel_rows = data[
                    (data[field_data[data_types.DATE]].dt.month == curr_date.month) & (data[field_data[data_types.DATE]].dt.year == curr_date.year)
                ]
                if len(sel_rows) == 0: continue

                extracted[data_type][curr_date][data_types.WAVG] = sel_rows[field_data[data_types.WAVG]].mean()
                print(extracted)
        return True


if __name__ == "__main__":
    dataloader = DataLoader(start_date=datetime(year=2020, day=9, month=2), end_date=datetime(year=2020, day=9, month=2))
    dataloader.load_to_database()