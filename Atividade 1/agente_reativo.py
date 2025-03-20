from ambiente import Ambiente
import random

class AgenteReativo:
    def __init__(self, ambiente, capacidade_max=3):
        self.ambiente = ambiente
        self.pos = ambiente.pos_inicial
        self.capacidade_max = capacidade_max
        self.capacidade_atual = 0
        self.cor = "blue"  

    def mover_aleatoriamente(self):
        direcoes = [(0, 1), (0, -1), (1, 0), (-1, 0)]  
        dx, dy = random.choice(direcoes)
        nova_pos = (self.pos[0] + dx, self.pos[1] + dy)
        if 0 <= nova_pos[0] < self.ambiente.tamanho and 0 <= nova_pos[1] < self.ambiente.tamanho:
            if self.ambiente.grade[nova_pos[0]][nova_pos[1]] != -1:
                self.pos = nova_pos

    def coletar_recurso(self):
        if self.ambiente.grade[self.pos[0]][self.pos[1]] == 1:
            self.capacidade_atual += 1
            self.ambiente.grade[self.pos[0]][self.pos[1]] = 0  
            if self.pos in self.ambiente.recursos_pos:
                self.ambiente.recursos_pos.remove(self.pos)  
            self.ambiente.recursos_coletados += 1

    def verificar_vizinhos(self):
       
        direcoes = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in direcoes:
            x, y = self.pos[0] + dx, self.pos[1] + dy
            if 0 <= x < self.ambiente.tamanho and 0 <= y < self.ambiente.tamanho:
                if self.ambiente.grade[x][y] == 1:
                    return True
        return False

    def executar(self):
        if self.capacidade_atual < self.capacidade_max:
            if self.verificar_vizinhos():
                self.coletar_recurso()
            else:
                self.mover_aleatoriamente()
        else:
            self.pos = self.ambiente.pos_inicial
            self.cor = "red"  