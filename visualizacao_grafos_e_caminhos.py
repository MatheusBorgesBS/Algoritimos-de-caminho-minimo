from Dijkstra import *
from Aestrela import *
from kruskal import *

import matplotlib.pyplot as plt
import networkx as nx



import random


def gerar_grafo_aleatorio(
    quantidade_nos,
    arestas_extras=5,
    peso_min=1,
    peso_max=10,
    seed=42,
):
    random.seed(seed)

    grafo = {
        f"N{i}": {}
        for i in range(quantidade_nos)
    }

    coords = {
        no: (
            random.uniform(0, 10),
            random.uniform(0, 10),
        )
        for no in grafo
    }

    nos = list(grafo.keys())

    for i in range(1, len(nos)):
        no_atual = nos[i]
        no_anterior = random.choice(nos[:i])

        peso = random.randint(peso_min, peso_max)

        grafo[no_atual][no_anterior] = peso
        grafo[no_anterior][no_atual] = peso

    adicionadas = 0

    while adicionadas < arestas_extras:
        no1, no2 = random.sample(nos, 2)

        if no2 in grafo[no1]:
            continue

        peso = random.randint(peso_min, peso_max)

        grafo[no1][no2] = peso
        grafo[no2][no1] = peso

        adicionadas += 1

    return grafo, coords

grafo, coords = gerar_grafo_aleatorio(
    quantidade_nos=12,
    arestas_extras=10,
    peso_min=1,
    peso_max=10,
)


origem = 'N0'
destino = 'N11'

a = int(input('Digite 1 para Dijkstra, 2 para A* ou 3 para MST (Kruskal): '))


if a == 1:
    distancias, antecessores = dijkstra(grafo, origem)
    caminho = caminhos(antecessores, origem, destino)
    arestas_destaque = list(zip(caminho, caminho[1:]))
    nos_destaque = caminho
    resultado = f'Custo do caminho Dijkstra: {distancias[destino]}'
elif a == 2:
    distancias, antecessores = a_estrela(grafo, origem, destino, coords)
    caminho = caminhos(antecessores, origem, destino)
    arestas_destaque = list(zip(caminho, caminho[1:]))
    nos_destaque = caminho
    resultado = f'Custo do caminho A*: {distancias[destino]}'
else:
    mst, custo_total = kruskal(grafo)
    arestas_destaque = [(no_a, no_b) for no_a, no_b, _ in mst]
    nos_destaque = []
    resultado = f'Custo total da MST (Kruskal): {custo_total}'


G = nx.Graph()
for node, vizinhos in grafo.items():
    for vizinho, peso in vizinhos.items():
          G.add_edge(node,vizinho,weight = peso)

pos = nx.spring_layout(G,seed=42)
plt.figure(figsize=(8, 6))

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=16, font_weight='bold')


labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=arestas_destaque,
    edge_color="red",
    width=4,
)

if nos_destaque:
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=nos_destaque,
        node_color="orange",
        node_size=800,
    )
print(resultado)
plt.show()
