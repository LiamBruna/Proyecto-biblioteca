import tkinter as tk # Modulo para crear la interfaz gráfica
import customtkinter as ck # Modulo para mejorar la interfaz gráfica
from tkinter import messagebox # Modulo para mostrar mensajes en ventanas emergentes
from tkinter import ttk # Modulo para darle estilos a los widgets presentes en la app
from PIL import Image, ImageTk # Modulo para importar imágenes
import re # Modulo para poder validar si el correo electrónico es un correo electrónico

from model.conexion_db import *
from model.classes import *


# Ventana de registro
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

    def registerWindow(self):
        # Crea los campos de entrada de datos para el registro
        self.nombre_entry = ck.CTkEntry(self, placeholder_text='Nombre (*)', width=220, height=40)
        self.nombre_entry.grid(columnspan=2, row=1, padx=4, pady=4)

        self.apellido_entry = ck.CTkEntry(self, placeholder_text='Apellido (*)', width=220, height=40)
        self.apellido_entry.grid(columnspan=2, row=2, padx=4, pady=4)

        self.correo_entry = ck.CTkEntry(self, placeholder_text='Correo electrónico (*)', width=220, height=40)
        self.correo_entry.grid(columnspan=2, row=3, padx=4, pady=4)

        self.contraseña_entry = ck.CTkEntry(self, placeholder_text='Contraseña', width=220, height=40, show="*")
        self.contraseña_entry.grid(columnspan=2, row=4, padx=4, pady=4)

        self.contraseña_entry_confirmar = ck.CTkEntry(self, placeholder_text='Confirmar Contraseña', width=220, height=40, show="*")
        self.contraseña_entry_confirmar.grid(columnspan=2, row=5, padx=4, pady=4)

        self.rut_entry = ck.CTkEntry(self, placeholder_text='RUT (con puntos y guión)', width=220, height=40)
        self.rut_entry.grid(columnspan=2, row=6, padx=4, pady=4)
        self.rut_entry.bind("<Return>", self.registrar)

        self.mostrarContraseña_Registro = tk.BooleanVar()
        show_password_checkbox = ck.CTkCheckBox(self, text="Mostrar contraseña", variable=self.mostrarContraseña_Registro, command=self.mostrarContraseñaRegistro)
        show_password_checkbox.grid(column=4, row=5, padx=4, pady=4)

        registro_image = Image.open("img\\registro.png")
        registro_photo = ck.CTkImage(registro_image)

        # Crea el botón de registro
        button_registrar = ck.CTkButton(self, text="Registrar", command=self.registrar, image=registro_photo)
        button_registrar.grid(columnspan=2, row=7, padx=4, pady=4)

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
        correo = self.correo_entry.get()
        contraseña = self.contraseña_entry.get()
        confirmarContraseña = self.contraseña_entry_confirmar.get()
        rut = self.rut_entry.get()

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

        label_log = ck.CTkLabel(master=frame, text="Iniciar Sesión", font=('Century Gothic',35))
        label_log.place(x=50, y=45)

        self.correo = ck.CTkEntry(master=frame, placeholder_text='Correo electrónico', width=220, height=40)
        self.correo.place(x=50, y=110)

        self.contraseña = tk.StringVar()
        self.contraseña_entry = ck.CTkEntry(master=frame, placeholder_text='Contraseña', width=220, height=40, show="*")
        self.contraseña_entry.place(x=50, y=165)
        self.contraseña_entry.bind("<Return>", self.login)

        # Checkbox para mostrar/ocultar la contraseña
        self.mostrar_contraseña = tk.BooleanVar()
        self.checkbox_mostrar_contraseña = ck.CTkCheckBox(master=frame, text="Mostrar contraseña", variable=self.mostrar_contraseña, command=self.mostrarContraseña)
        self.checkbox_mostrar_contraseña.place(x=30, y=220)

        iniciar_sesion_image = Image.open("img\\iniciar_sesion.png")
        iniciar_sesion_photo = ck.CTkImage(iniciar_sesion_image)
        self.button_login = ck.CTkButton(master=frame, text="Iniciar sesión", command=self.login, image=iniciar_sesion_photo)
        self.button_login.place(x=12, y=280)

        registrarse_image = Image.open("img\\registrarse.png")
        registrarse_photo = ck.CTkImage(registrarse_image)
        self.button_registrar = ck.CTkButton(master=frame, text="Registrarse", command=self.abrir_ventana_registro, image=registrarse_photo)
        self.button_registrar.place(x=168, y=280)

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

        # Crear Frame lateral de navegación
        self.frameNavegacion = ck.CTkFrame(self, corner_radius=0)
        self.frameNavegacion.grid(row=0, column=0, sticky="nsew")
        self.frameNavegacion.grid_rowconfigure(4, weight=1)


        # Crear icono en frame lateral
        self.frameNavegacion_label = ck.CTkLabel(self.frameNavegacion, text="  Biblioteca Virtual", image=self.logo_imagen,
                                                  compound="left", font=ck.CTkFont(size=15, weight="bold"))
        self.frameNavegacion_label.grid(row=0, column=0, padx=20, pady=20)

        # Botón de Inicio en navegación
        self.inicio_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Inicio",
                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                        hover_color=("gray70", "gray30"), image=self.home_image, anchor="w",
                                        command=self.inicio_button_evento, font=('Calibri (body)', 20, 'bold'))
        self.inicio_button.grid(row=1, column=0, sticky="ew")

        self.catalogo_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Catalogo",
                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                        hover_color=("gray70", "gray30"), image=self.home_image, anchor="w",
                                        command=self.catalogo_button_evento, font=('Calibri (body)', 20, 'bold'))
        self.catalogo_button.grid(row=2, column=0, sticky="ew")

        # Botón de Stock en navegación
        self.stock_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Stock",
                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"), image=self.stock_image, anchor="w",
                                         command=self.stock_button_evento, font=('Calibri (body)', 20, 'bold'))
        self.stock_button.grid(row=3, column=0, sticky="ew")

        # Botón de Usuarios en navegación
        self.usuario_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Usuarios Registrados",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                           image=self.usuario_image, anchor="w",command=self.usuario_button_evento, font=('Calibri (body)', 20, 'bold'))
        self.usuario_button.grid(row=4, column=0, sticky="ew")

        # Botón de Realizar prestamos en navegación
        self.realizar_prestamo_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10,
                                           text="Realizar Prestamo", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), image=self.chat_image, anchor="w",
                                           command=self.realizarPrestamo_button_evento, font=('Calibri (body)', 20, 'bold'))
        self.realizar_prestamo_button.grid(row=5, column=0, sticky="ew")

        # Otro botón
        self.frame_3_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10,
                                           text="Frame 3", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), image=self.add_user_image, anchor="w",
                                           command=self.frame_3_button_event, font=('Calibri (body)', 20, 'bold'))
        self.frame_3_button.grid(row=6, column=0, sticky="ew")

        # Menu de opciones para cambiar de apariencia la app
        self.menu_apariencia = ck.CTkOptionMenu(self.frameNavegacion, font=('Calibri (body)', 15, 'bold'), values=["Dark", "Light"], command=self.evento_cambiar_apariencia)
        self.menu_apariencia.grid(row=7, column=0, padx=20, pady=20, sticky="s")

        # Botón para cerrar sesion
        self.button_cerrarSesion = ck.CTkButton(self.frameNavegacion, font=('Calibri (body)', 15, 'bold'), text="Cerrar sesión", image=self.cerrar_sesion_imagen, command=self.cerrar_sesion)
        self.button_cerrarSesion.grid(row=8, column=0, padx=20, pady=20, sticky="s")

        # Crear contenedor main
        self.main_frame = ck.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # Crear frame inicio
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

        # Crear frame para el catalogo
        self.catalogo = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.catalogo.grid(row=0, column=0, sticky="nsew")
        self.catalogo.grid_columnconfigure(0, weight=1)  # Expansión horizontal
        self.catalogo.grid_rowconfigure(1, weight=1)  # Expansión vertical

        # Crear frame para el stock
        self.stock = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.stock.grid(row=0, column=0, sticky="nsew")

        self.actualizar_stock_label_image = ck.CTkLabel(self.stock, text="", image=self.actualizar_stock_image)
        self.actualizar_stock_label_image.grid(row=0, columnspan=3, padx=20)

        self.buscar_libro_isbn_label = ck.CTkLabel(self.stock, text="Ingrese el ISBN del libro para actualizar stock: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.buscar_libro_isbn_label.grid(row=10, column=0, padx=10)

        self.buscar_libro_isbn_entry = ck.CTkEntry(self.stock, width=140, textvariable=self.buscar_actualiza)
        self.buscar_libro_isbn_entry.grid(row=10, column=1, padx=10)
        self.buscar_libro_isbn_entry.bind("<Return>", self.actualizarStock)

        # Botón para buscar el libro
        self.buscar_libro_isbn_button = ck.CTkButton(self.stock, command=self.actualizarStock, text="BUSCAR", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
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

        # Botón para actualizar el stock del libro
        self.buscar_libro_isbn_button = ck.CTkButton(self.stock, text="ACTUALIZAR", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.buscar_libro_isbn_button.place(x=600, y=400)

        # Crear frame para mostrar a los usuarios
        self.usuario = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent", bg_color="gray90")
        self.usuario.grid(row=0, column=0, sticky="nsew")
        self.usuario.grid_columnconfigure(0, weight=1)  # Expansión horizontal
        self.usuario.grid_rowconfigure(1, weight=1)  # Expansión vertical

        actualizar_button = ck.CTkButton(self.usuario, text='ACTUALIZAR TABLA', font=('Arial', 11, 'bold'), command=self.mostrarDatos)
        actualizar_button.grid(columnspan=1, row=2, pady=5)
        
        # Estilo de la tabla para mostrar los datos
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font=('Helvetica', 10, 'bold'), foreground='black', background='white')
        estilo_tabla.map('Treeview', background=[('selected', 'green')], foreground=[('selected', 'black')])
        estilo_tabla.configure('Heading', background='white', foreground='navy', padding=3, font=('Calibri (body)', 10, 'bold'))
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

        self.tabla_uno.bind("<<TreeviewSelect>>", self.obtener_fila)

        # Ajustar expansión del marco principal
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


        # Crear frame realizar préstamos
        self.realizar_prestamo = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")

        # select default frame
        self.seleccion_frame_nombre("home")


    # Método para buscar el frame por el nombre del frame
    def seleccion_frame_nombre(self, name):
        self.inicio_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.catalogo_button.configure(fg_color=("gray75", "gray25") if name == "catalogo" else "transparent")
        self.usuario_button.configure(fg_color=("gray75", "gray25") if name == "usuarios" else "transparent")
        self.stock_button.configure(fg_color=("gray75", "gray25") if name == "stock" else "transparent")
        self.realizar_prestamo_button.configure(fg_color=("gray75", "gray25") if name == "realizar_prestamo" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # Mostrar frame seleccionado
        if name == "home":
            self.inicio_frame.grid(row=0, column=0, sticky="nsew")
            self.catalogo.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.realizar_prestamo.grid_forget()
            self.third_frame.grid_forget()
        elif name == "catalogo":
            self.inicio_frame.grid_forget()
            self.catalogo.grid(row=0, column=0, sticky="nsew")
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.realizar_prestamo.grid_forget()
            self.third_frame.grid_forget()
        elif name == "stock":
            self.inicio_frame.grid_forget()
            self.stock.grid(row=0, column=0, sticky="nsew")
            self.usuario.grid_forget()
            self.realizar_prestamo.grid_forget()
            self.third_frame.grid_forget()
        elif name == "usuarios":
            self.inicio_frame.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid(row=0, column=0, sticky="nsew")
            self.realizar_prestamo.grid_forget()
            self.third_frame.grid_forget()
        elif name == "realizar_prestamo":
            self.inicio_frame.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.realizar_prestamo.grid(row=0, column=0, sticky="nsew")
            self.third_frame.grid_forget()
        elif name == "frame_3":
            self.inicio_frame.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.realizar_prestamo.grid_forget()
            self.third_frame.grid(row=0, column=0, sticky="nsew")

    # Métodos para que cuando se presione el botón con este método, muestre el frame relacionado
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

    def frame_3_button_event(self):
        self.seleccion_frame_nombre("frame_3")

    # Método para cambiar la apariencia de la app
    def evento_cambiar_apariencia(self, new_appearance_mode):
        ck.set_appearance_mode(new_appearance_mode)

    # Método para actualizar el stock de libros
    def actualizarStock(self, event = None):
        isbn = self.buscar_actualiza.get()  # Obtener el ISBN ingresado

        if isbn == "":
            messagebox.showerror("Stock", "Debe de ingresar un ISBN para realizar la busqueda.")
            return
        
        libros = self.bd.buscarLibro(isbn)  # Buscar el libro en la base de datos
        
        if libros:
            isbn, titulo, num_paginas, stock = libros[0][1:5]  # Tomar los elementos del índice 1 al 4
            self.isbn.set(str(isbn))  # Actualizar el campo ISBN
            self.titulo.set(str(titulo))  # Actualizar el campo Título
            self.numero_paginas.set(int(num_paginas))  # Actualizar el campo Número de Páginas
            self.stockLibro.set(int(stock))  # Actualizar el campo Stock
        else:
            messagebox.showerror("Stock", f"El libro con el ISBN {isbn} no existe.")
            self.limpiarCampos()



    def limpiarCampos(self):
        self.isbn.set('')
        self.titulo.set('')
        self.numero_paginas.set('')
        self.stockLibro.set('')



    # Método para mostrar los datos en la tabla de usuarios
    def mostrarDatos(self):
        datos = self.bd.mostrarUsuarios()
        self.tabla_uno.delete(*self.tabla_uno.get_children())
        i = -1
        for dato in datos:
            i = i + 1
            self.tabla_uno.insert('', i, text=datos[i][0], values=datos[i][1:8])

        messagebox.showinfo("Usuarios registrados", "La tabla ha sido actualizada.")

    # Método para poder seleccionar la fila en la tabla de usuarios
    def obtener_fila(self, event):
        current_item = self.tabla_uno.focus()
        if not current_item:
            return
        data = self.tabla_uno.item(current_item)
        self.nombre_borrar = data['values'][0]

    # Método para cerrar sesion en la app
    def cerrar_sesion(self):
        self.destroy()
        self.parent.deiconify()