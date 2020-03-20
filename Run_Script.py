
import time
import Optimization
import Data_Generator
import CTM_function
import ICP
import pandas as pd

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
    data.create_source_cells()
    data.create_and_update_vehicle_dict(routing_from_opt=optimization_model.optimal_routes)

    return data

# def test(data):
#     data.arc_file = 'jiberish'
#     return

def transaction_manager_sim_loop(simulation_time,data,df_vehicles,df_opt):
    # move some vehilces down roads
    CTM_function.ctm_function_t_i(data)

    #move some vehilces in intersections
    ICP.ICP(data)

    # setting new trip attributes
    data.tm_creating_trips_for_next_t(simulation_time=simulation_time)
    # getting new routing from opt
    optimization_model = Optimization.MinCostFlow(node_set=data.get_node_set(),
                                              trip_set=data.get_trip_set(),
                                              trip_net_demand=data.get_trip_net_demand(),
                                              arc_capacity=data.get_arc_capacity(),
                                              arc_cost=data.get_arc_cost(),
                                              arc_set=data.get_arc_set())
    # solve model
    optimization_model.solve()
    optimization_model.get_Var()

    # update vehicle routes
    data.create_and_update_vehicle_dict(routing_from_opt=optimization_model.optimal_routes)

    #sink logic and recording vehicle data
    data.sink_logic(df_vehicles=df_vehicles,
                    simulation_time=simulation_time)
    #record some data
    df_opt.append([simulation_time,optimization_model.i.OBJ()])
    return

def run_simulation():
    data = initialize_setup()
    columns_v = ['vehicle_id','origin','destination','initial_route','route_traveled','time_taken','time_out','time_in']
    columns_opt = ['simulation_time','cost']
    df_vehicles = pd.DataFrame(columns=columns_v)
    df_opt = pd.DataFrame(columns=columns_opt)
    for simulation_time in range(0,data.exper_total_sim_time,data.exper_simulation_time_interval):
        transaction_manager_sim_loop(simulation_time=simulation_time,
                                     data= data,
                                     df_vehicles=df_vehicles,
                                     df_opt=df_opt)
    return df_vehicles,df_opt


# data = initialize_setup()
run_simulation()
end_time = time.time()
print("--- runtime = %s seconds ---" %(end_time - start_time))

