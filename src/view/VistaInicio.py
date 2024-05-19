import tkinter as tk
from PIL import Image, ImageTk

class VistaInicio(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(bg="lightgray")
        self.place(relx=0, rely=0, relwidth=1, relheight=1)  # Ocupar toda la ventana

        # Cargar imagen de fondo
        self.bg_image = ImageTk.PhotoImage(Image.open("/Users/juanpabloduqueb/Documents/Proyecto grafos/src/data/Interfaz proyecto grafos.png"))

        # Crear canvas para manejar la imagen
        self.canvas = tk.Canvas(self, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)

        # Agregar imagen al canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)