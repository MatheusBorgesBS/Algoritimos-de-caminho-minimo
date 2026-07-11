from Dijkstra import *
from Aestrela import *

import matplotlib.pyplot as plt
import networkx as nx



import random


def gerar_grafo_grade(linhas, colunas, peso_min=1, peso_max=5, seed=42):
    random.seed(seed)

    grafo = {}
    coords = {}

    for linha in range(linhas):
        for coluna in range(colunas):
            no = f"N{linha}_{coluna}"

            grafo[no] = {}
            coords[no] = (coluna, linha)

    movimentos = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    for linha in range(linhas):
        for coluna in range(colunas):
            no_atual = f"N{linha}_{coluna}"

            for delta_linha, delta_coluna in movimentos:
                nova_linha = linha + delta_linha
                nova_coluna = coluna + delta_coluna

                if (
                    0 <= nova_linha < linhas
                    and 0 <= nova_coluna < colunas
                ):
                    vizinho = f"N{nova_linha}_{nova_coluna}"

                    # Evita gerar pesos diferentes nos dois sentidos
                    if no_atual in grafo[vizinho]:
                        peso = grafo[vizinho][no_atual]
                    else:
                        peso = random.randint(peso_min, peso_max)

                    grafo[no_atual][vizinho] = peso

    return grafo, coords


grafo, coords = gerar_grafo_grade(
    linhas=5,
    colunas=5,
    peso_min=1,
    peso_max=5,
)


origem = 'N0_0'
destino = 'N4_4'

a = int(input('Digite 1 para Dijkstra ou 2 para A*:'))

if a == 1:
    distancias,antecessores = dijkstra(grafo,origem)
    caminho = caminhos(antecessores,origem,destino)
else:
    distancias, antecessores = a_estrela(grafo,origem,destino,coords)
    caminho = caminhos(antecessores,origem,destino)


G = nx.Graph()
for node, vizinhos in grafo.items():
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
print(distancias[destino])
plt.show()
