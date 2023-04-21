from enum import IntEnum,auto

class experiment_enum(IntEnum):
    Experiment_number = 0
    coordination_flag = auto()
    coordination_period = auto()
    demand_multiplier =auto()
    cell_travel_time_calc_flag = auto()
    simulation_time_interval = auto()
    total_simulation_time = auto()
    vehicle_length = auto()
    trials = auto()