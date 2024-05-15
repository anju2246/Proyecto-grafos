import networkx as nx
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VistaGrafo(tk.Frame):
    def __init__(self, master, grafo):
        super().__init__(master)
        self.config(bg="white")
        self.grafo = grafo

        # Crear un lienzo para mostrar el grafo
        fig, ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Renderizar el grafo en el lienzo
        self.render_grafo(ax)

        # Agregar campos de entrada y botón para trayectoria más corta
        self.entrada_origen = tk.Entry(self)
        self.entrada_origen.pack(pady=5)
        self.entrada_destino = tk.Entry(self)
        self.entrada_destino.pack(pady=5)
        boton_trayectoria = tk.Button(self, text="Calcular Trayectoria", command=self.calcular_trayectoria)
        boton_trayectoria.pack(pady=5)

    def render_grafo(self, ax):
        # Obtener el grafo desde la capa de modelo
        grafo = self.grafo

        # Diccionario para asignar colores a los nodos según su tipo
        colores_nodos = {'Host': 'green', 'Invitado': 'blue', 'Prospecto': 'orange'}

        # Obtener la posición de los nodos usando Kamada-Kawai Layout
        pos = nx.kamada_kawai_layout(grafo)

        # Obtener los colores de los nodos según su tipo
        node_colors = [colores_nodos[grafo.nodes[nodo]['tipo']] for nodo in grafo.nodes]

        # Obtener el grado de los nodos
        grados = [grado for _, grado in grafo.degree()]

        # Calcular el tamaño de los nodos basado en su grado
        node_sizes = [grado * 100 for grado in grados]

        # Obtener los nombres de los nodos
        nombres_nodos = {nodo: grafo.nodes[nodo]['nombre'] for nodo in grafo.nodes}

        # Renderizar el grafo utilizando networkx
        nx.draw(grafo, pos, ax=ax, node_color=node_colors, node_size=node_sizes, with_labels=True, labels=nombres_nodos)
        ax.set_title("Grafo de Personas")

    def calcular_trayectoria(self):
        nodo_origen_str = self.entrada_origen.get()
        nodo_destino_str = self.entrada_destino.get()
        print(f"Nodo de origen (str): {nodo_origen_str}")
        print(f"Nodo de destino (str): {nodo_destino_str}")
        
        try:
            nodo_origen = int(nodo_origen_str)
            nodo_destino = int(nodo_destino_str)
        except ValueError:
            print("Los valores ingresados deben ser números enteros.")
            return

        print(f"Nodo de origen (int): {nodo_origen}")
        print(f"Nodo de destino (int): {nodo_destino}")

        if nodo_origen and nodo_destino:
            app = self.master
            app.obtener_trayectoria_mas_corta(nodo_origen, nodo_destino)