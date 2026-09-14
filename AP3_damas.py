"""APS 03 - Problema das N damas com busca sistematica."""

from io import StringIO
from time import perf_counter

from aigyminsper.search.graph import State
from aigyminsper.search.search_algorithms import BuscaLargura, BuscaProfundidade


class NDamas(State):
    """Estado parcial: cada posicao da tupla indica a coluna de uma dama."""

    def __init__(self, n, colunas=(), operator="Estado inicial"):
        super().__init__(operator)
        self.n = n
        self.colunas = tuple(colunas)

    def successors(self):
        sucessores = []
        proxima_linha = len(self.colunas)

        # Coloca uma dama na proxima linha, somente em posicoes seguras.
        for coluna in range(self.n):
            if self._posicao_segura(proxima_linha, coluna):
                novas_colunas = self.colunas + (coluna,)
                operacao = (
                    f"colocar dama na linha {proxima_linha}, coluna {coluna}"
                )
                sucessores.append(NDamas(self.n, novas_colunas, operacao))

        return sucessores

    def _posicao_segura(self, linha, coluna):
        for linha_existente, coluna_existente in enumerate(self.colunas):
            mesma_coluna = coluna == coluna_existente
            mesma_diagonal = (
                abs(linha - linha_existente)
                == abs(coluna - coluna_existente)
            )

            if mesma_coluna or mesma_diagonal:
                return False

        return True

    def is_goal(self):
        return len(self.colunas) == self.n

    def description(self):
        return f"Problema das {self.n} damas"

    def cost(self):
        return 1

    def env(self):
        # A tupla e imutavel e pode ser usada pela poda geral da biblioteca.
        return self.colunas

    def tabuleiro(self):
        linhas = []
        for coluna_dama in self.colunas:
            linha = ["."] * self.n
            linha[coluna_dama] = "D"
            linhas.append(" ".join(linha))

        # Estados parciais recebem linhas vazias no final.
        for _ in range(self.n - len(self.colunas)):
            linhas.append(" ".join(["."] * self.n))

        return "\n".join(linhas)


def resolver(n, tipo_busca="profundidade"):
    estado_inicial = NDamas(n)

    if tipo_busca == "largura":
        algoritmo = BuscaLargura()
        return algoritmo.search(estado_inicial, pruning="general")

    if tipo_busca == "profundidade":
        algoritmo = BuscaProfundidade()
        # A solucao possui exatamente N colocacoes, portanto limite N.
        return algoritmo.search(estado_inicial, m=n, pruning="general")

    raise ValueError("tipo_busca deve ser 'largura' ou 'profundidade'")


def executar(tipo_busca, saida):
    print(f"Algoritmo: busca em {tipo_busca}\n", file=saida)
    for n in range(4, 12):
        inicio = perf_counter()
        resultado = resolver(n, tipo_busca)
        duracao = perf_counter() - inicio

        print(f"N = {n}", file=saida)
        if resultado is None:
            print("Nao achou solucao", file=saida)
        else:
            print(resultado.state.tabuleiro(), file=saida)
            print(f"Configuracao: {resultado.state.colunas}", file=saida)
            print(f"Profundidade: {resultado.depth}", file=saida)
            print(f"Tempo: {duracao:.6f} s", file=saida)
        print(file=saida)


def main():
    saida = StringIO()
    executar("largura", saida)
    executar("profundidade", saida)

    resultados = saida.getvalue()
    print(resultados, end="")
    with open("resultados_damas.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(resultados)

    print("Resultados salvos em resultados_damas.txt")


if __name__ == "__main__":
    main()