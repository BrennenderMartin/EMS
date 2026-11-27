from ems.data.data_config import time_type, data_types, simulation_types
from ems.data_loader import DataLoader

class Simulator:
    def __init__(self, dataloader_instance: DataLoader):
        self.dataloader = dataloader_instance
        self.curr_sim_date: dict[time_type, int] = self.dataloader.start_date
        self.db_data: dict[data_types, dict[data_types, float | None]] = self.dataloader.get_data_for_date(self.curr_sim_date)
        self.data: dict[simulation_types, float] = dict()

    def calc_solar_output(self, panels: int) -> float: 
        "Output in megawatt"
        if not self.db_data[data_types.WEATHER_DATA][data_types.SSUM]: return 0
        return panels * (0.291 * self.db_data[data_types.WEATHER_DATA][data_types.SSUM]) # type: ignore because check if data point is not none beforehand
