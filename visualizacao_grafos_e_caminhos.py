from src import *


import matplotlib.pyplot as plt
import networkx as nx



import random
import math


def gerar_grafo_conectado(quantidade_nos,arestas_extras=5,peso_min=1,peso_max=10,seed=42,):
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

def gerar_grafo_completo(quantidade_nos,seed=42,):
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

    for i in range(len(nos)):
        for j in range(i + 1, len(nos)):
            no1 = nos[i]
            no2 = nos[j]

            x1, y1 = coords[no1]
            x2, y2 = coords[no2]

            peso = round(
                math.dist((x1, y1), (x2, y2)),
                2,
            )

            grafo[no1][no2] = peso
            grafo[no2][no1] = peso

    return grafo, coords

def escolher_algoritmo():
    while True:
        print("\n=== Visualização de Algoritmos em Grafos ===")
        print("[1] Dijkstra — caminho mínimo")
        print("[2] A* — caminho mínimo com heurística")
        print("[3] Kruskal — árvore geradora mínima")
        print("[4] Vizinho Mais Próximo — rota aproximada do TSP")

        try:
            opcao = int(input("\nEscolha uma opção: "))

            if opcao in (1, 2, 3, 4):
                return opcao

            print("\nOpção inválida. Digite um número entre 1 e 4.")

        except ValueError:
            print("\nEntrada inválida. Digite apenas números.")

a = escolher_algoritmo()
origem = 'N0'
destino = 'N11'




if a in (1, 2):
    grafo, coords = gerar_grafo_conectado(
        quantidade_nos=12,
        arestas_extras=10,
        peso_min=1,
        peso_max=10,
    )

elif a == 3:
    grafo, coords = gerar_grafo_conectado(
        quantidade_nos=12,
        arestas_extras=15,
        peso_min=1,
        peso_max=10,
    )

elif a == 4:
    grafo, coords = gerar_grafo_completo(
        quantidade_nos=12,
    )

else:
    raise ValueError("Opção inválida.")

if a == 1:
    distancias, antecessores = dijkstra(grafo, origem)
    caminho = caminhos(antecessores, origem, destino)

    arestas_destaque = list(zip(caminho, caminho[1:]))
    nos_destaque = caminho

    resultado = (
        f"Caminho Dijkstra: {' -> '.join(caminho)}\n"
        f"Custo: {distancias[destino]}"
    )

elif a == 2:
    distancias, antecessores = a_estrela(
        grafo,
        origem,
        destino,
        coords,
    )

    caminho = caminhos(antecessores, origem, destino)

    arestas_destaque = list(zip(caminho, caminho[1:]))
    nos_destaque = caminho

    resultado = (
        f"Caminho A*: {' -> '.join(caminho)}\n"
        f"Custo: {distancias[destino]}"
    )

elif a == 3:
    mst, custo_total = kruskal(grafo)

    arestas_destaque = [
        (no_a, no_b)
        for no_a, no_b, peso in mst
    ]

    nos_destaque = []

    resultado = f"Custo total da MST: {custo_total}"

elif a == 4:
    caminho, custo_total = nearestNeighbors(grafo, origem)

    arestas_destaque = list(zip(caminho, caminho[1:]))
    nos_destaque = caminho

    resultado = (
        f"Caminho Vizinho Mais Próximo: {' -> '.join(caminho)}\n"
        f"Custo total: {custo_total}"
    )

G = nx.Graph()
for node, vizinhos in grafo.items():
    for vizinho, peso in vizinhos.items():
          G.add_edge(node,vizinho,weight = peso)

pos = nx.kamada_kawai_layout(G, weight="weight", scale=2)
plt.figure(figsize=(12, 9))


nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=16, font_weight='bold')


labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

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
plt.margins(0.1)
plt.show()
