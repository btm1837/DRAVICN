
import time
import Optimization
import Data_Generator

start_time = time.time()


# Initializing the model
arc_file = 'arcs.csv'
node_file = 'nodes.csv'
trip_file = 'trips.csv'
vehicle_file = "vehicles.csv"
cell_file = "cells.csv"
experiment_file = "Experiments.csv"

data = Data_Generator.Data(arc_file=arc_file,
                           node_file=node_file,
                           trip_file=trip_file,
                           vehicle_file=vehicle_file,
                           cell_file=cell_file,
                           experiment_file=experiment_file)

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
vehicle_dict = data.get_vehicle_dict(trip_opt_routes=optimization_model.optimal_routes)
cell_dict = data.get_cell_dict()



end_time = time.time()
print("--- runtime = %s seconds ---" %(end_time - start_time))

