import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import numpy as np

# Charger le fichier OSM
tree = ET.parse('map/map_molsheim.osm')
root = tree.getroot()

# Créer un graphe dirigé avec networkx
G = nx.DiGraph()

# valeur par défaut de la vitesse
default_speed = "default"

# Parcourir les nœuds (nodes) du fichier OSM
for node in root.findall(".//node"):
    node_id = node.get('id')
    lat = float(node.get('lat'))
    lon = float(node.get('lon'))
    G.add_node(node_id, pos=(lon, lat))

# Parcourir les relations (ways) du fichier OSM
for way in root.findall(".//way"):
    # Eliminer les ways qui ne sont pas des routes
    highway = way.find(".//tag[@k='highway']")
    if highway is None:
        continue
    # Eliminer les ways qui sont des footways
    if highway.get('v') == 'footway':
        continue
    
    # Vérifier si la relation (way) est à sens unique
    if way.find(".//tag[@k='oneway']") is not None:
        oneway = way.find(".//tag[@k='oneway']").get('v')
        if oneway == 'yes':
            edge_color = 'red'
            edge_type = 'oneway'
        else:
            edge_color = 'gray'
            edge_type = 'twoway'
    else:
        edge_color = 'gray'
        edge_type = 'twoway'
    
    # Ajouter la vitesse sur la voie
    speed_tag = way.find(".//tag[@k='maxspeed']")
    #speed = int(speed_tag.get('v').split()[0]) if speed_tag is not None else "default"  # La vitesse par défaut est 50 km/h
    
    speed_value = speed_tag.get('v').split()[0] if speed_tag is not None and speed_tag.get('v').split()[0].isdigit() else default_speed
    speed = int(speed_value) if speed_value.isdigit() else default_speed  # La vitesse par défaut est 50 km/h
        
    way_id = way.get('id')
    nodes = [nd.get('ref') for nd in way.findall(".//nd")]
    G.add_edges_from(zip(nodes[:-1], nodes[1:]), id=way_id, color=edge_color, type=edge_type, speed=speed)

# Retirer les noeuds isolés
G.remove_nodes_from(list(nx.isolates(G)))

# Calculer la longueur des routes
for edge in G.edges():
    length = 0
    for i in range(len(edge)-1):
        lat1 = float(G.nodes[edge[i]]['pos'][1])
        lon1 = float(G.nodes[edge[i]]['pos'][0])
        lat2 = float(G.nodes[edge[i+1]]['pos'][1])
        lon2 = float(G.nodes[edge[i+1]]['pos'][0])
        # formule de haversine
        R = 6371e3
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2-lat1)
        delta_lambda = np.radians(lon2-lon1)
        a = np.sin(delta_phi/2) * np.sin(delta_phi/2) + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2) * np.sin(delta_lambda/2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        length += R * c
    G[edge[0]][edge[1]]['length'] = length

# Identifier les nœuds avec une route entrante et une route sortante
nodes_to_remove = []
for node in G.nodes():
    predecessors = list(G.predecessors(node))
    successors = list(G.successors(node))
    if len(predecessors) == 1 and len(successors) == 1:
        pred_edge_type = G[predecessors[0]][node]['type']
        succ_edge_type = G[node][successors[0]]['type']
        pred_edge_speed = G[predecessors[0]][node]['speed']
        succ_edge_speed = G[node][successors[0]]['speed']
        
        # Vérifier que la vitesse et le type de route sont les mêmes pour les deux arêtes
        if pred_edge_type == succ_edge_type and pred_edge_speed == succ_edge_speed:
            nodes_to_remove.append(node)

# Supprimer les nœuds et ajouter les routes directes entre les voisins
for node in nodes_to_remove:
    predecessors = list(G.predecessors(node))
    successors = list(G.successors(node))
    pred_edge_type = G[predecessors[0]][node]['type']
    pred_edge_color = G[predecessors[0]][node]['color']
    pred_edge_speed = G[predecessors[0]][node]['speed']
    pred_edge_length = G[predecessors[0]][node]['length']
    succ_edge_length = G[node][successors[0]]['length']
    G.remove_node(node)
    G.add_edge(predecessors[0], successors[0], type=pred_edge_type, color=pred_edge_color, speed=pred_edge_speed, length=pred_edge_length+succ_edge_length)

#supprimer les arrêtes qui bouclent sur elles-mêmes
edges_to_remove = []
for edge in G.edges():
    if edge[0] == edge[1]:
        edges_to_remove.append(edge)
G.remove_edges_from(edges_to_remove)

nodes_without_position = [node for node in G.nodes() if 'pos' not in G.nodes[node]]
print(f"Nombre de noeuds sans position: {len(nodes_without_position)}")
G.remove_nodes_from(nodes_without_position)
print(f"Nombre de noeuds: {len(G.nodes())}")
print(f"Nombre de routes: {len(G.edges())}")
print(f"Nombre de routes à sens unique: {len([edge for edge in G.edges() if G[edge[0]][edge[1]]['type'] == 'oneway'])}")
print(f"Nombre de routes à double sens: {len([edge for edge in G.edges() if G[edge[0]][edge[1]]['type'] == 'twoway'])}")
print(f"Nombre de routes sans vitesse: {len([edge for edge in G.edges() if G[edge[0]][edge[1]]['speed'] == default_speed])}")
print(f"Nombre de routes avec vitesse: {len([edge for edge in G.edges() if G[edge[0]][edge[1]]['speed'] != default_speed])}")
print(f"Vitesse maximale: {max([G[edge[0]][edge[1]]['speed'] for edge in G.edges() if G[edge[0]][edge[1]]['speed'] != default_speed])} km/h")
print(f"Vitesse minimale: {min([G[edge[0]][edge[1]]['speed'] for edge in G.edges() if G[edge[0]][edge[1]]['speed'] != default_speed])} km/h")
print(f"Vitesse moyenne: {sum([G[edge[0]][edge[1]]['speed'] for edge in G.edges() if G[edge[0]][edge[1]]['speed'] != default_speed]) / len([edge for edge in G.edges() if G[edge[0]][edge[1]]['speed'] != default_speed])} km/h")

# Dessiner le graphe avec les valeurs de vitesse maximale
pos = nx.get_node_attributes(G, 'pos')
edge_colors = [G[edge[0]][edge[1]]['color'] for edge in G.edges()]

# Dessiner le graphe avec les valeurs de vitesse maximale
# edges_with_speed = [(edge[0], edge[1]) for edge in G.edges() if 'speed' in G[edge[0]][edge[1]]]
# edge_labels = {(edge[0], edge[1]): f"{G[edge[0]][edge[1]]['speed']} km/h" for edge in edges_with_speed}

# Dessiner le graphe avec les valeurs de longueur des routes
#edge_labels = {(edge[0], edge[1]): f"{G[edge[0]][edge[1]]['length']} m" for edge in G.edges()}

nx.draw(G, pos, with_labels=False, font_size=5, node_size=5, node_color='lightblue', edge_color=edge_colors, linewidths=0.1)
#nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, alpha=0.7)
plt.show()


# exporter le graphe sous la forme d'une liste d'adjacence avec les attributs 'speed' et 'type' ainsi que les positions des noeuds et leur identifiant
Node_list = []
for node in G.nodes():
    Node_list.append([node, G.nodes[node]['pos'][0], G.nodes[node]['pos'][1]])

Edge_list = []
for edge in G.edges():
    #précise le sens de l'arête oneway
    Edge_list.append([edge[0], edge[1], G[edge[0]][edge[1]]['speed'], G[edge[0]][edge[1]]['type'], G[edge[0]][edge[1]]['length']])
    
#convertir la liste en dataframe
import pandas as pd
df = pd.DataFrame(Node_list)
df.columns = ['node_id', 'lon', 'lat']
df.to_csv('Node_list.csv', index=False)

df = pd.DataFrame(Edge_list)
df.columns = ['node_id1', 'node_id2', 'speed', 'type', 'length']
df.to_csv('Edge_list.csv', index=False)


