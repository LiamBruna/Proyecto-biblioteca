import tkinter as tk
import customtkinter as ck
from tkinter import messagebox
from PIL import Image
import os

from model.conexion_db import *
from model.classes import *

class VentanaRegistro(ck.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Registro")
        self.parent.iconbitmap('img\libros.ico')
        self.resizable(0, 0)

        self.bd = BD()

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
        ventana_registro = VentanaRegistro(self.root)
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
        self.parent.iconbitmap('img\\libros.ico')
        self.title("Ventana Principal")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        self.logo_image = ck.CTkImage(Image.open("img\\CustomTkinter_logo_single.png"), size=(20, 20))
        self.large_test_image = ck.CTkImage(Image.open("img\\large_test_image.png"), size=(20, 20))
        self.image_icon_image = ck.CTkImage(Image.open("img\\image_icon_light.png"), size=(20, 20))
        self.home_image = ck.CTkImage(light_image=Image.open("img\\home_dark.png"), size=(20, 20))
        self.chat_image = ck.CTkImage(light_image=Image.open("img\\chat_dark.png"), size=(20, 20))
        self.add_user_image = ck.CTkImage(light_image=Image.open("img\\add_user_dark.png"),size=(20, 20))

        # create navigation frame
        self.navigation_frame = ck.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ck.CTkLabel(self.navigation_frame, text="  Image Example", image=self.logo_image,
                                                             compound="left", font=ck.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ck.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = ck.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = ck.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = ck.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        self.button_cerrarSesion = ck.CTkButton(self.navigation_frame, text="Cerrar sesión", command=self.cerrar_sesion)
        self.button_cerrarSesion.grid(row = 7, column = 0, padx=20, pady=20, sticky="s")


        # create home frame
        self.home_frame = ck.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = ck.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = ck.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = ck.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = ck.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = ck.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = ck.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = ck.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        ck.set_appearance_mode(new_appearance_mode)

    def cerrar_sesion(self):
        self.destroy()
        self.parent.deiconify()
