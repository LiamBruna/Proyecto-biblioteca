import tkinter as tk
import customtkinter as ck
from tkinter import messagebox

from model.conexion_db import *
from model.classes import *

class VentanaRegistro(ck.CTkToplevel):
    def __init__(self, parent, bd):
        super().__init__(parent)
        self.parent = parent
        self.bd = bd
        self.title("Registro") #Titulo de la Ventana
        self.wm_iconbitmap('img/libros.ico')
        self.resizable(0, 0)

        self.show_password = tk.BooleanVar(value=False)  # Variable para controlar la visibilidad de la contraseña

        self.registerWindow()
        self.crear_boton_registrar()

    def registerWindow(self):
        # Crea los campos de entrada de datos para el registro
        self.nombre_entry = ck.CTkEntry(self, placeholder_text='Nombre', width=220, height=40)
        self.nombre_entry.grid(columnspan=2, row=1, padx=4, pady=4)

        self.apellido_entry = ck.CTkEntry(self, placeholder_text='Apellido', width=220, height=40)
        self.apellido_entry.grid(columnspan=2, row=2, padx=4, pady=4)

        self.correo_entry = ck.CTkEntry(self, placeholder_text='Correo electrónico', width=220, height=40)
        self.correo_entry.grid(columnspan=2, row=3, padx=4, pady=4)

        self.contraseña_entry = ck.CTkEntry(self, placeholder_text='Contraseña', width=220, height=40, show="*")
        self.contraseña_entry.grid(columnspan=2, row=4, padx=4, pady=4)

        self.contraseña_entry_confirmar = ck.CTkEntry(self, placeholder_text='Confirmar Contraseña', width=220, height=40, show="*")
        self.contraseña_entry_confirmar.grid(columnspan=2, row=5, padx=4, pady=4)

        self.rut_entry = ck.CTkEntry(self, placeholder_text='RUT', width=220, height=40)
        self.rut_entry.grid(columnspan=2, row=6, padx=4, pady=4)
        self.rut_entry.bind("<Return>", self.registrar)

        self.mostrarContraseña_Registro = tk.BooleanVar()
        show_password_checkbox = ck.CTkCheckBox(self, text="Mostrar contraseña", variable=self.mostrarContraseña_Registro, command=self.mostrarContraseñaRegistro)
        show_password_checkbox.grid(column=4, row=5, padx=4, pady=4)

    def crear_boton_registrar(self):
        # Crea el botón de registro
        button_registrar = ck.CTkButton(self, text="Registrar", command=self.registrar)
        button_registrar.grid(columnspan=2, row=7, padx=4, pady=4)


    def mostrarContraseñaRegistro(self):
        # Cambia la visibilidad de la contraseña basado en el estado del checkbox
        if self.mostrarContraseña_Registro.get():
            self.contraseña_entry.configure(show="")
            self.contraseña_entry_confirmar.configure(show="")
        else:
            self.contraseña_entry.configure(show="*")
            self.contraseña_entry_confirmar.configure(show="*")

    def registrar(self, event=None):
        # Obtiene los datos ingresados por el usuario
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        correo = self.correo_entry.get()
        contraseña = self.contraseña_entry.get()
        confirmarContraseña = self.contraseña_entry_confirmar.get()
        rut = self.rut_entry.get()

        if correo == "":
            messagebox.showerror("Error de registro", "Debe ingresar un correo")
            return
        
        if contraseña != confirmarContraseña:
            messagebox.showerror("Error de registro", "Las contraseña no coinciden")
            return

        if self.bd.registro(nombre, apellido, correo, contraseña, rut):
            self.withdraw()  # Oculta la ventana de registro
            self.parent.deiconify()  # Muestra la ventana principal
            self.destroy()


class Frame(ck.CTkFrame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.bd = BD()
        self.bd.conectar()

        self.pack()
        
        self.loginWindow()

    def login(self, event = None):
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

    def mostrarContraseña(self):
        if self.show_password.get():
            self.contraseña_entry.configure(show="")
        else:
            self.contraseña_entry.configure(show="*")

    def abrir_ventana_registro(self):
        ventana_registro = VentanaRegistro(self.root, self.bd)
        self.root.wait_window(ventana_registro)

    def loginWindow(self):
        # Correo electrónico
        self.correo = ck.CTkEntry(self, placeholder_text='Correo electrónico', width=220, height=40)
        self.correo.grid(columnspan=2, row=1, padx=4, pady=4)

        # Contraseña
        self.contraseña = tk.StringVar()
        self.contraseña_entry = ck.CTkEntry(self, placeholder_text='Contraseña', width=220, height=40, show="*")
        self.contraseña_entry.grid(columnspan=2, row=2, padx=4, pady=4)
        self.contraseña_entry.bind("<Return>", self.login)

        # Checkbox para mostrar/ocultar la contraseña
        self.show_password = tk.BooleanVar()
        show_password_checkbox = ck.CTkCheckBox(self, text="Mostrar contraseña", variable=self.show_password, command=self.mostrarContraseña)
        show_password_checkbox.grid(column=8, row=2, padx=4, pady=4)

        # Botón
        button_login = ck.CTkButton(self, text="Iniciar sesión", command=self.login)
        button_login.grid(columnspan=2, row=4, padx=4, pady=4)

        button_registrar = ck.CTkButton(self, text="Registrarse", command=self.abrir_ventana_registro)
        button_registrar.grid(columnspan=2, row=5, padx=4, pady=4)



class VentanaPrincipal(ck.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.bd = BD()
        self.iconbitmap('img/libros.ico')
        self.title("Ventana Principal")

        self.menu_principal = ck.CTkOptionMenu(self)
        self.config(menu=self.menu_principal)

        self.menu_registro = ck.CTkOptionMenu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Registrar", menu=self.menu_registro)
        self.menu_registro.add_command(label="Registrar Préstamo", command=self.mostrar_formulario_prestamo)

        # Variables de control para los entrys
        self.usuario_var = tk.StringVar()
        self.fecha_devolucion_var = tk.StringVar()

    def mostrar_formulario_prestamo(self):
        # Limpiar la ventana principal antes de mostrar el formulario
        self.clear_main_window()

        # Crear los labels y los entrys para el formulario de préstamo
        label_usuario = ck.CTkLabel(self, text="Usuario:")
        label_usuario.pack()
        entry_usuario = ck.CTkEntry(self, textvariable=self.usuario_var)
        entry_usuario.pack()

        label_fecha_devolucion = ck.CTkLabel(self, text="Fecha de devolución:")
        label_fecha_devolucion.pack()
        entry_fecha_devolucion = ck.CTkEntry(self, textvariable=self.fecha_devolucion_var)
        entry_fecha_devolucion.pack()

        button_registrar = ck.CTkLabel(self, text="Registrar", command=self.registrar_prestamo_bd)
        button_registrar.pack()

    def registrar_prestamo_bd(self):
        usuario = self.usuario_var.get()
        fecha_devolucion = self.fecha_devolucion_var.get()

        # Aquí puedes llamar al método registrarPrestamo de la clase BD
        self.bd.registrarPrestamo(usuario)

        self.clear_main_window()
    
    def clear_main_window(self):
        # Limpiar la ventana principal eliminando todos los widgets existentes
        for widget in self.winfo_children():
            widget.destroy()

    def cerrar_sesion(self):
        self.destroy()
        self.parent.deiconify()