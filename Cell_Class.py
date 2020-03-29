import pandas
import collections
import numpy as np

class Cell:
    """
    Basic Format for what a cell in the model is comprised of

    Takes in Node and Arc Data and coverts to cell based discretized network

    Uses Method Move_Vehicles to move vehicles through cells

    Uses Setter methods to set various atributes, these are used in the Transaction Manager to update the cells values

    Uses Getter Methods to get various atribute values.

    """

    def __init__(self, cell_id, start_node, end_node, free_flow_speed, max_vehicles, cell_length, cell_travel_time,direction):
        # General cell identification attributes
        self.cell_id = cell_id
        self.direction = direction
        self.intersection_status =''

        # Cell ocupancy at in time period prior to CTM equaltions, initial
        # n_i(t0)
        self.number_in_t_i = 0

        # number in t initial of types m
        self.number_in_t_i_make_dict = {}


        # Number of vehicles in the cell after CTM equations, final
        # n_i(t1)
        self.number_in_t_f = 0
        # of type m in cell at end of t
        self.number_in_t_f_make_dict = {}

        # initialized and resest within the ICP
        # Number of vehicles entering cell from cell i-1 at time t
        # Yj
        # key (from arc) = (node,node)
        self.number_entering_cell_from_arc = {}
        self.number_entering_cell_from_arc_make_dict = {}


        # Queue of vehicles in the cell
        # left of queue is end of deque to add vehicles to left use  .appendleft(vehicle)
        # right end is the front to remove on right use a = .pop to get vehicle a
        self.cell_queue = collections.deque()

        # uf , speed if vehicles are moving freely
        self.free_flow_speed = free_flow_speed
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

        # prior cell
        self.prior_cell = ''

        # for transaction manager
        self.cell_travel_time = cell_travel_time

        # list of travel times through cell
        self.cell_travel_time_list = [cell_travel_time]

        # for ICP need cell capacity
        self.cell_capacity = 0

    # Getters Block
    def get__(self):
        # set something
        i = 0
    def set_status(self,status):
        self.intersection_status = status
        return

    # Setters Block
    def set_(self):
        # do something
        i = 0

    # Methods

    def get_vehicle_atributes_set(self):
        for vehicle in self.cell_queue:
            self.vehicle_make_dict[vehicle.make] = (vehicle.reaction_time, vehicle.length)
        return

    # def set_initial_cell_density_for_make(self, vehicle_type_dict):
    #     for vehicle_type in vehicle_type_dict.keys():
    #         self.cell_density_for_make[vehicle_type] = (0, 0)
    #
    # def calc_initial_cell_density_for_make(self):
    #     for vehicle in self.cell_queue:
    #         self.cell_density_for_make[vehicle.make] = (self.cell_density_for_make[vehicle.make][0] + 1,
    #                                                     (self.cell_density_for_make[vehicle.make][0] + 1) / self.length)
    #         self.total_cell_density
    #

    def get_number_in_t_i(self):
        self.number_in_t_i = 0
        for vehicle_type in self.number_in_t_i_make_dict:
            self.number_in_t_i = self.number_in_t_i + self.number_in_t_i_make_dict[vehicle_type]
        return

    def get_number_entering_cell_from_arc(self,cell_id):
        self.number_entering_cell_from_arc[cell_id] = 0
        for vehicle_type in self.number_in_t_i_make_dict:
            self.number_entering_cell_from_arc[cell_id] = self.number_entering_cell_from_arc[cell_id] + self.number_in_t_i_make_dict[vehicle_type]
        return

    def get_number_in_t_f(self):
        self.number_in_t_f = 0
        for vehicle_type in self.number_in_t_f_make_dict:
            self.number_in_t_i = self.number_in_t_f + self.number_in_t_f_make_dict[vehicle_type]
        return

    def get_number_in_t_i_and_make_dict_from_cell_queue(self):
        for make in self.number_in_t_i_make_dict:
            self.number_in_t_i_make_dict[make]=0
            if len(self.cell_queue) !=0:
                if self.cell_queue[0] == list():
                    self.cell_queue.clear()
            for vehicle in self.cell_queue:
                self.number_in_t_i_make_dict[vehicle.make] = self.number_in_t_i_make_dict[vehicle.make] + 1
            self.number_in_t_i = sum(self.number_in_t_i_make_dict.values())
        return



    # def set_number_in_t_f_make_dict(self:
    #     nu
    def get_receiving_flow(self):
        #gets the maximum amount of vehicles that could enter the cell
        # proceedure is now done before ICP for all cells
        # self.get_number_in_t_i()
        return self.max_vehicles - self.number_in_t_i

    def make_source_cell(self):
        #1 billion capacity to receive vehicles
        self.max_vehicles = 1000000000000
        return

    def get_and_set_cell_travel_time(self):
        self.cell_travel_time = round(np.average(self.cell_travel_time_list), 2)
        self.cell_travel_time_list = [self.cell_travel_time]
        return self.cell_travel_time

    def get_cell_capacity(self):
        #for ICP need cell capacities for the cr capacities and turning move capacities
        self.cell_capacity = max(self.max_vehicles - self.number_in_t_i,0)
        return self.cell_capacity

    # def put_vehicles_in_number_t_i_make_dict(self):
    #     for make in self.number_in_t_i_make_dict:
    #
    #
    #     for vehicle in self.cell_queue:
    #         if vehicle.make in self.number_in_t_i_make_dict:
    #
    #         for make in self.number_in_t_i_make_dict:



