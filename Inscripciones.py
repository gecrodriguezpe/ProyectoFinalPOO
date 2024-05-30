# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
from pathlib import Path
from datetime import datetime
from idlelib.tooltip import Hovertip
import re

# Directorio del archivo Inscripciones.py
PATH = str((Path(__file__).resolve()).parent)

# Directorio donde se encuentra el icono principal del programa
ICON = r"/img/buho.ico"

# Directorio donde se encuentra el reloj
RELOJ = r"/img/reloj.png"

# Directorio donde se encuentra la base de datos 
DB = r"/db/Inscripciones.db"

# Clase con la interfaz gráfica del programa
class Inscripciones:

    # Constructor de la clase Inscripciones
    def __init__(self, master=None):

        # Base de datos que alimenta al programa 
        self.db_Name = PATH + DB # Base de datos

        # Contador que permite almancer el valor del autoincremental que corresponde al siguiente número de inscripción 
        self.autoincrementar_Contador = self.obtener_Autoincrementar_Contador() 

        ''' Ventana principal del programa '''

        # Ventana principal del programa
        ancho_Win = 800;  alto_Win = 600 # Dimensiones de la ventana principal
        self.win = tk.Tk(master) # Ventana principal
        self.win.configure(background="#f7f9fd", height=alto_Win, width=ancho_Win) # Configuraciones de la ventana
        self.win.geometry(f"{ancho_Win}x{alto_Win}") # Geometría de la ventana
        self.win.resizable(False, False) # No permitir cambiar las dimensiones de la ventana
        self.centrar_Pantalla(self.win, ancho_Win, alto_Win) # Centrado de pantalla
        self.win.iconbitmap(PATH + ICON) # Icono de la ventana 
        self.win.title("Inscripciones de Materias y Cursos") # Título de la ventana

        ''' Widgets: Elementos de la ventana principal del programa '''

        # Creación del frame asociada a la ventana principal: "frm_1"
        self.frm_1 = tk.Frame(self.win, name="frm_1")
        self.frm_1.configure(background="#f7f9fd", height=600, width=800)
        
        #Label No. Inscripción
        self.lblNumInscripcion = ttk.Label(self.frm_1, name="lblNumInscripcion")
        self.lblNumInscripcion.configure(background="#f7f9fd", font="{Arial} 11 {bold}",
                                        justify="left", state="normal",
                                        takefocus=False, text='No.Inscripción')
        self.lblNumInscripcion.place(anchor="nw", x=680, y=20)
        
        #Combobox No. Inscripción
        self.cmbx_Num_Inscripcion = ttk.Combobox(self.frm_1, name="cmbx_Num_Inscripcion", state="readonly")
        self.cmbx_Num_Inscripcion.place(anchor="nw", width=100, x=682, y=42)
        self.obtener_Inscripciones() # Permite obtener la lista de los números inscripción e introducirla al combobox "cmbx_Num_Inscripcion".

        #Label Fecha
        self.lblFecha = ttk.Label(self.frm_1, name="lblfecha")
        self.lblFecha.configure(background="#f7f9fd", text='Fecha:')
        self.lblFecha.place(anchor="nw", x=630, y=80)

        #Entry Fecha
        self.fecha = ttk.Entry(self.frm_1, name="fecha", validate="key", validatecommand=(self.frm_1.register(self.valida_Fecha_Entrada), "%P")) # Solo permite ingresar digitos o "/" en el Entry "fecha"
        self.fecha.configure(justify="center")
        self.fecha.place(anchor="nw", width=90, x=680, y=80)

        ## Bindings asociados al input que se va introduciendo en el Entry "fecha"
        self.fecha.bind("<KeyRelease>", self.valida_Formato_Fecha) # Valida que sea la fecha tenga el formato correcto de "dd/mm/aaaa"
        self.fecha.bind("<KeyRelease>", self.validar_fecha, "+") # Valida que sea la fecha sea una fecha válida (e.g.verifica que en los años bisiesto, el día 29 de febrero existe)
        self.fecha.bind("<BackSpace>", self.borrar_Caracter_Fecha) # Para borrar carácteres dentro de la cadena de texto que se encuentre en el Entry "fecha"

        ## Desabilitar movimiento del cursor dentro del Entry "fecha"
        self.fecha.bind("<Left>", lambda _: "break")
        self.fecha.bind("<Right>", lambda _: "break")
        self.fecha.bind("<Home>", lambda _: "break")
        self.fecha.bind("<End>", lambda _: "break")

        ## Desabilitar la tecla Delete dentro del Entry "fecha"
        self.fecha.bind("<Delete>", lambda _: "break")

        ## Desabilitar la opción de click y seleccionar dentro del Entry "fecha"
        self.fecha.bind("<B1-Motion>", lambda _: "break")

        ## Posicionar el cursor siempre al final del Entry "fecha"
        self.fecha.bindtags(((str(self.fecha)), "TEntry", "post-click", ".", "all")) #  Agregar la posibilidad de mover el cursor al final del Entry
        self.fecha.bind_class("post-click", "<Button-1>", self.mover_Cursor_Al_Final) # Mueve el cursor al final del Entry

        #Boton Reloj
        self.img_Boton=tk.PhotoImage(file=PATH + RELOJ) # Imagen del reloj que va a estar sobre el botón
        self.btnReloj = ttk.Button(self.frm_1, name="btnreloj", image=self.img_Boton, compound="center")
        self.btnReloj.place(width=23, height=23, x=771, y=79)
        
        ## Configuraciones adicionales para el botón "btnReloj"
        self.btnReloj.image = self.img_Boton.subsample(2, 2)  # Reducir el tamaño de la imagen para que quepa en el botón
        self.btnReloj.config(padding=(-10, -10, -10, -10)) # Ajustar la posición de la imagen dentro del botón utilizando la opción padding
        self.btnReloj.bind("<Button-1>", self.obtener_Fecha) # Asociar el evento de presión sobre el botón "btnReloj" con la función "obtener_Fecha"
        self.msj_btnReloj = Hovertip(self.btnReloj, text="Presione para obtener la fecha actual", hover_delay=50) # Muestra un mensaje cuando el cursor este sobre el botón reloj

        #Label Alumno
        self.lblIdAlumno = ttk.Label(self.frm_1, name="lblidalumno")
        self.lblIdAlumno.configure(background="#f7f9fd", text='Id Alumno:')
        self.lblIdAlumno.place(anchor="nw", x=20, y=80)

        #Combobox Alumno
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1, name="cmbx_id_alumno", state="readonly")
        self.cmbx_Id_Alumno.place(anchor="nw", width=112, x=100, y=80)
        self.obtener_Alumnos() # Permite obtener la lista de IDs de los alumnos de la tabla Alumnos e introducirla al combobox "cmbx_Id_Alumno"
        self.cmbx_Id_Alumno.bind("<<ComboboxSelected>>", self.escoger_Alumno)    # Asignar al evento de selección del ID del estudiante en el combobox "cmbx_Id_Alumno" la función "escoger_Alumno"

        #Label Nombres
        self.lblNombres = ttk.Label(self.frm_1, name="lblnombres")
        self.lblNombres.configure(text='Nombre(s):')
        self.lblNombres.place(anchor="nw", x=20, y=130)

        #Entry Nombres
        self.nombres = ttk.Entry(self.frm_1, name="nombres",state="disabled")
        self.nombres.place(anchor="nw", width=200, x=100, y=130)

        #Label Apellidos
        self.lblApellidos = ttk.Label(self.frm_1, name="lblapellidos")
        self.lblApellidos.configure(text='Apellido(s):')
        self.lblApellidos.place(anchor="nw", x=400, y=130)

        #Entry Apellidos
        self.apellidos = ttk.Entry(self.frm_1, name="apellidos",state="disabled")
        self.apellidos.place(anchor="nw", width=200, x=485, y=130)

        #Label Curso
        self.lblIdCurso = ttk.Label(self.frm_1, name="lblidcurso")
        self.lblIdCurso.configure(background="#f7f9fd",state="normal",text='Id Curso:')
        self.lblIdCurso.place(anchor="nw", x=20, y=185)

        #Combobox Curso
        self.cmbx_Id_Curso = ttk.Combobox(self.frm_1, name="id_curso", state="readonly")
        self.cmbx_Id_Curso.place(anchor="nw", width=166, x=100, y=185)
        self.obtener_Cursos() # Permite obtener la lista de códigos de los cursos de la tabla Cursos e introducirla al combobox "cmbx_Id_Curso"
        self.cmbx_Id_Curso.bind("<<ComboboxSelected>>", self.escoger_Curso)    # Asignar al evento de selección del código del curso en el combobox "cmbx_Id_Curso" la función "escoger_Curso"

        #Label Descripción del Curso
        self.lblDscCurso = ttk.Label(self.frm_1, name="lbldsccurso")
        self.lblDscCurso.configure(background="#f7f9fd",state="normal",text='Curso:')
        self.lblDscCurso.place(anchor="nw", x=275, y=185)

        #Entry de Descripción del Curso 
        self.descripc_Curso = ttk.Entry(self.frm_1, name="descripc_curso")
        self.descripc_Curso.configure(justify="left", width=166, state="disabled")
        self.descripc_Curso.place(anchor="nw", width=300, x=325, y=185)

        #Label Horario
        self.lblHorario = ttk.Label(self.frm_1, name="label3")
        self.lblHorario.configure(background="#f7f9fd",state="normal",text='Hora:')
        self.lblHorario.place(anchor="nw", x=635, y=185)

        #Entry del Horario
        self.horario = ttk.Entry(self.frm_1, name="entry3")
        self.horario.configure(justify="left", width=166)
        self.horario.place(anchor="nw", width=100, x=680, y=185)

        ''' Botones de la Aplicación '''

        # Estilo para los botones default
        self.botones = ttk.Style()
        self.botones.configure("TButton", foreground = "RoyalBlue") # Todos los botones van a tener un "foreground" de color azul
        self.botones.map("TButton", foreground=[("active", "red2")]) # Cuándo el mouse pase sobre los botones, el "foreground" cambia a rojo

        #Estilo para los botones alterno
        estilo = ttk.Style() # Aplica cuándo los alternos, en específico para el botón "confirmar"
        estilo.map("Boton.TButton", foreground=[("active", "black")]) # Cuándo el mouse pase sobre los botones, el "foreground" cambia a negro
        estilo.configure("Boton.TButton", foreground="red") # "foreground" de color rojo

        #Boton Buscar
        self.btnBuscar = ttk.Button(self.frm_1, name="btnbuscar")
        self.btnBuscar.configure(text='Buscar')
        self.btnBuscar.place(anchor="nw", x=155, y=260)
        self.btnBuscar.bind("<Button-1>", self.mostrar_Datos) # Asignar al evento de dar click izquierdo sobre el botón "btnBuscar" la función "mostrar_Datos"
        
        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name="btnguardar")
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor="nw", x=255, y=260)
        self.btnGuardar.bind("<Button-1>", self.guardar_Inscripcion) # Asignar al evento de dar click izquierdo sobre el botón "btnGuardar" la función "guardar_Inscripcion"
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name="btneditar")
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=355, y=260)
        self.btnEditar.bind("<Button-1>", self.editar_Curso) # Asignar al evento de dar click izquierdo sobre el botón "btnEditar" la función "editar_Curso"

        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name="btneliminar")
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor="nw", x=455, y=260)
        self.btnEliminar.bind("<Button-1>", self.crear_Ventana_Eliminar) # Asignar al evento de dar click izquierdo sobre el botón "btnEliminar" la función "crear_Ventana_Eliminar"
        
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name="btncancelar")
        self.btnCancelar.configure(text='Cancelar')
        self.btnCancelar.place(anchor="nw", x=555, y=260)
        self.btnCancelar.bind("<Button-1>", self.limpiar_Campos) # Asignar al evento de dar click izquierdo sobre el botón "btnCancelar" la función "limpiar_Campos"

        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="nw", width=796, x=2, y=245)

        ''' Treeview de la Aplicación '''    

        # Estilo para el Treeview
        self.style = ttk.Style()
        self.style.configure("estilo.Treeview", highlightthickmess=0, bd=0, background="#e0e0e0", font = ("Calibri Light", 10))
        self.style.configure("estilo.Treeview.Heading", background = "Azure", font = ("Calibri Light", 10, "bold"))
        self.style.layout("estilo.Treeview", [("estilo.Treeview.treearea", {"sticky":"nswe"})])

        # Creción del Treeview
        self.treeInscritos = ttk.Treeview(self.frm_1, name="treeInscritos", style = "estilo.Treeview")
        self.treeInscritos.configure(selectmode="browse")
        
        #Columnas del Treeview
        self.treeInscritos_cols = ['tV_curso','tV_descripción','tV_horario']
        self.treeInscritos_dcols = ['tV_curso','tV_descripción', 'tV_horario']
        self.treeInscritos.configure(columns=self.treeInscritos_cols,displaycolumns=self.treeInscritos_dcols)
        self.treeInscritos.column("#0",anchor="w",stretch=True,width=55,minwidth=10)
        self.treeInscritos.column("tV_horario",anchor="w",stretch=True,width=55,minwidth=25)
        self.treeInscritos.column("tV_descripción",anchor="w",stretch=True,width=200,minwidth=50)
        self.treeInscritos.column("tV_curso",anchor="w",stretch=True,width=100,minwidth=50)
        
        #Cabeceras
        self.treeInscritos.heading("#0", anchor="w", text='Id Alumno')
        self.treeInscritos.heading("tV_horario", anchor="w", text='Horario')
        self.treeInscritos.heading("tV_descripción", anchor="w", text='Descripción')
        self.treeInscritos.heading("tV_curso", anchor="w", text='Curso')
        self.treeInscritos.place(anchor="nw", height=300, width=790, x=4, y=300)

        #Scrollbars
        self.scroll_H = ttk.Scrollbar(self.frm_1, name="scroll_h")
        self.scroll_H.configure(orient="horizontal")
        self.scroll_H.place(anchor="s", height=12, width=1534, x=15, y=595)
        self.scroll_Y = ttk.Scrollbar(self.frm_1, name="scroll_y")
        self.scroll_Y.configure(orient="vertical")
        self.scroll_Y.place(anchor="s", height=275, width=12, x=790, y=582)
        self.frm_1.pack(side="top")
        self.frm_1.pack_propagate(0)

        # Widget (ventana) principal
        self.mainwindow = self.win

    # Función que permite que la interfaz gráfica permanezca activa y funcional mientras no se cierra ésta. 
    def run(self):
        """
        Ejecuta el bucle principal de la aplicación.

        Esta función inicia el bucle principal de la aplicación, que escucha y
        procesa eventos como la entrada del usuario y eventos de ventana. Se llama
        normalmente después de inicializar la aplicación y configurar todos los
        componentes necesarios.

        Permite la interacción continua con el usuario mientras la ventana principal esté activa.

        Parámetros:
            self (object): La instancia de la clase.

        Retorna:
            None
        """        
        self.mainwindow.mainloop()

    ''' Función de centrado de la pantalla '''

    ## Centrado de la pantalla
    def centrar_Pantalla(self, pantalla, ancho, alto):
        """
        Centra la ventana dada en la pantalla.

        Parámetros:
            pantalla (tkinter.Tk): La ventana a centrar.
            ancho (int): El ancho de la ventana.
            alto (int): La altura de la ventana.

        Retorna:
            None
        """

        # Argumentos para posicionar la pantalla
        x = (pantalla.winfo_screenwidth() // 2) - (ancho // 2)
        y = (pantalla.winfo_screenheight() // 2) - (alto // 2)

        # Posicionar la pantalla: ({ancho}x{alto} determina las dimensiones de la pantalla y {x}+{y-30} determina la posición de la pantalla)
        pantalla.geometry(f"{ancho}x{alto}+{x}+{y-30}")

        # Hacer la pantalla visible
        pantalla.deiconify()

    ''' Funciones de validación de la fecha '''

    # Función auxiliar 1 de validación de fecha: Mueve el cursor al final del Entry `fecha`.
    def mover_Cursor_Al_Final(self, event):
        """
        Mueve el cursor al final del widget de entrada `fecha`.

        Parámetros:
            event (Event): El evento que activó la función.

        Retorna:
            None
        """
        # Mueve el cursor al final del Entry        
        self.fecha.icursor(len(self.fecha.get()))
    
    # Función auxiliar 2 de validación de fecha: Permite obtener la fecha actual o inmediata que se encuentra en el sistema del computador tan pronto se hizo la solicitud de ésta. 
    def obtener_Fecha(self,event = None):
        """
        Elimina el contenido actual del Entry `self.fecha` e inserta la fecha actual en el formato "dd/mm/yyyy" que se encuentre en el sistema del computador tan pronto se hizo la solicitud de ésta.  
        Llama al método `self.valida_Formato_Fecha()` después de cada inserción de caracter, para validar que se esté ingresando un carácter correcto. 

        Parámetros:
            event (Event): Parámetro opcional de evento.

        Retorna:
            None
        """

        # Borra todo el contenido que se encuentre en el Entry "fecha"    
        self.fecha.delete(0, "end")

        # Utiliza la librería datetime para obtener la fecha actual en formato " %d %m %Y "
        fecha_Actual = datetime.now().strftime("%d%m%Y")
            # Itera a través de la cadena de texto "fecha_Actual"
        for caracter in fecha_Actual:
            
            # Inserta cada carácter, uno por uno, de la cadena de texto "fecha_Actual"
            self.fecha.insert("end", caracter)
            
            # Revisa que el formato de fecha que se va insertando cada vez que se agrega un carácter nuevo sea válido
            self.valida_Formato_Fecha()

    # Función auxiliar 3: Valida que dentro del Entry "fecha" solo se puedan insertar dígitos o barras diagonales ("/")
    def valida_Fecha_Entrada(self, texto):
        """
        Valida la entrada de texto para asegurarse de que solo contenga dígitos o barras diagonales.

        Parámetros:
            text (str): El texto de entrada a validar.

        Retorna:
            bool: True si el texto de entrada es válido, False en caso contrario.
        """        

        # Verifica que el texto de entrada solo contenga dígitos o barras diagonales
        return all(char.isdigit() or char == "/" for char in texto)
    
    # Función auxiliar 4: Configura el formato correcto en el campo Fecha
    def valida_Formato_Fecha(self, event = None):  
        """
        Configura el formato correcto en el Entry Fecha dd/mm/aaaa.

        Esta función verifica la longitud de la fecha en el Entry `fecha` e inserta un carácter "/" en la posición adecuada si la longitud es de 2 o 5. 
        Si la longitud es mayor a 10, muestra un mensaje de error y elimina los caracteres desde la posición 10 en adelante.

        Parámetros:
            event (Event, opcional): El evento que activó la función. Por defecto es None.

        Retorna:
            None
        """

        # Obtener la cadena de texto que se encuentra en el Entry "fecha"
        fecha = self.fecha.get()
        # _dd()mm()
        # Verifica la longitud de la fecha y inserta un carácter "/" en la posición adecuada
        if (len(fecha) in [2, 5]):
            self.fecha.insert(fecha.index(" ") + 1 if " " in fecha else len(fecha), "/") # En las posiciones 2 y 5, inserta un "/"
        elif len(fecha) > 10: 
            mssg.showerror("Error","Solo es permitido un máximo de 10 carácteres") # No permite ingresar más de 10 carácteres en el Entry "Fecha"
            self.fecha.delete(10, "end")

    # Función auxiliar 5: Valida que la fecha ingresada sea un día, mes y año valido
    def validacion_Dias_Mes_Año(self, d, m, a):
        """
        Valida el día, mes y año de una fecha dada.

        Parámetros:
            d (int): El día de la fecha.
            m (int): El mes de la fecha.
            a (int): El año de la fecha.

        Retorna:
            bool: True si la fecha es válida, False de lo contrario.
        """        
        # Retorna False si algo en la fecha no es valido

        ## Verifica si el año es válido (superior a 1754)
        if a <= 1754:   
            mssg.showerror("Error","Solo es permitido un año superior a 1754")  
            return False  
        
        ## Verifica si el mes está dentro del rango válido (1 a 12)
        if not (1 <= m <= 12):  
            mssg.showerror("Error","Solo es permitido un mes entre 1 y 12")
            return False
        
        ## Verifica que la información relacionada con cada mes específico sea válida. 
        if m in (1, 3, 5, 7, 8, 10, 12):     
            if not (1 <= d <= 31):  # Verifica si el día está dentro del rango válido para estos meses (1 a 31)
                mssg.showerror("Error", f"Solo es permitido un día entre 1 y 31 para el mes {m}")
                return False
        elif m == 2: # Verifica si el mes es febrero
            biciesto = a % 4 == 0 and (a % 100 != 0 or a % 400 == 0) # Calcula si el año es bisiesto
            if biciesto:  # Si el año es bisiesto
                if not (1 <= d <= 29): # Verifica si el día está dentro del rango válido para febrero en un año bisiesto (1 a 29)
                    mssg.showerror("Error", f"Solo es permitido un día entre 1 y 29 para el mes {m} de un año bisiesto")
                    return False
            else:  # Si el año no es bisiesto
                if not (1 <= d <= 28): # Verifica si el día está dentro del rango válido para febrero en un año no bisiesto (1 a 28)
                    mssg.showerror("Error", f"Solo es permitido un día entre 1 y 28 para el mes {m} de un año no bisiesto")
                    return False
        else: # Para los meses restantes (30 días)
            if not (1 <= d <= 30): # Verifica si el día está dentro del rango válido para estos meses (1 a 30)
                mssg.showerror("Error", f"Solo es permitido un día entre 1 y 30 para el mes {m}")
                return False
        
        # Si no hay un error en la fecha, entonces se retorna True indicando que la fecha es válida
        return True 
    
    # Función auxiliar 6: Emplea la función `validacion_Dias_Mes_Año` para verificar si la fecha ingresada por el usuario es una fecha válida 
    def validar_fecha(self, event = None):
        """
        Valida la fecha dada separándola en componentes de día, mes y año y llamando a la función `validacion_Dias_Mes_Año` con esos componentes. 
        Si la fecha no está en el formato dd/mm/aaaa o si la fecha es inválida, borra el contenido del Entry `fecha`.

        Parámetros:
            event (Event, opcional): El evento que activó la función. Por defecto es None.

        Retorna:
            None
        """
        # Obtener la cadena de texto dentro del Entry "fecha"
        fecha = self.fecha.get()

        # Verifica la longitud de la fecha y procede a hacer la validación de si la fecha es una fecha correcta en caso de que la fecha tenga una longitud de 10 carácteres
        if len(fecha) == 10:

        # Dividir la fecha en día, mes y año
            dia, mes, año = map(int, fecha.split('/')) # La función "map" transforma cada uno de los elementos que fuerón separados de la fecha por el split a tipos enteros (int)

            # Llamar a la función validacion_Dias_Mes_Año con los componentes de fecha
            if not self.validacion_Dias_Mes_Año(dia, mes, año):
                self.fecha.delete(0, "end") # En caso de que sea una fecha inválida, borra el contenido del Entry "fecha"
            else:
                pass
        else:
            pass

    # Función auxiliar 7: Permite borrar carácteres dentro de la cadena de texto que se encuentre en el Entry `fecha`
    def borrar_Caracter_Fecha(self, event = None):
        """
        Elimina el último carácter de la cadena de texto que se encuentre en el Entry `self.fecha` si es un dígito o un carácter "/".

        Parámetros:
            event (Event, opcional): El evento que desencadenó la función. Por defecto es None.

        Retorna:
            None
        """        
        
        # Obtener la cadena de texto que se encuentra en el Entry "fecha"
        texto = self.fecha.get()

        # Verifica la longitud de la cadena de texto y procede a borrar el carácter si la longitud es mayor a 0
        if len(texto) == 0:
            pass
        #dd/mm/aaaa
        else: 
            if texto[-1].isdigit():
                self.fecha.delete(len(self.fecha.get())) # En caso de que el último carácter sea un dígito, borra solo el dígito            
            elif texto[-1] == "/":
                self.fecha.delete(len(self.fecha.get())-2, "end") # En caso de que el último carácter sea un "/", borra el "/" y los dígitos que anteceden directamente al carácter "/" 

    ''' Función principal de interacción con la base de datos '''

    # Función principal para realizar los querys e interactuar con la base de datos
    def run_Query(self, query, parameters=(), op_Busqueda=0):
        """
        Ejecuta una consulta SQLite y devuelve el resultado.

        Parámetros:
            query (str): La consulta SQL a ejecutar.
            parameters (tuple, opcional): Los parámetros a enlazar a la consulta. Por defecto es ().
            op_Busqueda (int, opcional): El tipo de búsqueda a realizar. 1 para fetchone, 2 para fetchall. Por defecto es 0.

        Retorna:
            El resultado de la consulta. Si op_Busqueda es 1, devuelve una sola fila como una tupla. Si op_Busqueda es 2, devuelve todas las filas como una lista de tuplas. Si op_Busqueda no es 1 ni 2, devuelve None.

        Levanta:
            sqlite3.Error: Si hay un error al ejecutar la consulta.

        Ejemplo:
            run_Query("SELECT * FROM table WHERE column = ?", ('value',))
        """    
        try:
            with sqlite3.connect(self.db_Name) as conn:
                self.cur = conn.cursor()
                self.cur.execute(query, parameters)
                if op_Busqueda == 1:
                    return self.cur.fetchone()
                elif op_Busqueda == 2:
                    return self.cur.fetchall()
                else:
                    return None  # Si op_Busqueda no es válido
        except sqlite3.Error as e:
            print("Error executing query:", e)
            return None

    ''' Funciones para el llenado de campos dentro del programa '''

    # Función para inicializar el contador del autoincremental dentro del programa utilizando la información dentro de la tabla "Autoincremental"
    def obtener_Autoincrementar_Contador(self):
        """
        Recupera el valor almacenado en la columna "No_Inscripcion_Autoincremental" de la tabla "Autoincremental",
        que se utilizará como contador para asignar el valor del autoincremento al campo "No.Inscripcion".
        
        Retorna:
            int: El valor recuperado de la columna "No_Inscripcion_Autoincremental" si la tabla no está vacía.
            int: 1 si la tabla está vacía, lo que indica que aún no se ha generado ningún registro o inscripción en la tabla "Inscritos".
        """        
        query = "SELECT No_Inscripcion_Autoincremental FROM Autoincremental"
        resultado = self.run_Query(query, (), 1)

        # Condicional que determina que acción ejectuar, dependiendo de si la tabla "Autoincremental" está vacía o no
        # Si la tabla está vacía, significa que aún no se ha generado el primer registro o inscripción en la tabla "Inscritos"
        if resultado == None: 
            return 1
        else:
            return resultado[0]

   # Función para obtener los IDs de los alumnos de la tabla "Alumnos" e insertarlos dentro del combobox "cmbx_Id_Alumno"
    def obtener_Alumnos(self):
        """
        Recupera los IDs de los estudiantes distintos de la tabla "Alumnos" y los agrega al combobox "cmbx_Id_Alumno".

        Esta función ejecuta una consulta SQL para seleccionar los IDs de los estudiantes distintos de la tabla "Alumnos". 
        Los resultados se almacenan en la variable "results". Si la variable "results" no está vacía, la función itera sobre cada resultado y extrae el primer elemento (el ID del estudiante) en la lista "ids_alumnos".
        Finalmente, la lista "ids_alumnos" se asigna como valores del combobox "cmbx_Id_Alumno".

        Parámetros:
            self (objeto): La instancia de la clase a la que pertenece el método.

        Retorna:
            None
        """      

        # Seleccionar los IDs de los alumnos de la columna Id_Alumno de la tabla "Alumnos" y ordenandolos de forma ascendente
        query = "SELECT DISTINCT Id_Alumno FROM Alumnos ORDER BY Id_Alumno"
        resultados = self.run_Query(query, (), 2)
        
        # Si la variable resultados no está vacía, la función itera sobre cada resultado y extrae el primer elemento (el ID del estudiante) en la lista ids_Alumnos. Dicha lista se usa para llenar combobox "cmbx_Id_Alumno"
        if resultados:

            # Generar la lista "ids_Alumnos" la cual contiene los IDs de los alumnos que resultarón de la cosulta 
            ids_Alumnos = [resultado[0] for resultado in resultados]

            # Llenar el combobox "cmbx_Id_Alumno" con los IDs de los alumnos que se encuentran en la lista "ids_Alumnos"
            self.cmbx_Id_Alumno['values'] = ids_Alumnos

    # Función para ingresar los nombres y apellidos correspondientes al ID del estudiante que se encuentre dentro del combobox "cmbx_Id_Alumno" en los Entrys "nombres" y "apellidos"
    def escoger_Alumno(self, event = None):
        """
        Selecciona un estudiante del combobox "cmbx_Id_Alumno" y rellena las entradas "nombres" y "apellidos".

        Parámetros:
            self (objeto): La instancia de la clase a la que pertenece el método.
            event (Event, opcional): El evento que desencadenó la función. Por defecto es None.

        Retorna:
            None
        """        

        # Recuperar el ID del estudiante del combobox "cmbx_Id_Alumno"
        id_Alumno = self.cmbx_Id_Alumno.get()

        # Seleccionar los nombres y apellidos del estudiante de las columnas Nombres y Apellidos de la tabla "Alumnos"
        query = "SELECT Nombres, Apellidos FROM Alumnos WHERE Id_Alumno = ?"
        resultado = self.run_Query(query, (id_Alumno,), 1)
        
        # Si la variable resultado no está vacía, la función rellena las entradas "nombres" y "apellidos" con los valores recuperados de la consulta
        if resultado:
            
            # Llenar las entradas "nombres" y "apellidos" con los valores recuperados de la consulta
            nombre = resultado[0]
            apellidos = resultado[1]

            # Habilita las Entrys "nombres" y "apellidos"
            self.nombres.configure(state="normal")
            self.apellidos.configure(state="normal")

            # Borra todo lo que se encuentra dentro de la Entry "nombres" e inserta el valor de los nombres del estudiante recuperado de la consulta
            self.nombres.delete(0, "end")
            self.nombres.insert(0, nombre)

            # Borra todo lo que se encuentra dentro de la Entry "apellidos" e inserta el valor de los apellidos del estudiante recuperado de la consulta
            self.apellidos.delete(0, "end")
            self.apellidos.insert(0, apellidos)

            # Deshabilita las Entrys "nombres" y "apellidos"
            self.apellidos.configure(state="disabled")
            self.nombres.configure(state="disabled")

    # Función para inicializar el combobox "cmbx_Num_Inscripcion" con los valores que se encuentren en la variable "No_Inscrpcion" de la tabla "Inscritos"
    def obtener_Inscripciones(self):    
        """
        Recupera las inscripciones de la tabla "Inscritos" y las rellena en el combobox "cmbx_Num_Inscripcion".

        Esta función elimina los valores existentes en el combobox "cmbx_Num_Inscripcion" y recupera los números de inscripción distintos de la tabla "Inscritos". 
        Si la tabla no está vacía, la función inserta el siguiente número de inscripción al principio de la lista y lo establece como el valor predeterminado. 
        Si la tabla está vacía, la función establece el valor predeterminado en el siguiente número de inscripción.

        Parámetros:
            self (objeto): La instancia de la clase a la que pertenece el método.

        Retorna:
            None
        """
        
        # Elimina los valores existentes en el combobox "cmbx_Num_Inscripcion"
        self.cmbx_Num_Inscripcion.delete(0, "end")

        # Recupera los números de inscripción distintos de la tabla "Inscritos" ordenados de manera descendiente. 
        query = "SELECT DISTINCT No_Inscripcion FROM Inscritos ORDER BY No_Inscripcion DESC"
        resultados = self.run_Query(query, (), 2)

        # Condicional que determina que función ejecutar, dependiendo de si la tabla "Inscritos" está vacía o no
        if resultados:
            # Caso que ocurre cuándo la tabla "Inscritos" no está vacía

            # Crea una lista de los números de inscripción
            ids_Inscripciones = [result[0] for result in resultados]

            # Inserta el siguiente número de inscripción al principio de la lista y lo establece como el valor predeterminado almacenado en "self.autoincrementar_Contador"
            sig_Num_Inscripcion = self.autoincrementar_Contador
            ids_Inscripciones.insert(0, sig_Num_Inscripcion)

            # Inserta los valores de la lista dentro del combobox "cmbx_Num_Inscripcion"
            self.cmbx_Num_Inscripcion['values'] = ids_Inscripciones

            # 
            id_Predeterminado = sig_Num_Inscripcion
            
        else:
            # Caso que ocurre cuándo la tabla "Inscritos" está vacía

            # Establece el valor predeterminado del combobox "cmbx_Num_Inscripcion" como el valor almacenado en la variable self.autoincrementar_Contador
            id_Predeterminado = self.autoincrementar_Contador

            # Inserta los valores de la variable self.autoincrementar_Contador dentro del combobox "cmbx_Num_Inscripcion"
            self.cmbx_Num_Inscripcion['values'] = [id_Predeterminado]

        # Establece el valor predeterminado del combobox "cmbx_Num_Inscripcion"
        self.cmbx_Num_Inscripcion.set(id_Predeterminado)
    
    # Función para obtener los códigos de los cursos de la tabla "Cursos" e insertarlos dentro del combobox "cmbx_Id_Curso"
    def obtener_Cursos(self):
        """
        Recupera una lista de códigos de curso distintos de la tabla "Cursos" y los rellena en el combobox "cmbx_Id_Curso".

        Esta función ejecuta una consulta SQL para recuperar los códigos de curso distintos de la tabla "Cursos". 
        La consulta ordena los resultados por el código de curso. Si la consulta devuelve algún resultado, la función crea una lista del primer campo de cada fila de resultado. 
        Esta lista se asigna al atributo "values" del combobox "cmbx_Id_Curso".

        Parámetros:
            self (objeto): La instancia de la clase a la que pertenece este método.

        Retorna:
            None
        """

        # Seleccionar los códigos de los cursos de la columna Codigo_Curso de la tabla "Cursos" y ordenandolos de forma ascendente
        query = "SELECT DISTINCT Codigo_Curso FROM Cursos ORDER BY Codigo_Curso"
        resultados = self.run_Query(query, (), 2)

        # Si la variable resultados no está vacía, la función itera sobre cada resultado y extrae el primer elemento (el código del curso) en la lista codigos_Cursos. Dicha lista se usa para llenar combobox "cmbx_Id_Curso"
        if resultados:

            # Genera la lista "codigos_Cursos" la cual contiene los códigos de los curso que resultarón de la cosulta
            codigos_Cursos = [resultado[0] for resultado in resultados]

            # Llena el combobox "cmbx_Id_Curso" con los códigos de los curso que se encuentran en la lista "codigos_Cursos"
            self.cmbx_Id_Curso['values'] = codigos_Cursos
            
    # Función para ingresar la descripción del curso y el horario correspondientes al código del curso que se encuentre dentro del combobox "cmbx_Id_Curso" en los Entrys "descripc_Curso" y "horario"
    def escoger_Curso(self, event= None):
        """
        Selecciona un curso desde el combobox "cmbx_Id_Curso" y completa las entradas "descripc_Curso" y "horario" con la descripción y número de horas correspondientes.

        Parámetros:
            self (objeto): La instancia de la clase a la que pertenece este método.
            event (Event, opcional): El evento que desencadenó la función. Por defecto es None.

        Retorna:
            None
        """
        
        # Recuperar el código del curso del combobox "cmbx_Id_Curso"
        id_Curso = self.cmbx_Id_Curso.get()  
        
        # Seleccionar la descripción del curso y el número de horas del curso de las columnas Descrip_Curso y Num_Horas de la tabla "Cursos"
        query = "SELECT Descrip_Curso, Num_Horas FROM Cursos WHERE Codigo_Curso = ?"
        resultado = self.run_Query(query, (id_Curso,), 1)
        
        # Si la variable resultado no está vacía, la función rellena las entradas "descripc_Curso" y "horario" con los valores recuperados de la consulta
        if resultado:

            # Llenar las entradas "descripc_Curso" y "horario" con los valores recuperados de la consulta
            descrip = resultado[0]
            num_Horas = resultado[1]

            # Habilitar las Entrys "descripc_Curso" y "horario"            
            self.descripc_Curso.configure(state="normal")
            self.horario.configure(state="normal")

            # Borra todo lo que se encuentra dentro de la Entry "descripc_Curso" e inserta el valor de la descripción del curso recuperado de la consulta
            self.descripc_Curso.delete(0, "end")
            self.descripc_Curso.insert(0, descrip)

            # Borra todo lo que se encuentra dentro de la Entry "horario" e inserta el valor del horario del curso recuperado de la consulta
            self.horario.delete(0, "end")
            self.horario.insert(0, num_Horas)
            
            # Deshabilita el Entry "descripc_Curso"
            self.descripc_Curso.configure(state="disabled")

    ''' Funcionalidad para el botón "Guardar" '''

    # Función auxiliar1 botón Guardar: Permite verificar que un alumno no inscriba el mismo curso dos veces en la misma inscripcion
    def verificar_Integridad_Cursos(self, id_Alumno, nombre_Curso, id_Curso, no_Inscripcion):
        """
        Verifica que un estudiante no se inscriba en el mismo curso dos veces en la misma inscripción.

        Parámetros:
            id_Alumno (int): El ID del estudiante.
            nombre_Curso (str): El nombre del curso.
            id_Curso (int): El ID del curso.
            no_Inscripcion (int): El número de inscripción.

        Retorna:
            bool: True si el estudiante ya se ha inscrito en el curso o si el nombre del curso coincide con alguno de los cursos inscritos, False de lo contrario.
        """
        
        # Selecciona los codigos de los cursos de la tabla "Inscritos" del estudiante que se encuentre en la inscripción "no_Inscripcion"
        query = "SELECT Codigo_Curso FROM Inscritos WHERE Id_Alumno = ? AND No_Inscripcion = ?"
        resultados = self.run_Query(query, (id_Alumno, no_Inscripcion), 2) # Trae los codigos del curso en los que esta incrito el alumno
        
        # Convierte la tupla de resultados en una lista de solo contiene los IDs de curso
        id_Cursos_Del_Alumno = [resultado[0] for resultado in resultados] 

        # Crea una lista vacía que almacena los nombres de los curss que se repitan 
        nombres_cursos = []
        
        # Recorre la lista de IDs de curso
        for codigo_Curso in id_Cursos_Del_Alumno: 
            
            # Selecciona la descripción del curso de la tabla "Cursos" correspondiente al del ID del curso ("codigo_Curso")
            query2 = "SELECT Descrip_Curso FROM Cursos WHERE Codigo_Curso = ?"
            resultado2 = self.run_Query(query2, (codigo_Curso,), 1)
            
            # Si el resultado del query no es vacío y adicionalmente la descripción del curso corresponde a "nombre_Curso"
            if resultado2 and resultado2[0] == nombre_Curso:

                # Agrega dicha descripción del curso en la lista "nombres_cursos"
                nombres_cursos.append(resultado2[0]) 

        # Verifica si el ID del curso que se acaba de ingresar es igual a algún ID de los cursos actualmente inscritos por el alumno en dicha inscripción o si el nombre del curso es igual a algún nombre de los cursos inscritos por el alumno
        return id_Curso in id_Cursos_Del_Alumno or nombre_Curso in nombres_cursos 

        
    # Función auxiliar2 botón Guardar: No permite que dos alumnos diferentes inscriban en la misma inscripción 
    def verificar_No_Dos_Alumnos_Misma_Inscripcion(self, no_Inscripcion, id_Alumno):
        """
        Verifica si hay dos estudiantes diferentes inscritos en la misma inscripción.

        Parámetros:
            no_Inscripcion (int): El número de inscripción.
            id_Alumno (int): El ID del estudiante.

        Retorna:
            bool: True si hay dos estudiantes diferentes inscritos en la misma inscripción, False de lo contrario.
        """
        
        # Selecciona el ID del estudiante de la columna "Id_Alumno" de la tabla "Inscritos" con el número de inscripción "no_Inscripcion"
        query = "SELECT Id_Alumno FROM Inscritos WHERE No_Inscripcion = ?"
        resultado = self.run_Query(query, (no_Inscripcion, ), 1)

        # Verifica si el query arroja un resultado "None" o no, que implica que si el número de inscripción se encuentra en la base de datos "Inscritos" o no
        if resultado == None:
            # El número de inscripción no se encuentra aún registrado en la columna "No_Inscripcion" de la base de datos "Inscritos"
            return False 
        else:
            if id_Alumno != resultado[0]:
                # Los dos alumnos son diferentes, lo cuál no es permitido
                return True  
            else:
                # El alumno es el mismo, y no hay problema con la inscripción
                return False 
            
    # Función auxiliar3 botón Guardar: No permite que un determinado alumno pueda tener más de una inscripción
    def verificar_Registro_Alumno(self, no_Inscripcion, id_Alumno):
        """
        Verifica si un estudiante ya está inscrito en otra inscripción.

        Parámetros:
            no_Inscripcion (int): El número de inscripción actual del estudiante.
            id_Alumno (int): El ID del estudiante.

        Retorna:
            bool: True si el estudiante ya está inscrito en otra inscripción, False de lo contrario.
        """
        
        # Selecciona el número de inscripción de la columna "No_Inscripcion" de la tabla "Inscritos" con el ID del estudiante "id_Alumno" y el número de inscripción "no_Inscripcion"
        query = "SELECT No_Inscripcion FROM Inscritos WHERE Id_Alumno = ? AND No_Inscripcion != ?"
        resultado = self.run_Query(query, (id_Alumno, no_Inscripcion), 1)
        
        # Verifica si el query arroja un resultado "None" o no
        if resultado is not None:
            confirmacion = mssg.askquestion("Confirmacion", f"¿Desea inscribir el alumno {id_Alumno} en su registro perteneciente a la inscripción {resultado[0]}?")
            if confirmacion == "yes":
                self.limpiar_Campos()
                for i, curso in enumerate(self.cmbx_Num_Inscripcion["values"]):
                    if resultado[0] == int(curso):
                        self.cmbx_Num_Inscripcion.current(i)
                        self.cmbx_Num_Inscripcion.event_generate("<<ComboboxSelected>>")
                        #self.cmbx_Num_Inscripcion.set(self.cmbx_Num_Inscripcion["values"][i]) esta puede ser otra opcion pra subir las cosas al combobox
                        break
                
                # Establece el valor del ComboBox
                self.mostrar_Datos()
                
                # El alumno está inscrito en otro número de inscripción
                return True  
            else:
                # Lipia los campos
                self.limpiar_Campos()
                
                # El usuario decidió no trasladarse a otra inscripción
                return True  
        return False

    
    # Función para guardar un curso: Permite guardar una curso dentro de la inscripción 
    def guardar_Inscripcion(self, event):
        """
        Guarda una inscripción para un curso.

        Parámetros:
            event (Event): El evento que activó la función.

        Retorna:
            None

        Esta función verifica que todos los campos requeridos para la inscripción estén diligenciados por el usuario. 
        Verifica los Comboboxes "cmbx_Id_Alumno", "cmbx_Id_Curso" y el Entry "fecha" porque al llenarlos se llenan automáticamente el resto del formulario.

        La función luego verifica si el usuario ya ha registrado un curso en la inscripción actual. Si es así, no hace nada. 
        Si no, verifica que el estudiante que se está registrando en la inscripción corresponda al estudiante asociado a la inscripción y no a un estudiante diferente.

        Si el estudiante ya se ha registrado para el curso en la inscripción actual, muestra un mensaje de error. De lo contrario, inserta la nueva inscripción en la tabla "Inscritos".

        Si el número de inscripción actualmente en el Combobox "cmbx_Num_Inscripcion" es igual al valor almacenado en la variable "autoincrementar_Contador", incrementa el valor de "autoincrementar_Contador" 
        y lo inserta en el Combobox "cmbx_Num_Inscripcion".

        Si esta es la primera vez que se guarda una inscripción o registro en la tabla "Inscritos", crea un registro en la columna "No_Inscripcion_Autoincremental" de la tabla "Autoincremental". 
        De lo contrario, actualiza el valor en la columna "No_Inscripcion_Autoincremental" de la tabla "Autoincremental" al valor almacenado en la variable "autoincrementar_Contador".

        Después de guardar la inscripción con éxito, muestra un mensaje de éxito y refresca los datos.
        """

        # Inicialmente, se verifica que el usuario haya diligenciado todos los campos requeridos para formalizar la inscripción: 
        # Se verifican los Combobx "cmbx_Id_Alumno", "cmbx_Id_Curso" y el Entry "fecha" porque al llenar éstos, se llena el resto del formulario 
        id_Alumno = self.cmbx_Id_Alumno.get()
        id_Curso = self.cmbx_Id_Curso.get()
        fecha = self.fecha.get()
        desc_Curso = self.descripc_Curso.get()

        # Número de inscripción que se encuentra actualmente en el combobox "no_Inscripcion"
        no_Inscripcion = self.cmbx_Num_Inscripcion.get()

        # Horario de inscripción 
        horario_Curso = self.horario.get()   
        
        # Valida que la fecha ingresada se encuentre en el formato correcto dd/mm/aaaa
        if re.fullmatch(r"^\d{2}/\d{2}/\d{4}", fecha):       
            # Se verifica que no haya campos importantes vacíos para realizar la inscripción
            if not id_Alumno or not id_Curso or not fecha:
                mssg.showerror("Error", "Por favor, complete todos los campos")
            else:
                if self.verificar_Registro_Alumno(no_Inscripcion, id_Alumno):
                    pass
                else:
                # Verificar que el alumno que está inscribiendo en la inscriçión correspondiente a "no_Inscripcion" es el que corresponde a la inscripción y no un alumnto diferente
                    if self.verificar_No_Dos_Alumnos_Misma_Inscripcion(no_Inscripcion, id_Alumno):  
                        mssg.showerror("Error", f"El código del alumno {id_Alumno} no corresponde al código del alumno correspondiente a la inscripción {no_Inscripcion}")
                    else:
                        # Verificar si el alumno ya inscribió el curso en está inscripción (i.e. no puede haber cursos repetidos para un alumno en la misma inscripción)
                        if self.verificar_Integridad_Cursos(id_Alumno, desc_Curso, id_Curso, no_Inscripcion):
                            mssg.showerror("Error", f"El alumno identificado con código {id_Alumno} ya se encuentra inscrito en el curso con nombre {desc_Curso} para la inscripción No. {no_Inscripcion}")
                        else:
                            # Query que inserta nueva inscripción en la tabla Inscritos
                            query = "INSERT INTO Inscritos (No_Inscripcion, Id_Alumno, Codigo_Curso, Fecha_Inscripcion, Horario) VALUES (?, ?, ?, ?, ?)"
                            parametros = (no_Inscripcion, id_Alumno, id_Curso, fecha, horario_Curso)
                            self.run_Query(query, parametros)

                            # Condicional para verificar si se debe incrementar el contador del autoincrementar
                            if (int(no_Inscripcion) == int(self.autoincrementar_Contador)):
                                # Se incrementa el valor del autoincrementar del No. de inscripción
                                self.autoincrementar_Contador += 1

                                # Se ingresa dicho valor del nuevo autoincrementar dentro del combobox "cmbx_Num_Inscripcion"
                                lista_No_Inscripcion = list(self.cmbx_Num_Inscripcion["values"])
                                lista_No_Inscripcion.insert(0, self.autoincrementar_Contador)
                                self.cmbx_Num_Inscripcion["values"] = lista_No_Inscripcion

                                # Se actualiza el valor almacenado en la columna "No_Inscripcion_Autoincremental" de la tabla "Autoincremental"

                                # Si es la primera vez que se guarda una inscripción o registro en la tabla "Inscritos", entonces se crea el registro dentro de la columna "No_Inscripcion_Autoincremental" de la tabla "Autoincremental"
                                # De lo contrario, se actualiza el valor dentro de la columna "No_Inscripcion_Autoincremental" de la tabla "Autoincremental" al valor que se encuentre almancenado en la variable self.autoincrementar_Contador
                                if (self.autoincrementar_Contador == 2):
                                    query2 = "INSERT INTO Autoincremental (No_Inscripcion_Autoincremental) VALUES (?)"
                                    parametros2 = (self.autoincrementar_Contador, )
                                    self.run_Query(query2, parametros2)
                                else:    
                                    query2 = "UPDATE Autoincremental SET No_Inscripcion_Autoincremental = ?"
                                    parametros2 = (self.autoincrementar_Contador, )
                                    self.run_Query(query2, parametros2)
                        
                            # Mensaje que confirma que la inscripción se ha realizado con éxito
                            mssg.showinfo("Exito", "Inscripcion realizada con exito")

                            self.mostrar_Datos()
                            
                            # Configura los campos luego de realizar una inscripción con éxito 
                            
                            ## Coloca dentro del combobox "cmbx_Num_Inscripcion" el valor almacenado en la variable no_Inscripcion
                            self.cmbx_Num_Inscripcion.set(no_Inscripcion)

                            ## Limpia el combobox "cmbx_Id_Alumno"
                            self.cmbx_Id_Curso.configure(state="normal")
                            self.cmbx_Id_Curso.delete(0, "end")
                            self.cmbx_Id_Curso.configure(state="readonly")

                            ## Limpia el Entry "descripc_Curso"
                            self.descripc_Curso.configure(state="normal")
                            self.descripc_Curso.delete(0, "end")
                            self.descripc_Curso.configure(state="disabled")

                            ## Limpia el Entry "horario"
                            self.horario.configure(state="normal")
                            self.horario.delete(0, "end")
                            self.horario.configure(state="disabled")

        else: 
            mssg.showerror("Error", "Digite una fecha en el formato correcto dd/mm/aaaa")
                    
    ''' Funcionalidad para el botón "Buscar" '''
    
    # Función para mostrar datos en el Treeview: Permite mostrar los datos en el Treeview de la interfaz gráfica
    def mostrar_Datos(self, event = None):
        """
        Trae los registros de la tabla Inscritos basándose en el número de inscripción seleccionado en el combobox "cmbx_Num_Inscripcion" y los muestra en el Treeview.
    
        Parámetros:
            event (opcional): El evento que desencadenó la función. Predeterminado a None.
    
        Retorna:
            None
    
        Esta función recupera el número de inscripción del combobox `cmbx_Num_Inscripcion` y ejecuta una consulta SQL para recuperar los datos correspondientes de la tabla `Inscritos`. 
        Si la consulta devuelve un resultado, la función borra el Treeview, lo llena con los datos recuperados y actualiza el combobox `cmbx_Id_Alumno` con el valor correspondiente. 
        También actualiza los comboboxes `cmbx_Id_Curso` y `descripc_Curso` con los datos recuperados. Si la consulta no devuelve un resultado, se muestra un mensaje de advertencia.
        """
        
        # Recuperar el número de inscripción del combobox "cmbx_Num_Inscripcion"
        no_Inscripcion = self.cmbx_Num_Inscripcion.get()

        # Seleccionar el ID_Alumno, Codigo_Curso, Horario, Fecha_Inscripcion de la tabla "Inscritos" donde No_Inscripcion = no_Inscripcion
        query = "SELECT Id_Alumno, Codigo_Curso, Horario, Fecha_Inscripcion FROM Inscritos WHERE No_Inscripcion = ?"
        resultados = self.run_Query(query, (no_Inscripcion,), 2)
    
        # Si la consulta no es vacía entonces llena el TreeView con los resultados de la consulta, de lo contrario, muestra un mensaje de error
        if resultados:
            
            # Limpia el Treeview
            self.treeInscritos.delete(*self.treeInscritos.get_children())

            # Llenar el Treeview con cada registro que se trajo de la consulta
            for datos_DB in resultados:          
                codigo_Curso = (datos_DB[1],) # Código del curso asociado a dicho registro 

                # Seleccionar el Descrip_Curso de la tabla "Cursos" donde Codigo_Curso = Codigo_Curso del registro
                query2 = "SELECT Descrip_Curso FROM Cursos WHERE Codigo_Curso = ?"
                resultado2 = self.run_Query(query2, codigo_Curso, 1)

                # Llenar el Treeview con cada registro que se trajo de la consulta
                self.treeInscritos.insert("", 0, text=datos_DB[0], values = (datos_DB[1], resultado2[0], datos_DB[2]))   
            
            # Llenar el Combobox "cmbx_Id_Alumno" con el ID_Alumno del registro que se obtuvo de la consulta 
            self.cmbx_Id_Alumno.configure(state= "normal")
            self.cmbx_Id_Alumno.delete(0, "end")
            self.cmbx_Id_Alumno.insert(0, datos_DB[0]) # Es correcto, porque el cada inscripción uno y solo un estudiante 
            self.cmbx_Id_Alumno.configure(state= "disabled")

            # Llenar los Entrys "nombres" y "apellidos" con los nombres y apellidos del alumno correspondiente a la inscripción
            self.escoger_Alumno()

            # Limpia el combobox "cmbx_Id_Curso"
            self.cmbx_Id_Curso.configure(state="normal")
            self.cmbx_Id_Curso.delete(0, "end")

            # Habilita los Entrys "descripc_Curso" y "horario"
            self.descripc_Curso.configure(state="normal")
            self.horario.configure(state="normal")

            # Limpia el Entry "descripc_Curso"
            self.descripc_Curso.delete(0, "end")

            # Habilita el combobox "cmbx_Id_Curso" en modo de solo lectura ("readonly")
            self.cmbx_Id_Curso.configure(state="readonly")

            # Deshabilita el Entry "descripc_Curso"
            self.descripc_Curso.configure(state="disabled")

            # Llenar el Entry "fecha" con la fecha de la inscripción 
            self.fecha.delete(0, "end")
            self.fecha.insert(0, datos_DB[3])
        else:
            mssg.showerror("Advertencia", f"No se encuentra ninguna inscripción con el No. de inscripción: {self.cmbx_Num_Inscripcion.get()}")

    ''' Funcionalidad para el botón "Eliminar" '''

    # Función para crear ventana emergente que pregunta si se debe eliminar un curso o toda la inscripción
    def crear_Ventana_Eliminar(self, event):
        """
        Crea una nueva ventana para eliminar datos.

        Parámetros:
            event (Event): El evento que activó la función.

        Retorna:
            None

        Esta función crea una nueva ventana para eliminar datos. Establece el título de la ventana a "Borrar datos" y configura su ancho y alto. 
        Luego centra la ventana en la pantalla. La ventana no es redimensionable.

        La función crea un marco de etiqueta con el texto "¿Qué desea realizar?" y establece su color de primer plano a "RoyalBlue". 
        Luego empaqueta el marco de etiqueta con un relleno de 10 píxeles en la parte superior e izquierda.

        La función crea dos botones de opción, "Borrar un curso" y "Borrar toda la inscripción", y los asocia con la variable `self.opcion`. 
        Los botones de opción tienen diferentes valores (1 y 2) y tienen sus colores de primer plano y activo establecidos en "RoyalBlue" y "red2", respectivamente.

        La función crea un botón con el texto "Borrar" y lo enlaza a la función `self.eliminar_Cursos`. El botón
        """

        # Creacion de la ventana
        self.ventana_Borrar = tk.Toplevel()
        self.ventana_Borrar.config(width= 300, height= 150)
        
        # No permitir cambiar tamaño de la ventana
        self.ventana_Borrar.resizable(False, False)

        # Configuración adicional de la ventana
        self.centrar_Pantalla(self.ventana_Borrar, 300, 150)
        self.ventana_Borrar.iconbitmap(PATH + ICON) # Icono de la ventana 
        self.ventana_Borrar.title("Borrar datos")
        
        # Creación labelframe        
        self.marco = tk.LabelFrame(self.ventana_Borrar, text = "¿Que desea realizar?", fg="RoyalBlue")
        self.marco.pack(pady=10, padx=10)

        # Crear variable para los radiobuttons
        self.opcion = tk.IntVar()

        # Crear radiobuttons

        ## Radiobutton1
        self.radiobutton1 = tk.Radiobutton(self.marco, text="Borrar un curso", variable= self.opcion, value= 1, 
                                           foreground = "RoyalBlue", activeforeground="red2"
                                           )       
        self.radiobutton1.pack(anchor="w", pady=5)
        
        ## Radiobutton2
        self.radiobutton2 = tk.Radiobutton(self.marco, text="Borrar toda la inscripción", variable= self.opcion, value=2,
                                           foreground = "RoyalBlue", activeforeground="red2"
                                           )
        self.radiobutton2.pack(anchor="w", pady=5)
        
        # Crear el botón de borrar dentro de la ventana emergente "ventana_Borrar"
        self.btn_Vna_Borrar = ttk.Button(self.ventana_Borrar, name="btn_Vna_Borrar")
        self.btn_Vna_Borrar.configure(text="Borrar")

        # Asociar el evento de click izquierdo del botón borrar de la pestaña emergente la función "self.eliminar_Cursos"
        self.btn_Vna_Borrar.bind("<Button-1>", self.eliminar_Cursos)
        self.btn_Vna_Borrar.pack()
        
        # Moverse hacia la ventana borrar 
        self.ventana_Borrar.after(100, self.ventana_Borrar.focus)
        
        # Mantenerse en la ventana borrar
        self.ventana_Borrar.grab_set()

    # Función para eliminar un curso o toda la inscripción completa
    def eliminar_Cursos(self, event):
        """
        Esta función se utiliza para eliminar un curso o eliminar por completo la inscripción.
        Se activa mediante un evento de mouse.
        
        Parámetros:
            event (Event): El evento de mouse que activa la función.
        
        Retorna:
            None
        """
        
        # Que opcion de raditbutton está seleccionando: Si la opción 1, la opción 2 o ninguno
        opcion = self.opcion.get()
        
        #verificar si esta seleccionado una opcion en la ventana borrar
        if opcion:
            #verificar que opcion esta seleccionado en la ventana borrar
            if opcion == 1:
                #Eliminar un curso
                #verificar si esta seleccionado un curso en el treewiew
                if self.treeInscritos.selection():
                    
                    # Seleccion es el índice que denota el registro que actualmente se encuentra seleccionado en el TreeView
                    seleccion = self.treeInscritos.selection()[0]

                    # Recuperar los valores que se encuentran en el registro seleccionado en el TreeView
                    seleccion_Values = self.treeInscritos.item(seleccion, "values")

                    # Ingresa la información recuperada del registro seleccionado en el TreeView en los Entrys correspondientes
                    codigo_Curso = seleccion_Values[0]
                    nombre_Curso = seleccion_Values[1]

                    # Mensaje de confirmación de si se quiere o no eliminar el curso
                    mensaje = f"¿Desea eliminar este curso: ({codigo_Curso}) {nombre_Curso}?"
                    confirmacion = mssg.askokcancel("Confirmacion", mensaje)

                    # Verificar si desea o no eliminar el curso 
                    if confirmacion:

                        # Obtener el número de inscripción del combobox "cmbx_Num_Inscripcion"                    
                        num_Incripcion = self.cmbx_Num_Inscripcion.get()

                        # Recuperar la cantidad de inscripciones de cursos de la tabla Inscritos del número de inscripción "num_Incripcion"
                        query1 = "SELECT COUNT(No_Inscripcion) FROM Inscritos WHERE No_Inscripcion = ?"
                        parametros1 = (num_Incripcion,)
                        cantidad_Inscripciones = self.run_Query(query1, parametros1, 1)[0]

                        # Eliminar el curso de la tabla Inscritos
                        query2 = "DELETE FROM Inscritos WHERE No_Inscripcion = ? AND Codigo_Curso = ?"
                        parametros2 = (num_Incripcion, codigo_Curso)
                        borrar = self.run_Query(query2, parametros2)    

                        # Busqueda para verificar si se elimino el curso o no
                        query3 = "SELECT COUNT(No_Inscripcion) FROM Inscritos WHERE No_Inscripcion = ? AND Codigo_Curso = ?"
                        confirmacion_Eliminar = self.run_Query(query3, parametros2, 1)[0]
                        
                        # Confirmar si se elimino el curso
                        if confirmacion_Eliminar == 0:
                            mensaje = f"El curso ({codigo_Curso}) {nombre_Curso} ha sido borrado con exito."
                            # Condicional para saber si se elimina toda la inscripción o solo el curso
                            if cantidad_Inscripciones == 1:
                                # Para destruir la ventana emergente
                                self.ventana_Borrar.destroy()
                                mssg.showinfo("Exito", mensaje)

                                # Limpiar los campos
                                self.limpiar_Campos()

                                # Para actualizar los datos del combobox "cmbx_Num_Inscripcion"
                                self.obtener_Inscripciones()
                            else:
                                self.treeInscritos.delete(seleccion)
                                
                                # Para destruir la ventana emergente
                                self.ventana_Borrar.destroy()
                                mssg.showinfo("Exito", mensaje)
                                
                        else:
                            mensaje = f"No se ha podido borrar el curso ({codigo_Curso}) {nombre_Curso}."
                            
                            # Para destruir la ventana emergente
                            self.ventana_Borrar.destroy()
                            mssg.showerror("Error", mensaje)
                        
                else:
                    # Para destruir la ventana emergente
                    self.ventana_Borrar.destroy()
                    mssg.showerror("Error", "Seleccione un curso")
            # Eliminar todos los cursos
            elif opcion == 2:
                # Creación de mensaje de confirmación
                confirmacion = mssg.askokcancel("Confirmacion", "¿Desea eliminar todos los cursos?")
                if confirmacion:
                    # Recupear el número de inscripción del combobox "cmbx_Num_Inscripcion"
                    num_Incripcion = self.cmbx_Num_Inscripcion.get()
                    
                    # Recuperar la cantidad de inscripciones de cursos de la tabla Inscritos del número de inscripción "num_Incripcion"
                    query = "SELECT COUNT(No_Inscripcion) FROM Inscritos WHERE No_Inscripcion = ?"
                    parametro = (num_Incripcion,)
                    result = self.run_Query(query, parametro, 1)[0]

                    # Verificar si el número de inscripción tiene cursos inscritos 
                    if result >= 1:
                        
                        # Eliminar todos los registros asociados al número de inscripción "num_Incripcion" de la tabla "Inscritos"
                        query = "DELETE FROM Inscritos WHERE No_Inscripcion = ?"
                        parametro = (num_Incripcion,)
                        ejecucion = self.run_Query(query, parametro)

                        # Mensaje de confirmación de si se han eliminado todos los cursos
                        mensaje = f"Se han borrado todos los cursos de la inscripcion No.{num_Incripcion}"

                        # Limpiar los campos
                        self.limpiar_Campos()

                        # Para actualizar los datos del combobox "cmbx_Num_Inscripcion"
                        self.obtener_Inscripciones()

                        # Para destruir la ventana emergente
                        self.ventana_Borrar.destroy()
                        mssg.showinfo("Exito", mensaje)
                    else:
                        # Mensaje de error en caso de que el número de inscripción no tenga cursos inscritos
                        mensaje = f"El numero de inscripcion {num_Incripcion} no tiene cursos inscritos."
                        
                        # Para destruir la ventana emergente
                        self.ventana_Borrar.destroy()
                        mssg.showerror("Error", mensaje)

        else:
           # Mensaje en caso de que no se haya seleccionado una opción del radiobutton
           mssg.showerror("Error", "Seleccione una opcion")
    
    ''' Funcionalidad para el botón "Editar" '''

    # Función que se ejecuta cuando se oprime el botón editar: Subir los datos del Treeview al entry e inhabilita los botones guardar, buscar. Habilita el botón "confirmar" y siguen habilitando el botón cancelar
    def editar_Curso(self, event):
        """
        Edita el curso seleccionado en el TreeView.
        
        Parámetros:
            event (Event): El evento que activó la función.
        
        Retorna:
            None
        
        Esta función se llama cuando el usuario presiona el botón "Editar". 
        Verifica si se ha seleccionado un curso en el TreeView. Si se ha seleccionado un curso, configura los combobox y entrys para permitir la edición. 
        Luego, recupera los valores del curso seleccionado y actualiza los campos de combobox y entry con esos valores. 
        Los campos de combobox y entry se deshabilitan para evitar que se realicen más ediciones. Los botones de búsqueda, eliminación y guardado también se deshabilitan. 
        El botón "Confirmar" se habilita y se enlaza a la función `confirmar_Editar`. El combobox se establece en modo solo lectura. Si no se ha seleccionado ningún curso, se muestra un mensaje de error.
        """

        # Verificar si se ha seleccionado un curso en el TreeView, de lo contrario arroja un mensaje de error. 
        if self.treeInscritos.selection():

            # Recupera los valores del registro que actualmente se encuentra seleccionado en el TreeView y configura los Entrys y combobox correspondientes para la edición 

            ## Configura el combobox "cmbx_Id_Curso" en estado editable
            self.cmbx_Id_Curso.configure(state="normal")

            ## Seleccion es el índice que denota el registro que actualmente se encuentra seleccionado en el TreeView
            seleccion = self.treeInscritos.selection()[0]

            ## Recuperar los valores que se encuentran en el registro seleccionado en el TreeView
            seleccion_Values = self.treeInscritos.item(seleccion, "values")

            ## Configura el entry "descripc_Curso" en estado editable
            self.descripc_Curso.configure(state="normal")
            
            ## Ingresa la información recuperada del registro seleccionado en el TreeView en los Entrys correspondientes
            self.curso_Actual = seleccion_Values[0]
            self.desc_Curso_Actual = seleccion_Values[1]
            self.horario_Actual = seleccion_Values[2]

            ## Limpia el combobox "cmbx_Id_Curso" y lo rellena con el valor que se encuentra en la variable "curso_Actual"
            self.cmbx_Id_Curso.delete(0, "end")
            self.cmbx_Id_Curso.insert(0, self.curso_Actual)

            ## Limpia el Entry "descripc_Curso" y lo rellena con el valor que se encuentra en la variable "desc_Curso_Actual". Luego desahabilita el Entry.
            self.descripc_Curso.delete(0, "end")
            self.descripc_Curso.insert(0, self.desc_Curso_Actual)
            self.descripc_Curso.configure(state="disabled")
            
            ## Limpia el Entry "horario" y lo rellena con el valor que se encuentra en la variable "horario_Actual"
            self.horario.delete(0, "end")
            self.horario.insert(0, self.horario_Actual)

            # Con el ID del curso que se encuentra en el combobox "cmbx_Id_Curso" se llena los Entrys "descripc_Curso" y "horario"
            self.cmbx_Id_Curso.bind("<<ComboboxSelected>>", self.escoger_Curso)

            # Bloquear los botones, Entrys y comboboxes
            
            ## Se desahabilita el Entry "descripc_Curso"
            self.descripc_Curso.configure(state="disabled")

            ## Se deshabilita el botón "Buscar" 
            self.btnBuscar.configure(state="disabled")
            self.btnBuscar.unbind("<Button-1>")

            ## Se deshabilita el botón "Eliminar" 
            self.btnEliminar.configure(state="disabled")
            self.btnEliminar.unbind("<Button-1>")

            ## Se deshabilita el botón "Guardar" 
            self.btnGuardar.configure(state="disabled")
            self.btnGuardar.unbind("<Button-1>")

            ## Se deshabilita el botón "Editar"
            self.btnEditar.configure(text="Confirmar", style="Boton.TButton")
            self.btnEditar.unbind("<Button-1>")

            ## Se modifica el botón "Editar" y se habilita ahora con el nombre de botón "Confirmar"
            self.btnEditar.bind("<Button-1>", self.confirmar_Editar)

            ## Se habilita el combobox "cmbx_Id_Curso" en el estado de solo lectura ("readonly")
            self.cmbx_Id_Curso.configure(state="readonly")
        else:
            mssg.showerror("Error", "Seleccione un curso")

    # Función que se ejecuta cuando se oprime el botón confirmar: Hacer el cambio del curso en la base de datos y en el Treeview
    def confirmar_Editar(self, event):
        """
        Actualiza la información del curso de un estudiante en la tabla Inscritos.
        
        Parámetros:
            event (Event): El evento que desencadenó la función.
        
        Retorna:
            None
        
        Levanta:
            Exception: Si hay un error al ejecutar la consulta a la base de datos.
        
        Adicionalmente la función:
            - Actualiza la información del curso de un estudiante en la tabla Inscritos.
            - Actualiza el texto del botón "Editar" y las enlaces.
            - Habilita o deshabilita los botones en función de la validez de la entrada.
            - Actualiza el Treeview con la nueva información del curso.
        """
        
        # Obtener los valores que se encuentran en los comboboxes "cmbx_Id_Alumno" y "cmbx_Id_Curso" y Entry "horario"
        id_Alumno = self.cmbx_Id_Alumno.get()
        nuevo_Codigo_Curso = self.cmbx_Id_Curso.get()
        nuevo_horario = self.horario.get()

        # Obtener los valores que se encuentran en los combobox "cmbx_Num_Inscripcion" y Entrys "descripc_Curso" y "fecha"
        no_Inscripcion = self.cmbx_Num_Inscripcion.get()
        desc_Curso_Nuevo = self.descripc_Curso.get()
        fecha_Nueva = self.fecha.get()

        # Actualiza la información del curso que se edito y se actualizó en la tabla Inscritos
        query1 = "UPDATE Inscritos SET Codigo_Curso = ?, Horario = ?, Fecha_Inscripcion = ? WHERE No_Inscripcion = ? AND Codigo_Curso = ? AND Horario = ?"
        parametros1 = (nuevo_Codigo_Curso, nuevo_horario, fecha_Nueva, no_Inscripcion, self.curso_Actual, self.horario_Actual)
        
        # Verifica que todos los campos necesarias para guardar la edición del curso estén llenos 
        #exp 
        if re.fullmatch(r"^\d{2}/\d{2}/\d{4}", fecha_Nueva):  
            if not id_Alumno or not nuevo_Codigo_Curso or not fecha_Nueva:
                mssg.showerror("Error", "Por favor, complete todos los campos")
            else:
                # Verifica que no esté editando el mismo curso original
                if self.verificar_Integridad_Cursos(id_Alumno, desc_Curso_Nuevo, nuevo_Codigo_Curso,  no_Inscripcion):
                    mssg.showerror("Error", f"El alumno identificado con código {id_Alumno} ya se encuentra inscrito en el curso {desc_Curso_Nuevo} para la inscripción No. {no_Inscripcion}")
                else:
                    # Mensaje informativo de si la edición del curso fue exitosa o no 
                    try:
                        self.run_Query(query1, parametros1)
                        mssg.showinfo("Estado", f"La modificacion del curso {self.desc_Curso_Actual} por el curso {desc_Curso_Nuevo} ha sido realizada con exito")
                    except Exception as e:
                        mssg.showerror("Error", e)
                    
                    # Cambiar de nuevo el nombre del botón "Editar" de "Confirmar" de nuevo a "Editar"
                    self.btnEditar.configure(text="Editar", style="TButton")
                    
                    # Volver a habilitar los botones de la interfaz gráfica

                    ## Habilitar el botón "Editar"
                    self.btnEditar.unbind("<Button-1>")
                    self.btnEditar.bind("<Button-1>", self.editar_Curso)

                    ## Habilitar el botón "Buscar"
                    self.btnBuscar.configure(state="normal")
                    self.btnBuscar.bind("<Button-1>", self.mostrar_Datos)

                    ## Habilitar el botón "Guardar"
                    self.btnGuardar.configure(state="normal")
                    self.btnGuardar.bind("<Button-1>", self.guardar_Inscripcion)

                    ## Habilitar el botón "Eliminar"
                    self.btnEliminar.configure(state="normal")
                    self.btnEliminar.bind("<Button-1>", self.crear_Ventana_Eliminar)

                    ## Mostrar todos los cursos inscritos en la inscripción en el TreeView
                    self.mostrar_Datos()
        else: 
            mssg.showerror("Error", "Digite una fecha en el formato correcto dd/mm/aaaa")

            
    ''' Funcionalidad para el botón "Cancelar" '''

    # Función para cancelar: Limpia los campos de la interfaz gráfica
    def limpiar_Campos(self, event = None):
        """
        Limpia todos los campos en la interfaz gráfica y restablece el estado de varios botones y combobox.
        
        Parámetros:
            event (opcional): El evento que desencadenó la función.
        
        Retorna:
            None
        """

        # 1. Limpieza de los campos 

        ## Se limpia el campo "cmbx_Id_Alumno"
        self.cmbx_Id_Alumno.configure(state="readonly")
        self.cmbx_Id_Alumno.set("")

        ## Se limpia el campo "fecha"
        self.fecha.configure(state="normal")
        self.fecha.delete(0, "end")

        ## Se limpia el campo "nombres"
        self.nombres.configure(state="normal")
        self.nombres.delete(0, "end")
        self.nombres.configure(state="disabled")

        ## Se limpia el campo "apellidos"
        self.apellidos.configure(state="normal")
        self.apellidos.delete(0, "end")
        self.apellidos.configure(state="disabled")

        ## Se limpia el campo "cmbx_Id_Curso"
        self.cmbx_Id_Curso.configure(state="readonly")
        self.cmbx_Id_Curso.set("")

        ## Se limpia el campo "descripc_Curso"
        self.descripc_Curso.configure(state="normal")
        self.descripc_Curso.delete(0, "end")
        self.descripc_Curso.configure(state="disabled")

        ## Se limpia el campo "horario"
        self.horario.configure(state="normal")
        self.horario.delete(0, "end")
        self.horario.configure(state="disabled")

        ## Se limpia el campo "cmbx_Num_Inscripcion"
        self.cmbx_Num_Inscripcion.configure(state="normal")
        self.cmbx_Num_Inscripcion.delete(0, "end")

        # 2. Limpieza del TreeView
        self.treeInscritos.delete(*self.treeInscritos.get_children())
        self.treeInscritos.selection_remove()

        # 3. Rehabilitación de los botones

        ## Rehabilitar el botón "btnBuscar"
        self.btnBuscar.configure(state="normal")
        self.btnBuscar.bind("<Button-1>", self.mostrar_Datos)

        ## Rehabilitar el botón "btnGuardar"
        self.btnGuardar.configure(state="normal")
        self.btnGuardar.bind("<Button-1>", self.guardar_Inscripcion)

        ## Rehabilitar el botón "btnEditar"
        self.btnEditar.configure(state="normal")
        self.btnEditar.configure(text="Editar")
        self.btnEditar.unbind("<Button-1>")
        self.btnEditar.bind("<Button-1>", self.editar_Curso)
        self.btnEditar.configure(text="Editar", style="TButton")

        ## Rehabilitar el botón "btnEliminar"
        self.btnEliminar.configure(state="normal")
        self.btnEliminar.bind("<Button-1>", self.crear_Ventana_Eliminar)

        # 4. Añadir al combobox "cmbx_Num_Inscripcion" el valor de la siguiente inscripción disponible
        
        ## Añadir al combobox "cmbx_Num_Inscripcion" el valor de la siguiente inscripción disponible
        self.cmbx_Num_Inscripcion.set(self.cmbx_Num_Inscripcion["values"][0])

        ## Disabilitar el combobox cmbx_Num_Inscripcion para que no pueda ser editado
        self.cmbx_Num_Inscripcion.configure(state="readonly")     
           
# Ejecución del programa
if __name__ == "__main__":
    app = Inscripciones()
    app.run()
