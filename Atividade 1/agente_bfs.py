from collections import deque
from ambiente import Ambiente

class AgenteObjetivo:
    def __init__(self, ambiente, capacidade_max=3):
        self.ambiente = ambiente
        self.pos = ambiente.pos_inicial
        self.capacidade_max = capacidade_max
        self.capacidade_atual = 0
        self.cor = "blue"
        self.caminho = []
    
    def bfs(self, inicio, alvo):
        fila = deque([(inicio, [])])
        visitados = set()
        while fila:
            pos, caminho = fila.popleft()
            if pos == alvo:
                return caminho
            if pos in visitados:
                continue
            visitados.add(pos)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                x, y = pos[0] + dx, pos[1] + dy
                if 0 <= x < self.ambiente.tamanho and 0 <= y < self.ambiente.tamanho:
                    if self.ambiente.grade[x][y] != -1:
                        fila.append(((x, y), caminho + [(x, y)]))
        return None
    
    def encontrar_recurso_mais_proximo(self):
        recursos = []
        for x in range(self.ambiente.tamanho):
            for y in range(self.ambiente.tamanho):
                if self.ambiente.grade[x][y] == 1:
                    recursos.append((x, y))
        caminho_mais_curto = None
        for recurso in recursos:
            caminho = self.bfs(self.pos, recurso)
            if caminho and (not caminho_mais_curto or len(caminho) < len(caminho_mais_curto)):
                caminho_mais_curto = caminho
        return caminho_mais_curto
    
    def coletar_recurso(self):
        if self.ambiente.grade[self.pos[0]][self.pos[1]] == 1:
            self.capacidade_atual += 1
            self.ambiente.grade[self.pos[0]][self.pos[1]] = 0
            self.ambiente.recursos_coletados += 1
    
    def executar(self):
        if self.capacidade_atual < self.capacidade_max:
            if not self.caminho:
                self.caminho = self.encontrar_recurso_mais_proximo()
            if self.caminho:
                proxima_pos = self.caminho.pop(0)
                self.pos = proxima_pos
                if self.ambiente.grade[self.pos[0]][self.pos[1]] == 1:
                    self.coletar_recurso()
                    self.caminho = []
        else:
            self.pos = self.ambiente.pos_inicial
            self.cor = "red"