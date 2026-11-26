from ems.data.data_config import time_type, data_types
from ems.data_loader import DataLoader

class Simulator:
    def __init__(self, dataloader_instance: DataLoader):
        self.dataloader = dataloader_instance
        self.curr_sim_date: dict[time_type, int] = self.dataloader.start_date
        self.curr_data: dict[data_types, dict[data_types, float | None]] = self.dataloader.get_data_for_date(self.curr_sim_date)
