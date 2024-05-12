import tkinter as tk
from tkinter import ttk
from pathlib import Path
from datetime import datetime
# Crear una ventana
ventana = tk.Tk()
ventana.title("Ejemplo de botón con icono")
ventana.geometry("300x200")


# Directorio del archivo Inscripciones.py
PATH = str((Path(__file__).resolve()).parent)

# Directorio donde se encuentra el icono
ICON = r"/img/buho.ico"

# Directorio donde se encuentra la base de datos 
# DB = r"/db/Inscripciones.db"
DB = r"/db/Inscripciones_pruebas.db"

RELOJ = r"/img/reloj.gif"
# Clase con la interfaz gráf
# Cargar la imagen del icono
icono = tk.PhotoImage(file=PATH + RELOJ)

# Crear el botón con el icono
boton_icono = ttk.Button(ventana, image=icono)
boton_icono.pack(pady=20)

# Función para imprimir un mensaje al hacer clic en el botón
def imprimir_mensaje():
    print("¡Has hecho clic en el botón!")

# Enlazar la función imprimir_mensaje al evento clic del botón
boton_icono.config(command=imprimir_mensaje)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
