def dijkstra(grafo, origem):
    inf = float('inf')
    distancias = {
        no : inf for no in grafo
    }
    antecessores = {
        no: None for no in grafo
    }
    visitados = set()

    distancias[origem] = 0

    while len(visitados) < len(grafo):
        no_atual = None
        menor_dist = inf

        for no in grafo:
            if no not in visitados and distancias[no] < menor_dist:
                no_atual = no
                menor_dist = distancias[no]
        if no_atual is None:
            break


        visitados.add(no_atual)

        for vizinho, peso in grafo[no_atual].items():
            nova_dist = distancias[no_atual] + peso
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                antecessores[vizinho] = no_atual
    
    return distancias,antecessores

def caminhos(antecessores, inicio, destino):
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = antecessores[atual]
    caminho.reverse()

    if not caminho or caminho[0] != inicio:
        return []
    return caminho
