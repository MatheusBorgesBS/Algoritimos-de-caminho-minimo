import random
import math

def gerar_grafo_conectado(
    quantidade_nos,
    arestas_extras=5,
    peso_min=1,
    peso_max=10,
    seed=42,
):
    if quantidade_nos < 1:
        raise ValueError("A quantidade de nós deve ser positiva.")

    if peso_min > peso_max:
        raise ValueError("peso_min não pode ser maior que peso_max.")

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

    nos = list(grafo)

    for i in range(1, len(nos)):
        no_atual = nos[i]
        no_anterior = random.choice(nos[:i])
        peso = random.randint(peso_min, peso_max)

        grafo[no_atual][no_anterior] = peso
        grafo[no_anterior][no_atual] = peso

    pares_disponiveis = [
        (nos[i], nos[j])
        for i in range(len(nos))
        for j in range(i + 1, len(nos))
        if nos[j] not in grafo[nos[i]]
    ]

    quantidade_adicionar = min(
        arestas_extras,
        len(pares_disponiveis),
    )

    for no1, no2 in random.sample(
        pares_disponiveis,
        quantidade_adicionar,
    ):
        peso = random.randint(peso_min, peso_max)
        grafo[no1][no2] = peso
        grafo[no2][no1] = peso

    return grafo, coords

def gerar_grafo_direcionado(
    quantidade_nos,
    arestas_extras=5,
    capacidade_min=1,
    capacidade_max=10,
    seed=42,
):
    if quantidade_nos < 2:
        raise ValueError("A rede de fluxo precisa de pelo menos 2 nós.")

    if capacidade_min > capacidade_max:
        raise ValueError(
            "capacidade_min não pode ser maior que capacidade_max."
        )

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

    nos = list(grafo)

    for i in range(len(nos) - 1):
        origem = nos[i]
        destino = nos[i + 1]
        capacidade = random.randint(capacidade_min, capacidade_max)
        grafo[origem][destino] = capacidade


    pares_disponiveis = [
        (nos[i], nos[j])
        for i in range(len(nos))
        for j in range(i + 1, len(nos))
        if nos[j] not in grafo[nos[i]]
    ]

    quantidade_adicionar = min(
        arestas_extras,
        len(pares_disponiveis),
    )

    for origem, destino in random.sample(
        pares_disponiveis,
        quantidade_adicionar,
    ):
        grafo[origem][destino] = random.randint(
            capacidade_min,
            capacidade_max,
        )

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