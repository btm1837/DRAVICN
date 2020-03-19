
import time
import Optimization
import Data_Generator

start_time = time.time()


# Initializing the model
# arc_file = 'arcs.csv'
arc_file = r'arcs_set3.csv'
node_file = r'nodes.csv'
trip_file = r'trips.csv'
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
data.create_vehicle_dict(routing_from_opt=optimization_model.optimal_routes)




#master branch file
#cell_dict = data.get_cell_dict()
#intersection_dict = data.get_intersection_dict()
#cell_iteration_dict = data.get_cell_iteration_dict()



# Single Experiment loop
#for my_sim_time in range(0,3601,int(data.exper_simulation_time_interval)):
#    #run optimization model to get initial vehicle routing
#    optimization_model = Optimization.MinCostFlow(node_set=data.get_node_set(),
#                                                trip_set=data.get_trip_set(),
#                                                trip_net_demand=data.get_trip_net_demand(),
#                                                arc_capacity=data.get_arc_capacity(),
#                                                arc_cost=data.get_arc_cost(),
#                                                arc_set=data.get_arc_set())
#    optimization_model.solve()
#    print('\n\n---------------------------')
#    print('Cost: ', optimization_model.i.OBJ())

#    optimization_model.get_Var()

    # create initial vehicle dictionary list
#   vehicle_dict = data.get_vehicle_dict(routing_from_opt = optimization_model.optimal_routes)


end_time = time.time()
print("--- runtime = %s seconds ---" %(end_time - start_time))

