from math import sqrt

def distancia_euclidiana(no1, no2, coords):
    x1, y1 = coords[no1]
    x2, y2 = coords[no2]

    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def a_estrela(grafo,origem,destino,coords):
    inf = float("inf")

    g_score = {
        no: inf for no in grafo
    }
    f_score = {
        no: inf for no in grafo
    }
    antecessores = {
        no: None for no in grafo
    }

    open_list = {
        origem
    }
    closed_list = set()

    g_score[origem] = 0
    f_score[origem] = distancia_euclidiana(
        origem,
        destino,
        coords,
    )
    
    while open_list:
        no_atual = None
        menor_dist = inf
        for no in open_list:
            if f_score[no] < menor_dist:
                menor_dist = f_score[no]
                no_atual = no
        if no_atual == destino:
            return g_score, antecessores
        
        open_list.remove(no_atual)
        closed_list.add(no_atual)

        for vizinho, peso in grafo[no_atual].items():
            if vizinho in closed_list:
                continue
            novo_g = g_score[no_atual] + peso

            if novo_g < g_score[vizinho]:
                antecessores[vizinho] = no_atual
                g_score[vizinho] = novo_g

                h = distancia_euclidiana(vizinho,destino,coords)

                f_score[vizinho] = novo_g + h
                open_list.add(vizinho)

    return g_score,antecessores
