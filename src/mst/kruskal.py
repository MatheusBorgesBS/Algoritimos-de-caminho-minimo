def listar_arestas(grafo):
    arestas = []
    vistas = set()

    for no, vizinhos in grafo.items():
        for vizinho, peso in vizinhos.items():
            chave = frozenset({no, vizinho})

            if chave not in vistas:
                arestas.append((no, vizinho, peso))
                vistas.add(chave)
    return arestas

def kruskal(grafo):
    arestas = listar_arestas(grafo)
    arestas.sort(key=lambda aresta: aresta[2])

    componentes = [{no} for no in grafo]
    mst = []
    custo_total = 0

    for origem, destino, peso in arestas:
        componente_origem = None
        componente_destino = None

        for componente in componentes:
            if origem in componente:
                componente_origem = componente

            if destino in componente:
                componente_destino = componente

        if componente_origem is componente_destino:
            continue

        mst.append((origem, destino, peso))
        custo_total += peso

        nova_componente = componente_origem | componente_destino

        componentes.remove(componente_origem)
        componentes.remove(componente_destino)
        componentes.append(nova_componente)

        if len(mst) == len(grafo) - 1:
            break
    if len(mst) != len(grafo) - 1:
        raise ValueError("O grafo não é conexo.")

    return mst, custo_total
