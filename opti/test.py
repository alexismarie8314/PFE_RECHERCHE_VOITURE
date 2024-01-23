import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import numpy as np

# Charger le fichier OSM
tree = ET.parse('map_bischo_petit.osm')
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

# Dessiner le graphe avec les valeurs de vitesse maximale
pos = nx.get_node_attributes(G, 'pos')
edge_colors = [G[edge[0]][edge[1]]['color'] for edge in G.edges()]

# Dessiner le graphe avec les valeurs de longueur des routes
edge_labels = {(edge[0], edge[1]): f"{G[edge[0]][edge[1]]['length']} m" for edge in G.edges()}

nx.draw(G, pos, with_labels=False, font_size=5, node_size=5, node_color='lightblue', edge_color=edge_colors, linewidths=0.1)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, alpha=0.7)
plt.show()



#<node id="261611548" lat="48.4871385" lon="7.4987442"/>
#<node id="2131871907" lat="48.4870929" lon="7.4987906"/>
#<node id="453344584" lat="48.4870408" lon="7.4988547"/>






