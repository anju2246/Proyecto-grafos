import pandas as pd
from model.Persona import Persona

class CargarDatos:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo

    def cargarDatos(self):
        # Leer el archivo de Excel en un DataFrame de Pandas
        datos = pd.read_excel(self.ruta_archivo, header=None)
        print("Datos leídos del archivo:", datos)  # Línea de depuración

        # Crear una lista para almacenar las instancias de Persona
        personas = []

        # Iterar sobre las filas del DataFrame y crear instancias de Persona
        for _, fila in datos.iterrows():
            # Verificar si la fila está vacía
            if fila.notna().all():
                # Asegurar que la fila tenga al menos 4 elementos
                if len(fila) >= 4:
                    # [0] = ID, [1] = Nombre, [2] = Tipo, [3] = Conexiones
                    id_persona = int(fila[0])
                    nombre = fila[1]
                    tipo = fila[2]
                    conexiones_str = str(fila[3])  # Convertir a cadena
                    
                    # Verificar si conexiones_str es una cadena
                    if isinstance(conexiones_str, str):
                        conexiones = [int(conn) for conn in conexiones_str.split(',') if conn]
                    else:
                        conexiones = []
                    
                    persona = Persona(id_persona, nombre, tipo, conexiones)
                    personas.append(persona)
                else:
                    print(f"La fila {fila.tolist()} no tiene suficientes elementos.")
            else:
                # Salir del bucle si encontramos una fila vacía
                break

        print("Total de personas cargadas:", len(personas))  # Línea de depuración
        return personas