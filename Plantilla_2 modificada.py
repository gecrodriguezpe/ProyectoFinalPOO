# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
from pathlib import Path
from datetime import datetime

DB = str(Path.cwd()) + r"\db\Inscripciones.db"


class Inscripciones_2:
    def __init__(self, master=None):
         # Ventana principal
        self.db_name = DB
        self.win = tk.Tk(master)
        self.win.configure(background="#f7f9fd", height=600, width=800)
        self.win.geometry("800x600")
        self.win.resizable(False, False)
        self.win.title("Inscripciones de Materias y Cursos")
        # Crea los frames
        self.frm_1 = tk.Frame(self.win, name="frm_1")
        self.frm_1.configure(background="#f7f9fd", height=600, width=800)
        self.lblNoInscripcion = ttk.Label(self.frm_1, name="lblnoinscripcion")
        self.lblNoInscripcion.configure(background="#f7f9fd",font="{Arial} 11 {bold}",
                                        justify="left",state="normal",
                                        takefocus=False,text='No.Inscripción')
         #Label No. Inscripción
        self.lblNoInscripcion.place(anchor="nw", x=680, y=20)
        #Entry No. Inscripción
        # self.num_Inscripcion = ttk.Entry(self.frm_1, name="num_inscripcion")
        # self.num_Inscripcion.configure(justify="right")
        # self.num_Inscripcion.place(anchor="nw", width=100, x=682, y=42)
        
        #Combobox No_Inscripción
        self.num_Inscripción = ttk.Combobox(self.frm_1, name="num_Inscripción")
        self.num_Inscripción.place(anchor="nw", width=100, x=682, y=42)
        self.obtener_Inscripciones()
        #Label Fecha
        self.lblFecha = ttk.Label(self.frm_1, name="lblfecha")
        self.lblFecha.configure(background="#f7f9fd", text='Fecha:')
        self.lblFecha.place(anchor="nw", x=630, y=80)
        #Entry Fecha
        self.fecha = ttk.Entry(self.frm_1, name="fecha")
        self.fecha.configure(justify="center")
        self.fecha.place(anchor="nw", width=90, x=680, y=80)
        #Label Alumno
        self.lblIdAlumno = ttk.Label(self.frm_1, name="lblidalumno")
        self.lblIdAlumno.configure(background="#f7f9fd", text='Id Alumno:')
        self.lblIdAlumno.place(anchor="nw", x=20, y=80)
        #Combobox Alumno
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1, name="cmbx_id_alumno")
        self.cmbx_Id_Alumno.place(anchor="nw", width=112, x=100, y=80)
        self.obtener_Alumnos()
        self.cmbx_Id_Alumno.bind("<<ComboboxSelected>>", self.escoger_Alumno)    # Configurar ComboBox para permitir selección y vincular evento de selección a función

        #Label Alumno
        self.lblNombres = ttk.Label(self.frm_1, name="lblnombres")
        self.lblNombres.configure(text='Nombre(s):')
        self.lblNombres.place(anchor="nw", x=20, y=130)
        #Entry Alumno
        self.nombres = ttk.Entry(self.frm_1, name="nombres")
        self.nombres.place(anchor="nw", width=200, x=100, y=130)
        #Label Apellidos
        self.lblApellidos = ttk.Label(self.frm_1, name="lblapellidos")
        self.lblApellidos.configure(text='Apellido(s):')
        self.lblApellidos.place(anchor="nw", x=400, y=130)
        #Entry Apellidos
        self.apellidos = ttk.Entry(self.frm_1, name="apellidos")
        self.apellidos.place(anchor="nw", width=200, x=485, y=130)
        #Label Curso
        self.lblIdCurso = ttk.Label(self.frm_1, name="lblidcurso")
        self.lblIdCurso.configure(background="#f7f9fd",state="normal",text='Id Curso:')
        self.lblIdCurso.place(anchor="nw", x=20, y=185)
        #Entry Curso
        self.cmbx_Id_Curso = ttk.Combobox(self.frm_1, name="id_curso")
        self.cmbx_Id_Curso.place(anchor="nw", width=166, x=100, y=185)
        self.obtener_Cursos()
        self.cmbx_Id_Curso.bind("<<ComboboxSelected>>", self.escoger_Curso)    # Configurar ComboBox para permitir selección y vincular evento de selección a función

        #Label Descripción del Curso
        self.lblDscCurso = ttk.Label(self.frm_1, name="lbldsccurso")
        self.lblDscCurso.configure(background="#f7f9fd",state="normal",text='Curso:')
        self.lblDscCurso.place(anchor="nw", x=275, y=185)
        #Entry de Descripción del Curso 
        self.descripc_Curso = ttk.Entry(self.frm_1, name="descripc_curso")
        self.descripc_Curso.configure(justify="left", width=166)
        self.descripc_Curso.place(anchor="nw", width=300, x=325, y=185)
        #Label Horario
        self.lblHorario = ttk.Label(self.frm_1, name="label3")
        self.lblHorario.configure(background="#f7f9fd",state="normal",text='Hora:')
        self.lblHorario.place(anchor="nw", x=635, y=185)
        #Entry del Horario
        self.horario = ttk.Entry(self.frm_1, name="entry3")
        self.horario.configure(justify="left", width=166)
        self.horario.place(anchor="nw", width=100, x=680, y=185)

        ''' Botones  de la Aplicación'''
        #Boton Buscar
        self.btnGuardar = ttk.Button(self.frm_1, name="btnbuscar")
        self.btnGuardar.configure(text='Buscar')
        self.btnGuardar.place(anchor="nw", x=155, y=260)
        
        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name="btnguardar")
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor="nw", x=255, y=260)
        self.btnGuardar.bind("<Button-1>", self.guardar_Inscripcion)
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name="btneditar")
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=355, y=260)
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name="btneliminar")
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor="nw", x=455, y=260)
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name="btncancelar")
        self.btnCancelar.configure(text='Cancelar')
        self.btnCancelar.place(anchor="nw", x=555, y=260)
        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="nw", width=796, x=2, y=245)

        ''' Treeview de la Aplicación'''
        #Treeview
        self.tView = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")
        #Columnas del Treeview
        self.tView_cols = ['tV_curso','tV_descripción','tV_horario']
        self.tView_dcols = ['tV_curso','tV_descripción', 'tV_horario']
        self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
        self.tView.column("#0",anchor="w",stretch=True,width=55,minwidth=10)
        self.tView.column("tV_horario",anchor="w",stretch=True,width=55,minwidth=25)
        self.tView.column("tV_descripción",anchor="w",stretch=True,width=200,minwidth=50)
        self.tView.column("tV_curso",anchor="w",stretch=True,width=100,minwidth=50)

        #Cabeceras
        self.tView.heading("#0", anchor="w", text='Id Alumno')
        self.tView.heading("tV_horario", anchor="w", text='Horario')
        self.tView.heading("tV_descripción", anchor="w", text='Descripción')
        self.tView.heading("tV_curso", anchor="w", text='Curso')
        self.tView.place(anchor="nw", height=300, width=790, x=4, y=300)
        #Scrollbars
        self.scroll_H = ttk.Scrollbar(self.frm_1, name="scroll_h")
        self.scroll_H.configure(orient="horizontal")
        self.scroll_H.place(anchor="s", height=12, width=1534, x=15, y=595)
        self.scroll_Y = ttk.Scrollbar(self.frm_1, name="scroll_y")
        self.scroll_Y.configure(orient="vertical")
        self.scroll_Y.place(anchor="s", height=275, width=12, x=790, y=582)
        self.frm_1.pack(side="top")
        self.frm_1.pack_propagate(0)

        # Main widget
        self.mainwindow = self.win

    def run(self):
        self.mainwindow.mainloop()


    ''' A partir de este punto se deben incluir las funciones
     para el manejo de la base de datos '''

    def run_Query(self,query,parameters=(),op_Busqueda=0):
        try:
            with sqlite3.connect(self.db_name) as conn:
                self.cur = conn.cursor()
                self.cur.execute(query,parameters)
                if op_Busqueda == 1:
                    return self.cur.fetchone()
                elif op_Busqueda == 2:
                    return self.cur.fetchall()
                else:
                    return None  # Si op_Busqueda no es válido
        except sqlite3.Error as e:
            print("Error executing query:", e)
            return None
    def obtener_Alumnos(self):
            query = "SELECT DISTINCT Id_Alumno FROM Alumnos ORDER BY Id_Alumno"
            results = self.run_Query(query, (), 2)
            if results:
                ids_alumnos = [result[0] for result in results]
                self.cmbx_Id_Alumno['values'] = ids_alumnos
    
    def escoger_Alumno(self,event):
        id_Alumno = self.cmbx_Id_Alumno.get()
        query = "SELECT Nombres, Apellidos FROM Alumnos WHERE Id_Alumno = ?"
        result = self.run_Query(query, (id_Alumno,), 1)
        if result:
            nombre = result[0]
            apellidos = result[1]
            self.nombres.config(state="normal")
            self.apellidos.config(state="normal")
            self.nombres.delete(0, "end")
            self.nombres.insert(0, nombre)
            self.apellidos.delete(0, "end")
            self.apellidos.insert(0, apellidos)
            self.apellidos.config(state="disabled")
            self.nombres.config(state="disabled")
            self.num_Inscripción.config(state="disabled")
    def obtener_Inscripciones(self):
        self.num_Inscripción.delete(0, "end")
        query = "SELECT DISTINCT No_Inscripcion FROM Inscritos ORDER BY No_Inscripcion"
        results = self.run_Query(query, (), 2)
        if results:
            ids_inscripciones = [result[0] for result in results]
            self.num_Inscripción.insert(0,max(ids_inscripciones)+1)
            self.num_Inscripción['values'] = ids_inscripciones
        else:
            self.num_Inscripción['values'] = [1]
    
    def obtener_Cursos(self):
        query = "SELECT DISTINCT Codigo_Curso FROM Cursos ORDER BY Codigo_Curso"
        results = self.run_Query(query, (), 2)
        if results:
            codigos_cursos = [result[0] for result in results]
            self.cmbx_Id_Curso['values'] = codigos_cursos
            
    def escoger_Curso(self, event):
        id_Curso = self.cmbx_Id_Curso.get()  # Corregido de self.num_Curso a self.cmbx_Id_Curso
        query = "SELECT Descrip_Curso, Num_Horas FROM Cursos WHERE Codigo_Curso = ?"
        result = self.run_Query(query, (id_Curso,), 1)
        if result:
            descrip = result[0]
            num_Horas = result[1]
            self.descripc_Curso.config(state="normal")
            self.horario.config(state="normal")
            self.descripc_Curso.delete(0, "end")
            self.descripc_Curso.insert(0, descrip)
            self.horario.delete(0, "end")
            self.horario.insert(0, num_Horas)
            self.descripc_Curso.config(state="disabled")

    def guardar_Inscripcion(self, event):
        id_Alumno = self.cmbx_Id_Alumno.get()
        id_Curso = self.cmbx_Id_Curso.get()
        fecha = self.fecha.get()
        
        if not id_Alumno or not id_Curso or not fecha:
            mssg.showerror("Error", "Por favor, complete todos los campos")
        else:
            # Verificar si el alumno ya está inscrito en el curso
            if self.verificar_Inscripcion(id_Alumno, id_Curso):
                mssg.showerror("Error", "El alumno ya se encuentra inscrito en el curso")
            else:
                # Insertar nueva inscripción en la tabla Inscritos
                query = "INSERT INTO Inscritos (Id_Alumno, Codigo_Curso, Fecha_Inscripcion) VALUES (?, ?, ?)"
                parameters = (id_Alumno, id_Curso, fecha)
                self.run_Query(query, parameters)
                mssg.showinfo("Exito", "Inscripcion realizada con exito")
                self.obtener_Inscripciones()
                self.num_Inscripción.config(state="enabled")
                self.num_Inscripción.delete(0, "end")
                self.descripc_Curso.config(state="enabled")
                self.descripc_Curso.delete(0, "end")
                self.horario.delete(0, "end")
                self.cmbx_Id_Curso.delete(0, "end")
                self.fecha.delete(0, "end")
                self.cmbx_Id_Alumno.delete(0, "end")
                self.nombres.config(state="enabled")
                self.apellidos.config(state="enabled")
                self.nombres.delete(0, "end")
                self.apellidos.delete(0, "end")


    def verificar_Inscripcion(self, id_alumno, codigo_curso):
        query = "SELECT COUNT(*) FROM Inscritos WHERE Id_Alumno = ? AND Codigo_Curso = ?"
        result = self.run_Query(query, (id_alumno, codigo_curso), 1)
        if result[0] > 0:
            return True  # El alumno ya está inscrito en el curso
        else:
            return False 
    
    def obtener_datos(self, event):
        pass
    

           
        
if __name__ == "__main__":
    app = Inscripciones_2()
    app.run()
