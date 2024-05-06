import tkinter as tk
import sys
import os

# Agregar el directorio principal al sys.path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

# Importar después de haber agregado el directorio al path
from utils.CargarDatos import CargarDatos

def iniciar_interfaz():
    main = tk.Tk()  # Usamos tk.Tk() en lugar de solo Tk()
    main.mainloop()
  

def cargar_datos():
    print("hello world")

    ruta_archivo = "/Users/juanpabloduqueb/Documents/Proyecto grafos/src/data/Test.xlsx" 

    try:
        # Intenta cargar el archivo
        with open(ruta_archivo) as f:
            # Aquí iría tu lógica para procesar el archivo
            print("Archivo cargado exitosamente.")
    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo en la ruta: {ruta_archivo}")

    # Crear una instancia de CargarDatos y cargar los datos
    cargador_datos = CargarDatos(ruta_archivo)
    personas = cargador_datos.cargarDatos()

    # Imprimir las primeras 5 personas
    for persona in personas[:5]:
        print(f"ID: {persona.id}, Nombre: {persona.nombre}, Tipo: {persona.tipo}, Conexiones: {persona.conexiones}")

if __name__ == "__main__":
    iniciar_interfaz()
    cargar_datos()
