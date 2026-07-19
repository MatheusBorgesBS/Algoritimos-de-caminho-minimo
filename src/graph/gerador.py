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