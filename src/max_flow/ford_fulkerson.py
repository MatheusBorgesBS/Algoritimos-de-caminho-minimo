import sys

# Garante saída UTF-8 mesmo em consoles Windows (cp1252) para o caractere "→".
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def criar_rede_residual(grafo):
    residual = {no: {} for no in grafo}
    for origem, vizinhos in grafo.items():
        for destino, capacidade in vizinhos.items():
            residual[origem][destino] = capacidade
            if origem not in residual[destino]:
                residual[destino][origem] = 0
    return residual

def buscar_caminho_dfs(residual, atual, destino,visitados,antecessores):
    visitados.add(atual)
    if atual == destino:
        return True
    
    for vizinho,capacidade in residual[atual].items():
        if capacidade > 0 and vizinho not in visitados:
            antecessores[vizinho] = atual

            find = buscar_caminho_dfs(residual,vizinho,destino,visitados,antecessores)

            if find:
                return True
    
    return False

def reconstruir_caminho(antecessores, fonte, sumidouro):
    caminho = []
    atual = sumidouro

    while atual != fonte:
        caminho.append(atual)
        atual = antecessores[atual]

    caminho.append(fonte)
    caminho.reverse()

    return caminho

def calcular_gargalo(residual, caminho):
    gargalo = float("inf")

    for i in range(len(caminho) - 1):
        origem = caminho[i]
        destino = caminho[i + 1]

        gargalo = min(
            gargalo,
            residual[origem][destino],
        )

    return gargalo

def atualizar_residual(residual, caminho, gargalo):
    for i in range(len(caminho) - 1):
        origem = caminho[i]
        destino = caminho[i + 1]

        residual[origem][destino] -= gargalo
        residual[destino][origem] += gargalo


def ford_fulkerson(grafo, fonte, sumidouro):
    if fonte not in grafo:
        raise ValueError("A fonte não existe no grafo.")

    if sumidouro not in grafo:
        raise ValueError("O sumidouro não existe no grafo.")

    if fonte == sumidouro:
        raise ValueError(
            "A fonte e o sumidouro devem ser nós diferentes."
        )

    for vizinhos in grafo.values():
        for destino, capacidade in vizinhos.items():
            if destino not in grafo:
                raise ValueError(
                    f"O nó {destino} não está definido no grafo."
                )

            if capacidade < 0:
                raise ValueError(
                    "As capacidades não podem ser negativas."
                )

    residual = criar_rede_residual(grafo)

    fluxo_maximo = 0
    historico = []

    while True:
        antecessores = {no: None for no in residual}
        visitados = set()

        encontrou = buscar_caminho_dfs(
            residual,
            fonte,
            sumidouro,
            visitados,
            antecessores,
        )

        if not encontrou:
            break

        caminho = reconstruir_caminho(
            antecessores,
            fonte,
            sumidouro,
        )

        gargalo = calcular_gargalo(
            residual,
            caminho,
        )

        atualizar_residual(
            residual,
            caminho,
            gargalo,
        )

        fluxo_maximo += gargalo

        historico.append({
            "caminho": caminho.copy(),
            "gargalo": gargalo,
            "fluxo_acumulado": fluxo_maximo,
        })

    return fluxo_maximo, residual, historico
