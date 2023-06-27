import customtkinter as ck # Modulo para mejorar la interfaz gráfica
import tkinter as tk # Modulo para crear la interfaz gráfica
from tkinter import messagebox # Modulo para mostrar mensajes en ventanas emergentes
from tkinter import ttk # Modulo para darle estilos a los widgets presentes en la app
from tkcalendar import DateEntry # Modulo para seleccionar una fecha median un calendario
from PIL import Image, ImageTk # Modulo para importar imágenes
import re # Modulo para poder validar si el correo electrónico es un correo electrónico
import datetime as d

from model.conexion_db import *


# Ventana de registro
class VentanaRegistro(ck.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Registro")
        self.iconbitmap('img\\libros.ico')
        self.geometry("700x600")
        self.resizable(0, 0)

        self.bd = BD()

        self.mostrar_contraseña = tk.BooleanVar(value=False)  # Variable para controlar la visibilidad de la contraseña

        # Crear imagen de fondo como PhotoImage
        imagen_fondo = ImageTk.PhotoImage(Image.open("img\\pattern.png"))

        # Crear etiqueta para la imagen de fondo
        fondo = ck.CTkLabel(master=self, image=imagen_fondo)
        fondo.pack()

        frame_registro = ck.CTkFrame(master=fondo, corner_radius=15)
        frame_registro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        frame_registro.configure(width=500, height=500)

        label_log = ck.CTkLabel(master=frame_registro, text="Registrarse", font=ck.CTkFont(size=30, weight="bold", family="Calibri (body)"))
        label_log.place(x=170, y=45)

        # Crea los campos de entrada de datos para el registro
        self.nombre_entry = ck.CTkEntry(frame_registro, placeholder_text='Nombre (*)', width=220, height=40, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.nombre_entry.place(x=90, y=100)

        self.apellido_entry = ck.CTkEntry(frame_registro, placeholder_text='Apellido (*)', width=220, height=40, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.apellido_entry.place(x=90, y=150)

        self.rut_entry = ck.CTkEntry(frame_registro, placeholder_text='RUT (con puntos y guión)', width=220, height=40, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.rut_entry.place(x=90, y=200)

        self.correo_entry = ck.CTkEntry(frame_registro, placeholder_text='Correo electrónico (*)', width=220, height=40, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.correo_entry.place(x=90, y=250)

        self.contraseña_entry = ck.CTkEntry(frame_registro, placeholder_text='Contraseña', width=220, height=40, show="*",font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.contraseña_entry.place(x=90, y=300)

        self.contraseña_entry_confirmar = ck.CTkEntry(frame_registro, placeholder_text='Confirmar Contraseña', width=220, height=40, show="*", font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.contraseña_entry_confirmar.place(x=90, y=350)
        self.contraseña_entry_confirmar.bind("<Return>", self.registrar)

        # Este es un checkbox para mostrar la contraseña que estamos ingresando
        self.mostrarContraseña_Registro = tk.BooleanVar()
        mostrar_contraseña_checkbox = ck.CTkCheckBox(frame_registro, text="Mostrar contraseña", variable=self.mostrarContraseña_Registro, command=self.mostrarContraseñaRegistro, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        mostrar_contraseña_checkbox.place(x=320, y=358)

        self.registro_photo = ck.CTkImage(Image.open("img\\registro.png"), size=(30,30))

        # Botón para registrarse
        button_registrar = ck.CTkButton(frame_registro, width=200, text="Registrarse", command=self.registrar, image=self.registro_photo, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        button_registrar.place(x=150, y=420)

# Método para validar el correo electrónico
    def validarCorreo(self, correo):
        patron = r'^[\w\.-]+@\w+\.\w+$'

        if re.match(patron, correo):
            return True
        else:
            return False

# Método para validar el RUT ingresado
    def validarRut(self, rut):
        rut = rut.replace(".", "").replace("-", "") #Remover puntos y guiones
        rutSinDv = rut[:-1] #Obtener el rut sin dígito verificador
        dv = rut[-1] #Obtener el dígito verificador

        #Calcular el dígito verificador
        suma = 0
        multiplo = 2
        for i in reversed(rutSinDv):
            suma += int(i) * multiplo
            multiplo +=1
            if multiplo == 8:
                multiplo = 2

        resto = suma % 11
        dvEsperado = str(11 - resto) if resto > 1 else "0"

        if dv == dvEsperado:
            return True
        else:
            return False
        
# Método para mostrar la contraseña al presionar el Checkbox
    def mostrarContraseñaRegistro(self):
        # Cambia la visibilidad de la contraseña basado en el estado del checkbox
        if self.mostrarContraseña_Registro.get():
            self.contraseña_entry.configure(show="")
            self.contraseña_entry_confirmar.configure(show="")
        else:
            self.contraseña_entry.configure(show="*")
            self.contraseña_entry_confirmar.configure(show="*")

# Método para registrar un Bibliotecario
    def registrar(self, event=None):
        # Obtiene los datos ingresados por el usuario
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        rut = self.rut_entry.get()
        correo = self.correo_entry.get()
        contraseña = self.contraseña_entry.get()
        confirmarContraseña = self.contraseña_entry_confirmar.get()
        
        if nombre == "": # Comprobar que haya un nombre en el campo
            messagebox.showerror("Error de registro", "El campo 'nombre' no puede estar vació.")
            return

        if apellido == "": # Comprobar que haya un apellido en el campo
            messagebox.showerror("Error de registro", "El campo 'apellido' no puede estar vació.")

        if correo == "": #Comprobar que haya un correo en el campo
            messagebox.showerror("Error de registro", "Debe ingresar un correo.")
            return
        
        if not self.validarCorreo(correo):
            messagebox.showerror("Error de registro", f"Correo {correo} no válido.")
            return
        
        if contraseña != confirmarContraseña: #Validación de contraseña
            messagebox.showerror("Error de registro", "Las contraseña no coinciden.")
            return
        
        if not self.validarRut(rut): # Validación del RUT
            messagebox.showerror("Error de registro", f"Rut {rut} no válido.")
            return

        if self.bd.registro(nombre, apellido, correo, contraseña, rut):
            self.withdraw()  # Oculta la ventana de registro
        self.parent.deiconify()  # Muestra la ventana de login
        self.destroy()


# Ventana Login
class Frame(ck.CTkFrame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.bd = BD()
        self.bd.conectar()

        # Crear imagen de fondo como PhotoImage
        imagen_fondo = ImageTk.PhotoImage(Image.open("img\\pattern.png"))

        # Crear etiqueta para la imagen de fondo
        fondo = ck.CTkLabel(master=self.root, image=imagen_fondo)
        fondo.pack()

        frame=ck.CTkFrame(master=fondo, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_log = ck.CTkLabel(master=frame, text="Iniciar Sesión", font=ck.CTkFont(size=30, weight="bold", family="Calibri (body)"))
        label_log.place(x=60, y=45)

        self.correo = ck.CTkEntry(master=frame, placeholder_text='Correo electrónico', width=220, height=40, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.correo.place(x=50, y=110)

        self.contraseña = tk.StringVar()
        self.contraseña_entry = ck.CTkEntry(master=frame, placeholder_text='Contraseña', width=220, height=40, show="*", font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.contraseña_entry.place(x=50, y=165)
        self.contraseña_entry.bind("<Return>", self.login)

        # Checkbox para mostrar/ocultar la contraseña
        self.mostrar_contraseña = tk.BooleanVar()
        self.checkbox_mostrar_contraseña = ck.CTkCheckBox(master=frame, text="Mostrar contraseña", variable=self.mostrar_contraseña, command=self.mostrarContraseña, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.checkbox_mostrar_contraseña.place(x=30, y=220)

        iniciar_sesion_photo = ck.CTkImage(Image.open("img\\iniciar_sesion.png"), size=(25, 25))
        self.button_login = ck.CTkButton(master=frame, text="Iniciar sesión", command=self.login, image=iniciar_sesion_photo, font=ck.CTkFont(size=18, weight="bold", family="Calibri (body)"))
        self.button_login.place(x=80, y=253)

        registrarse_photo = ck.CTkImage(Image.open("img\\registrarse.png"), size=(25, 25))
        self.button_registrar = ck.CTkButton(master=frame, text="Registrarse", command=self.abrir_ventana_registro, image=registrarse_photo, font=ck.CTkFont(size=18, weight="bold", family="Calibri (body)"))
        self.button_registrar.place(x=86, y=300)

    def login(self, event=None):
        correo = self.correo.get()
        contraseña = self.contraseña_entry.get()

        if not correo:
            messagebox.showerror("Error de inicio de sesión", "Debe ingresar un correo.")
            return

        # Verifica si el correo existe en la base de datos
        if self.bd.login(correo, contraseña):
            self.root.withdraw()
            ventana_principal = VentanaPrincipal(self.root)
            self.root.wait_window(ventana_principal)
            self.limparCampos()

    def mostrarContraseña(self):
        if self.mostrar_contraseña.get():
            self.contraseña_entry.configure(show="")
        else:
            self.contraseña_entry.configure(show="*")

    def abrir_ventana_registro(self):
        self.root.withdraw()
        ventana_registro = VentanaRegistro(self.root)
        self.root.wait_window(ventana_registro)

    def limparCampos(self):
        self.correo.delete(0, 'end')
        self.contraseña_entry.delete(0, 'end')
        

# Ventana principal de la aplicación
class VentanaPrincipal(ck.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.bd = BD()
        self.iconbitmap('img\\libros.ico')
        self.title("Ventana Principal")
        self.resizable(0, 0)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Variables de texto para el Frame de stock
        self.stockLibro = ck.StringVar()
        self.numero_paginas = ck.StringVar()
        self.titulo = ck.StringVar()
        self.isbn = ck.StringVar()
        self.buscar_actualiza = ck.StringVar()

        # Variables de texto para el Frame Realizar Préstamo
        self.rut_usuario = ck.StringVar()
        self.tipo_usuario = ck.StringVar()

        # Cargar imágenes para Menu
        self.logo_imagen = ck.CTkImage(Image.open("img\\libros.ico"), size=(30, 30))
        self.large_test_image = ck.CTkImage(Image.open("img\\large_test_image.png"), size=(500, 150))
        self.image_icon_image = ck.CTkImage(Image.open("img\\image_icon_light.png"), size=(26, 26))
        self.home_image = ck.CTkImage(light_image=Image.open("img\\home_dark.png"), size=(26, 26))
        self.chat_image = ck.CTkImage(light_image=Image.open("img\\chat_dark.png"), size=(26, 26))
        self.add_user_image = ck.CTkImage(light_image=Image.open("img\\add_user_dark.png"), size=(26, 26))
        self.cerrar_sesion_imagen = ck.CTkImage(Image.open("img\\cerrar_sesion.png"))
        self.stock_image = ck.CTkImage(Image.open("img\\stock.png"), size=(26, 26))
        self.usuario_image = ck.CTkImage(Image.open("img\\usuarios.png"), size=(26, 26))
        self.actualizar_stock_image = ck.CTkImage(Image.open("img\\actualizar_stock.png"), size=(450, 120))
        self.usuarios_registrados_image = ck.CTkImage(Image.open("img\\usuarios_registrados.png"), size=(450, 120))
        self.libros_prestamo_image = ck.CTkImage(Image.open("img\\libros_en_prestamo.png"), size=(450, 120))
        self.realizar_prestamo_image = ck.CTkImage(Image.open("img\\realizar_prestamo.png"), size=(450, 120))

        # Crear Frame lateral de navegación
        self.frameNavegacion = ck.CTkFrame(self, corner_radius=0)
        self.frameNavegacion.grid(row=0, column=0, sticky="nsew")
        self.frameNavegacion.grid_rowconfigure(4, weight=1)


        # Crear icono en frame lateral
        self.frameNavegacion_label = ck.CTkLabel(self.frameNavegacion, text="  Biblioteca Virtual", image=self.logo_imagen,
                                                  compound="left", font=ck.CTkFont(size=30, weight="bold", family="Calibri (body)"))
        self.frameNavegacion_label.grid(row=0, column=0, padx=20, pady=20)

        # Botón de Inicio en navegación
        self.inicio_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Inicio",
                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                        hover_color=("gray70", "gray30"), image=self.home_image, anchor="w",
                                        command=self.inicio_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.inicio_button.grid(row=1, column=0, sticky="ew")

        self.catalogo_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Catalogo",
                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                        hover_color=("gray70", "gray30"), image=self.home_image, anchor="w",
                                        command=self.catalogo_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.catalogo_button.grid(row=2, column=0, sticky="ew")

        # Botón de Stock en navegación
        self.stock_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Actualizar Stock",
                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"), image=self.stock_image, anchor="w",
                                         command=self.stock_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.stock_button.grid(row=3, column=0, sticky="ew")

        # Botón de Usuarios en navegación
        self.usuario_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Usuarios Registrados",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                           image=self.usuario_image, anchor="w",command=self.usuario_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.usuario_button.grid(row=4, column=0, sticky="ew")

        # Botón de Realizar prestamos en navegación
        self.realizar_prestamo_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10,
                                           text="Realizar Prestamo", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), image=self.chat_image, anchor="w",
                                           command=self.realizarPrestamo_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.realizar_prestamo_button.grid(row=5, column=0, sticky="ew")

        # Otro botón
        self.frame_libros_en_prestamo_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10,
                                           text="Libros en Préstamo", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), image=self.add_user_image, anchor="w",
                                           command=self.frame_libros_en_prestamo_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.frame_libros_en_prestamo_button.grid(row=6, column=0, sticky="ew")

        # Menu de opciones para cambiar de apariencia la app
        self.menu_apariencia = ck.CTkOptionMenu(self.frameNavegacion, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"), values=["Dark", "Light"], command=self.evento_cambiar_apariencia)
        self.menu_apariencia.grid(row=7, column=0, padx=20, pady=20, sticky="s")

        # Botón para cerrar sesion
        self.button_cerrarSesion = ck.CTkButton(self.frameNavegacion, font=ck.CTkFont(size=18, weight="bold", family="Calibri (body)"), text="Cerrar sesión", image=self.cerrar_sesion_imagen, command=self.cerrar_sesion)
        self.button_cerrarSesion.grid(row=8, column=0, padx=20, pady=20, sticky="s")

        # CONTENEDOR MAINS
        self.main_frame = ck.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # FRAME INICIO DE APP
        self.inicio_frame = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.inicio_frame.grid(row=0, column=0, sticky="nsew")
        self.inicio_frame.grid_columnconfigure(0, weight=1)

        self.inicio_frame_large_image_label = ck.CTkLabel(self.inicio_frame, text="", image=self.large_test_image)
        self.inicio_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.inicio_frame_button_1 = ck.CTkButton(self.inicio_frame, text="", image=self.image_icon_image)
        self.inicio_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.inicio_frame_button_2 = ck.CTkButton(self.inicio_frame, text="CTkButton", image=self.image_icon_image,
                                                compound="right")
        self.inicio_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.inicio_frame_button_3 = ck.CTkButton(self.inicio_frame, text="CTkButton", image=self.image_icon_image,
                                                compound="top")
        self.inicio_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.inicio_frame_button_4 = ck.CTkButton(self.inicio_frame, text="CTkButton", image=self.image_icon_image,
                                                compound="bottom", anchor="w")
        self.inicio_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # FRAME MODIFICAR CATALOGO
        self.catalogo = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.catalogo.grid(row=0, column=0, sticky="nsew")
        self.catalogo.grid_columnconfigure(0, weight=1)  # Expansión horizontal
        self.catalogo.grid_rowconfigure(1, weight=1)  # Expansión vertical

        # FRAME ACTUALIZAR STOCK
        self.stock = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.stock.grid(row=0, column=0, sticky="nsew")

        self.actualizar_stock_label_image = ck.CTkLabel(self.stock, text="", image=self.actualizar_stock_image)
        self.actualizar_stock_label_image.grid(row=0, columnspan=3, padx=20)

        self.buscar_libro_isbn_label = ck.CTkLabel(self.stock, text="Ingrese el ISBN del libro para actualizar stock: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.buscar_libro_isbn_label.grid(row=10, column=0, padx=10)

        self.buscar_libro_isbn_entry = ck.CTkEntry(self.stock, width=140, textvariable=self.buscar_actualiza, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.buscar_libro_isbn_entry.grid(row=10, column=1, padx=10)
        self.buscar_libro_isbn_entry.bind("<Return>", self.buscarLibroStock) # Al presionar enter, me devuelve el dato solicitado

        # Botón para buscar el libro
        self.buscar_libro_isbn_button = ck.CTkButton(self.stock, command=self.buscarLibroStock, text="BUSCAR", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.buscar_libro_isbn_button.grid(row=10, column=2, padx=3)

        # Widgets del frame stock a mostrar
        self.isbn_label = ck.CTkLabel(self.stock, text="ISBN: ",
                        font=ck.CTkFont(size=20, weight="bold"))
        self.isbn_label.grid(row=15, column=0, pady=15)

        self.isbn_entry = ck.CTkEntry(self.stock, width=140, textvariable=self.isbn, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.isbn_entry.grid(row=15, columnspan=7, padx=10)
        
        self.titulo_label = ck.CTkLabel(self.stock, text="Titulo: ",
                        font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.titulo_label.grid(row=16, column=0, pady=10)

        self.titulo_entry = ck.CTkEntry(self.stock, width=200, textvariable=self.titulo, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.titulo_entry.grid(row=16, columnspan=7, padx=10)

        self.numero_paginas_label = ck.CTkLabel(self.stock, text="N° de Paginas: ",
                        font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.numero_paginas_label.grid(row=17, column=0, pady=10)

        self.numero_paginas_entry = ck.CTkEntry(self.stock, width=140, textvariable=self.numero_paginas, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.numero_paginas_entry.grid(row=17, columnspan=7, padx=10)

        # Campo que se va a actualizar
        self.stock_label = ck.CTkLabel(self.stock, text="Stock: ",
                        font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.stock_label.grid(row=18, column=0, pady=10)

        self.stock_entry = ck.CTkEntry(self.stock, width=140, textvariable=self.stockLibro, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.stock_entry.grid(row=18, columnspan=7, padx=10)
        self.stock_entry.bind("<Return>", self.actualizarStock)

        # Botón para actualizar el stock del libro
        self.actualizar_stock_button = ck.CTkButton(self.stock, command=self.actualizarStock, text="ACTUALIZAR", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.actualizar_stock_button.place(x=600, y=400)
        
        # FRAME MOSTRAR USUARIOS REGISTRADOS
        self.usuario = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.usuario.grid(row=0, column=0, sticky="nsew")
        self.usuario.grid_columnconfigure(0, weight=1)  # Expansión horizontal
        self.usuario.grid_rowconfigure(1, weight=1)  # Expansión vertical

        self.usuarios_registrados_label_image = ck.CTkLabel(self.usuario, text="", image=self.usuarios_registrados_image)
        self.usuarios_registrados_label_image.grid(row=0, columnspan=1, padx=20)

        self.actualizar_button = ck.CTkButton(self.usuario, text='ACTUALIZAR TABLA', font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"), command=self.mostrarDatosUsuario)
        self.actualizar_button.grid(columnspan=1, row=2, pady=5)
        
        # Estilo de la tabla para mostrar los datos
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font=ck.CTkFont(size=10, weight="bold", family="Calibri (body)"), foreground='black', background='white')
        estilo_tabla.map('Treeview', background=[('selected', 'green')], foreground=[('selected', 'black')])
        estilo_tabla.configure('Heading', background='white', foreground='navy', padding=3, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        estilo_tabla.configure('Item', foreground='transparent', focuscolor='DarkOrchid1')
        estilo_tabla.configure('TScrollbar', arrowcolor='DarkOrchid1', bordercolor='black', troughcolor='DarkOrchid1', background='white')

        # Mostrar la tabla en el frame usuario
        self.frame_tabla_uno = ck.CTkFrame(self.usuario)
        self.frame_tabla_uno.grid(column=0, row=1, sticky='nsew')

        self.tabla_uno = ttk.Treeview(self.frame_tabla_uno)
        self.tabla_uno.grid(column=0, row=0, sticky='nsew')

        ladox = ttk.Scrollbar(self.frame_tabla_uno, orient='horizontal', command=self.tabla_uno.xview)
        ladox.grid(column=0, row=1, sticky='ew')

        ladoy = ttk.Scrollbar(self.frame_tabla_uno, orient='vertical', command=self.tabla_uno.yview)
        ladoy.grid(column=1, row=0, sticky='ns')

        # Configurar expansión en todas las direcciones para el frame y la tabla
        self.frame_tabla_uno.grid_rowconfigure(0, weight=1)
        self.frame_tabla_uno.grid_columnconfigure(0, weight=1)
        self.tabla_uno.grid(sticky='nsew')

        # Columnas que se mostrarán en la tabla
        self.tabla_uno.configure(xscrollcommand=ladox.set, yscrollcommand=ladoy.set)
        self.tabla_uno['columns'] = ('Nombre', 'Apellido', 'Dirección', 'RUT', 'Celular', 'Correo electrónico', 'Tipo de usuario')

        # Ajustar ancho mínimo y ancho de cada columna de encabezado
        self.tabla_uno.column('#0', minwidth=60, width=70, anchor='center')
        self.tabla_uno.column('Nombre', minwidth=100, width=130, anchor='center')
        self.tabla_uno.column('Apellido', minwidth=100, width=120, anchor='center')
        self.tabla_uno.column('Dirección', minwidth=100, width=120, anchor='center')
        self.tabla_uno.column('RUT', minwidth=100, width=105, anchor='center')
        self.tabla_uno.column('Celular', minwidth=100, width=105, anchor='center')
        self.tabla_uno.column('Correo electrónico', minwidth=100, width=150, anchor='center')
        self.tabla_uno.column('Tipo de usuario', minwidth=100, width=120, anchor='center')

        # Configurar el texto de encabezado para que se muestre completo
        self.tabla_uno.heading('#0', text='Id', anchor='center')
        self.tabla_uno.heading('Nombre', text='Nombre', anchor='center')
        self.tabla_uno.heading('Apellido', text='Apellido', anchor='center')
        self.tabla_uno.heading('Dirección', text='Dirección', anchor='center')
        self.tabla_uno.heading('RUT', text='RUT', anchor='center')
        self.tabla_uno.heading('Celular', text='Celular', anchor='center')
        self.tabla_uno.heading('Correo electrónico', text='Correo electrónico', anchor='center')
        self.tabla_uno.heading('Tipo de usuario', text='Tipo de usuario', anchor='center')

        self.tabla_uno.bind("<<TreeviewSelect>>", self.obtener_filaUsuario)

        # Ajustar expansión del marco principal
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


        # FRAME REALIZAR PRESTAMO
        self.frame_realizar_prestamo = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_realizar_prestamo.grid(row=0, column=0, sticky="nsew")

        self.realizar_prestamo_label_image = ck.CTkLabel(self.frame_realizar_prestamo, text="", image=self.realizar_prestamo_image)
        self.realizar_prestamo_label_image.grid(row=0, columnspan=3, padx=20)

        self.rut_usuario_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Ingrese el RUT del Usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.rut_usuario_label.grid(row=10, column=0, pady=5)

        self.rut_usuario_entry = ck.CTkEntry(self.frame_realizar_prestamo, textvariable=self.rut_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.rut_usuario_entry.grid(row=10, column=1, pady=5)
        self.rut_usuario_entry.bind("<Return>", self.obtenerTipoUsuario) # Al presionar enter, me devuelve el dato solicitado
        
        # Botón para buscar al usuario por el rut
        self.buscar_usuario_rut = ck.CTkButton(self.frame_realizar_prestamo, command=self.obtenerTipoUsuario, text="BUSCAR", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.buscar_usuario_rut.grid(row=10, column=2, padx=3)

        self.isbn_libro_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Ingrese el ISBN del Libro: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.isbn_libro_label.grid(row=11, column=0, pady=5)

        self.isbn_libro_entry = ck.CTkEntry(self.frame_realizar_prestamo, width=140, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.isbn_libro_entry.grid(row=11, column=1, padx=5)

        self.fecha_inicio_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Fecha Inicio de Préstamo: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.fecha_inicio_label.grid(row=12, column=0, pady=5)
        
        self.fecha_inicio = DateEntry(self.frame_realizar_prestamo, width=12,
                          date_pattern='yyyy/mm/dd', font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"),
                          highlightbackground="deep sky blue", highlightthickness=1, corner_radius=10)
        self.fecha_inicio.grid(row=12, column=1, pady=5)

        self.fecha_devolucion_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Fecha Devolución de Préstamo: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.fecha_devolucion_label.grid(row=13, column=0, pady=5)

        self.fecha_devolucion = DateEntry(self.frame_realizar_prestamo, width=12,
                          date_pattern='yyyy/mm/dd', font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"),
                          highlightbackground="deep sky blue", highlightthickness=1, corner_radius=10)
        self.fecha_devolucion.grid(row=13, column=1, pady=5)

        self.tipo_usuario_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Tipo de Usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.tipo_usuario_label.grid(row=14, column=0, pady=5)

        self.tipo_usuario_entry = ck.CTkEntry(self.frame_realizar_prestamo, textvariable=self.tipo_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.tipo_usuario_entry.grid(row=14, column=1, padx=5)

        # Botón que realizara el prestamo
        self.completar_prestamo_button = ck.CTkButton(self.frame_realizar_prestamo, text="REALIZAR PRÉSTAMO", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.completar_prestamo_button.place(x=200, y=400)

        # FRAME LIBROS EN PRÉSTAMO
        self.frame_libros_en_prestamo = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_libros_en_prestamo.grid(row=0, column=0, sticky="nsew")
        self.frame_libros_en_prestamo.grid_columnconfigure(0, weight=1) # Expansión horizontal
        self.frame_libros_en_prestamo.grid_rowconfigure(1, weight=1) # Expansión vertical

        self.librosPrestamos_label_image = ck.CTkLabel(self.frame_libros_en_prestamo, text="", image=self.libros_prestamo_image)
        self.librosPrestamos_label_image.grid(row=0, columnspan=1, padx=20)

        actualizar_librosPrestamo_button = ck.CTkButton(self.frame_libros_en_prestamo, text='ACTUALIZAR TABLA LIBROS EN PRÉSTAMO', font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"), command=self.mostrarDatosLibros)
        actualizar_librosPrestamo_button.grid(columnspan=1, row=2, pady=5)

        # Estilo de la tabla para mostrar los datos
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font=ck.CTkFont(size=10, weight="bold", family="Calibri (body)"), foreground='black', background='white')
        estilo_tabla.map('Treeview', background=[('selected', 'green')], foreground=[('selected', 'black')])
        estilo_tabla.configure('Heading', background='white', foreground='navy', padding=3, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        estilo_tabla.configure('Item', foreground='transparent', focuscolor='DarkOrchid1')
        estilo_tabla.configure('TScrollbar', arrowcolor='DarkOrchid1', bordercolor='black', troughcolor='DarkOrchid1', background='white')

        # Mostrar la tabla en el frame libros en prestamo
        self.frame_tabla_dos = ck.CTkFrame(self.frame_libros_en_prestamo)
        self.frame_tabla_dos.grid(column=0, row=1, sticky='nsew')

        self.tabla_dos = ttk.Treeview(self.frame_tabla_dos)
        self.tabla_dos.grid(column=0, row=0, sticky='nsew')

        ladox = ttk.Scrollbar(self.frame_tabla_dos, orient='horizontal', command=self.tabla_dos.xview)
        ladox.grid(column=0, row=1, sticky='ew')

        ladoy = ttk.Scrollbar(self.frame_tabla_dos, orient='vertical', command=self.tabla_dos.yview)
        ladoy.grid(column=1, row=0, sticky='ns')

        # Configurar expansión en todas las direcciones para el frame y la tabla
        self.frame_tabla_dos.grid_rowconfigure(0, weight=1)
        self.frame_tabla_dos.grid_columnconfigure(0, weight=1)
        self.tabla_dos.grid(sticky='nsew')

        # Columnas que se mostrarán en la tabla
        self.tabla_dos.configure(xscrollcommand=ladox.set, yscrollcommand=ladoy.set)
        self.tabla_dos['columns'] = ('Titulo', 'Estado')

        # Ajustar ancho mínimo y ancho de cada columna de encabezado
        self.tabla_dos.column('#0', minwidth=60, width=70, anchor='center')
        self.tabla_dos.column('Titulo', minwidth=100, width=130, anchor='center')
        self.tabla_dos.column('Estado', minwidth=100, width=120, anchor='center')

        # Configurar el texto de encabezado para que se muestre completo
        self.tabla_dos.heading('#0', text='Id', anchor='center')
        self.tabla_dos.heading('Titulo', text='Titulo', anchor='center')
        self.tabla_dos.heading('Estado', text='Estado', anchor='center')

        self.tabla_dos.bind("<<TreeviewSelect>>", self.obtener_filaLibros)

        # Ajustar expansión del marco principal
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # FRAME SELECCIONADO POR DEFECTO
        self.seleccion_frame_nombre("home")

    # Método para buscar el frame por el nombre del frame
    def seleccion_frame_nombre(self, name):
        self.inicio_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.catalogo_button.configure(fg_color=("gray75", "gray25") if name == "catalogo" else "transparent")
        self.usuario_button.configure(fg_color=("gray75", "gray25") if name == "usuarios" else "transparent")
        self.stock_button.configure(fg_color=("gray75", "gray25") if name == "stock" else "transparent")
        self.realizar_prestamo_button.configure(fg_color=("gray75", "gray25") if name == "realizar_prestamo" else "transparent")
        self.frame_libros_en_prestamo.configure(fg_color=("gray75", "gray25") if name == "libros_prestamo" else "transparent")

        # Mostrar frame seleccionado
        if name == "home":
            self.inicio_frame.grid(row=0, column=0, sticky="nsew")
            self.catalogo.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
        elif name == "catalogo":
            self.inicio_frame.grid_forget()
            self.catalogo.grid(row=0, column=0, sticky="nsew")
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
        elif name == "stock":
            self.inicio_frame.grid_forget()
            self.stock.grid(row=0, column=0, sticky="nsew")
            self.usuario.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
        elif name == "usuarios":
            self.inicio_frame.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid(row=0, column=0, sticky="nsew")
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
        elif name == "realizar_prestamo":
            self.inicio_frame.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.frame_realizar_prestamo.grid(row=0, column=0, sticky="nsew")
            self.frame_libros_en_prestamo.grid_forget()
        elif name == "libros_prestamo":
            self.inicio_frame.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid(row=0, column=0, sticky="nsew")

    # Metodos para que cuando se presione el botón con este método, muestre el frame relacionado
    def inicio_button_evento(self):
        self.seleccion_frame_nombre("home")

    def catalogo_button_evento(self):
        self.seleccion_frame_nombre("catalogo")

    def stock_button_evento(self):
        self.seleccion_frame_nombre("stock")

    def usuario_button_evento(self):
        self.seleccion_frame_nombre("usuarios")

    def realizarPrestamo_button_evento(self):
        self.seleccion_frame_nombre("realizar_prestamo")

    def frame_libros_en_prestamo_button_evento(self):
        self.seleccion_frame_nombre("libros_prestamo")

    # Método para cambiar la apariencia de la app
    def evento_cambiar_apariencia(self, new_appearance_mode):
        ck.set_appearance_mode(new_appearance_mode)

    # METODOS PARA EL FRAME STOCK
    # Método para buscar un libro
    def buscarLibroStock(self, event = None):
        isbn = self.buscar_actualiza.get()  # Obtener el ISBN ingresado
        if isbn == "":
            messagebox.showerror("Stock", "Debe de ingresar un ISBN para realizar la busqueda.")
            self.limpiarCampos()
        libros = self.bd.buscarLibro(isbn)  # Buscar el libro en la base de datos
        if libros:
            isbn, titulo, num_paginas, stock = libros[0][1:5]  # Tomar los elementos del índice 1 al 4
            self.isbn.set(str(isbn))  # Actualizar el valor del campo ISBN
            self.titulo.set(str(titulo))  # Actualizar el valor del campo Título
            self.numero_paginas.set(int(num_paginas))  # Actualizar el valor del campo Número de Páginas
            self.stockLibro.set(int(stock))  # Actualizar el valor del campo Stock
        else:
            messagebox.showerror("Stock", f"El libro con el ISBN {isbn} no existe.")
            self.limpiarCampos()

    # Método para actualizar el stock de un libro
    def actualizarStock(self, event = None):
        isbn = self.isbn.get()
        stock = self.stockLibro.get()
        titulo = self.titulo.get()
        self.bd.actualizarStock(stock, isbn)  
        self.limpiarCampos()

    # METODOS PARA EL FRAME USUARIOS REGISTRADOS
    # Método para mostrar los datos en la tabla de usuarios
    def mostrarDatosUsuario(self):
        datos = self.bd.mostrarUsuarios()
        self.tabla_uno.delete(*self.tabla_uno.get_children())
        i = - 1
        for dato in datos:
            i += 1
            self.tabla_uno.insert('', i, text=datos[i][0], values=datos[i][1:8])
        messagebox.showinfo("Usuarios registrados", "La tabla ha sido actualizada.")

    # Método para poder seleccionar la fila en la tabla de usuarios
    def obtener_filaUsuario(self, event):
        current_item = self.tabla_uno.focus()
        if not current_item:
            return
        data = self.tabla_uno.item(current_item)
        self.nombre_borrar = data['values'][0]

    # METODOS PARA EL FRAME LIBROS EN PRESTAMO
    # Método para mostrar los datos en la tabla libros en préstamo
    def mostrarDatosLibros(self):
        datos = self.bd.mostrarLibrosPrestamo()
        self.tabla_dos.delete(*self.tabla_dos.get_children())
        i = - 1
        for dato in datos:
            i += 1
            self.tabla_dos.insert('', i, text=datos[i][0], values=datos[i][1:3])
        messagebox.showinfo("Libros en préstamo", "La tabla ha sido actualizada.")

    # Método para poder seleccionar la fila en la tabla de libros en préstamo
    def obtener_filaLibros(self, event):
        current_item = self.tabla_dos.focus()
        if not current_item:
            return
        data = self.tabla_dos.item(current_item)
        self.nombre_borrar = data['values'][0]

    # METODOS PARA EL FRAME REALIZAR PRESTAMO
    # Método para obtener el tipo de usuario mediante su RUT
    def obtenerTipoUsuario(self, event=None):
        rut = self.rut_usuario.get()
        tipo_usuario = self.bd.obtenerTipoUsuario(rut)
        if tipo_usuario:
            self.tipo_usuario.set(tipo_usuario)
            if tipo_usuario == "Alumno":
                fecha_devolucion = self.calcularFechaDevolucion()
                messagebox.showinfo("Realizar Préstamo", f"Se han sumado 7 días por ser {tipo_usuario}")
                if fecha_devolucion:
                    self.fecha_devolucion.set_date(fecha_devolucion)
            elif tipo_usuario == "Docente":
                self.fecha_devolucion.configure(state="normal")
                messagebox.showinfo("Realizar Préstamo", f"No tiene limite de ")
            else:
                self.fecha_devolucion.configure(state="disabled")
                

    def calcularFechaDevolucion(self):
        fecha_actual = datetime.now().date()
        fecha_devolucion = fecha_actual + timedelta(days=7)
        return fecha_devolucion

    # Método para limpiar los valores en los entry's
    def limpiarCampos(self):
        self.buscar_actualiza.set('')
        self.isbn.set('')
        self.titulo.set('')
        self.numero_paginas.set('')
        self.stockLibro.set('')

    # Método para cerrar sesion en la app
    def cerrar_sesion(self):
        self.destroy()
        self.parent.deiconify()