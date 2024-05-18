import tkinter as tk
import sys
import os
import networkx as nx

# Agregar el directorio principal al sys.path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

# Importar después de haber agregado el directorio al path
from utils.CargarDatos import CargarDatos
from view.VistaInicio import VistaInicio
from view.VistaGrafo import VistaGrafo

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mi Aplicación de Grafos")
        self.geometry("1400x800")
        self.prev_node_colors = {}
        self.prev_edge_colors = {}

        # Crear la vista de inicio
        self.vista_inicio = VistaInicio(self)
        self.vista_inicio.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Cargar los datos y crear el grafo
        self.grafo = self.cargar_datos()

        # Crear la vista del grafo y pasar el grafo como argumento
        self.vista_grafo = VistaGrafo(self, grafo=self.grafo)
        self.vista_grafo.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.vista_grafo.lower()  # Ocultar inicialmente la vista del grafo

        # Bindear el evento de scrollear hacia arriba
        self.bind("<MouseWheel>", self.on_scroll)

    def on_scroll(self, event):
        if event.delta > 0:  # Scrollear hacia arriba
            self.vista_inicio.place_forget()
            self.vista_grafo.lift()
            self.vista_grafo.tkraise()

    def cargar_datos(self):
        print("Cargando datos desde el archivo Test.xlsx")
        ruta_archivo = "src/data/Test.xlsx"
        try:
            # Crear una instancia de CargarDatos y cargar los datos
            cargador_datos = CargarDatos(ruta_archivo)
            personas = cargador_datos.cargarDatos()

            # Crear el grafo con la información de personas
            grafo = nx.Graph()

            # Agregar nodos únicos al grafo
            for persona in personas:
                grafo.add_node(persona.id, nombre=persona.nombre, tipo=persona.tipo)

            # Agregar aristas sin duplicados
            aristas = set()
            for persona in personas:
                for conexion in persona.conexiones:
                    arista = tuple(sorted((persona.id, conexion)))
                    aristas.add(arista)
            grafo.add_edges_from(aristas)

            # Imprimir los nodos en el grafo
            print(f"Nodos en el grafo: {list(grafo.nodes)}")

            print("Datos cargados y grafo creado correctamente.")
            return grafo
        except FileNotFoundError:
            print(f"No se pudo encontrar el archivo en la ruta: {ruta_archivo}")
            return None

    def obtener_trayectoria_mas_corta(self, nodo_origen, nodo_destino):
        try:
            ruta = nx.shortest_path(self.grafo, source=nodo_origen, target=nodo_destino)
            print(f"La trayectoria más corta de {nodo_origen} a {nodo_destino} es: {ruta}")

            # Guardar los colores previos
            self.prev_node_colors = {node: self.vista_grafo.node_colors[node] for node in self.grafo.nodes()}
            self.prev_edge_colors = {edge: self.vista_grafo.edge_colors[edge] for edge in self.grafo.edges()}

            # Restablecer los colores previos
            self.vista_grafo.reset_colors()

            # Cambiar los colores de los nodos y aristas en la trayectoria
            for node in ruta:
                self.vista_grafo.node_colors[node] = 'red'
            for i in range(len(ruta) - 1):
                edge = (ruta[i], ruta[i + 1])
                if edge in self.vista_grafo.edge_colors:
                    self.vista_grafo.edge_colors[edge] = 'red'
                else:
                    self.vista_grafo.edge_colors[(edge[1], edge[0])] = 'red'

            # Redibujar el grafo
            self.vista_grafo.redibujar_grafo()

        except nx.NetworkXNoPath:
            print(f"No existe una trayectoria entre {nodo_origen} y {nodo_destino}")
        except nx.NodeNotFound as e:
            print(f"Error: {e}")

    def calcular_centralidades(self):
        print("Calculando centralidades...")
        grado_centrality = nx.degree_centrality(self.grafo)
        betweenness_centrality = nx.betweenness_centrality(self.grafo)
        closeness_centrality = nx.closeness_centrality(self.grafo)

        print("\nCentralidad de Grado:")
        for nodo, grado in grado_centrality.items():
            print(f"Nodo {nodo}: {grado:.4f}")

        print("\nCentralidad de Intermediación:")
        for nodo, intermediacion in betweenness_centrality.items():
            print(f"Nodo {nodo}: {intermediacion:.4f}")

        print("\nCentralidad de Cercanía:")
        for nodo, cercania in closeness_centrality.items():
            print(f"Nodo {nodo}: {cercania:.4f}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
