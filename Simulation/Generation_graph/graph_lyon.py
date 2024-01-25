import pandas as pd
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Define the function to create a directed graph from two CSV files
def create_directed_graph(nodes_filepath, edges_filepath):
    # Read the CSV files
    nodes_df = pd.read_csv(nodes_filepath)
    edges_df = pd.read_csv(edges_filepath)
    
    # Replace 'default' with 50 in the 'speed' column
    edges_df['speed'] = edges_df['speed'].replace('default', 50)

    # Convert 'speed' column to numeric type
    edges_df['speed'] = pd.to_numeric(edges_df['speed'], errors='coerce')

    # Initialize a directed graph
    G = nx.DiGraph()
    
    # Add nodes with their positions
    for index, row in nodes_df.iterrows():
        G.add_node(row['node_id'], pos=(row['lon'], row['lat']))
    
    # Add edges with weights (time to travel)
    for index, row in edges_df.iterrows():
        node_start = row['node_id1']
        node_end = row['node_id2']
        if node_start in G and node_end in G:  # Check if nodes exist
            # Calculate the distance using geopy
            distance = geodesic(G.nodes[node_start]['pos'], G.nodes[node_end]['pos']).kilometers
            # Calculate the travel time in hours
            travel_time = distance / (row['speed'] / 60)  # speed is given in km/h
            # Add edge for oneway
            G.add_edge(node_start, node_end, weight=travel_time)
            # If twoway, add edge in the opposite direction as well
            if row['type'] == 'twoway':
                G.add_edge(node_end, node_start, weight=travel_time)
    
    return G

# File paths for the CSV files within the 'graph_LYON' folder
nodes_filepath = 'graph_LYON/Node_list.csv'
edges_filepath = 'graph_LYON/Edge_list.csv'

# Create the graph from the CSV files
G = create_directed_graph(nodes_filepath, edges_filepath)

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='black')
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
plt.show()
