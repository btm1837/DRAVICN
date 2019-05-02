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
        self.cell_list = []

        # Trip data parameters
        self.trip_data=pandas.read_csv('trips.csv')
        self.trip_set=set()
        self.trip_net_demand = {}

        # vehicle data parameters
        self.vehicle_data = pandas.read_csv('vehicles.csv')
        self.vehicle_list = []

        # Intersection Control Policy Parameters
        self.incoming_links = set()
        self.outgoing_links = set()
        self.list_conflict_regions = set()
        self.lists_cr_from_arci_to_arcj = {}
        self.intersections_set = set()
        self.intersection_incoming_links = {}
        self.intersection_outgoing_links = {}
        self.intersection_






        # experiment data parameters
        self.exper_data = pandas.read_csv('Experiments.csv')
        self.exper_experiment_list = set(self.exper_data['Experiment'])
        self.exper_num='NA'
        self.exper_coordination = 'NA'
        self.exper_coordination_period = 'NA'
        self.exper_demand_multiplier = 'NA'
        self.exper_cell_travel_time_calc = 'NA'
        self.exper_simulation_time_interval = 'NA'
        # Initialize to first experiment
        self.set_experiment_values(self,0)


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
            number_of_vehicles = (((item[1][2])/(3600) ) * self.exper_simulation_time_interval)* self.exper_demand_multiplier
            for trip in range(number_of_vehicles):
                temp = 'T' + str(trip)
                self.trip_set.add(temp)
                for node in self.node_set:
                    if item[1][0] == node:
                        self.trip_net_demand[item[1][0], temp] = -1
                    elif item[1][1] == node:
                        self.trip_net_demand[item[1][1], temp] = 1
                    else:
                        self.trip_net_demand[node,temp]=0
        return

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
        self.node_set = set(self.node_data['Node'])
        return
