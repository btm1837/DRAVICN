
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
def initialize_setup(run_id,path,arc_file,trip_file,df_experiment,vehicle_file,experiment_number):
    path = os.path.join(path,run_id)
    simulation_time = 0
    data = Data_Generator.simulation(arc_file=arc_file,
                                     trip_file=trip_file,
                                     vehicle_file=vehicle_file,
                                     df_experiment=df_experiment,
                                     path=path,
                                     experiment_number=experiment_number)


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


def get_experiment_data(path,experiment_file):
    experiment_file_path = os.path.join(path,experiment_file)
    exper_df = pd.read_csv(experiment_file_path)
    exper_experiment_list = list(exper_df['Experiment'])
    exper_experiment_set =set(exper_df['Experiment'])
    if len(exper_experiment_list) != exper_experiment_set:
        print("***\n*\nproblem in experiment setup file \n*\n***")
    return exper_df

            #     self.exper_num = self.exper_data.iloc[experiment_number][0]
            # self.exper_coordination = self.exper_data.iloc[experiment_number][1]
            # self.exper_coordination_period = self.exper_data.iloc[experiment_number][2]
            # self.exper_demand_multiplier = self.exper_data.iloc[experiment_number][3]
            # self.exper_cell_travel_time_calc = self.exper_data.iloc[experiment_number][4]
            # self.exper_simulation_time_interval = self.exper_data.iloc[experiment_number][5]
            # self.exper_total_sim_time = self.exper_data.iloc[experiment_number][6]
            # self.exper_vehicle_length = self.exper_data.iloc[experiment_number][7]
            # self.exper_trials_per_experiment = self.exper_data.iloc[experiment_number][8]


def run_simulation_experiments(run_id,path,path_out,arc_file,trip_file,experiment_file,vehicle_file):
    df_experiment = get_experiment_data(path,experiment_file)
    for row in df_experiment.iterrows():
        experiment_id = row[1][0]
        # coordinated experiment:
        run_simulation(run_id,path,path_out,arc_file,trip_file,df_experiment,vehicle_file,experiment_id)
        # uncoordinated experiment:
        run_simulation(run_id,path,path_out,arc_file,trip_file,df_experiment,vehicle_file,experiment_id)
    return

def run_simulation(run_id,path,path_out,arc_file,trip_file,df_experiment,vehicle_file,experiment_id):
    data = initialize_setup(run_id,path,arc_file,trip_file,df_experiment,vehicle_file,experiment_number=experiment_id)
    stop_list = [(i * 10 * data.exper_simulation_time_interval) for i in range(10)]
    for simulation_time in range(int(30),int(data.exper_total_sim_time),int(data.exper_simulation_time_interval)):
        transaction_manager_sim_loop(simulation_time=simulation_time,
                                     data= data)
        print(f"simulation_time is :{simulation_time}")

        if simulation_time in stop_list:
            print('sim time: \t' + str(simulation_time))
            print(f'Number of vehicles: ')

    # path = r'D:\Documents\Thesis_Docs\experiment_files'
    data.df_vehicles.to_csv(os.path.join(path_out,'experiment_'+experiment_id+'vehicle_OUTPUT.txt'),sep='\t')
    data.df_opt.to_csv(os.path.join(path_out,'experiment_'+experiment_id+ 'opt_OUTPUT.txt'), sep='\t')
    return 


# data = initialize_setup()
# run_simulation()
if __name__ =='__main__':

    path = r'D:\Documents\Thesis_Docs\experiment_files'
    set_up_file = r'set_up_2.yaml'
    # network and source/sinks file
    file_path = os.path.join(path,set_up_file)

    with open(file_path, 'r') as f:
        data_dict = yaml.load(f, Loader=yaml.CLoader)


    # run_id = 'setup_2'
    # path = r'D:\Documents\Thesis_Docs\experiment_files'
    # path_out = os.path.join(path,run_id+'_outputs')
    # if not os.path.exists(path_out):
    #     os.mkdir(path_out)
    # # path = os.path.join(path, run_id)
    # arc_file = 'arcs_' + run_id + '.csv'
    # trip_file = 'source_sink_' + run_id + '.csv'
    # experiment_file = r"Experiments.csv"
    # vehicle_file = r"vehicles.csv"



# start_time = time.time()
# df_vehicles,df_opt = run_simulation(run_id,path,arc_file,trip_file,experiment_file,vehicle_file)
# end_time = time.time()
# print("--- runtime = %s seconds ---" %(end_time - start_time))


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