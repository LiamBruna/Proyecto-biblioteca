import tkinter as tk
import customtkinter as ck
import tkinter.ttk as ttk
from tkinter import messagebox

from model.conexion_db import *

class VentanaRegistro(tk.Toplevel):
    def __init__(self, parent, bd):
        super().__init__(parent)
        self.parent = parent
        self.bd = BD()
        self.title("Registro")
        self.iconbitmap('img/libros.ico')
        self.config(bg="red")  # Color de la ventana de registro
        
        self.registerWindow()
        self.crear_boton_registrar()

    def registerWindow(self):
        # Crea los campos de entrada de datos para el registro
        self.nombre_entry = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='Nombre', border_color='green', fg_color='black', width=220, height=40)
        self.nombre_entry.grid(columnspan=2, row=1, padx=4, pady=4)

        self.apellido_entry = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='Apellido', border_color='green', fg_color='black', width=220, height=40)
        self.apellido_entry.grid(columnspan=2, row=2, padx=4, pady=4)

        self.correo_entry = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='Correo electrónico', border_color='green', fg_color='black', width=220, height=40)
        self.correo_entry.grid(columnspan=2, row=3, padx=4, pady=4)

        self.contraseña_entry = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='Contraseña', border_color='green', fg_color='black', width=220, height=40)
        self.contraseña_entry.grid(columnspan=2, row=4, padx=4, pady=4)

        self.rut_entry = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='RUT', border_color='green', fg_color='black', width=220, height=40)
        self.rut_entry.grid(columnspan=2, row=5, padx=4, pady=4)

    def crear_boton_registrar(self):
        # Crea el botón de registro
        button_registrar = tk.Button(self, text="Registrar", command=self.registrar)
        button_registrar.grid(columnspan=2, row=6, padx=4, pady=4)

    def registrar(self):
        # Obtiene los datos ingresados por el usuario
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        correo = self.correo_entry.get()
        contraseña = self.contraseña_entry.get()
        rut = self.rut_entry.get()

        # Llama al método de registro de la clase BD para crear un nuevo usuario
        self.bd.registro(nombre, apellido, correo, contraseña, rut)

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.bd = BD()
        self.pack()
        self.config(bg="red") #Color de la ventana
        
        self.loginWindow()

    def login(self):
        correo = self.correo.get()
        password = self.contraseña.get()
        
        if self.bd.login(correo, password):
            self.root.withdraw()
            ventana_principal = VentanaPrincipal(self.root)
            self.root.wait_window(ventana_principal)
        

    def abrir_ventana_registro(self):
        ventana_registro = VentanaRegistro(self.root, self.bd)
        self.root.wait_window(ventana_registro)

    def loginWindow(self):
        # Correo electrónico
        self.correo = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='Correo electrónico', border_color='green', fg_color='black', width=220, height=40)
        self.correo.grid(columnspan=2, row=1, padx=4, pady=4)

        # Contraseña
        self.contraseña = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='Contraseña', border_color='green', fg_color='black', width=220, height=40)
        self.contraseña.grid(columnspan=2, row=2, padx=4, pady=4)

        # Botón
        button_login = tk.Button(self, text="Iniciar sesión", command=self.login)
        button_login.grid(columnspan=2, row=3, padx=4, pady=4)

        button_registrar = tk.Button(self, text="Registrarse", command=self.abrir_ventana_registro)
        button_registrar.grid(columnspan=2, row=4, padx=4, pady=4)


class VentanaPrincipal(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Ventana Principal")
        self.config(bg="blue")  # Color de la ventana principal