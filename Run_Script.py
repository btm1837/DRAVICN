
import time
import Optimization
import Data_Generator
import CTM_function
import ICP
import pandas as pd
import os
#graphing tools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt




# Initializing the model
def initialize_setup(run_id,path,arc_file,trip_file,experiment_file,vehicle_file):
    # run_id = 'setup_1'
    # base_path = r'D:\Documents\Thesis_Docs\experiment_files'
    # arc_file = 'arcs_'+ run_id+'.csv'
    # trip_file = 'source_sink_' + run_id + '.csv'
    # experiment_file = r"Experiments.csv"
    # vehicle_file = r"vehicles.csv"

    path = os.path.join(path,run_id)


    # arc_file = 'arcs.csv'
    # arc_file = r'arcs_set3.csv'
    # node_file = r'nodes.csv'
    # trip_file = r'source_sink.csv'
    # vehicle_file = r"vehicles.csv"
    # cell_file = r"cells.csv"
    # experiment_file = r"Experiments.csv"
    # cell_iteration_dict_file = r"cell_iteration_list.csv"

    simulation_time = 0
    data = Data_Generator.simulation(arc_file=arc_file,
                                     trip_file=trip_file,
                                     vehicle_file=vehicle_file,
                                     experiment_file=experiment_file,
                                     path=path)

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


def transaction_manager_sim_loop(simulation_time,data):
    # move some vehilces down roads
    CTM_function.ctm_function_t_i_homogenous(data=data,
                                  simulation_time=simulation_time)

    # Set number of vehicles in cells for ICP and post CTM operations
    data.transaction_manager_post_CTM_before_ICP()

    #move some vehilces in intersections
    ICP.ICP(data=data,
            simulation_time=simulation_time)

    # TM adjustments after CTM & ICP before Opt :
    data.transaction_manager_post_vehicle_move(simulation_time=simulation_time)
    # getting new routing from Opt :
    optimization_model = Optimization.MinCostFlow(node_set=data.get_node_set(),
                                              trip_set=data.get_trip_set(),
                                              trip_net_demand=data.get_trip_net_demand(),
                                              arc_capacity=data.get_arc_capacity(),
                                              arc_cost=data.get_arc_cost(),
                                              arc_set=data.get_arc_set())
    # solve model
    print('\n\n---------------------------')
    opt_time_start = time.time()
    print(f'optimization start time: {opt_time_start}')
    optimization_model.solve()
    opt_time_end = time.time()
    print(f'optimization end time: {opt_time_end}')
    print(f'optimization solve time: {opt_time_start-opt_time_end}')

    print('Cost: ', optimization_model.i.OBJ())
    optimization_model.get_Var()

    # record some data
    opt_list = [simulation_time,optimization_model.i.OBJ()]
    temp = pd.DataFrame([opt_list],columns=data.columns_opt)
    data.df_opt = data.df_opt.append(temp)

    # TM adjustments after opt before CTM & ICP"
    #   -
    data.transaction_manager_post_opt(routing_from_opt=optimization_model.optimal_routes,
                                      simulation_time=simulation_time)

    return

def run_simulation(run_id,path,arc_file,trip_file,experiment_file,vehicle_file):
    data = initialize_setup(run_id,path,arc_file,trip_file,experiment_file,vehicle_file)
    stop_list = [(i * 10 * data.exper_simulation_time_interval) for i in range(10)]
    for simulation_time in range(int(30),int(data.exper_total_sim_time),int(data.exper_simulation_time_interval)):
        transaction_manager_sim_loop(simulation_time=simulation_time,
                                     data= data)
        print(f"simulation_time is :{simulation_time}")

        if simulation_time in stop_list:
            print('sim time: \t' + str(simulation_time))
            print(f'Number of vehicles: ')

    # path = r'D:\Documents\Thesis_Docs\experiment_files'
    data.df_vehicles.to_csv(os.path.join(path,'vehicle_OUTPUT.txt'),sep='\t')
    data.df_opt.to_csv(os.path.join(path, 'opt_OUTPUT.txt'), sep='\t')
    return data.df_vehicles,data.df_opt


# data = initialize_setup()
# run_simulation()


run_id = 'setup_2'
path = r'D:\Documents\Thesis_Docs\experiment_files'
# path = os.path.join(path, run_id)
arc_file = 'arcs_' + run_id + '.csv'
trip_file = 'source_sink_' + run_id + '.csv'
experiment_file = r"Experiments.csv"
vehicle_file = r"vehicles.csv"


start_time = time.time()
df_vehicles,df_opt = run_simulation(run_id,path,arc_file,trip_file,experiment_file,vehicle_file)
end_time = time.time()
print("--- runtime = %s seconds ---" %(end_time - start_time))


# #pass by ref verification
# def test1():
#     data =initialize_setup()
#     for i in range(10):
#         j = test2(data,i)
#     return j
#
# def test2(data,i):
#     data.exper_simulation_time_interval = str(data.exper_simulation_time_interval) + str(i)+'this'
#     j =  data.exper_simulation_time_interval
#     return j