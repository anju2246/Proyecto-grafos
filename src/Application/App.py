import tkinter as tk


print("hello world")

main = tk.Tk()  # Usamos tk.Tk() en lugar de solo Tk()

main.mainloop()

ruta_archivo = "../Data/test.xlsx"

cargador_datos = CargarDatos(ruta_archivo)
personas = cargador_datos.cargarDatos()