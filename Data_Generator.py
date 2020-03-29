import pandas
import numpy as np
import Cell_Class
import Vehicles_Class
import Intersections_Class
import ICP
import CTM_function
import random

import networkx as nx
import matplotlib.pyplot as plt

class simulation():
    """
    Takes Experimental set up intput values and creates attributes to be used by the models for initial values


    """
    def __init__(self,arc_file,node_file,trip_file,vehicle_file,cell_file,experiment_file,cell_iteration_list_file):
        """ create values based on input parameters"""
        # node set
        self.node_set = set()

        # arc data parameters
        self.arc_data = pandas.read_csv(arc_file, sep=',')
        self.arc_capacity={}
        self.arc_cost={}
        self.arc_set=set()

        # initiate the cell list
        self.cell_dict = {}
        self.cell_iteration_pandas_data = pandas.read_csv(cell_iteration_list_file)
        self.cell_iteration_dict = {}

        # Trip data parameters
        self.trip_data=pandas.read_csv(trip_file)
        self.trip_set=set()
        self.trip_net_demand = {}
        self.trip_vehicle_type_origin_dest = {}
        self.trip_total_initial_trips= 0
        self.trip_total_current_trips=0
        #new trip parameters
        self.source_dict = {}
        self.sink_dict = {}


        # vehicle data parameters
        self.vehicle_data = pandas.read_csv(vehicle_file)
        self.initial_vehicle_routes = set()
        self.vehicle_dict = {}
        #vehicle types
        self.vehicle_type_dict={}
        self.set_vehicle_type_dict()
        self.vehicle_total_num_types = len(self.vehicle_type_dict)
        #vehicle type probabilities
        # self.vehicle_type_prob_dict = {}

        # Intersection Control Policy Parameters
        # self.incoming_cells = set()
        # self.outgoing_cells = set()
        # self.list_conflict_regions = {'cr1', 'cr2', 'cr3', 'cr4'}
        # self.intersections_set = set()
        # self.intersection_data_file = pandas.read_csv('Intersection.csv')

        # intersection dictionary
        self.intersection_dict = {}
        # self.intersection_data_dictionary = {}
        # # Dictionary that describes the cr corresponding to an incoming or outgoing arc
        # self.cr_for_arc_i = {}
        # # Subset of CRs for incoming link i to out going link j
        # self.cr_subset_from_i_to_j = {}
        # # Conflict Region Capacity
        # self.cr_capacity = {}
        # # Capacity of turning movement
        # self.turning_movement_capacity = {}
        # # Equivialent flow entering conflict region
        # self.cr_equivalent_flow = {}

        #Data recording structures
        self.columns_v = ['vehicle_id', 'origin', 'destination', 'initial_route', 'route_traveled', 'time_taken', 'time_out',
                     'time_in']
        self.columns_opt = ['simulation_time', 'cost']
        self.df_vehicles = pandas.DataFrame(columns=self.columns_v)
        self.df_opt = pandas.DataFrame(columns=self.columns_opt)

        # experiment data parameters
        self.exper_data = pandas.read_csv('Experiments.csv')
        self.exper_experiment_list = set(self.exper_data['Experiment'])
        self.exper_num='NA'
        self.exper_coordination = 'NA'
        self.exper_coordination_period = 0
        self.exper_demand_multiplier = 0
        self.exper_cell_travel_time_calc = 'NA'
        self.exper_simulation_time_interval = 0
        self.exper_total_sim_time = 0
        self.exper_vehicle_length = 0
        # Initialize to first experiment
        self.set_experiment_values(0)

        #graph network
        self.network_graph=0
        self.pos = 0
        self.arc_label ={}
        self.number_in_cell = {}

    def set_experiment_values(self,experiment_number):
        if experiment_number in self.exper_experiment_list:
            self.exper_num = self.exper_data.iloc[experiment_number][0]
            self.exper_coordination = self.exper_data.iloc[experiment_number][1]
            self.exper_coordination_period = self.exper_data.iloc[experiment_number][2]
            self.exper_demand_multiplier = self.exper_data.iloc[experiment_number][3]
            self.exper_cell_travel_time_calc = self.exper_data.iloc[experiment_number][4]
            self.exper_simulation_time_interval = self.exper_data.iloc[experiment_number][5]
            self.exper_total_sim_time = self.exper_data.iloc[experiment_number][6]
            self.exper_vehicle_length = self.exper_data.iloc[experiment_number][7]
        self.create_data_for_experiment()
        return

    def create_data_for_experiment(self):
        self.set_node_set_from_pandas()
        self.set_arc_attributes_from_pandas()
        self.set_trip_attributes_initial()
        self.create_cell_dict()
        self.set_intersection_from_arcs()
        self.set_global_cell_intersection_status()
        self.set_cell_iteration_dict()
        return

    def set_trip_attributes_initial(self):
        self.set_source_sink_dict()
        self.trip_check()
        self.create_trips(0)
        return

    def set_network_graph(self):
        # make graph object
        for arc in self.arc_cost:
            self.arc_label[arc] = 'tt'+str(self.arc_cost[arc]) +'_mv' +str(self.arc_capacity[arc])+'_nic'+str(self.number_in_cell[arc])

        self.network_graph = nx.from_pandas_edgelist(self.arc_data, 'Start', 'End',edge_attr='Cost',create_using=nx.DiGraph)
        # Make the graph position object
        self.pos = nx.spring_layout(self.network_graph)


        return


    def create_network_graph(self):
        nx.draw(self.network_graph, pos=self.pos,with_labels=True, node_size=1500, alpha=0.3, arrows=True)
        nx.draw_networkx_edge_labels(self.network_graph,self.pos,edge_labels=self.arc_label)
        return

    def set_source_sink_dict(self):
        """
        Uses the pandas object created by pandas.read_csv('trips_opt_table.csv') to populate:
        self.trip_net_demand
        self.trip_set
        :return:
        """
        for item in self.trip_data.iterrows():
            #temp variables for easy debugging
            Node = item[1][0]
            Type = item[1][1]
            Uniform_Flow_perHour = item[1][2]
            #using dictionaries for removeing vehicles and adding them
            # dictionary value is trips/sim time unit
            if Type=='source':
                self.source_dict[Node] = round( Uniform_Flow_perHour * (1/3600) * (self.exper_simulation_time_interval))
            #sink has touple format to know how many trips have been allocated during a sim unit
            elif Type=='sink':
                self.sink_dict[Node] = [round( Uniform_Flow_perHour * (1/3600) * (self.exper_simulation_time_interval)),0]
            else:
                print('###########################')
                print('fatal error in trips data')
                print(Node)
                print(Type)

        return
    # check source and sink to make sure net flow is zero
    def trip_check(self):
        source_sum = sum(self.source_dict.values())
        sink_sum = sum([item[0] for item in self.sink_dict.values()])

        if source_sum!=sink_sum:
            print('###########################')
            print('fatal error source sink are not network net 0')
            print ('source total')
            print(source_sum)
            print('sink total')
            print(sink_sum)
        return

    # need to initialize trips set
    def create_trips(self,simulation_time):
        # for uncoordinated runs only tell the optimzation to use new trips
        if self.exper_coordination == 0:
            self.trip_set = set()

        self.set_sink_capcity_to_zero()
        for source_node in self.source_dict:
            for i in range(0,int(self.source_dict[source_node])):
                sink_list = [node1 for node1 in self.sink_dict if self.sink_dict[node1][1] < self.sink_dict[node1][0]]
                sel_sink = random.choice(sink_list)
                trip_name = str(source_node) +'_to_' +str(sel_sink) +'_@t_' +str(simulation_time)+'_#'+str(i)
                self.trip_set.add(trip_name)
                #auto set all vehicle types to 1
                # need to set vehicle types according to source sink profile
                self.trip_vehicle_type_origin_dest[trip_name] = (0,source_node,sel_sink)
                self.sink_dict[sel_sink][1] = self.sink_dict[sel_sink][1] + 1

                #same net demand logic
                for node in self.node_set:
                    if source_node == node:
                        # A demand node on the trip
                        self.trip_net_demand[source_node, trip_name] = -1
                    elif sel_sink == node:
                        # A supply node on the trip
                        self.trip_net_demand[sel_sink, trip_name] = 1
                    else:
                        # all other nodes on the trip matrix
                        self.trip_net_demand[node,trip_name]=0
        self.set_sink_capcity_to_zero()
        return

    def set_sink_capcity_to_zero(self):
        for node in self.sink_dict:
            self.sink_dict[node][1] = 0
        return

    def set_moving_trip_net_demand_in_sim(self):
        for vehicle_id in self.vehicle_dict:
            vehicle = self.vehicle_dict[vehicle_id]
            last_node = vehicle.current_cell_location[0]
            current_node = vehicle.current_cell_location[1]
            self.trip_net_demand[last_node,vehicle_id] = 0
            self.trip_net_demand[current_node,vehicle_id] = -1
        return

    # setting the cost of traversing an arc in sim
    def set_moving_arc_cost(self):
        # need to clear cell_travel_time list after this
        for cell_key in self.cell_dict:
            cell = self.cell_dict[cell_key]
            travel_time = cell.get_and_set_cell_travel_time()
            self.arc_cost[cell.cell_id] = travel_time
            self.arc_data.loc[(self.arc_data['Start'] == 'start') & (self.arc_data['End'] == 'B'), 'Cost'] = travel_time
        return
    # def add_vehicles_to_sim(self):

    #creating the sink logic to remove vehcles from a cell
    def sink_logic(self,simulation_time):
        #clear the sink current capacities
        self.set_sink_capcity_to_zero()

        #make columns for output
        # make a list of vehicles leaving
        vehicle_leaving_list = []
        for vehicle_key in self.vehicle_dict:
            vehicle = self.vehicle_dict[vehicle_key]
            if vehicle.destination == vehicle.current_cell_location[1]:
                vehicle_leaving_list.append(vehicle_key)

        #remove vehicles from the simlation and take some data down while I do it
        for vehicle_key in vehicle_leaving_list:
            vehicle = self.vehicle_dict[vehicle_key]
            cell = self.cell_dict[vehicle.current_cell_location]
            node = cell.cell_id[1]
            if self.sink_dict[node][1] < self.sink_dict[node][0]:
                removed_v = cell.cell_queue.pop()
                #get data for output
                removed_v.time_out_sim = simulation_time
                time_taken = removed_v.time_out_sim - removed_v.time_in_sim
                list = [removed_v.vehicle_id,removed_v.origin,removed_v.destination,removed_v.initial_routing,
                        removed_v.route_traveled,time_taken,removed_v.time_out_sim,removed_v.time_in_sim]
                temp = pandas.DataFrame([list],columns=self.columns_v)
                self.df_vehicles= self.df_vehicles.append(temp)
                del self.vehicle_dict[vehicle_key]

                # if the experiement is with coordination tell the optimiation not to include this trip
                # otherwise in un-coordinated runs this trip is already removed from tripset
                if self.exper_coordination == 1:
                    self.trip_set.remove(removed_v.vehicle_id)

                self.sink_dict[node][1] = self.sink_dict[node][1] +1
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
        self.node_set = set(self.arc_data['Start'])
        return

    def set_vehicle_type_dict(self):
        """
        Creates a dictionary for all vehicle type attributes based on manufacterer/type
        key = vehicle make number
        values = (reaction time)
        :return:
        """
        for item in self.vehicle_data.iterrows():
            self.vehicle_type_dict[item[1][0]]=item[1][1]
        return

    def create_source_cells(self):
        for node in self.source_dict:
            for cell_key in self.cell_dict:
                if cell_key[0] == node:
                    cell = self.cell_dict[cell_key]
                    cell.make_source_cell()
                    self.arc_capacity[cell_key] = cell.max_vehicles
        return


    def create_and_update_vehicle_dict(self,routing_from_opt,simulation_time):
        """
        Sets the intitial routing of vehicles from the optimization variable data
        :param routing_from_opt:
        :return:
        """
        #self.vehicle_routes = {}
        for trip in self.trip_set:
            #add vehicles to vehicle list
            route = []
            #self.vehicle_routes[trip]=set()
            for arc in self.arc_set:
                #define arcs on the trip's optimal path
                if (arc[0],arc[1],trip) in routing_from_opt:
                    #self.vehicle_routes[trip].add(arc)
                    route.append(arc)
            if trip in self.vehicle_dict:
                self.vehicle_dict[trip].route = route
            else:
                self.vehicle_dict[trip] = Vehicles_Class.Vehicle(vehicle_ID=trip,
                                                                 make=self.trip_vehicle_type_origin_dest[trip][0],
                                                                 origin=self.trip_vehicle_type_origin_dest[trip][1],
                                                                 destination=self.trip_vehicle_type_origin_dest[trip][2],
                                                                 routing_arcs=route)
                #put vehicle in initial cell
                vehicle = self.vehicle_dict[trip]
                for cell_id in vehicle.route:
                    if cell_id[0] == vehicle.origin:
                        vehicle.current_cell_location = cell_id
                        vehicle.route_traveled.add(cell_id)
                        vehicle.cell_time_in = simulation_time
                        vehicle.time_in_sim = simulation_time
                        # update cell properties
                        cell = self.cell_dict[cell_id]
                        cell.number_in_t_i_make_dict[vehicle.make] = cell.number_in_t_i_make_dict[vehicle.make] + 1
                        cell.cell_queue.appendleft(vehicle)

        return


    def update_all_cells_number_in_cell(self):
        for cell_key in self.cell_dict:
            cell=self.cell_dict[cell_key]
            cell.get_number_in_t_i_and_make_dict_from_cell_queue()
            self.number_in_cell[cell_key] = cell.number_in_t_i
        return

    def update_ICP_cells_number_in_cell(self):
        for intersection_key in self.intersection_dict:
            intersection = self.intersection_dict[intersection_key]
            for outgoing_cell_id in intersection.outgoing_cells:
                outgoing_cell = self.cell_dict[outgoing_cell_id]
                outgoing_cell.get_number_in_t_i_and_make_dict_from_cell_queue()
            for incoming_cell_id in intersection.incoming_cells:
                incoming_cell = self.cell_dict[incoming_cell_id]
                incoming_cell.get_number_in_t_i_and_make_dict_from_cell_queue()
        return




    def set_intersection_from_arcs(self):
        # find if a node needs to become an intersection
        node_intersection_list = []
        for node in self.node_set:
            outgoing_cells=[]
            incoming_cells=[]
            for arc in self.arc_set:
                if node==arc[0]:
                    outgoing_cells.append(arc)
                if node==arc[1]:
                    incoming_cells.append(arc)
            if len(outgoing_cells)>2:
                node_intersection_list.append(node)
                self.intersection_dict[node] = Intersections_Class.Intersection(located_at_node=node)
                self.intersection_dict[node].set_incoming_cells(incoming_cells)
                self.intersection_dict[node].set_outgoing_cells(outgoing_cells)
                for arc in incoming_cells:
                    if self.cell_dict[arc].direction == 'E':
                        self.intersection_dict[node].set_cr_for_arc_i(arc,'SW')
                    elif self.cell_dict[arc].direction == 'W':
                        self.intersection_dict[node].set_cr_for_arc_i(arc,'NE')
                    elif self.cell_dict[arc].direction == 'S':
                        self.intersection_dict[node].set_cr_for_arc_i(arc, 'NW')
                    elif self.cell_dict[arc].direction == 'N':
                        self.intersection_dict[node].set_cr_for_arc_i(arc, 'SE')
                for arc in outgoing_cells:
                    if self.cell_dict[arc].direction == 'E':
                        self.intersection_dict[node].set_cr_for_arc_i(arc,'SE')
                    elif self.cell_dict[arc].direction == 'W':
                        self.intersection_dict[node].set_cr_for_arc_i(arc,'NW')
                    elif self.cell_dict[arc].direction == 'S':
                        self.intersection_dict[node].set_cr_for_arc_i(arc, 'SW')
                    elif self.cell_dict[arc].direction == 'N':
                        self.intersection_dict[node].set_cr_for_arc_i(arc, 'NE')
                self.intersection_dict[node].set_intitial_cr_subset_from_i_to_j()
        return

    def set_global_cell_intersection_status(self):
        for intersection_key in self.intersection_dict:
            intersection = self.intersection_dict[intersection_key]
            for cell_id in intersection.incoming_cells:
                cell = self.cell_dict[cell_id]
                cell.intersection_status = 'end_cell'
            for cell_id in intersection.outgoing_cells:
                cell = self.cell_dict[cell_id]
                cell.intersection_status = 'pre_start'
                start_node = cell.start_node
                end_node = cell.end_node
                if end_node=='start' or end_node =='end':
                    continue

                next_node = [next_node for (c_end_node, next_node) in self.arc_set if c_end_node == end_node and next_node != start_node][0]
                self.cell_dict[(end_node, next_node)].intersection_status = 'start_cell'
                self.cell_dict[(end_node, next_node)].prior_cell = cell.cell_id
        return


    def create_cell_dict(self):
        for item in self.arc_data.iterrows():
            cell_id = (item[1][0],item[1][1])
            self.cell_dict[cell_id] = Cell_Class.Cell(cell_id=cell_id,
                                                      start_node=item[1][0],
                                                      end_node=item[1][1],
                                                      free_flow_speed=item[1][5],
                                                      max_vehicles=item[1][3],
                                                      cell_length=item[1][4],
                                                      cell_travel_time=item[1][2],
                                                      direction=item[1][6])
            for make in self.vehicle_type_dict:
                self.cell_dict[cell_id].number_in_t_i_make_dict[make] = 0
            self.cell_dict[cell_id].cell_queue.clear()

        return

    # Recursive methods for obtaining the cell iteration dict for the cell transmission model to operate on
    def set_cell_iteration_dict(self):
        for cell_key in self.cell_dict:
            cell = self.cell_dict[cell_key]
            if cell.intersection_status=='start_cell':
                cell_iteration_list = []
                cell_iteration_list= self.set_iteration_list(cell,cell_iteration_list)
                self.cell_iteration_dict[cell_key]=cell_iteration_list
        return

    def set_iteration_list(self,cell,cell_iteration_list):
        cell_iteration_list.append(cell.cell_id)

        #get prior cell
        node2 = [prior_node for (prior_node,c_start_node) in self.arc_set if c_start_node == cell.start_node and prior_node != cell.end_node][0]
        cell.prior_cell = (node2, cell.start_node)

        if cell.intersection_status =='end_cell':
            return cell_iteration_list
        else:
            node = [next_node for (c_end_node, next_node) in self.arc_set if c_end_node == cell.end_node and next_node != cell.start_node][0]
            cell.next_cell = (cell.end_node,node)
            return self.set_iteration_list(self.cell_dict[(cell.end_node,node)],cell_iteration_list)


#vehicles are now put in initial cells when created
    # def put_vehicles_in_initial_cells(self):
    #     #need to create vehicle dict prior to running this
    #     # puts vehicle in the correct cell corresponding to its origin node and vehicle route
    #
    #     for vehicle in self.vehicle_dict.keys():
    #         if vehicle.current_cell_location == "":
    #             for cell in vehicle.route:
    #                 if cell[0] == vehicle.origin:
    #                     vehicle.current_cell_location = cell
    #                     self.cell_dict[cell].cell_queue.appendleft(vehicle)
    #     return

    def transaction_manager_post_vehicle_move(self,simulation_time):
    # This is the main transaction manager proceedure
        # first create any new trips
        self.create_trips(simulation_time=simulation_time)
        #set the net demand for those trips
        self.set_moving_trip_net_demand_in_sim()

        #set the arc travel cost for those trips
        self.set_moving_arc_cost()

        #update outgoing_cells to be able to use CTM on next time around using cell queue
        self.update_ICP_cells_number_in_cell()

        # send some vehicles down the drain
        self.sink_logic(simulation_time=simulation_time)
        return

    def transaction_manager_post_opt(self,simulation_time,routing_from_opt):

        #updates vehicle routes, and creates and places new vehicles in cells
        self.create_and_update_vehicle_dict(routing_from_opt=routing_from_opt,
                                            simulation_time=simulation_time)
        #updates the number in each cell for CTM
        self.update_all_cells_number_in_cell()
        return

    def transaction_manager_post_CTM_before_ICP(self):
        # need to update the number in all cells before ICP so that it knows the number in incoming and outgoing cells
        # and so that the number is set for next iteration for all other cells
        #using cell queue
        self.update_all_cells_number_in_cell()

        #update the cr capacity, turning move capacity, and cell capacities for the ICP
        self.update_intersection_capacities()

        return


    def update_intersection_capacities(self):
        # for all intersections
        for interesection_id in self.intersection_dict:
            intersection_obj = self.intersection_dict[interesection_id]
            # for all incoming cells
            for outgoing_cell_id in intersection_obj.outgoing_cells:
                outgoing_cell_obj = self.cell_dict[outgoing_cell_id]
                # get/set cell capacity
                outgoing_cell_obj.get_cell_capacity()

            for incoming_cell_id in intersection_obj.incoming_cells:
                incoming_cell_obj = self.cell_dict[incoming_cell_id]
                # set cell capacity / get one
                incoming_cell_obj.get_cell_capacity()
                #for all outgoing cells
                for outgoing_cell_id in intersection_obj.outgoing_cells:
                    outgoing_cell_obj = self.cell_dict[outgoing_cell_id]
                    # get/set cell capacity
                    intersection_obj.turning_movement_capacity[incoming_cell_id, outgoing_cell_id] = min(incoming_cell_obj.cell_capacity,
                                                                                         outgoing_cell_obj.cell_capacity)

            intersection_obj.calc_all_cr_capacities()
            #set flows for this time period to zero
            intersection_obj.reset_cr_equivalent_flow()
        return



    ####### GETTER BLOCK

    def get_node_set(self):
        return self.node_set

    def get_arc_set(self):
        return self.arc_set

    def get_arc_cost(self):
        return self.arc_cost

    def get_arc_capacity(self):
        return self.arc_capacity

    def get_trip_set(self):
        return self.trip_set

    def get_trip_net_demand(self):
        return self.trip_net_demand
    def get_vehicle_dict(self,routing_from_opt):
        self.create_vehicle_dict(routing_from_opt=routing_from_opt)
        return self.vehicle_dict
    def get_cell_dict(self):
        return self.cell_dict
    def get_intersection_dict(self):
        return self.intersection_dict
    def get_cell_iteration_dict(self):
        return self.cell_iteration_dict