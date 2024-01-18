import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

# ... (votre code existant)

# Dessiner le graphe avec les valeurs de vitesse maximale
pos = nx.get_node_attributes(G, 'pos')
edge_colors = [G[edge[0]][edge[1]]['color'] for edge in G.edges()]
edge_labels = {(edge[0], edge[1]): f"{G[edge[0]][edge[1]]['speed']} km/h" for edge in G.edges()}

nx.draw(G, pos, with_labels=True, font_size=5, node_size=5, node_color='lightblue', edge_color=edge_colors, linewidths=0.1)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, alpha=0.7)

plt.show()
