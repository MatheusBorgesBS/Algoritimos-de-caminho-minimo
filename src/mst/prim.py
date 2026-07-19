def prim(grafo, origem):
    visitados = {origem}
    mst = []
    custo_total = 0

    while len(visitados) < len(grafo):
        menor_aresta = None
        menor_peso = float('inf')

        for no in visitados:
            for vizinho, peso in grafo[no].items():
                if vizinho not in visitados and peso < menor_peso:
                    menor_aresta = (no,vizinho,peso)
                    menor_peso = peso
        if menor_aresta is None:
            raise ValueError("O grafo não é conexo.")
        no, vizinho, peso = menor_aresta
        mst.append(menor_aresta)
        custo_total += peso
        visitados.add(vizinho)

    return mst, custo_total

