"""Ponto de entrada do UrbanRouteLab.

Rode a partir da raiz do projeto:

    python app.py

Ele pergunta o algoritmo, a quantidade de nós, a seed (que controla o grafo
gerado — mesma seed = mesmo grafo), os nós envolvidos e se você quer ver a
resolução passo a passo. O desenho em si fica em src/visualization.
"""

from src import (
    dijkstra,
    caminhos,
    a_estrela,
    kruskal,
    prim,
    boruvka,
    nearestNeighbors,
    ford_fulkerson,
    gerar_grafo_conectado,
    gerar_grafo_completo,
)
from src.visualization.visualizar import desenhar_grafo


# ---------------------------------------------------------------------------
# Entrada do usuário
# ---------------------------------------------------------------------------

def ler_inteiro(mensagem, minimo=None, maximo=None):
    """Lê um inteiro do usuário, validando faixa opcional."""
    while True:
        try:
            valor = int(input(mensagem))

            if minimo is not None and valor < minimo:
                print(f"Digite um número maior ou igual a {minimo}.")
                continue

            if maximo is not None and valor > maximo:
                print(f"Digite um número menor ou igual a {maximo}.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida. Digite apenas números.")


def ler_sim_nao(mensagem):
    """Lê uma resposta sim/não e devolve True/False."""
    while True:
        resposta = input(mensagem).strip().lower()

        if resposta in ("s", "sim", "y", "yes"):
            return True
        if resposta in ("n", "nao", "não", "no"):
            return False

        print("Responda com 's' (sim) ou 'n' (não).")


def escolher_algoritmo():
    while True:
        print("\n=== Visualização de Algoritmos em Grafos ===")
        print("[1] Dijkstra — caminho mínimo")
        print("[2] A* — caminho mínimo com heurística")
        print("[3] Kruskal — árvore geradora mínima")
        print("[4] Prim — árvore geradora mínima")
        print("[5] Borůvka — árvore geradora mínima")
        print("[6] Vizinho Mais Próximo — rota aproximada do TSP")
        print("[7] Ford-Fulkerson — fluxo máximo")

        return ler_inteiro("\nEscolha uma opção: ", minimo=1, maximo=7)


def escolher_no(mensagem, nos):
    """Lê o nome de um nó válido (ex.: N0), aceitando também só o número."""
    while True:
        entrada = input(mensagem).strip().upper()

        # Permite digitar "5" no lugar de "N5"
        if entrada.isdigit():
            entrada = f"N{entrada}"

        if entrada in nos:
            return entrada

        print(f"Nó inválido. Escolha entre {nos[0]} e {nos[-1]}.")


# ---------------------------------------------------------------------------
# Preparação: gera o grafo certo para cada algoritmo
# ---------------------------------------------------------------------------

def gerar_grafo(algoritmo, quantidade_nos, seed):
    # TSP e fluxo máximo precisam de um grafo completo (todo mundo conectado).
    if algoritmo in (6, 7):
        return gerar_grafo_completo(
            quantidade_nos=quantidade_nos,
            seed=seed,
        )

    # MSTs ficam mais interessantes com mais arestas extras.
    arestas_extras = 15 if algoritmo in (3, 4, 5) else 10

    return gerar_grafo_conectado(
        quantidade_nos=quantidade_nos,
        arestas_extras=arestas_extras,
        peso_min=1,
        peso_max=10,
        seed=seed,
    )


# ---------------------------------------------------------------------------
# Execução: cada algoritmo é normalizado para (sequencia_arestas, nos, texto)
# ---------------------------------------------------------------------------

def resolver(algoritmo, grafo, coords, nos):
    if algoritmo == 1:
        origem = escolher_no("\nQual é o nó inicial? ", nos)
        destino = escolher_no("Qual é o nó final? ", nos)

        distancias, antecessores = dijkstra(grafo, origem)
        caminho = caminhos(antecessores, origem, destino)

        sequencia = list(zip(caminho, caminho[1:]))
        texto = (
            f"Caminho Dijkstra: {' -> '.join(caminho)}\n"
            f"Custo: {distancias[destino]}"
        )
        return sequencia, caminho, texto

    if algoritmo == 2:
        origem = escolher_no("\nQual é o nó inicial? ", nos)
        destino = escolher_no("Qual é o nó final? ", nos)

        distancias, antecessores = a_estrela(grafo, origem, destino, coords)
        caminho = caminhos(antecessores, origem, destino)

        sequencia = list(zip(caminho, caminho[1:]))
        texto = (
            f"Caminho A*: {' -> '.join(caminho)}\n"
            f"Custo: {distancias[destino]}"
        )
        return sequencia, caminho, texto

    if algoritmo in (3, 4, 5):
        if algoritmo == 3:
            mst, custo_total = kruskal(grafo)
            nome = "Kruskal"
        elif algoritmo == 4:
            origem = escolher_no("\nDe qual nó a árvore deve começar? ", nos)
            mst, custo_total = prim(grafo, origem)
            nome = "Prim"
        else:
            mst, custo_total = boruvka(grafo)
            nome = "Borůvka"

        sequencia = [(no_a, no_b) for no_a, no_b, peso in mst]
        texto = f"Custo total da MST ({nome}): {custo_total}"
        return sequencia, [], texto

    if algoritmo == 6:
        origem = escolher_no("\nQual é o nó inicial da rota? ", nos)

        resultado = nearestNeighbors(grafo, origem)

        # nearestNeighbors devolve uma string se não há caminho de volta.
        if isinstance(resultado, str):
            return [], [], resultado

        caminho, custo_total = resultado
        sequencia = list(zip(caminho, caminho[1:]))
        texto = (
            f"Caminho Vizinho Mais Próximo: {' -> '.join(caminho)}\n"
            f"Custo total: {custo_total}"
        )
        return sequencia, caminho, texto

    if algoritmo == 7:
        fonte = escolher_no("\nQual é a fonte (origem do fluxo)? ", nos)
        sumidouro = escolher_no("Qual é o sumidouro (destino do fluxo)? ", nos)

        fluxo_maximo, _residual, historico = ford_fulkerson(
            grafo,
            fonte,
            sumidouro,
        )

        # A sequência de passos é a concatenação das arestas de cada
        # caminho aumentante encontrado, na ordem em que apareceram.
        sequencia = []
        linhas = [f"Fluxo máximo de {fonte} até {sumidouro}: {fluxo_maximo}"]

        for i, passo in enumerate(historico, start=1):
            caminho = passo["caminho"]
            sequencia.extend(zip(caminho, caminho[1:]))
            linhas.append(
                f"  Caminho {i}: {' -> '.join(caminho)} "
                f"(gargalo {passo['gargalo']})"
            )

        return sequencia, [fonte, sumidouro], "\n".join(linhas)

    raise ValueError("Opção inválida.")


# ---------------------------------------------------------------------------
# Fluxo principal
# ---------------------------------------------------------------------------

def main():
    algoritmo = escolher_algoritmo()

    quantidade_nos = ler_inteiro(
        "\nQuantos nós você quer no grafo? ",
        minimo=2,
    )

    # A seed controla o grafo aleatório: a mesma seed sempre gera o mesmo
    # grafo, o que ajuda a reproduzir e comparar resultados. Veja o README.
    seed = ler_inteiro("Qual seed você quer usar (ex.: 42)? ")

    passo_a_passo = ler_sim_nao(
        "Quer ver a resolução passo a passo? (s/n) "
    )

    nos = [f"N{i}" for i in range(quantidade_nos)]

    grafo, coords = gerar_grafo(algoritmo, quantidade_nos, seed)

    sequencia, nos_destaque, texto = resolver(algoritmo, grafo, coords, nos)

    desenhar_grafo(
        grafo,
        sequencia,
        nos_destaque,
        texto,
        passo_a_passo=passo_a_passo,
    )


if __name__ == "__main__":
    main()
