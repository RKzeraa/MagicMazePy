import tkinter as tk
from tkinter import filedialog
from collections import deque

class Grafo:
    def __init__(self, labirinto):
        self.labirinto = labirinto
        self.num_linhas = len(labirinto)
        self.num_colunas = len(labirinto[0])

    def adicionar_aresta(self, u):
        self.labirinto[u[0]][u[1]] = 1

    def remover_aresta(self, u):
        self.labirinto[u[0]][u[1]] = 0

    def bfs(self, inicio, fim):
        visitados = set()
        fila = deque([(inicio, [inicio])])

        while fila:
            no, caminho = fila.popleft()
            visitados.add(no)

            if no == fim:
                return caminho

            for vizinho in self.vizinhos(no):
                if vizinho not in visitados:
                    fila.append((vizinho, caminho + [vizinho]))

    def vizinhos(self, no):
        linha, coluna = no
        vizinhos = []

        if linha > 0 and self.labirinto[linha - 1][coluna] == 1:
            vizinhos.append((linha - 1, coluna))
        if linha < self.num_linhas - 1 and self.labirinto[linha + 1][coluna] == 1:
            vizinhos.append((linha + 1, coluna))
        if coluna > 0 and self.labirinto[linha][coluna - 1] == 1:
            vizinhos.append((linha, coluna - 1))
        if coluna < self.num_colunas - 1 and self.labirinto[linha][coluna + 1] == 1:
            vizinhos.append((linha, coluna + 1))

        return vizinhos

    def atualizar_tela(self, canvas):
        canvas.delete("all")
        for linha in range(self.num_linhas):
            for coluna in range(self.num_colunas):
                x0, y0 = coluna * 20, linha * 20
                x1, y1 = x0 + 20, y0 + 20
                cor = "black" if self.labirinto[linha][coluna] == 0 else "white"
                canvas.create_rectangle(x0, y0, x1, y1, fill=cor)

        if app.inicio:
            if any(self.labirinto[linha][coluna] == 1 for linha, coluna in self.vizinhos(app.inicio)):
                cor_inicio = "green"
            else:
                cor_inicio = "white"
            canvas.create_oval(app.inicio[1] * 20, app.inicio[0] * 20, (app.inicio[1] + 1) * 20, (app.inicio[0] + 1) * 20, fill=cor_inicio)
        if app.fim:
            canvas.create_oval(app.fim[1] * 20, app.fim[0] * 20, (app.fim[1] + 1) * 20, (app.fim[0] + 1) * 20, fill="red")

class LabirintoApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Jogo do Labirinto")

        self.labirinto = None
        self.canvas = None
        self.grafo = None

        self.inicio = (0, 0)
        self.fim = None
        self.caminho = None

        self.definindo_saida = False

        self.criar_interface()

    def criar_interface(self):
        self.canvas = tk.Canvas(self.janela, width=400, height=400)
        self.canvas.pack()

        self.carregar_botao = tk.Button(self.janela, text="Carregar Labirinto", command=self.carregar_labirinto)
        self.carregar_botao.pack()

        self.adicionar_aresta_botao = tk.Button(self.janela, text="Adicionar Aresta", state=tk.DISABLED, command=self.iniciar_adicao_aresta)
        self.adicionar_aresta_botao.pack()

        self.remover_aresta_botao = tk.Button(self.janela, text="Remover Aresta", state=tk.DISABLED, command=self.iniciar_remocao_aresta)
        self.remover_aresta_botao.pack()

        self.resolver_botao = tk.Button(self.janela, text="Resolver", state=tk.DISABLED, command=self.resolver_labirinto)
        self.resolver_botao.pack()

        self.definir_saida_botao = tk.Button(self.janela, text="Definir Saída", state=tk.DISABLED, command=self.iniciar_definicao_saida)
        self.definir_saida_botao.pack()

    def carregar_labirinto(self):
        nome_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
        if nome_arquivo:
            self.labirinto = self.carregar_labirinto_do_arquivo(nome_arquivo)
            self.fim = None
            self.grafo = Grafo(self.labirinto)
            self.grafo.atualizar_tela(self.canvas)
            self.resolver_botao.config(state=tk.DISABLED)
            self.definir_saida_botao.config(state=tk.NORMAL)
            self.adicionar_aresta_botao.config(state=tk.NORMAL)
            self.remover_aresta_botao.config(state=tk.NORMAL)

    def carregar_labirinto_do_arquivo(self, nome_arquivo):
        labirinto = []
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                labirinto.append(list(map(int, linha.strip())))
        return labirinto

    def desenhar_labirinto(self):
        self.grafo.atualizar_tela(self.canvas)

    def iniciar_definicao_saida(self):
        self.definir_saida_botao.config(state=tk.DISABLED)
        self.canvas.bind("<Button-1>", self.marcar_saida)
        self.definindo_saida = True

    def iniciar_adicao_aresta(self):
        self.canvas.bind("<Button-1>", self.adicionar_aresta)
        self.adicionar_aresta_botao.config(state=tk.DISABLED)
        self.remover_aresta_botao.config(state=tk.DISABLED)

    def iniciar_remocao_aresta(self):
        self.canvas.bind("<Button-1>", self.remover_aresta)
        self.adicionar_aresta_botao.config(state=tk.DISABLED)
        self.remover_aresta_botao.config(state=tk.DISABLED)

    def marcar_saida(self, evento):
        if self.definindo_saida:
            coluna = evento.x // 20
            linha = evento.y // 20
            if self.labirinto[linha][coluna] == 1:
                self.fim = (linha, coluna)
                self.canvas.create_oval(coluna * 20, linha * 20, (coluna + 1) * 20, (linha + 1) * 20, fill="red")
                self.canvas.unbind("<Button-1>")
                self.resolver_botao.config(state=tk.NORMAL)

    def adicionar_aresta(self, evento):
        coluna = evento.x // 20
        linha = evento.y // 20
        if self.labirinto[linha][coluna] == 0:
            self.grafo.adicionar_aresta((linha, coluna))
            self.desenhar_labirinto()
            self.canvas.unbind("<Button-1>")
            self.adicionar_aresta_botao.config(state=tk.NORMAL)
            self.remover_aresta_botao.config(state=tk.NORMAL)

    def remover_aresta(self, evento):
        coluna = evento.x // 20
        linha = evento.y // 20
        if self.labirinto[linha][coluna] == 1:
            self.grafo.remover_aresta((linha, coluna))
            self.desenhar_labirinto()
            self.canvas.unbind("<Button-1>")
            self.adicionar_aresta_botao.config(state=tk.NORMAL)
            self.remover_aresta_botao.config(state=tk.NORMAL)

    def resolver_labirinto(self):
        if not self.fim:
            return

        self.caminho = self.grafo.bfs(self.inicio, self.fim)
        if self.caminho:
            print("Caminho encontrado:", self.caminho)
            self.desenhar_caminho()
        else:
            print("Não há caminho de fuga.")

    def desenhar_caminho(self):
        for no in self.caminho:
            x0, y0 = no[1] * 20, no[0] * 20
            x1, y1 = x0 + 20, y0 + 20
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")

if __name__ == "__main__":
    janela = tk.Tk()
    app = LabirintoApp(janela)
    janela.mainloop()
