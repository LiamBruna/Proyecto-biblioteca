import tkinter as tk
import customtkinter as ck
import tkinter.ttk as ttk
from tkinter import messagebox

from model.conexion_db import *
from model.classes import *

class VentanaRegistro(tk.Toplevel):
    def __init__(self, parent, bd):
        super().__init__(parent)
        self.parent = parent
        self.bd = BD()
        self.title("Registro")
        self.iconbitmap('img/libros.ico')
        self.config(bg="white")  # Color de la ventana de registro
        self.resizable(0,0)
        
        self.registerWindow()
        self.crear_boton_registrar()

    def registerWindow(self):
        # Crea los campos de entrada de datos para el registro
        self.nombre_entry = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='Nombre', border_color='black', fg_color='white', width=220, height=40)
        self.nombre_entry.grid(columnspan=2, row=1, padx=4, pady=4)

        self.apellido_entry = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='Apellido', border_color='black', fg_color='white', width=220, height=40)
        self.apellido_entry.grid(columnspan=2, row=2, padx=4, pady=4)

        self.correo_entry = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='Correo electrónico', border_color='black', fg_color='white', width=220, height=40)
        self.correo_entry.grid(columnspan=2, row=3, padx=4, pady=4)

        self.contraseña_entry = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='Contraseña', border_color='black', fg_color='white', width=220, height=40, show="*")
        self.contraseña_entry.grid(columnspan=2, row=4, padx=4, pady=4)

        self.rut_entry = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='RUT', border_color='black', fg_color='white', width=220, height=40)
        self.rut_entry.grid(columnspan=2, row=5, padx=4, pady=4)

    def crear_boton_registrar(self):
        # Crea el botón de registro
        button_registrar = ck.CTkButton(self, text="Registrar", command=self.registrar)
        button_registrar.grid(columnspan=2, row=6, padx=4, pady=4)

    def registrar(self):
        # Obtiene los datos ingresados por el usuario
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        correo = self.correo_entry.get()
        contraseña = self.contraseña_entry.get()
        rut = self.rut_entry.get()

        if correo == "":
            messagebox.showerror("Error de registro", "Debe ingresar un correo")
            return

        registrado = self.bd.registro(nombre, apellido, correo, contraseña, rut)

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.bd = BD()
        self.bd.conectar()
        self.pack()
        self.config(bg="white") #Color de la ventana
        
        self.loginWindow()

    def login(self):
        correo = self.correo.get()
        contraseña = self.contraseña_entry.get()

        if (not correo):
            messagebox.showerror("Error de inicio de sesión", "Debe ingresar un correo.")
            return
        
        # Verifica si el correo existe en la base de datos
        if self.bd.login(correo, contraseña):
            self.root.withdraw()
            ventana_principal = VentanaPrincipal(self.root)
            self.root.wait_window(ventana_principal)

    def toggle_password_visibility(self):
        if self.show_password.get():
            self.contraseña_entry.configure(show="")
        else:
            self.contraseña_entry.configure(show="*")
        

    def abrir_ventana_registro(self):
        ventana_registro = VentanaRegistro(self.root, self.bd)
        self.root.wait_window(ventana_registro)

    def loginWindow(self):
        # Correo electrónico
        self.correo = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='Correo electrónico', border_color='black', fg_color='white', width=220, height=40)
        self.correo.grid(columnspan=2, row=1, padx=4, pady=4)

        # Contraseña
        self.contraseña = tk.StringVar()
        self.contraseña_entry = ck.CTkEntry(self, font=('sans-serif', 12), placeholder_text='Contraseña', border_color='black', fg_color='white', width=220, height=40, show="*")
        self.contraseña_entry.grid(columnspan=2, row=2, padx=4, pady=4)

        # Checkbox para mostrar/ocultar la contraseña
        self.show_password = tk.BooleanVar()
        show_password_checkbox = ck.CTkCheckBox(self, text="Mostrar contraseña", variable=self.show_password, command=self.toggle_password_visibility)
        show_password_checkbox.grid(column=8, row=2, padx=4, pady=4)

        # Botón
        button_login = ck.CTkButton(self, text="Iniciar sesión", command=self.login)
        button_login.grid(columnspan=2, row=4, padx=4, pady=4)

        button_registrar = ck.CTkButton(self, text="Registrarse", command=self.abrir_ventana_registro)
        button_registrar.grid(columnspan=2, row=5, padx=4, pady=4)



class VentanaPrincipal(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.iconbitmap('img/libros.ico')
        self.title("Ventana Principal")
        self.config(bg="blue")  # Color de la ventana principal

        self.mainWindow()

    def mainWindow(self):
        button_cerrar_sesion = ck.CTkButton(self, text="Cerrar sesión", command=self.cerrar_sesion)
        button_cerrar_sesion.grid(columnspan=2, row=1, padx=4, pady=4)

    def cerrar_sesion(self):
        self.destroy()
        self.parent.deiconify()