import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Build a dataframe with your connections
# This time a pair can appear 2 times, in one side or in the other!
df = pd.DataFrame({'from': ['D', 'A', 'B', 'C', 'A'], 'to': ['A', 'D', 'A', 'E', 'C']})
df

# Build your graph. Note that we use the DiGraph function to create the graph!
G = nx.from_pandas_dataframe(df, 'from', 'to', create_using=nx.DiGraph())

# Make the graph
nx.draw(G, with_labels=True, node_size=1500, alpha=0.3, arrows=True)

& nbsp;

# ------- UNDIRECTED

# # Build a dataframe with your connections
# # This time a pair can appear 2 times, in one side or in the other!
# df = pd.DataFrame({'from': ['D', 'A', 'B', 'C', 'A'], 'to': ['A', 'D', 'A', 'E', 'C']})
# df
#
# # Build your graph. Note that we use the Graph function to create the graph!
# G = nx.from_pandas_dataframe(df, 'from', 'to', create_using=nx.Graph())
#
# # Make the graphnx.draw(G, with_labels=True, node_size=1500, alpha=0.3, arrows=True)
# plt.title("UN-Directed")

