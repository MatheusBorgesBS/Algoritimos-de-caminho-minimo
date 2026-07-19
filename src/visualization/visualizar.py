"""Desenho de grafos e destaque de resultados de algoritmos.

Este módulo NÃO pede nada ao usuário — ele só desenha. A entrada (menu,
escolha de nós, seed, etc.) fica no `app.py`, na raiz do projeto.

A função `desenhar_grafo` recebe uma sequência de arestas *em ordem* e sabe
tanto mostrar tudo de uma vez quanto animar passo a passo. Como todos os
algoritmos são normalizados para esse mesmo formato (uma lista ordenada de
arestas), não é preciso alterar nenhum algoritmo para animar o resultado.
"""

import matplotlib.pyplot as plt
import networkx as nx


def _construir_grafo(grafo):
    G = nx.Graph()
    for node, vizinhos in grafo.items():
        for vizinho, peso in vizinhos.items():
            G.add_edge(node, vizinho, weight=peso)
    return G


def _desenhar_base(G, pos):
    """Desenha o grafo cinza de fundo com rótulos de peso."""
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=700,
        font_size=16,
        font_weight="bold",
    )
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)


def _destacar(G, pos, arestas, nos):
    """Pinta de vermelho as arestas e de laranja os nós informados."""
    if arestas:
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=arestas,
            edge_color="red",
            width=4,
        )
    if nos:
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=nos,
            node_color="orange",
            node_size=800,
        )


def desenhar_grafo(
    grafo,
    sequencia_arestas,
    nos_destaque,
    resultado,
    passo_a_passo=False,
    intervalo=0.9,
):
    """Desenha o grafo e destaca o resultado do algoritmo.

    Parâmetros
    ----------
    grafo : dict
        Grafo no formato de dicionário de adjacências.
    sequencia_arestas : list[tuple]
        Arestas do resultado, JÁ na ordem em que devem aparecer.
    nos_destaque : list
        Nós a destacar no fim (ex.: o caminho encontrado).
    resultado : str
        Texto a ser impresso no terminal ao final.
    passo_a_passo : bool
        Se True, anima revelando uma aresta por vez.
    intervalo : float
        Segundos entre cada passo da animação.
    """
    G = _construir_grafo(grafo)
    pos = nx.kamada_kawai_layout(G, weight="weight", scale=2)

    if not passo_a_passo:
        plt.figure(figsize=(12, 9))
        _desenhar_base(G, pos)
        _destacar(G, pos, sequencia_arestas, nos_destaque)
        print("\n" + resultado)
        plt.margins(0.1)
        plt.show()
        return

    # --- Modo passo a passo -------------------------------------------------
    plt.ion()
    plt.figure(figsize=(12, 9))

    for i in range(len(sequencia_arestas) + 1):
        plt.clf()
        _desenhar_base(G, pos)

        arestas_ate_agora = sequencia_arestas[:i]
        # Nós já tocados pelas arestas reveladas até aqui.
        nos_ate_agora = {no for aresta in arestas_ate_agora for no in aresta}

        _destacar(G, pos, arestas_ate_agora, list(nos_ate_agora))

        plt.title(f"Passo {i} de {len(sequencia_arestas)}", fontsize=16)
        plt.margins(0.1)
        plt.pause(intervalo)

    # Quadro final: garante o destaque completo dos nós pedidos.
    _destacar(G, pos, sequencia_arestas, nos_destaque)
    plt.draw()

    print("\n" + resultado)
    plt.ioff()
    plt.show()
