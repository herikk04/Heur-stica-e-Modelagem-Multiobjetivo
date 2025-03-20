from ambiente import Ambiente
from agente_reativo import AgenteReativo
from agente_bfs import AgenteObjetivo
import tkinter as tk
from tkinter import ttk

class SimulacaoInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulação de Agentes (NetLogo-like)")
        self.canvas = None
        self.agente = None
        self.cell_size = 40
        self.delay = 200
        
        
        self.janela_config = tk.Toplevel(self.root)
        self.janela_config.title("Configuração")
        self.criar_widgets_configuracao()

    def criar_widgets_configuracao(self):
        self.tipo_agente = tk.StringVar(value="reativo")
        self.tamanho = tk.IntVar(value=10)
        self.recursos = tk.IntVar(value=5)
        self.obstaculos = tk.IntVar(value=3)
        self.capacidade = tk.IntVar(value=3)
        
        
        ttk.Label(self.janela_config, text="Tipo de Agente:").grid(row=0, column=0, padx=10, pady=5)
        ttk.Combobox(self.janela_config, textvariable=self.tipo_agente, values=["reativo", "bfs"], state="readonly").grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(self.janela_config, text="Tamanho do Ambiente:").grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(self.janela_config, textvariable=self.tamanho).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(self.janela_config, text="Número de Recursos:").grid(row=2, column=0, padx=10, pady=5)
        ttk.Entry(self.janela_config, textvariable=self.recursos).grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(self.janela_config, text="Número de Obstáculos:").grid(row=3, column=0, padx=10, pady=5)
        ttk.Entry(self.janela_config, textvariable=self.obstaculos).grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(self.janela_config, text="Capacidade do Agente:").grid(row=4, column=0, padx=10, pady=5)
        ttk.Entry(self.janela_config, textvariable=self.capacidade).grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Button(self.janela_config, text="Iniciar Simulação", command=self.iniciar_simulacao).grid(row=5, columnspan=2, pady=10)

    def iniciar_simulacao(self):
        self.janela_config.destroy()
        self.ambiente = Ambiente(
            tamanho=self.tamanho.get(),
            num_recursos=self.recursos.get(),
            num_obstaculos=self.obstaculos.get()
        )
        
        if self.tipo_agente.get() == "reativo":
            self.agente = AgenteReativo(self.ambiente, self.capacidade.get())
        else:
            self.agente = AgenteObjetivo(self.ambiente, self.capacidade.get())
        
 
        self.canvas = tk.Canvas(
            self.root,
            width=self.ambiente.tamanho * self.cell_size,
            height=self.ambiente.tamanho * self.cell_size,
            bg="white"
        )
        self.canvas.pack()
        
     
        self.desenhar_ambiente()
        self.desenhar_agente()
        
   
        self.root.after(self.delay, self.atualizar_simulacao)

    def desenhar_ambiente(self):
        for x in range(self.ambiente.tamanho):
            for y in range(self.ambiente.tamanho):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                

                if self.ambiente.grade[x][y] == -1:
                    fill = "black"  
                elif self.ambiente.grade[x][y] == 1:
                    fill = "green"  
                else:
                    fill = "white"  
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="gray")

    def desenhar_agente(self):
        x, y = self.agente.pos
        x_center = x * self.cell_size + self.cell_size // 2
        y_center = y * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 3
        self.canvas.create_oval(
            x_center - radius, y_center - radius,
            x_center + radius, y_center + radius,
            fill=self.agente.cor, tags="agente"
        )

    def atualizar_simulacao(self):
        if self.agente.capacidade_atual < self.agente.capacidade_max:
            self.agente.executar()
            
            self.canvas.delete("all")
            self.desenhar_ambiente()
            self.desenhar_agente()
            
            self.root.after(self.delay, self.atualizar_simulacao)  
        else:
            self.canvas.create_text(
                self.ambiente.tamanho * self.cell_size // 2,
                self.ambiente.tamanho * self.cell_size // 2,
                text="Simulação Concluída!",
                fill="red",
                font=("Arial", 16)
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulacaoInterface(root)
    root.mainloop()