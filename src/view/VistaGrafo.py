import tkinter as tk
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Configurar el estilo de seaborn
sns.set_style("dark")

class VistaGrafo(tk.Frame):
    def __init__(self, master, grafo):
        super().__init__(master)
        self.config(bg="black")  # Fondo del Frame principal
        self.grafo = grafo
        self.node_sizes = {}  # Inicializar self.node_sizes como un diccionario vacío


        # Crear un frame para el lienzo del grafo y la barra de herramientas
        self.frame_grafo = tk.Frame(self, bg="#202946")  # Fondo oscuro
        self.frame_grafo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un frame para el dashboard
        self.frame_dashboard = tk.Frame(self, bg="black")
        self.frame_dashboard.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, ipadx=10, ipady=10)

        # Crear el lienzo para el grafo
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafo)
        self.ax.set_facecolor('dimgray')  # Establecer el fondo oscuro del lienzo del grafo
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Diccionario para los colores de nodos y aristas
        self.node_colors = {}
        self.node_text_colors = {}
        for node in self.grafo.nodes():
            if self.grafo.nodes[node]['tipo'] == 'host':
                self.node_colors[node] = '#FFE699'  # Amarillo para hosts
                self.node_text_colors[node] = 'black'
            elif self.grafo.nodes[node]['tipo'] == 'prospecto':
                self.node_colors[node] = '#FFA7A7'  # Rosa para prospectos
                self.node_text_colors[node] = 'white'
            else:
                self.node_colors[node] = '#0EF9FF'  # Cyan para invitados
                self.node_text_colors[node] = 'black'

        self.edge_colors = {edge: '#0EF9FF' for edge in self.grafo.edges()}

        # Ajustar parámetros del subplot
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0.2, hspace=0.2)
        
        # Agregar la barra de herramientas de navegación
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_grafo)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    

        # Renderizar el grafo en el lienzo
        self.render_grafo()

        # Estilo para los campos de entrada
        entry_style = {
            "bg": "#373542",
            "fg": "white",
            "bd": 2,
            "relief": "flat",
            "highlightthickness": 0,
            "insertbackground": "white",
            "highlightbackground": "#373542",
            "highlightcolor": "#373542",
            "borderwidth": 0,
        }

        # Agregar campos de entrada y botones al dashboard
        self.entrada_origen = tk.Entry(self.frame_dashboard, **entry_style)
        self.entrada_origen.pack(pady=5, ipady=5, ipadx=10)

        self.entrada_destino = tk.Entry(self.frame_dashboard, **entry_style)
        self.entrada_destino.pack(pady=5, ipady=5, ipadx=10)

        # Crear los botones redondeados
        self.create_round_button("Calcular Trayectoria", self.calcular_trayectoria, "#029FE1").pack(pady=5, ipadx=10, ipady=5)
        self.create_round_button("Centralidad de Grado", self.mostrar_centralidad_grado, "#029FE1").pack(pady=5, ipadx=10, ipady=5)
            # Agregar el botón de reset
        self.create_round_button("Restablecer Colores", self.resetear_colores, "#029FE1").pack(pady=5, ipadx=10, ipady=5)

    def create_round_button(self, text, command, color):
        button_frame = tk.Frame(self.frame_dashboard, bg="black")
        button_frame.pack(pady=5)

        button_width = 140  # Ancho del botón

        # Crear el Canvas con el tamaño adecuado
        button_canvas = tk.Canvas(button_frame, width=button_width, height=40, bg=color, highlightthickness=0)
        button_canvas.pack()

        # Dibujar el texto en el centro del botón
        button_canvas.create_text(button_width // 2, 20, text=text, fill="white", font=("Helvetica", 10, "bold"), anchor="center")

        # Funciones de control de eventos para el botón
        button_canvas.bind("<Enter>", lambda event: self.on_enter_button(button_canvas))
        button_canvas.bind("<Leave>", lambda event: self.on_leave_button(button_canvas, color))
        button_canvas.bind("<Button-1>", lambda event: command())

        return button_frame

    def on_enter_button(self, button_canvas):
        button_canvas.config(bg="#0370A1")  # Cambiar color de fondo cuando el mouse entra

    def on_leave_button(self, button_canvas, color):
        button_canvas.config(bg=color)  # Restaurar color original cuando el mouse sale

    def render_grafo(self):
        self.ax.clear()  # Limpiar el eje antes de redibujar
        self.ax.set_facecolor('#202946')  # Establecer el color de fondo del eje

        # Obtener la posición de los nodos usando Kamada-Kawai Layout
        pos = nx.kamada_kawai_layout(self.grafo)

        # Aplicar efecto de resplandor y renderizar el grafo
        self.draw_glowing_graph(pos)

        self.ax.set_title("Grafo de Personas", color='white')
        self.canvas.draw()

        # Crear un rectángulo que cubra un área grande
        extra_space = 1000  # Ajustar según sea necesario
        canvas_width = self.canvas.get_tk_widget().winfo_width() + extra_space
        canvas_height = self.canvas.get_tk_widget().winfo_height() + extra_space

        # Crear un rectángulo que cubra todo el lienzo y establecer su color de fondo
        self.ax.add_patch(plt.Rectangle((-extra_space // 2, -extra_space // 2), canvas_width, canvas_height, color='#202946', zorder=-1))
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # Actualizar el lienzo para mostrar el rectángulo
        self.canvas.draw()

    def draw_glowing_graph(self, pos):
        
        n_lines = 10
        diff_linewidth = 1.05
        alpha_value = 0.03

        for edge in self.grafo.edges():
            for n in range(1, n_lines+1):
                nx.draw_networkx_edges(
                    self.grafo, pos, edgelist=[edge], ax=self.ax,
                    edge_color=self.edge_colors[edge],
                    width=2 + (diff_linewidth * n),
                    alpha=alpha_value
                )

        for node in self.grafo.nodes():
            for n in range(1, n_lines+1):
                nx.draw_networkx_nodes(
                    self.grafo, pos, nodelist=[node], ax=self.ax,
                    node_color=self.node_colors[node],
                    node_size=400,
                    linewidths=2 + (diff_linewidth * n),
                    alpha=alpha_value
                )

        # Dibujar nodos y aristas finales
        nx.draw(self.grafo, pos, ax=self.ax, node_color=list(self.node_colors.values()), edge_color=list(self.edge_colors.values()), with_labels=True, font_color='white')

        # Etiquetar los nodos con los nombres de las personas
        labels = {node: self.grafo.nodes[node]['nombre'] for node in self.grafo.nodes()}
        for node, label in labels.items():
            x, y = pos[node]
            self.ax.text(x, y - 0.1, label, fontsize=8, ha='center', va='top', color='white')



            

    def calcular_trayectoria(self):
        origen = self.entrada_origen.get()
        destino = self.entrada_destino.get()
        try:
            ruta = nx.shortest_path(self.grafo, source=int(origen), target=int(destino))
            print(f"La trayectoria más corta de {origen} a {destino} es: {ruta}")

            # Resetear los colores
            self.reset_colors()

            # Cambiar colores de los nodos y aristas en la ruta
            for node in ruta:
                self.node_colors[node] = 'red'
            for i in range(len(ruta) - 1):
                edge = (ruta[i], ruta[i + 1])
                if edge in self.edge_colors:
                    self.edge_colors[edge] = 'red'
                else:
                    self.edge_colors[(edge[1], edge[0])] = 'red'

            # Redibujar el grafo
            self.render_grafo()

            # Limpiar los campos de entrada
            self.entrada_origen.delete(0, tk.END)
            self.entrada_destino.delete(0, tk.END)

        except nx.NetworkXNoPath:
            print(f"No existe una trayectoria entre {origen} y {destino}")
        except nx.NodeNotFound as e:
            print(f"Error: {e}")

    def mostrar_centralidad_grado(self):
        print("Calculando centralidades...")
        grado_centrality = nx.degree_centrality(self.grafo)

        # Obtener los valores de centralidad y normalizarlos para el mapa de colores
        centrality_values = np.array(list(grado_centrality.values()))
        cmap = plt.get_cmap('Reds')  # Usar la paleta 'Reds' para tonos rosa
        node_colors = cmap(centrality_values)

        # Crear un dict de colores para nodos
        self.node_colors = {node: node_colors[i] for i, node in enumerate(self.grafo.nodes())}

        # Resetear colores de aristas
        self.edge_colors = {edge: 'dimgray' for edge in self.grafo.edges()}

        # Asignar colores de aristas según el nodo más central cercano
        for edge in self.grafo.edges():
            node1, node2 = edge
            if grado_centrality[node1] >= grado_centrality[node2]:
                self.edge_colors[edge] = self.node_colors[node1]
            else:
                self.edge_colors[edge] = self.node_colors[node2]

        # Ajustar tamaños de nodos según su centralidad
        node_sizes = [500 * centrality for centrality in centrality_values]
        self.node_sizes = dict(zip(self.grafo.nodes(), node_sizes))

        # Redibujar el grafo con los nuevos colores de centralidad
        self.render_grafo()

    def reset_colors(self):
        self.node_colors = {}
        self.node_text_colors = {}
        for node in self.grafo.nodes():
            if self.grafo.nodes[node]['tipo'] == 'host':
                self.node_colors[node] = '#FFE699'  # Amarillo para hosts
                self.node_text_colors[node] = 'black'
            elif self.grafo.nodes[node]['tipo'] == 'prospecto':
                self.node_colors[node] = '#FFA7A7'  # Rosa para prospectos
                self.node_text_colors[node] = 'white'
            else:
                self.node_colors[node] = '#0EF9FF'  # Cyan para invitados
                self.node_text_colors[node] = 'black'

        self.edge_colors = {edge: '#0EF9FF' for edge in self.grafo.edges()}

    def resetear_colores(self):
        self.reset_colors()
        self.render_grafo()