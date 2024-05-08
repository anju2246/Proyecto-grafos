import tkinter as tk

class VistaInicio(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(bg="lightgray")
        self.place(relx=0, rely=0, relwidth=1, relheight=1)  # Ocupar toda la ventana

        # Agregar widgets a la vista de inicio
        label = tk.Label(self, text="Bienvenido a mi Aplicación de Grafos", font=("Arial", 18))
        label.pack(pady=20)

        button = tk.Button(self, text="Mostrar Grafo", command=master.on_scroll)
        button.pack()