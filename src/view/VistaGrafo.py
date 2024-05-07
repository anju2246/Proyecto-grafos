import networkx as nx
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class VistaGrafo(tk.Frame):
    def __init__(self, master, grafo=None):
        super().__init__(master)
        self.config(bg="white")
        self.grafo = grafo  # Asignar el grafo que se pasa como argumento

        # Crear un lienzo para mostrar el grafo
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Renderizar el grafo en el lienzo
        self.render_grafo()

    def render_grafo(self):
        if self.grafo is not None:
            # Limpiar el eje antes de dibujar
            self.ax.clear()

            # Renderizar el grafo utilizando networkx
            pos = nx.spring_layout(self.grafo)
            nx.draw(self.grafo, pos, ax=self.ax, node_color='lightblue', with_labels=True)

            # Actualizar el lienzo
            self.canvas.draw()