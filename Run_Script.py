
import time
import Optimization
import Data_Generator
import CTM_function
import ICP
import pandas as pd
#graphing tools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

start_time = time.time()


# Initializing the model
def initialize_setup():
    # arc_file = 'arcs.csv'
    arc_file = r'arcs_set3.csv'
    node_file = r'nodes.csv'
    trip_file = r'source_sink.csv'
    vehicle_file = r"vehicles.csv"
    cell_file = r"cells.csv"
    experiment_file = r"Experiments.csv"
    cell_iteration_dict_file = r"cell_iteration_list.csv"
    simulation_time = 0

    data = Data_Generator.simulation(arc_file=arc_file,
                                     node_file=node_file,
                                     trip_file=trip_file,
                                     vehicle_file=vehicle_file,
                                     cell_file=cell_file,
                                     experiment_file=experiment_file,
                                     cell_iteration_list_file= cell_iteration_dict_file)
    #                            experiment_file=experiment_file)

    optimization_model = Optimization.MinCostFlow(node_set=data.get_node_set(),
                                                  trip_set=data.get_trip_set(),
                                                  trip_net_demand=data.get_trip_net_demand(),
                                                  arc_capacity=data.get_arc_capacity(),
                                                  arc_cost=data.get_arc_cost(),
                                                  arc_set=data.get_arc_set())

    optimization_model.solve()
    print('\n\n---------------------------')
    print('Cost: ', optimization_model.i.OBJ())
    optimization_model.get_Var()

    #record some data
    opt_list = [simulation_time,optimization_model.i.OBJ()]
    temp = pd.DataFrame([opt_list],columns=data.columns_opt)
    data.df_opt = data.df_opt.append(temp)

    data.create_source_cells()
    data.transaction_manager_post_opt(routing_from_opt=optimization_model.optimal_routes,
                                      simulation_time=simulation_time)

    return data

# def test(data):
#     data.arc_file = 'jiberish'
#     return

def transaction_manager_sim_loop(simulation_time,data):
    # move some vehilces down roads
    CTM_function.ctm_function_t_i(data=data,
                                  simulation_time=simulation_time)

    # Set number of vehicles in cells for ICP and post CTM operations
    data.transaction_manager_post_CTM_before_ICP()

    #move some vehilces in intersections
    ICP.ICP(data=data,
            simulation_time=simulation_time)

    # TM adjustments after CTM & ICP before Opt :
    #   -
    data.transaction_manager_post_vehicle_move(simulation_time=simulation_time)
    # getting new routing from opt
    optimization_model = Optimization.MinCostFlow(node_set=data.get_node_set(),
                                              trip_set=data.get_trip_set(),
                                              trip_net_demand=data.get_trip_net_demand(),
                                              arc_capacity=data.get_arc_capacity(),
                                              arc_cost=data.get_arc_cost(),
                                              arc_set=data.get_arc_set())
    # solve model
    optimization_model.solve()
    print('\n\n---------------------------')
    print('Cost: ', optimization_model.i.OBJ())
    optimization_model.get_Var()

    #record some data
    opt_list = [simulation_time,optimization_model.i.OBJ()]
    temp = pd.DataFrame([opt_list],columns=data.columns_opt)
    data.df_opt = data.df_opt.append(temp)

    # TM adjustments after opt before CTM & ICP"
    #   -
    data.transaction_manager_post_opt(routing_from_opt=optimization_model.optimal_routes,
                                      simulation_time=simulation_time)

    return

def run_simulation():
    data = initialize_setup()

    for simulation_time in range(int(30),int(data.exper_total_sim_time),int(data.exper_simulation_time_interval)):
        transaction_manager_sim_loop(simulation_time=simulation_time,
                                     data= data)
        print(simulation_time)

    return data.df_vehicles,data.df_opt


# data = initialize_setup()
# run_simulation()
df_vehicles,df_opt = run_simulation()
end_time = time.time()
print("--- runtime = %s seconds ---" %(end_time - start_time))


#pass by ref verification
def test1():
    data =initialize_setup()
    for i in range(10):
        j = test2(data,i)
    return j

def test2(data,i):
    data.exper_simulation_time_interval = str(data.exper_simulation_time_interval) + str(i)+'this'
    j =  data.exper_simulation_time_interval
    return j