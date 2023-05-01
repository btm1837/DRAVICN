import networkx as nx
import pandas as pd
import os
import matplotlib.pyplot as plt

run_id = 'setup_3'
path = r'D:\Documents\Thesis_Docs\experiment_files'
path_out = os.path.join(path, run_id, 'outputs')
if not os.path.exists(path_out):
    os.mkdir(path_out)
# path = os.path.join(path, run_id)
arc_file = 'arcs_' + run_id + '.csv'
trip_file = 'source_sink_' + run_id + '.csv'
experiment_file = r"Experiments.csv"
vehicle_file = r"vehicles.csv"

data_df = pd.read_csv(os.path.join(path,run_id,arc_file),sep=',')



network_graph = nx.from_pandas_edgelist(data_df, 'Start', 'End', edge_attr='Free_Flow_Speed',
                                             create_using=nx.DiGraph)
pos = nx.kamada_kawai_layout(network_graph)
nx.draw(network_graph, pos=pos, with_labels=True, node_size=200, alpha=0.3, arrows=True)
# nx.draw_networkx_edge_labels(network_graph, pos, edge_labels=arc_cost, label_pos=0.3, font_size=7)
# nx.draw_networkx_edge_labels(network_graph, pos,edge_labels=arc_set, label_pos=0.3, font_size=7)
ax = plt.gca()
ax.set_ylim(-1,1)
ax.set_xlim(-1, 1)
