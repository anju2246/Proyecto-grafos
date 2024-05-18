import tkinter as tk
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

class VistaGrafo(tk.Frame):
    def __init__(self, master, grafo):
        super().__init__(master)
        self.config(bg="white")
        self.grafo = grafo

        # Crear un frame para el lienzo del grafo y la barra de herramientas
        self.frame_grafo = tk.Frame(self)
        self.frame_grafo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un frame para el dashboard
        self.frame_dashboard = tk.Frame(self, bg="lightgray")
        self.frame_dashboard.pack(side=tk.LEFT, fill=tk.BOTH)

        # Crear el lienzo para el grafo
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafo)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Agregar la barra de herramientas de navegación
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_grafo)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Diccionario para los colores de nodos y aristas
        self.node_colors = {node: 'skyblue' for node in self.grafo.nodes()}
        self.edge_colors = {edge: 'skyblue' for edge in self.grafo.edges()}

        # Renderizar el grafo en el lienzo
        self.render_grafo()

        # Agregar campos de entrada y botones al dashboard
        self.entrada_origen = tk.Entry(self.frame_dashboard)
        self.entrada_origen.pack(pady=5)
        self.entrada_destino = tk.Entry(self.frame_dashboard)
        self.entrada_destino.pack(pady=5)
        boton_trayectoria = tk.Button(self.frame_dashboard, text="Calcular Trayectoria", command=self.calcular_trayectoria)
        boton_trayectoria.pack(pady=5)

        # Agregar botón de Centralidad de Grado
        boton_centralidad_grado = tk.Button(self.frame_dashboard, text="Centralidad de Grado", command=self.mostrar_centralidad_grado)
        boton_centralidad_grado.pack(pady=5)

    def render_grafo(self):
        # Limpiar el eje antes de redibujar
        self.ax.clear()

        # Obtener la posición de los nodos usando Kamada-Kawai Layout
        pos = nx.kamada_kawai_layout(self.grafo)

        # Obtener los colores de los nodos
        node_colors = [self.node_colors[node] for node in self.grafo.nodes()]
        edge_colors = [self.edge_colors[edge] for edge in self.grafo.edges()]

        # Renderizar el grafo utilizando networkx
        nx.draw(self.grafo, pos, ax=self.ax, node_color=node_colors, edge_color=edge_colors, with_labels=True)

        self.ax.set_title("Grafo de Personas")
        self.canvas.draw()

    def reset_colors(self):
        self.node_colors = {node: 'skyblue' for node in self.grafo.nodes()}
        self.edge_colors = {edge: 'skyblue' for edge in self.grafo.edges()}

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
            self.reset_colors()
            try:
                path = nx.shortest_path(self.grafo, source=nodo_origen, target=nodo_destino)
                print(f"La trayectoria más corta de {nodo_origen} a {nodo_destino} es: {path}")
                for i in range(len(path) - 1):
                    self.edge_colors[(path[i], path[i+1])] = 'red'
                    self.edge_colors[(path[i+1], path[i])] = 'red'
                    self.node_colors[path[i]] = 'red'
                self.node_colors[path[-1]] = 'red'
            except nx.NetworkXNoPath:
                print(f"No existe una trayectoria entre {nodo_origen} y {nodo_destino}")
            except nx.NodeNotFound as e:
                print(f"Error: {e}")

            self.render_grafo()

            # Limpiar los campos de entrada después de calcular la ruta más corta
            self.entrada_origen.delete(0, tk.END)
            self.entrada_destino.delete(0, tk.END)

    def mostrar_centralidad_grado(self):
        self.reset_colors()  # Restablecer los colores antes de calcular la centralidad de grado

        grado_centrality = nx.degree_centrality(self.grafo)

        # Obtener lista de centralidades y nodos ordenados
        nodes, centralities = zip(*sorted(grado_centrality.items(), key=lambda x: x[1], reverse=True))
        
        # Normalizar las centralidades para los tamaños
        node_sizes = [5000 * c for c in centralities]

        # Mapear centralidades a colores de mapa de calor
        cmap = plt.get_cmap('Reds')  # Usar la paleta 'Reds' para rojo intenso a azul claro
        centrality_values = np.array(centralities)
        node_colors = cmap(centrality_values)

        self.node_colors = {node: node_colors[i] for i, node in enumerate(nodes)}

        # Ajustar tamaño de los nodos en función de la centralidad
        self.fig.clf()  # Limpiar la figura
        self.ax = self.fig.add_subplot(111)
        self.canvas.draw()

        self.render_centralidad_grado(node_sizes)

    def render_centralidad_grado(self, node_sizes):
        self.ax.clear()
        pos = nx.kamada_kawai_layout(self.grafo)

        # Obtener los colores de los nodos
        node_colors = [self.node_colors[node] for node in self.grafo.nodes()]
        edge_colors = [self.edge_colors[edge] for edge in self.grafo.edges()]

        # Renderizar el grafo utilizando networkx
        nx.draw(self.grafo, pos, ax=self.ax, node_color=node_colors, edge_color=edge_colors, with_labels=True, node_size=node_sizes)

        self.ax.set_title("Grafo de Personas - Centralidad de Grado")
        self.canvas.draw()
