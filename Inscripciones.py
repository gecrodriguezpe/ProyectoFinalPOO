# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
from pathlib import Path
from datetime import datetime
from idlelib.tooltip import Hovertip


# Directorio del archivo Inscripciones.py
PATH = str((Path(__file__).resolve()).parent)

# Directorio donde se encuentra el icono principal del programa
ICON = r"/img/buho.ico"

# Directorio donde se encuentra el reloj
RELOJ = r"/img/reloj.png"

# Directorio donde se encuentra la base de datos 
# DB = r"/db/Inscripciones.db"
DB = r"/db/Inscripciones_pruebas.db"


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

        ''' Widgets: Elementos de la Ventana principal del programa '''

        # Creación del frame del programa
        self.frm_1 = tk.Frame(self.win, name="frm_1")
        self.frm_1.configure(background="#f7f9fd", height=600, width=800)
        
        #Label No. Inscripción
        self.lblNumInscripcion = ttk.Label(self.frm_1, name="lblNumInscripcion")
        self.lblNumInscripcion.configure(background="#f7f9fd",font="{Arial} 11 {bold}",
                                        justify="left",state="normal",
                                        takefocus=False,text='No.Inscripción')
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
        self.fecha = ttk.Entry(self.frm_1, name="fecha", validate="key", validatecommand=(self.frm_1.register(self.valida_Fecha_Entrada), "%P")) # Solo permite ingresar digitos o "/" en el try "fecha"
        self.fecha.configure(justify="center")
        self.fecha.place(anchor="nw", width=90, x=680, y=80)
        self.fecha.bind("<KeyRelease>", self.valida_Formato_Fecha)
        self.fecha.bind("<KeyRelease>", self.validar_fecha, "+")
        self.fecha.bind("<BackSpace>", lambda _: self.fecha.delete(len(self.fecha.get())), "end")

        #Boton Reloj
        self.img_Boton=tk.PhotoImage(file=PATH + RELOJ)
        self.btnReloj = ttk.Button(self.frm_1, name="btnreloj", image=self.img_Boton,compound="center")
        self.btnReloj.place(width=23, height=23, x=771, y=79)
        
        # Ajustar la posición de la imagen dentro del botón utilizando la opción padding
        self.btnReloj.image = self.img_Boton.subsample(2, 2)  # Reducir el tamaño de la imagen para que quepa en el botón
        self.btnReloj.config(padding=(-10, -10, -10, -10))
        self.btnReloj.bind("<Button-1>", self.obtener_Fecha)
        self.msj_btnReloj = Hovertip(self.btnReloj, text="Presione para obtener la fecha actual", hover_delay=50)

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

        #Entry Curso
        self.cmbx_Id_Curso = ttk.Combobox(self.frm_1, name="id_curso", state="readonly")
        self.cmbx_Id_Curso.place(anchor="nw", width=166, x=100, y=185)
        self.obtener_Cursos() # Permite obtener la lista de códigos de los cursos de la tabla Cursos e introducirla al combobox "cmbx_Id_Alumno"
        self.cmbx_Id_Curso.bind("<<ComboboxSelected>>", self.escoger_Curso)    # Asignar al evento de selección del código del curso en el combobox "cmbx_Id_Alumno" la función "escoger_Curso"

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

        ## Cambiar a un combobox que contenga la lista predeterminada de horarios permitidos. La lista se crea manualmene en el programa cuando se instancie la clase
        ## Lo que se puede hacer es colocar de manera automática el número de horas o el número de créditos directo en el Treeview

        #Entry del Horario
        self.horario = ttk.Entry(self.frm_1, name="entry3")
        self.horario.configure(justify="left", width=166)
        self.horario.place(anchor="nw", width=100, x=680, y=185)

        ''' Botones de la Aplicación '''

        # Estilo para los botones default
        self.botones = ttk.Style()
        self.botones.configure("TButton", foreground = "RoyalBlue")
        self.botones.map("TButton", foreground=[("active", "red2")])

        #Estilo para los botones alterno
        estilo = ttk.Style()
        estilo.map("Boton.TButton", foreground=[("active", "black")])
        estilo.configure("Boton.TButton", foreground="red")
        
        #Boton Buscar
        self.btnBuscar = ttk.Button(self.frm_1, name="btnbuscar")
        self.btnBuscar.configure(text='Buscar')
        self.btnBuscar.place(anchor="nw", x=155, y=260)
        self.btnBuscar.bind("<Button-1>", self.mostrar_Datos)
        
        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name="btnguardar")
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor="nw", x=255, y=260)
        self.btnGuardar.bind("<Button-1>", self.guardar_Inscripcion)
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name="btneditar")
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=355, y=260)
        self.btnEditar.bind("<Button-1>", self.editar_Curso)

        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name="btneliminar")
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor="nw", x=455, y=260)
        self.btnEliminar.bind("<Button-1>", self.crear_Ventana_Eliminar)
        
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name="btncancelar")
        self.btnCancelar.configure(text='Cancelar')
        self.btnCancelar.place(anchor="nw", x=555, y=260)
        self.btnCancelar.bind("<Button-1>", self.limpiar_Campos)

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

    ## Función de validación del formato de la fecha
    def obtener_Fecha(self,event = None):
        """
        Elimina el contenido actual del widget `self.fecha` y inserta la fecha actual en el formato "ddmmyyyy". 
        Llama al método `self.valida_Formato_Fecha()` después de cada inserción de caracter.

        Parámetros:
            event (Event): Parámetro opcional de evento.

        Retorna:
            None
        """

        self.fecha.delete(0, "end")
        ahora = datetime.now().strftime("%d%m%Y")
        for d in ahora:
            self.fecha.insert("end", d)
            self.valida_Formato_Fecha()

# Función que valida que dentro del Entry "fecha" solo se puedan insertar dígitos o barras diagonales
    def valida_Fecha_Entrada(self, text):
        """
        Valida la entrada de texto para asegurarse de que solo contenga dígitos o barras diagonales.

        Parámetros:
            text (str): El texto de entrada a validar.

        Retorna:
            bool: True si el texto de entrada es válido, False en caso contrario.
        """        
        return all(char.isdigit() or char == "/" for char in text)
    
    def valida_Formato_Fecha(self, event = None):  
        """
        Configura el formato correcto en el campo Fecha dd/mm/aaaa.

        Esta función verifica la longitud de la fecha en el widget de entrada `fecha` y inserta un carácter "/" en la posición adecuada si la longitud es de 2 o 5. Si la longitud es mayor a 10, muestra un mensaje de error y elimina los caracteres desde la posición 10 hasta el final del widget de entrada.

        Parámetros:
            event (Event, opcional): El evento que activó la función. Por defecto es None.

        Retorna:
            None
        """

        fecha = self.fecha.get()

        if len(fecha) in [2,5]:
            self.fecha.insert(fecha.index(" ") + 1 if " " in fecha else len(fecha), "/")
        elif len(fecha) > 10: 
            mssg.showerror("Error","Solo es permitido un máximo de 10 carácteres")
            self.fecha.delete(10, "end")

    ## Función que valida la fecha
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
        #siempre va a retornar false si algo en la fecha no es valido
        if a <= 1754:   # Verifica si el año es válido (superior a 1754)
            mssg.showerror("Error","Solo es permitido un año superior a 1754")  
            return False  
        if not (1 <= m <= 12):  # Verifica si el mes está dentro del rango válido (1 a 12)
            mssg.showerror("Error","Solo es permitido un mes entre 1 y 12")
            return False
        if m in (1, 3, 5, 7, 8, 10, 12):     # Verifica los meses que tienen 31 días
            if not (1 <= d <= 31):  # Verifica si el día está dentro del rango válido para estos meses (1 a 31)
                mssg.showerror("Error",f"Solo es permitido un día entre 1 y 31 para el mes {m}")
                return False
        elif m == 2: # Verifica si el mes es febrero
            biciesto = a % 4 == 0 and (a % 100 != 0 or a % 400 == 0) # Calcula si el año es bisiesto
            if biciesto:  # Si el año es bisiesto
                if not (1 <= d <= 29): # Verifica si el día está dentro del rango válido para febrero en un año bisiesto (1 a 29)
                    mssg.showerror("Error",f"Solo es permitido un día entre 1 y 29 para el mes {m} de un año bisiesto")
                    return False
            else:  # Si el año no es bisiesto
                if not (1 <= d <= 28): # Verifica si el día está dentro del rango válido para febrero en un año no bisiesto (1 a 28)
                    mssg.showerror("Error",f"Solo es permitido un día entre 1 y 28 para el mes {m} de un año no bisiesto")
                    return False
        else: # Para los meses restantes (30 días)
            if not (1 <= d <= 30): # Verifica si el día está dentro del rango válido para estos meses (1 a 30)
                mssg.showerror("Error",f"Solo es permitido un día entre 1 y 30 para el mes {m}")
                return False
        return True # Retorna True indicando que la fecha es válida
    
    def validar_fecha(self, event = None):
        """
        Valida la fecha dada dividiéndola en componentes de día, mes y año y llamando a la función `validacion_Dias_Mes_Año` con esos componentes. Si la fecha no está en el formato dd/mm/aaaa o si la fecha es inválida, borra el contenido del widget `fecha`.

        Parámetros:
            event (Event, opcional): El evento que activó la función. Por defecto es None.

        Retorna:
            None
        """
        # Obtener la fecha
        fecha = self.fecha.get()

        if len(fecha) == 10:
        # Dividir la fecha en día, mes y año
            dia, mes, año = map(int, fecha.split('/'))

            # Llamar a la función validacion_Dias_Mes_Año con los componentes de fecha
            if not self.validacion_Dias_Mes_Año(dia, mes, año):
                self.fecha.delete(0, "end")
            else:
                pass
        else:
            pass

    ''' Función principal de interacción con la base de datos '''

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

    def obtener_Alumnos(self):
        """
        Recupera los IDs de los estudiantes distintos de la tabla "Alumnos" y los agrega al combobox "cmbx_Id_Alumno".

        Esta función ejecuta una consulta SQL para seleccionar los IDs de los estudiantes distintos de la tabla "Alumnos". Los resultados se almacenan en la variable "results". Si la variable "results" no está vacía, la función itera sobre cada resultado y extrae el primer elemento (el ID del estudiante) en la lista "ids_alumnos". Finalmente, la lista "ids_alumnos" se asigna como valores del combobox "cmbx_Id_Alumno".

        Parámetros:
            self (objeto): La instancia de la clase a la que pertenece el método.

        Retorna:
            None
        """                  
        query = "SELECT DISTINCT Id_Alumno FROM Alumnos ORDER BY Id_Alumno"
        results = self.run_Query(query, (), 2)
        if results:
            ids_alumnos = [result[0] for result in results]
            self.cmbx_Id_Alumno['values'] = ids_alumnos

    
    def escoger_Alumno(self, event = None):
        """
        Selecciona un estudiante del combobox "cmbx_Id_Alumno" y rellena las entradas "nombres" y "apellidos".

        Parámetros:
            self (objeto): La instancia de la clase a la que pertenece el método.
            event (Event, opcional): El evento que desencadenó la función. Por defecto es None.

        Retorna:
            None
        """        
        id_Alumno = self.cmbx_Id_Alumno.get()
        query = "SELECT Nombres, Apellidos FROM Alumnos WHERE Id_Alumno = ?"
        result = self.run_Query(query, (id_Alumno,), 1)
        if result:
            nombre = result[0]
            apellidos = result[1]
            self.nombres.configure(state="normal")
            self.apellidos.configure(state="normal")
            self.nombres.delete(0, "end")
            self.nombres.insert(0, nombre)
            self.apellidos.delete(0, "end")
            self.apellidos.insert(0, apellidos)
            self.apellidos.configure(state="disabled")
            self.nombres.configure(state="disabled")
            #self.cmbx_Num_Inscripcion.configure(state="disabled")

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
    
    def obtener_Cursos(self):
        """
        Recupera una lista de códigos de curso distintos de la tabla "Cursos" y los rellena en el combobox "cmbx_Id_Curso".

        Esta función ejecuta una consulta SQL para recuperar los códigos de curso distintos de la tabla "Cursos". La consulta ordena los resultados por el código de curso. Si la consulta devuelve algún resultado, la función crea una lista del primer campo de cada fila de resultado. Esta lista se asigna al atributo "values" del combobox "cmbx_Id_Curso".

        Parámetros:
            self (objeto): La instancia de la clase a la que pertenece este método.

        Retorna:
            None
        """
        query = "SELECT DISTINCT Codigo_Curso FROM Cursos ORDER BY Codigo_Curso"
        results = self.run_Query(query, (), 2)
        if results:
            codigos_cursos = [result[0] for result in results]
            self.cmbx_Id_Curso['values'] = codigos_cursos
            
    # Corregir la funcionalidad de horario!!! Se puede modificar la funcionalidad, para que actue diferente 
    def escoger_Curso(self, event= None):
        """
        Selecciona un curso desde el combobox "cmbx_Id_Curso" y completa las entradas "descripc_Curso" y "horario" con la descripción y número de horas correspondientes.

        Parámetros:
            self (objeto): La instancia de la clase a la que pertenece este método.
            event (Event, opcional): El evento que desencadenó la función. Por defecto es None.

        Retorna:
            None
        """
        id_Curso = self.cmbx_Id_Curso.get()  # Corregido de self.num_Curso a self.cmbx_Id_Curso
        query = "SELECT Descrip_Curso, Num_Horas FROM Cursos WHERE Codigo_Curso = ?"
        result = self.run_Query(query, (id_Curso,), 1)
        if result:
            descrip = result[0]
            num_Horas = result[1]
            self.descripc_Curso.configure(state="normal")
            self.horario.configure(state="normal")
            self.descripc_Curso.delete(0, "end")
            self.descripc_Curso.insert(0, descrip)
            self.horario.delete(0, "end")
            self.horario.insert(0, num_Horas)
            #self.horario.configure(state="disabled")
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
        query = "SELECT Codigo_Curso FROM Inscritos WHERE Id_Alumno = ? AND No_Inscripcion = ?"
        result = self.run_Query(query, (id_Alumno, no_Inscripcion), 2) #trae los codigos del curso en los que esta incrito el alumno
        id_Cursos_Del_Alumno = [resultado[0] for resultado in result] #convierte la tupla en una lista de solo IDS de curso
        nombres_cursos = []
        for codigo_Curso in id_Cursos_Del_Alumno: #recorre la lista de IDs de curso y convierte en nombres de curso
            query2 = "SELECT Descrip_Curso FROM Cursos WHERE Codigo_Curso = ?"
            result2 = self.run_Query(query2, (codigo_Curso,), 1)
            if result2 and result2[0] == nombre_Curso:
                nombres_cursos.append(result2[0]) #va añadiedno a la lista de nombres de cursos los nombres de los cursos que estan en la lista de IDs de cursos
        return id_Curso in id_Cursos_Del_Alumno or nombre_Curso in nombres_cursos # verifica si el ID del curso es igual al ID del curso del alumno o si el nombre del curso es igual al nombre del curso del alumno

        
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
        query = "SELECT Id_Alumno FROM Inscritos WHERE No_Inscripcion = ?"
        result = self.run_Query(query, (no_Inscripcion, ), 1)

        # Verifica si el query arroja un resultado "None" o no, que implica que si el número de inscripción se encuentra en la base de datos "Inscritos" o no
        if result == None:
            return False # El número de inscripción no se encuentra aún registrado en la columna "No_Inscripcion" de la base de datos "Inscritos"
        else:
            if id_Alumno != result[0]:
                return True  # Los dos alumnos son diferentes, lo cuál no es permitido
            else:
                return False # El alumno es el mismo, y no hay problema con la inscripción
            
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
        query = "SELECT No_Inscripcion FROM Inscritos WHERE Id_Alumno = ? AND No_Inscripcion != ?"
        result = self.run_Query(query, (id_Alumno, no_Inscripcion), 1)
        # Verifica si el query arroja un resultado "None" o no
        if result is not None:
            confirmacion = mssg.askquestion("Confirmacion", f"¿Desea inscribir el alumno {id_Alumno} en su registro perteneciente a la inscripción {result[0]}?")
            if confirmacion == "yes":
                self.limpiar_Campos()
                for i, curso in enumerate(self.cmbx_Num_Inscripcion["values"]):
                    if result[0] == int(curso):
                        self.cmbx_Num_Inscripcion.current(i)
                        self.cmbx_Num_Inscripcion.event_generate("<<ComboboxSelected>>")
                        #self.cmbx_Num_Inscripcion.set(self.cmbx_Num_Inscripcion["values"][i]) esta puede ser otra opcion pra subir las cosas al combobox
                        break
                 # Establece el valor del ComboBox
                self.mostrar_Datos()
                return True  # El alumno está inscrito en otro número de inscripción
            else:
                self.limpiar_Campos()
                return True  # El usuario decidió no trasladarse a otra inscripción
        return False

    
    # Función para guardar un curso: Permite guardar una curso dentro de la inscripción 
    def guardar_Inscripcion(self, event):
        """
        Guarda una inscripción para un curso.

        Parámetros:
            event (Event): El evento que activó la función.

        Retorna:
            None

        Esta función verifica que todos los campos requeridos para la inscripción estén diligenciados por el usuario. Verifica los Comboboxes "cmbx_Id_Alumno", "cmbx_Id_Curso" y el Entry "fecha" porque al llenarlos se llenan automáticamente el resto del formulario.

        La función luego verifica si el usuario ya ha registrado un curso en la inscripción actual. Si es así, no hace nada. Si no, verifica que el estudiante que se está registrando en la inscripción corresponda al estudiante asociado a la inscripción y no a un estudiante diferente.

        Si el estudiante ya se ha registrado para el curso en la inscripción actual, muestra un mensaje de error. De lo contrario, inserta la nueva inscripción en la tabla "Inscritos".

        Si el número de inscripción actualmente en el Combobox "cmbx_Num_Inscripcion" es igual al valor almacenado en la variable "autoincrementar_Contador", incrementa el valor de "autoincrementar_Contador" y lo inserta en el Combobox "cmbx_Num_Inscripcion".

        Si esta es la primera vez que se guarda una inscripción o registro en la tabla "Inscritos", crea un registro en la columna "No_Inscripcion_Autoincremental" de la tabla "Autoincremental". De lo contrario, actualiza el valor en la columna "No_Inscripcion_Autoincremental" de la tabla "Autoincremental" al valor almacenado en la variable "autoincrementar_Contador".

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
                        parameters = (no_Inscripcion, id_Alumno, id_Curso, fecha, horario_Curso)
                        self.run_Query(query, parameters)

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
                                parameters2 = (self.autoincrementar_Contador, )
                                self.run_Query(query2, parameters2)
                            else:    
                                query2 = "UPDATE Autoincremental SET No_Inscripcion_Autoincremental = ?"
                                parameters2 = (self.autoincrementar_Contador, )
                                self.run_Query(query2, parameters2)
                    
                        # Mensaje que confirma que la inscripción se ha realizado con éxito
                        mssg.showinfo("Exito", "Inscripcion realizada con exito")
                        self.mostrar_Datos()
                        
                        # Configura los campos luego de realizar una inscripción con éxito 
                        
                        ## 
                        self.cmbx_Num_Inscripcion.set(no_Inscripcion)

                        ## 
                        self.cmbx_Id_Curso.configure(state="normal")
                        self.cmbx_Id_Curso.delete(0, "end")

                        self.descripc_Curso.configure(state="normal")
                        self.descripc_Curso.delete(0, "end")

                        self.horario.configure(state="normal")
                        self.horario.delete(0, "end")
                    
    ''' Funcionalidad para el botón "Buscar" '''
    
    # Función para mostrar datos en el Treeview: Permite mostrar los datos en el Treeview de la interfaz gráfica
    def mostrar_Datos(self, event = None):
        """
        Recupera datos de la base de datos basados en el número de inscripción seleccionado y los muestra en el Treeview.
    
        Parámetros:
            event (opcional): El evento que desencadenó la función. Predeterminado a None.
    
        Retorna:
            None
    
        Esta función recupera el número de inscripción del combobox `cmbx_Num_Inscripcion` y ejecuta una consulta SQL para recuperar los datos correspondientes de la tabla `Inscritos`. Si la consulta devuelve un resultado, la función borra el Treeview, lo llena con los datos recuperados y actualiza el combobox `cmbx_Id_Alumno` con el valor correspondiente. También actualiza los comboboxes `cmbx_Id_Curso` y `descripc_Curso` con los datos recuperados. Si la consulta no devuelve un resultado, se muestra un mensaje de advertencia.
        """
        no_Inscripcion = self.cmbx_Num_Inscripcion.get()

        query = "SELECT Id_Alumno, Codigo_Curso, Horario FROM Inscritos WHERE No_Inscripcion = ?"
        result = self.run_Query(query, (no_Inscripcion,), 2)
    
        if result:
            # Para limpiar el Treeview
            self.treeInscritos.delete(*self.treeInscritos.get_children())

            # Llenar el Treeview de cada dato que trajo el result
            for datos_DB in result:          
                codigo_Curso = (datos_DB[1],)
                query2 = "SELECT Descrip_Curso FROM Cursos WHERE Codigo_Curso = ?"
                result2 = self.run_Query(query2, codigo_Curso, 1)
                self.treeInscritos.insert("", 0, text= datos_DB[0], values = (datos_DB[1], result2[0], datos_DB[2]))   
            
            # Llnear el Combobox "cmbx_Id_Alumno"
            self.cmbx_Id_Alumno.configure(state= "normal")
            self.cmbx_Id_Alumno.delete(0, "end")
            self.cmbx_Id_Alumno.insert(0, datos_DB[0])
            self.cmbx_Id_Alumno.configure(state= "disabled")

            # Llenar los nombres y apellidos de los alumnos
            self.escoger_Alumno()

            # 
            self.cmbx_Id_Curso.configure(state="normal")
            self.cmbx_Id_Curso.delete(0, "end")
            self.descripc_Curso.configure(state="normal")
            self.horario.configure(state="normal")
            self.descripc_Curso.delete(0, "end")
            self.cmbx_Id_Curso.configure(state="readonly")
            self.descripc_Curso.configure(state="disabled")
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

        Esta función crea una nueva ventana para eliminar datos. Establece el título de la ventana a "Borrar datos" y configura su ancho y alto. Luego centra la ventana en la pantalla. La ventana no es redimensionable.

        La función crea un marco de etiqueta con el texto "¿Qué desea realizar?" y establece su color de primer plano a "RoyalBlue". Luego empaqueta el marco de etiqueta con un relleno de 10 píxeles en la parte superior e izquierda.

        La función crea dos botones de opción, "Borrar un curso" y "Borrar toda la inscripción", y los asocia con la variable `self.opcion`. Los botones de opción tienen diferentes valores (1 y 2) y tienen sus colores de primer plano y activo establecidos en "RoyalBlue" y "red2", respectivamente.

        La función crea un botón con el texto "Borrar" y lo enlaza a la función `self.eliminar_Cursos`. El botón
        """

        #Creacion de la ventana
        self.ventana_Borrar = tk.Toplevel()
        self.ventana_Borrar.title("Borrar datos")
        self.ventana_Borrar.config(width= 300, height= 150)
        self.centrar_Pantalla(self.ventana_Borrar, 300, 150)
        
        #No permitir cambiar tamaño de la ventana
        self.ventana_Borrar.resizable(False, False)
        
        #creacion labelframe        
        self.marco = tk.LabelFrame(self.ventana_Borrar, text = "¿Que desea realizar?", fg="RoyalBlue")
        self.marco.pack(pady=10, padx=10)

        self.opcion = tk.IntVar()

        #crear radiobutton
        self.radiobutton1 = tk.Radiobutton(self.marco, text="Borrar un curso", variable= self.opcion, value= 1, 
                                           foreground = "RoyalBlue", activeforeground="red2"
                                           )       
        self.radiobutton1.pack(anchor="w", pady=5)
        self.radiobutton2 = tk.Radiobutton(self.marco, text="Borrar toda la inscripción", variable= self.opcion, value=2,
                                           foreground = "RoyalBlue", activeforeground="red2"
                                           )
        self.radiobutton2.pack(anchor="w", pady=5)
        
        self.btn_Vna_Borrar = ttk.Button(self.ventana_Borrar, name="btn_Vna_Borrar")
        self.btn_Vna_Borrar.configure(text="Borrar")
        self.btn_Vna_Borrar.bind("<Button-1>", self.eliminar_Cursos)
        self.btn_Vna_Borrar.pack()
        
        #Moverse hacia la ventana borrar 
        self.ventana_Borrar.after(100, self.ventana_Borrar.focus)
        
        #Mantenerse en la ventana borrar
        self.ventana_Borrar.grab_set()
        #crear boton borrar
        #self.close_button = tk.Button(self.ventana_Borrar, text="Borrar", command= self.ventana_Borrar.destroy, width=10, height=1)
        #self.close_button.pack(pady=5)

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
        opcion = self.opcion.get()
        #verificar si esta seleccionado una opcion en la ventana borrar
        if opcion:
            #verificar que opcion esta seleccionado en la ventana borrar
            if opcion == 1:
                #Eliminar un curso
                #verificar si esta seleccionado un curso en el treewiew
                if self.treeInscritos.selection():
                    seleccion = self.treeInscritos.selection()[0]
                    seleccion_Values = self.treeInscritos.item(seleccion, "values")
                    codigo_Curso = seleccion_Values[0]
                    nombre_Curso = seleccion_Values[1]
                    mensaje = f"¿Desea eliminar este curso: ({codigo_Curso}) {nombre_Curso}?"
                    confirmacion = mssg.askokcancel("Confirmacion", mensaje)
                    if confirmacion:
                        num_Incripcion = self.cmbx_Num_Inscripcion.get()
                        query1 = "SELECT COUNT(No_Inscripcion) FROM Inscritos WHERE No_Inscripcion = ?"
                        parametros1 = (num_Incripcion,)
                        cantidad_Inscripciones = self.run_Query(query1, parametros1, 1)[0]
                        query2 = "DELETE FROM Inscritos WHERE No_Inscripcion = ? AND Codigo_Curso = ?"
                        parametros2 = (num_Incripcion, codigo_Curso)
                        borrar = self.run_Query(query2, parametros2)    
                        query3 = "SELECT COUNT(No_Inscripcion) FROM Inscritos WHERE No_Inscripcion = ? AND Codigo_Curso = ?"
                        confirmacion_Eliminar = self.run_Query(query3,parametros2, 1)[0]
                        #confirmar si se elimino el curso
                        if confirmacion_Eliminar == 0:
                            mensaje = f"El curso ({codigo_Curso}) {nombre_Curso} ha sido borrado con exito."
                            if cantidad_Inscripciones == 1:
                                self.ventana_Borrar.destroy()
                                mssg.showinfo("Exito", mensaje)
                                self.limpiar_Campos()
                                self.obtener_Inscripciones()
                            else:
                                self.treeInscritos.delete(seleccion)
                                self.ventana_Borrar.destroy()
                                mssg.showinfo("Exito", mensaje)
                                
                        else:
                            mensaje = f"No se ha podido borrar el curso ({codigo_Curso}) {nombre_Curso}."
                            self.ventana_Borrar.destroy()
                            mssg.showerror("Error", mensaje)
                        
                else:
                    self.ventana_Borrar.destroy()
                    mssg.showerror("Error", "Seleccione un curso")
            elif opcion == 2:
                #Eliminar todos los cursos
                confirmacion = mssg.askokcancel("Confirmacion", "¿Desea eliminar todos los cursos?")
                if confirmacion:
                    num_Incripcion = self.cmbx_Num_Inscripcion.get()
                    query = "SELECT COUNT(No_Inscripcion) FROM Inscritos WHERE No_Inscripcion = ?"
                    parametro = (num_Incripcion,)
                    result = self.run_Query(query, parametro, 1)[0]
                    if result >= 1:
                        query = "DELETE FROM Inscritos WHERE No_Inscripcion = ?"
                        parametro = (num_Incripcion,)
                        ejecucion = self.run_Query(query, parametro)
                        mensaje = f"Se han borrado todos los cursos de la inscripcion No.{num_Incripcion}"
                        self.limpiar_Campos()
                        self.obtener_Inscripciones()
                        self.ventana_Borrar.destroy()
                        mssg.showinfo("Exito", mensaje)
                    else:
                        mensaje = f"El numero de inscripcion {num_Incripcion} no tiene cursos inscriptos."
                        self.ventana_Borrar.destroy()
                        mssg.showerror("Error", mensaje)

        else:
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
        
        Esta función se llama cuando el usuario presiona el botón "Editar". Verifica si se ha seleccionado un curso en el árbol. Si se ha seleccionado un curso, configura los campos de combobox y entry para permitir la edición. Luego, recupera los valores del curso seleccionado y actualiza los campos de combobox y entry con esos valores. Los campos de combobox y entry se deshabilitan para evitar que se realicen más ediciones. Los botones de búsqueda, eliminación y guardado también se deshabilitan. El botón "Confirmar" se habilita y se enlaza a la función `confirmar_Editar`. El combobox se establece en de solo lectura. Si no se ha seleccionado ningún curso, se muestra un mensaje de error.
        """
        if self.treeInscritos.selection():
            self.cmbx_Id_Curso.configure(state="normal")
            seleccion = self.treeInscritos.selection()[0]
            seleccion_Values = self.treeInscritos.item(seleccion, "values")
            self.descripc_Curso.configure(state="normal")
            self.curso_Actual = seleccion_Values[0]
            self.desc_Curso_Actual = seleccion_Values[1]
            self.horario_Actual = seleccion_Values[2]
            self.cmbx_Id_Curso.delete(0, "end")
            self.cmbx_Id_Curso.insert(0, self.curso_Actual)
            self.descripc_Curso.delete(0, "end")
            self.descripc_Curso.insert(0, self.desc_Curso_Actual)
            self.descripc_Curso.configure(state="disabled")
            self.horario.delete(0, "end")
            self.horario.insert(0, self.horario_Actual)
            #Bloquear los botones 
            self.descripc_Curso.configure(state="disabled")
            self.btnBuscar.configure(state="disabled")
            self.btnBuscar.unbind("<Button-1>")
            self.btnEliminar.configure(state="disabled")
            self.btnEliminar.unbind("<Button-1>")
            self.btnGuardar.configure(state="disabled")
            self.btnGuardar.unbind("<Button-1>")
            self.btnEditar.configure(text="Confirmar", style="Boton.TButton")
            self.btnEditar.unbind("<Button-1>")
            self.btnEditar.bind("<Button-1>", self.confirmar_Editar)
            self.cmbx_Id_Curso.configure(state="readonly")
        else:
            mssg.showerror("Error", "Seleccione un curso")

    # Función que se ejecuta cuando se oprime el botón confirmar: Hacer el cambio del curso en la base de datos y en el Treeview
    def confirmar_Editar(self, event):
        """
        Actualiza la información del curso de un estudiante en la base de datos.
        
        Parámetros:
            event (Event): El evento que desencadenó la función.
        
        Retorna:
            None
        
        Levanta:
            Exception: Si hay un error al ejecutar la consulta a la base de datos.
        
        Adicionalmente la función:
            - Actualiza la información del curso de un estudiante en la base de datos.
            - Actualiza el texto del botón y las enlaces.
            - Habilita o deshabilita los botones en función de la validez de la entrada.
            - Actualiza el Treeview con la nueva información del curso.
        """
        id_Alumno = self.cmbx_Id_Alumno.get()
        nuevo_codigo_curso = self.cmbx_Id_Curso.get()
        nuevo_horario = self.horario.get()
        numero_De_inscripcion = self.cmbx_Num_Inscripcion.get()
        desc_Curso_Nuevo = self.descripc_Curso.get()
        fecha_Nueva = self.fecha.get()
        query1 = "UPDATE Inscritos SET Codigo_Curso = ?, Horario = ?, Fecha_Inscripcion = ? WHERE No_Inscripcion = ? AND Codigo_Curso = ? AND Horario = ?"
        parametros1 = (nuevo_codigo_curso, nuevo_horario, fecha_Nueva,numero_De_inscripcion, self.curso_Actual, self.horario_Actual)
        if self.verificar_Integridad_Cursos(id_Alumno, desc_Curso_Nuevo, nuevo_codigo_curso,  numero_De_inscripcion):
            mssg.showerror("Error", f"El alumno identificado con código {id_Alumno} ya se encuentra inscrito en el curso {desc_Curso_Nuevo} para la inscripción No. {numero_De_inscripcion}")
        else:
            try:
                self.run_Query(query1, parametros1)
                mssg.showinfo("Estado", f"La modificacion del curso {self.desc_Curso_Actual} por el curso {desc_Curso_Nuevo} ha sido realizada con exito")
            except Exception as e:
                mssg.showerror("Error", e)
            self.btnEditar.configure(text="Editar", style="TButton")
            self.btnEditar.unbind("<Button-1>")
            self.btnEditar.bind("<Button-1>", self.editar_Curso)
            self.btnBuscar.configure(state="normal")
            self.btnBuscar.bind("<Button-1>", self.mostrar_Datos)
            self.btnGuardar.configure(state="normal")
            self.btnGuardar.bind("<Button-1>", self.guardar_Inscripcion)
            self.btnEliminar.configure(state="normal")
            self.btnEliminar.bind("<Button-1>", self.crear_Ventana_Eliminar)
            self.mostrar_Datos()

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
