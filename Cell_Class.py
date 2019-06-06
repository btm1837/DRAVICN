
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

        #number in t initial of types m
        self.number_in_t_i_make_dict = {}

        #Number of vehicles in the cell after CTM equations, final
        # n_i(t1)
        self.number_in_t_f = 0
        #of type m in cell at end of t
        self.number_in_t_f_make_dict = {}

        # Number of vehicles entering cell from cell i-1 at time t
        # Yj
        #key (from arc) = (node,node)
        self.number_entering_cell_from_arc = {}

        #number entering cell from arc of type m
        # key (from arc, make)
        self.number_entering_cell_from_arc_make_dict = {}

        #Queue of vehicles in the cell
        self.cell_queue = collections.deque([])

        # uf , speed if vehicles are moving freely
        self.free_flow_speed =free_flow_speed
        self.max_vehicles = max_vehicles
        self.length = cell_length
        self.num_vehicle_types = 0
        self.start_node = start_node
        self.end_node = end_node
        self.num_lanes = 1

        # cell proceeding intersection
        self.is_before_intersection = bool

        # next cell
        self.next_cell = ''

        # for transaction manager
        self.cell_travel_time = cell_travel_time

        # desnity of type M
        self.cell_density_for_make = {}
        #total density of cells
        self.total_cell_density = 0

    # Getters Block
    def get__(self):
        # set something
        i = 0
    # Setters Block
    def set_(self):
        # do something
        i=0
    # Methods




    def get_vehicle_atributes_set(self):
        for vehicle in self.cell_queue:
            self.vehicle_make_dict[vehicle.make] = (vehicle.reaction_time,vehicle.length)
        return

    def set_initial_cell_density_for_make(self,vehicle_type_dict):
        for vehicle_type in vehicle_type_dict.keys():
            self.cell_density_for_make[vehicle_type]=(0,0)

    def calc_initial_cell_density_for_make(self):
        for vehicle in self.cell_queue:
            self.cell_density_for_make[vehicle.make] = (self.cell_density_for_make[vehicle.make][0]+1,
                                                        (self.cell_density_for_make[vehicle.make][0]+1)/self.length)
            self.total_cell_density

