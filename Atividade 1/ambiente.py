import random

class Ambiente:
    def __init__(self, tamanho=10, num_recursos=5, num_obstaculos=3):
        self.tamanho = tamanho
        self.grade = [[0 for _ in range(tamanho)] for _ in range(tamanho)]
        self.pos_inicial = (0, 0)
        self.recursos_coletados = 0
        self.recursos_pos = []
        self.obstaculos_pos = []  
        self._posicionar_elementos(num_recursos, num_obstaculos)
    
    def _posicionar_elementos(self, num_recursos, num_obstaculos):
        
        for _ in range(num_recursos):
            x, y = random.randint(0, self.tamanho-1), random.randint(0, self.tamanho-1)
            self.grade[x][y] = 1
            self.recursos_pos.append((x, y))
        
        
        for _ in range(num_obstaculos):
            x, y = random.randint(0, self.tamanho-1), random.randint(0, self.tamanho-1)
            if self.grade[x][y] != 1:  
                self.grade[x][y] = -1
                self.obstaculos_pos.append((x, y))