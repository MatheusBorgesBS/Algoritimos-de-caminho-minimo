from Dijkstra import *

import matplotlib.pyplot as plt
import networkx as nx

graph = {
   "A": {"B": 3, "C": 3},
   "B": {"A": 3, "D": 3.5, "E": 2.8},
   "C": {"A": 3, "E": 2.8, "F": 3.5},
   "D": {"B": 3.5, "E": 3.1, "G": 10},
   "E": {"B": 2.8, "C": 2.8, "D": 3.1, "G": 7},
   "F": {"G": 2.5, "C": 3.5},
   "G": {"F": 2.5, "E": 7, "D": 10},
}

origem = 'A'
destino = 'G'


distancias,antecessores = dijkstra(graph,origem)
caminho = caminhos(antecessores,origem,destino)


G = nx.Graph()
for node, vizinhos in graph.items():
    for vizinho, peso in vizinhos.items():
          G.add_edge(node,vizinho,weight = peso)

pos = nx.spring_layout(G,seed=42)
plt.figure(figsize=(8, 6))

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=16, font_weight='bold')


labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

arestas_caminho = list(zip(caminho,caminho[1:]))
# Destaca as arestas do menor caminho
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=arestas_caminho,
    edge_color="red",
    width=4,
)

# Destaca os nós do menor caminho
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=caminho,
    node_color="orange",
    node_size=800,
)


plt.title(f"Grafo")
plt.show()
