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

def boruvka(grafo):
    arestas = listar_arestas(grafo)

    componentes = [{no} for no in grafo]
    mst = []
    custo_total = 0

    while len(componentes) > 1:
        menores_arestas = []

        for componente in componentes:
            menor_aresta = None
            menor_peso = float("inf")

            for origem, destino, peso in arestas:
                origem_dentro = origem in componente
                destino_dentro = destino in componente

                # A aresta precisa sair da componente
                if origem_dentro == destino_dentro:
                    continue

                if peso < menor_peso:
                    menor_aresta = (origem, destino, peso)
                    menor_peso = peso

            if menor_aresta is not None:
                menores_arestas.append(menor_aresta)

        houve_uniao = False

        for origem, destino, peso in menores_arestas:
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

            houve_uniao = True

        if not houve_uniao:
            raise ValueError("O grafo não é conexo.")

    return mst, custo_total