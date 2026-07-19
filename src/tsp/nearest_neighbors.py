def nearestNeighbors(grafo, origem):
    visitados = set()
    caminho = []
    custo_total = 0
    no_atual = origem
    visitados.add(no_atual)
    caminho.append(no_atual)

    while len(visitados) < len(grafo):
        menor_distancia = float('inf')
        melhor_vizinho = None
    
        for vizinho, peso in grafo[no_atual].items():
            if vizinho not in visitados and peso < menor_distancia:
                menor_distancia = peso
                melhor_vizinho = vizinho
        if melhor_vizinho is None:
            return 'Não foi possivel visitar todos os nós'

        visitados.add(melhor_vizinho)
        caminho.append(melhor_vizinho)
        custo_total += menor_distancia
        no_atual = melhor_vizinho
    if origem in grafo[no_atual]:
        custo_total += grafo[no_atual][origem]
        caminho.append(origem)
    else:
        return ('Não há caminho de volta a origem')
    if len(visitados) != len(grafo):
        return "Não foi possível visitar todos os nós."

    return caminho, custo_total

