
import pandas
import collections

class Cell:
    """
    Basic Format for what a cell in the model is comprised of

    Takes in Node and Arc Data and coverts to cell based discretized network

    Uses Method Move_Vehicles to move vehicles through cells

    Uses Setter methods to set various atributes, these are used in the Transaction Manager to update the cells values

    Uses Getter Methods to get various atribute values.

    """

    def __init__(self,cell_id,start_node,end_node,free_flow_speed,max_vehicles,cell_length,cell_travel_time):
        self.cell_id = cell_id
        #Cell ocupancy at in time period prior to CTM equaltions, initial
        # n_i(t0)
        self.number_in_t_i = 0

        #Number of vehicles in the cell after CTM equations, final
        # n_i(t1)
        self.number_in_t_f = 0

        # Number of vehicles entering cell from cell i-1 at time t
        # Y
        self.number_entering_cell_from_arc = {}

        #Queue of vehicles in the cell
        # left of queue is end of deque to add vehicles to left use  .appendleft(vehicle)
        # right end is the front to remove on right use a = .pop to get vehicle a
        self.cell_queue = collections.deque([])

        # uf , speed if vehicles are moving freely
        self.free_flow_speed =free_flow_speed
        self.max_vehicles = max_vehicles
        self.length = cell_length
        self.num_vehicle_types = 0
        self.start_node = start_node
        self.end_node = end_node
        self.num_lanes = 1

        # for transaction manager
        self.cell_travel_time = cell_travel_time
    # Getters Block
    def get__(self):
        # set something
        i = 0
    # Setters Block
    def set_(self):
        # do something
        i=0
    # Methods
