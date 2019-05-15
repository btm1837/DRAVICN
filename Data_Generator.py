import pandas
import numpy as np


class Data:
    """
    Takes Experimental set up intput values and creates attributes to be used by the models for initial values


    """
    def __init__(self):
        """ create values based on input parameters"""
        # node set
        self.node_set = set()

        # arc data parameters
        self.arc_data = pandas.read_csv('arcs.csv')
        self.arc_capacity={}
        self.arc_cost={}
        self.arc_set=set()

        # initiate the cell list
        self.cell_dict = []

        # Trip data parameters
        self.trip_data=pandas.read_csv('trips.csv')
        self.trip_set=set()
        self.trip_net_demand = {}
        self.trip_vehicle_type = {}
        self.total_initial_trips= 0
        self.total_current_trips=0

        # vehicle data parameters
        self.vehicle_data = pandas.read_csv('vehicles.csv')
        self.initial_vehicle_routes = set()
        self.vehicle_dict = {}
        self.vehicle_type_dictionary={}
        self.set_vehicle_type_dictionary()

        # Intersection Control Policy Parameters
        self.incoming_cells = set()
        self.outgoing_cells = set()
        self.list_conflict_regions = set(['cr1', 'cr2', 'cr3', 'cr4'])
        self.intersections_set = set()
        self.intersection_data_file = pandas.read_csv('Intersection.csv')
        self.intersection_data_dictionary = {}
        # Dictionary that describes the cr corresponding to an incoming or outgoing arc
        self.cr_for_arc_i = {}
        # Subset of CRs for incoming link i to out going link j
        self.cr_subset_from_i_to_j = {}
        # Conflict Region Capacity
        self.cr_capacity = {}
        # Capacity of turning movement
        self.turning_movement_capacity = {}
        # Equivialent flow entering conflict region
        self.cr_equivalent_flow = {}


        # experiment data parameters
        self.exper_data = pandas.read_csv('Experiments.csv')
        self.exper_experiment_list = set(self.exper_data['Experiment'])
        self.exper_num='NA'
        self.exper_coordination = 'NA'
        self.exper_coordination_period = 0
        self.exper_demand_multiplier = 0
        self.exper_cell_travel_time_calc = 'NA'
        self.exper_simulation_time_interval = 0
        # Initialize to first experiment
        self.set_experiment_values(0)

    def set_experiment_values(self,experiment_number):
        if experiment_number in self.exper_experiment_list:
            self.exper_num = self.exper_data.iloc[experiment_number][0]
            self.exper_coordination = self.exper_data.iloc[experiment_number][1]
            self.exper_coordination_period = self.exper_data.iloc[experiment_number][2]
            self.exper_demand_multiplier = self.exper_data.iloc[experiment_number][3]
            self.exper_cell_travel_time_calc = self.exper_data.iloc[experiment_number][4]
            self.exper_simulation_time_interval = self.exper_data.iloc[experiment_number][5]
        self.create_data_for_experiment()
        return

    def create_data_for_experiment(self):
        self.set_node_set_from_pandas()
        self.set_arc_attributes_from_pandas()
        self.set_trip_attributes_initial()
        return

    def set_trip_attributes_initial(self):
        """
        Uses the pandas object created by pandas.read_csv('trips_opt_table.csv') to populate:
        self.trip_net_demand
        self.trip_set
        :return:
        """
        #Need to iterate over vehicles in trip set or make vehicle ids here
        # vehicle ID needs to be the same as trip ID
        for item in self.trip_data.iterrows():
            #calculate the number of vehicles assigned to a given trip
            number_of_vehicles = (((item[1][2])/(3600.0) ) * self.exper_simulation_time_interval)* self.exper_demand_multiplier
            for trip in range(int(number_of_vehicles)):
                # Creating the Trip optimization matrix
                temp = 'T' + str(trip)
                self.trip_set.add(temp)
                self.trip_vehicle_type[temp] = item[1][3]
                for node in self.node_set:
                    if item[1][0] == node:
                        # A demand node on the trip
                        self.trip_net_demand[item[1][0], temp] = -1
                    elif item[1][1] == node:
                        # A supply node on the trip
                        self.trip_net_demand[item[1][1], temp] = 1
                    else:
                        # all other nodes on the trip matrix
                        self.trip_net_demand[node,temp]=0
            self.total_initial_trips = trip
            self.total_current_trips = self.total_initial_trips+1
        return

######################################################################
    def set_new_trip_attributes(self):
        """
        This function is to avoid iterating excessivley

        it relies on the self.trip_net_demand unchanging

        MIGHT NOT BE NEEDED
        :return:
        """
        for trip in range(self.total_current_trips,self.total_current_trips+self.total_initial_trips):
            temp = 'T' + str(trip)
            #add new trips to trip_set
            self.trip_set.add(temp)
            #number equivalent to this initial trip generated
            trip_equivalent = trip-self.total_current_trips + 1
            temp2 = 'T' + str(trip_equivalent)
            self.trip_vehicle_type[temp] = self.trip_vehicle_type[temp2]
            for node in self.node_set:
                self.trip_net_demand[node,temp] = self.trip_net_demand[node,temp2]

        self.total_current_trips = trip
######################################################################################

    def set_arc_attributes_from_pandas(self):
        """
        Uses the pandas object created by pandas.read_csv('arcs.csv') to populate:
        self.arc_capacity
        self.arc_cost
        self.arc_set

        :return:
        """
        for item in self.arc_data.iterrows():
            self.arc_capacity[item[1][0],item[1][1]]=item[1][3]
            self.arc_cost[item[1][0],item[1][1]]=item[1][2]
            self.arc_set.add((item[1][0],item[1][1]))
        return

    def set_node_set_from_pandas(self):
        """
        Uses the pandas object created by pandas.read_csv('arcs.csv') to populate:
        self.node_set
        :return:
        """
        self.node_set = set(self.arc_data['Start'])
        return

    def set_vehicle_type_dictionary(self):
        """
        Creates a dictionary for all vehicle type attributes based on manufacterer/type

        :return:
        """
        for item in self.vehicle_data.iterrows():
            self.vehicle_type_dictionary[item[1][0]]=(item[1][1],item[1][2])
        return

    def create_initial_vehicle_list(self):
        """
        Creates the initial list of a all vehicles on the network and makes them objects with propper data

        :return:
        """


    def initial_routing(self,routing_from_opt):
        """
        Sets the intitial routing of vehicles from the optimization variable data
        :param routing_from_opt:
        :return:
        """
        self.vehicle_routes = {}
        self.vehicle_list = []
        for trip in self.trip_set:
            #add vehicles to vehicle list
            self.vehicle_routes[trip]=set()
            for arc in self.arc_set:
                #define arcs on the trip's optimal path
                if (arc[0],arc[1],trip) in routing_from_opt:
                    self.vehicle_routes[trip].add(arc)
        return

    def intitial_routing_new_trips(self,new_trip_set,routing_from_opt):
        """
        For formating the routing of new trips that are added to the simulation

        :param new_trip_set:
        :param routing_from_opt:
        :return:
        """
        for trip in new_trip_set:
            # create set for iteration and adding
            self.vehicle_routes[trip]=set()
            for arc in self.arc_set:
                # define arcs on the trip's optimal path
                if (arc[0],arc[1],trip) in routing_from_opt:
                    self.vehicle_routes[trip].add(arc)
        return

# Setting intersection data sets to correct values
    def set_intersection_data_dictionary(self):
        for item in self.intersection_data_file.iterrows():
            self.intersection_data_dictionary[item[1][0]]=(item[1][1],item[1][2],item[1][3],item[1][4],\
                                                           item[1][5],item[1][6],item[1][7],item[1][8])
        return