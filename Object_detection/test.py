import matplotlib.pyplot as plt
import networkx as nx
import string
import random
import itertools

# Variables globales
number_of_nodes = 5
number_of_edges = 15
number_of_perturbations = 7
weight_of_perturbation = 3
minimum_of_weight = 1
maximum_of_weight = 3
simplified = True

def create_graph():
    """Creates and returns a directed graph with nodes labeled as alphabet letters and weighted edges."""
    G = nx.DiGraph()
    nodes = list(string.ascii_uppercase[:6])  # Letters from 'A' to 'W'
    G.add_nodes_from(nodes)

    edges = [
        ('A', 'B', {'weight': 2}),
        ('A', 'C', {'weight': 1}),
        ('C', 'D', {'weight': 1}),
        ('B', 'D', {'weight': 1}),
        ('D', 'E', {'weight': 1}),
        ('D', 'F', {'weight': 1}),
        ('E', 'G', {'weight': 2}),
        ('F', 'G', {'weight': 1}),
    ]

    G.add_edges_from(edges)
    return G

# create function that create a random graph
def create_random_graph(nodes, number_of_edges):
    rG = nx.DiGraph()
    rG.add_nodes_from(nodes)
    edges = set()
    while len(edges) < number_of_edges:
        source_node = random.choice(nodes)
        target_node = random.choice(nodes)
        # Ensure the target node is different from the source node
        while target_node == source_node:
            target_node = random.choice(nodes)
        # Add only the source and target nodes to the set to maintain uniqueness
        edge = (source_node, target_node)
        if edge not in edges:
            edges.add(edge)
            # Include the weight attribute when adding the edge to the graph
            rG.add_edge(source_node, target_node, weight=get_random_integer(minimum_of_weight, maximum_of_weight))
    
    return rG

# display the graph
def display_graph(G):
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='black', linewidths=1, font_size=15)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

# create function that create a list of nodes from an integer passed in parameters
def create_nodes(n):
    # Générer toutes les combinaisons possibles de lettres majuscules et minuscules
    all_combinations = list(itertools.product(string.ascii_uppercase, string.ascii_uppercase))
    # Limiter le nombre de combinaisons au nombre demandé 'n'
    limited_combinations = all_combinations[:n]
    # Convertir les tuples en chaînes de caractères
    nodes = [''.join(comb) for comb in limited_combinations]
    return nodes

# create a function that return a random value between a minimum and maximum value
def get_random_integer(min_value, max_value):
    return random.randint(min_value, max_value)

def find_shortest_path(G, source, target):
    """Finds and returns the shortest path between two nodes in the graph."""
    path = nx.dijkstra_path(G, source=source, target=target, weight='weight')
    return path

def display_size_and_path(path, source, target):
    path_length = sum(rg[u][v]['weight'] for u, v in zip(path, path[1:]))
    print(f"Shortest path from {source} to {target}: {' -> '.join(path)}")
    print(f"Length of path: {path_length}")

def add_perturbations(G, perturbed_edges):
    """Adds a consistent perturbation to the specified edges in the graph."""
    for edge in perturbed_edges:
        G[edge[0]][edge[1]]['weight'] += weight_of_perturbation
    return perturbed_edges

def draw_graph_with_dijkstra_path(G, path, perturbed_edges=None):
    """Draws the graph with the Dijkstra's shortest path and perturbed edges highlighted."""
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500,
            font_size=10, font_color='black', font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if perturbed_edges:
        nx.draw_networkx_edges(
            G, pos, edgelist=perturbed_edges, edge_color='red', width=2)

    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                           edge_color='green', width=2)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='lightgreen')

    plt.title("Graph with Dijkstra's Shortest Path and Perturbation")
    plt.show()

def display_path_info(G, source, target):
    """Calculates and displays the shortest path and its length."""
    try:
        path = nx.dijkstra_path(G, source, target, weight='weight')
        length = nx.shortest_path_length(G, source, target, weight='weight')
        if simplified:
            print(f"S4 : {length}")
        else:
            print(f"Shortest path from {source} to {target}: {' -> '.join(map(str, path))}")
            print(f"Length of path: {length}")
    except nx.NetworkXNoPath:
        print(f"No path found from {source} to {target}")

def simulation_with_post_perturbation(G, source, target, perturbed_edges):
    """Simulation where perturbations are applied to the weights of the edges of the initial shortest path."""
    # Find the shortest path before perturbations
    initial_path = find_shortest_path(G, source, target)
    # Apply perturbations
    add_perturbations(G, perturbed_edges)
    # Recalculate the length of the initial path with perturbed weights
    perturbed_length = sum(G[u][v]['weight'] for u, v in zip(initial_path, initial_path[1:]))
    if simplified:
        print(f"S1 : {perturbed_length}")
    else:
        print(f"Shortest path from {source} to {target}: {' -> '.join(initial_path)}")
        print(f"Length of path: {perturbed_length}")
    # Draw the graph highlighting the initial path and perturbed edges
    # draw_graph_with_dijkstra_path(G, initial_path, perturbed_edges)

def simulation_with_pre_perturbation(G, source, target, perturbed_edges):
    """Simulation where perturbations are applied before finding the shortest path."""
    # Apply perturbations before finding the path
    add_perturbations(G, perturbed_edges)
    # Find the shortest path
    path = find_shortest_path(G, source, target)
    # Display path info with perturbations considered
    display_path_info(G, source, target)
    # draw_graph_with_dijkstra_path(G, path, perturbed_edges)

def simulation_with_pre_perturbation_iterative(G, source, target, perturbed_edges):
    # Create a copy of the graph
    G_copy = G.copy()
    # Apply perturbations before finding the path
    add_perturbations(G, perturbed_edges)
    # Find the shortest path
    path = find_shortest_path(G_copy, source, target)
    # Iteratively adjust the path if a perturbed edge is encountered
    adjusted_path = []
    current_node = source
    perturbed_edge = source
    # print(path)
    while current_node != target:
        next_node = path[path.index(current_node) + 1]
        adjusted_path.append(current_node)
        # print('Voisins de ' + current_node + ' : ' + str(tuple(G_copy.neighbors(current_node))))
        # Check if any edge from the current node is perturbed
        perturbed = False
        for next_node in G_copy.neighbors(current_node):
            if (current_node, next_node) in perturbed_edges:
                perturbed = True
                perturbed_edge = next_node
                break
        if(perturbed):
            # print('perturbed edges connected to the node : ' + str(current_node) + ' with the node : ' + str(perturbed_edge))
            # add the perturbation on the copy
            G_copy[current_node][perturbed_edge]['weight'] = G[current_node][perturbed_edge]['weight']
            # on relance djikstra pour obtenir une liste
            path = find_shortest_path(G_copy, current_node, target)
        current_node = path[path.index(current_node) + 1]
    adjusted_path.append(current_node)
    # print('Adjusted path : ' + str(adjusted_path))
    adjusted_length = sum(G[u][v]['weight'] for u, v in zip(adjusted_path[:-1], adjusted_path[1:]))
    if simplified:
        print(f"S2 : {adjusted_length}")
    else:
        print(f"Shortest path from {source} to {target}: {' -> '.join(map(str, adjusted_path))}")
        print(f"Length of path: {adjusted_length}")
    # Draw the graph highlighting the adjusted path and perturbed edges
    # draw_graph_with_dijkstra_path(G, adjusted_path, perturbed_edges)

def simulation_with_selective_perturbation(G, source, target, perturbed_edges, max_distance=6):
    """Simulation where the shortest path is adjusted only if the perturbed edge's node is more than max_distance away."""
    # Apply perturbations
    add_perturbations(G, perturbed_edges)
    # Find the initial shortest path
    initial_path = find_shortest_path(G, source, target)
    # Adjust the path based on perturbations and distance constraint
    adjusted_path = [source]
    current_node = source
    for next_node in initial_path[1:]:
        if (current_node, next_node) in perturbed_edges:
            # Recalculate shortest path from current_node to next_node
            sub_path = find_shortest_path(G, current_node, next_node)
            adjusted_path.extend(sub_path[1:])  # Exclude the first node to avoid duplication
        else:
            adjusted_path.append(next_node)
        current_node = next_node
    # Calculate and display the length of the adjusted path
    adjusted_length = sum(G[u][v]['weight']
                          for u, v in zip(adjusted_path, adjusted_path[1:]))
    print(
        f"Selective path from {source} to {target}: {' -> '.join(adjusted_path)}")
    print(f"Length of path: {adjusted_length}")
    # Draw the graph
    draw_graph_with_dijkstra_path(G, adjusted_path, perturbed_edges)

def runsim(num_perturbations):
    source = 'A'
    target = 'G'
    G = create_graph()
    # Randomly select edges to perturb
    all_edges = list(G.edges())
    # perturbed_edges = [('F','G')]
    perturbed_edges = random.sample(
        all_edges, min(num_perturbations, len(all_edges)))
    print(f"Simulation with the following perturbations: {perturbed_edges}")
    print("================================================")
    # Case 1: Simulation with post-perturbations
    print("Simulation with post-perturbations:")
    G_post = G.copy()
    simulation_with_post_perturbation(G_post, source, target, perturbed_edges)
    print("================================================")
    # Case 2: Simulation with pre-perturbation iterative
    print("Simulation with pre-perturbations iterative:")
    G_pre_iterative = G.copy()
    simulation_with_pre_perturbation_iterative(G_pre_iterative, source, target, perturbed_edges)
    print("================================================")
    # # Case 3: Simulation with selective perturbations
    # print("Simulation with selective perturbations:")
    # G_selective = G.copy()
    # simulation_with_selective_perturbation(G_selective, source, target, perturbed_edges)
    # print("================================================")
    # Case 4: Simulation with pre-perturbations
    print("Simulation with pre-perturbations:")
    G_pre = G.copy()
    simulation_with_pre_perturbation(G_pre, source, target, perturbed_edges)
    print("================================================")

if __name__ == "__main__":
    for i in range(20):
        # Parameters of the simulation
        # print("================================")
        # print("Number of nodes : " + str(number_of_nodes))
        # print("Number of edges : " + str(number_of_edges))
        # print("Number of perturbations : " + str(number_of_perturbations))
        # print("Weight of perturbation : " + str(weight_of_perturbation))
        # print("Weight of perturbation between " + str(minimum_of_weight) + " and " + str(maximum_of_weight))
        
        # Nodes Creation
        nodes = create_nodes(number_of_nodes)
        
        # Source and Target nodes
        source = nodes[0]
        target = nodes[-1]

        # Graph creation
        rg = create_random_graph(nodes, number_of_edges)
        
        # Perturbed edges creation
        all_edges = rg.edges(data=False)
        edges_list = list(all_edges)
        perturbed_edges = random.sample(edges_list, k=min(number_of_perturbations, len(edges_list)))
        print('Perturbed edges : ' + str(perturbed_edges))
        print("================================")
        if simplified != True:
            print("Simulation with no perturbations : ")
        # Find the shortest path with djikstra without perturbations
        path = find_shortest_path(rg, source, target)
        # Calculate and display the length of the path without perturbations
        if simplified:
            path_length = sum(rg[u][v]['weight'] for u, v in zip(path, path[1:]))
            print(f"S0 : {path_length}")
        else:
            display_size_and_path(path, source, target)
            print("================================")
        if simplified != True:
            print("Simulation with post perturbations : ")
        G_post = rg.copy()
        simulation_with_post_perturbation(G_post, source, target, perturbed_edges)
        if simplified != True:
            print("================================")
            print("Simulation with pre-perturbations iterative : ")
        G_pre_iterative = rg.copy()
        simulation_with_pre_perturbation_iterative(G_pre_iterative, source, target, perturbed_edges)
        if simplified != True:
            print("================================")
            print("Simulation with pre-perturbations : ")
        G_pre = rg.copy()
        simulation_with_pre_perturbation(G_pre, source, target, perturbed_edges)
        print("================================================")


    # display_graph(rg)
    # draw_graph_with_dijkstra_path(rg, path, perturbed_edges)
    # runsim(number_of_perturbations)