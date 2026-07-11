### Testes

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

graph = {
   "A": {"B": 3, "C": 3},
   "B": {"A": 3, "D": 3.5, "E": 2.8},
   "C": {"A": 3, "E": 2.8, "F": 3.5},
   "D": {"B": 3.5, "E": 3.1, "G": 10},
   "E": {"B": 2.8, "C": 2.8, "D": 3.1, "G": 7},
   "F": {"G": 2.5, "C": 3.5},
   "G": {"F": 2.5, "E": 7, "D": 10},
}

distancias, antecessores = dijkstra(graph, "A")


caminho = caminhos(antecessores,"A","F")


