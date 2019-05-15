

import Optimization


# Initializing the model
arc_file = 'arcs.csv'
node_file = 'nodes.csv'
trip_opt_table_pandas = 'trips_opt_table.csv'

optimization_model = Optimization.MinCostFlow(node_file,arc_file,trip_opt_table_pandas)
optimization_model.solve()
print('\n\n---------------------------')
print('Cost: ', optimization_model.i.OBJ())
optimization_model.get_Var()
