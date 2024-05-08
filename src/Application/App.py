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
        self.geometry("800x600")

        # Crear la vista de inicio
        self.vista_inicio = VistaInicio(self)
        self.vista_inicio.place(relx=0, rely=0, relwidth=1, relheight=1)  # Ocupar toda la ventana

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

            print("Datos cargados y grafo creado correctamente.")
            return grafo
        except FileNotFoundError:
            print(f"No se pudo encontrar el archivo en la ruta: {ruta_archivo}")
            return None

if __name__ == "__main__":
    app = App()
    app.mainloop()