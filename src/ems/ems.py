from ems.data_loader import DataLoader
from ems.simulation import Simulator

from ems.data.data_config import time_type

dataloader = DataLoader(
    start_date={time_type.YEAR: 2012, time_type.MONTH: 1},
    end_date={time_type.YEAR: 2024, time_type.MONTH: 12}
)
dataloader.load_to_database()
simulation = Simulator(dataloader_instance=dataloader)

print(simulation.curr_sim_date)
print(simulation.curr_data)