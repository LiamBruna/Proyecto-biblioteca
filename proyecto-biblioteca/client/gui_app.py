import customtkinter as ck # Modulo para mejorar la interfaz gráfica
import tkinter as tk # Modulo para crear la interfaz gráfica
from tkinter import messagebox # Modulo para mostrar mensajes en ventanas emergentes
from tkinter import ttk # Modulo para darle estilos a los widgets presentes en la app
from tkcalendar import DateEntry # Modulo para seleccionar una fecha median un calendario
from PIL import Image, ImageTk # Modulo para importar imágenes
import re # Modulo para poder validar si el correo electrónico es un correo electrónico
import random # Modulo para crear un código random
from twilio.rest import Client
import io
import time
from datetime import datetime, timedelta
import numpy as np
import cv2

from model.conexion_db import BD
from client.barra import BarraProgreso


# Ventana de registro
class VentanaRegistro(ck.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Biblioteca Virtual")
        #self.iconbitmap('img\\libros.ico')
        self.geometry("700x600")
        self.resizable(0, 0)

        self.bd = BD()

        icono = ImageTk.PhotoImage(Image.open("img\libros.ico"))

        self.iconphoto(True, icono)

        self.mostrar_contraseña = tk.BooleanVar(value=False)  # Variable para controlar la visibilidad de la contraseña
        self.celular = ck.StringVar(value="+56 9")

        # Crear imagen de fondo como PhotoImage
        imagen_fondo = ImageTk.PhotoImage(Image.open("img\\pattern.png"))

        # Crear etiqueta para la imagen de fondo
        fondo = ck.CTkLabel(master=self, image=imagen_fondo)
        fondo.pack()

        frame_registro = ck.CTkFrame(master=fondo, corner_radius=15)
        frame_registro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        frame_registro.configure(width=500, height=500)

        label_log = ck.CTkLabel(master=frame_registro, text="Registrarse", font=ck.CTkFont(size=30, weight="bold", family="Calibri (body)"))
        label_log.place(x=170, y=30)

        # Crea los campos de entrada de datos para el registro
        self.nombre_entry = ck.CTkEntry(frame_registro, placeholder_text='Nombre (*)', width=220, height=40, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.nombre_entry.place(x=90, y=80)

        self.apellido_entry = ck.CTkEntry(frame_registro, placeholder_text='Apellido (*)', width=220, height=40, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.apellido_entry.place(x=90, y=130)

        self.rut_entry = ck.CTkEntry(frame_registro, placeholder_text='RUT (con puntos y guión)', width=220, height=40, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.rut_entry.place(x=90, y=180)

        self.correo_entry = ck.CTkEntry(frame_registro, placeholder_text='Correo electrónico (*)', width=220, height=40, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.correo_entry.place(x=90, y=230)

        self.celular_entry = ck.CTkEntry(frame_registro, placeholder_text='N° de Celular (*)', textvariable=self.celular, width=220, height=40, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.celular_entry.place(x=90, y=280)

        self.contraseña_entry = ck.CTkEntry(frame_registro, placeholder_text='Contraseña', width=220, height=40, show="*",font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.contraseña_entry.place(x=90, y=330)

        self.contraseña_entry_confirmar = ck.CTkEntry(frame_registro, placeholder_text='Confirmar Contraseña', width=220, height=40, show="*", font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.contraseña_entry_confirmar.place(x=90, y=380)
        self.contraseña_entry_confirmar.bind("<Return>", self.registrar)

        # Este es un checkbox para mostrar la contraseña que estamos ingresando
        self.mostrarContraseña_Registro = tk.BooleanVar()
        mostrar_contraseña_checkbox = ck.CTkCheckBox(frame_registro, text="Mostrar contraseña", variable=self.mostrarContraseña_Registro, command=self.mostrarContraseñaRegistro, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        mostrar_contraseña_checkbox.place(x=320, y=388)

        self.registro_photo = ck.CTkImage(Image.open("img\\registro.png"), size=(30,30))

        # Botón para registrarse
        button_registrar = ck.CTkButton(frame_registro, width=200, text="Registrarse", command=self.registrar, image=self.registro_photo, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        button_registrar.place(x=100, y=430)

        self.volver_button = ck.CTkButton(master = frame_registro, command=self.volverLogin, text="Volver", font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.volver_button.place(x=338, y=460)

# Método para validar el correo electrónico
    def validarCorreo(self, correo):
        patron = r'^[\w\.-]+@\w+\.\w+$'

        if re.match(patron, correo):
            return True
        else:
            return False

# Método para validar el RUT ingresado
    def validarRut(self, rut):
        rut = rut.replace(".", "").replace("-", "")  # Remover puntos y guiones
        rut = rut.replace("k", "0")  # Reemplazar "k" por "0"
        rutSinDv = rut[:-1]  # Obtener el rut sin dígito verificador
        dv = rut[-1]  # Obtener el dígito verificador

        # Calcular el dígito verificador
        suma = 0
        multiplo = 2
        for i in reversed(rutSinDv):
            suma += int(i) * multiplo
            multiplo += 1
            if multiplo > 7:
                multiplo = 2

        resto = suma % 11
        dvEsperado = str(11 - resto) if resto > 1 else "0"

        return dv == dvEsperado
        
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
        celular = self.celular_entry.get()
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

        if self.bd.registro(nombre, apellido, correo, contraseña, rut, celular):
            self.withdraw()  # Oculta la ventana de registro
        self.parent.deiconify()  # Muestra la ventana de login
        self.destroy()

    def volverLogin(self):
        self.destroy()
        self.parent.deiconify()

# Ventana recuperar contraseña
class VentanaRecuperarContraseña(ck.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.bd = BD()
        self.iconbitmap('img\\libros.ico')
        self.title("Biblioteca Virtual")
        self.geometry("600x700")
        self.resizable(0, 0)

        # Variables para obtener los datos de los entry´s
        self.celular_bibliotecario = ck.StringVar(value="+56 9")
        self.codigo_ingresado = ck.StringVar()

        # Crear imagen de fondo como PhotoImage
        imagen_fondo = ImageTk.PhotoImage(Image.open("img\\pattern.png"))

        # Crear etiqueta para la imagen de fondo
        fondo = ck.CTkLabel(master=self, image=imagen_fondo, text="")
        fondo.pack()

        self.frame_recuperar_contraseña = ck.CTkFrame(master=fondo, corner_radius=15)
        self.frame_recuperar_contraseña.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.frame_recuperar_contraseña.configure(width=320, height=520)

        self.numero_celular_label = ck.CTkLabel(master=self.frame_recuperar_contraseña, text="Ingrese su numero de celular: ", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.numero_celular_label.place(x=25, y=0)

        self.numero_celular_entry = ck.CTkEntry(master=self.frame_recuperar_contraseña, textvariable=self.celular_bibliotecario, width=250, height=30, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.numero_celular_entry.place(x=35, y=40)

        self.button_celular = ck.CTkButton(master = self.frame_recuperar_contraseña, command=self.enviar_codigo_celular, text="Enviar código", font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.button_celular.place(x=90, y=80)

        self.codigo_celular_label = ck.CTkLabel(master=self.frame_recuperar_contraseña, text="Ingrese el código recibido: ", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.codigo_celular_label.place(x=40, y=120)

        self.codigo_celular_entry = ck.CTkEntry(master=self.frame_recuperar_contraseña, placeholder_text='Ingrese el código aquí ', textvariable=self.codigo_ingresado, width=250, height=30, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.codigo_celular_entry.place(x=35, y=160)

        self.codigo_celular_button = ck.CTkButton(master = self.frame_recuperar_contraseña, command=self.verificar_codigo_ingresado, text="Verificar codigo", font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.codigo_celular_button.place(x=90, y=200)

        self.volver_button = ck.CTkButton(master = self.frame_recuperar_contraseña, command=self.volverLogin, text="Volver", font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.volver_button.place(x=170, y=480)

    # Método para generar un código único de 7 dígitos
    def generar_codigo_unico(self):
        codigo = random.randint(1000000, 9999999)  # Generar un código de 7 dígitos
        return str(codigo)
    
    # Método para enviar el código SMS
    def enviar_codigo_celular(self):
        celular = self.celular_bibliotecario.get()# Número de celular de destino
        if celular == "":
            messagebox.showerror("Recuperación de Contraseña", "Debe ingresar un numero de celular.")
            return
        codigo = self.generar_codigo_unico() # Generar el código único
        mensaje = f"Su código de recuperación de contraseña es: {codigo}"

        # Configurar las credenciales de Twilio
        account_sid = 'ACc5fcca03bf8e78a8d943d1e71c0099ed'
        auth_token = '8e549a03d607cdd90de517a898026b20'
        client = Client(account_sid, auth_token)

        try:
            # Enviar el mensaje de texto
            message = client.messages.create(
                body=mensaje,
                from_='+14178554277',
                to=celular
            )

            # Almacenar el código enviado por Twilio en una variable de instancia
            self.codigo_enviado_por_twilio = codigo

            messagebox.showinfo("Recuperación de Contraseña", "Mensaje enviado correctamente.")
            return codigo
        except Exception as e:
            messagebox.showerror("Recuperación de Contraseña", f"Error al enviar el mensaje: {str(e)}")
            return None
        
    # Método para verificar el codigo ingresado por el bibliotecario
    def verificar_codigo_ingresado(self):
        codigo_enviado = self.codigo_enviado_por_twilio
        codigo_ingresado = self.codigo_ingresado.get()
        if codigo_ingresado == codigo_enviado:
            messagebox.showinfo("Recuperación de Contraseña", "Los códigos coinciden")
            self.mostrar_actualizar_contraseña()
        else:
            messagebox.showerror("Recuperación de Contraseña", "Los códigos no coinciden")
    
    def mostrar_actualizar_contraseña(self):
        self.contraseña_label = ck.CTkLabel(master=self.frame_recuperar_contraseña, text="Ingrese su nueva contraseña: ", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.contraseña_label.place(x=25, y=240)

        self.contraseña_entry = ck.CTkEntry(master=self.frame_recuperar_contraseña, width=250, height=30, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.contraseña_entry.place(x=35, y=280)

        self.confirmar_contraseña_label = ck.CTkLabel(master=self.frame_recuperar_contraseña, text="Confirme su contraseña: ", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.confirmar_contraseña_label.place(x=40, y=320)

        self.contraseña_entry_confirmar = ck.CTkEntry(master=self.frame_recuperar_contraseña, width=250, height=30, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.contraseña_entry_confirmar.place(x=35, y=360)

        # Este es un checkbox para mostrar la contraseña que estamos ingresando
        self.mostrarContraseña_Registro = tk.BooleanVar()
        self.mostrar_contraseña_checkbox = ck.CTkCheckBox(master=self.frame_recuperar_contraseña, text="Mostrar contraseña", variable=self.mostrarContraseña_Registro, command=self.mostrarContraseñaRegistro, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.mostrar_contraseña_checkbox.place(x=75, y=400)

        self.actualizar_contraseña_button = ck.CTkButton(master = self.frame_recuperar_contraseña, command=self.actualizar_contraseña, text="Actualizar contraseña", font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.actualizar_contraseña_button.place(x=75, y=440)
        
    def actualizar_contraseña(self):
        celular = self.numero_celular_entry.get()
        contraseña = self.contraseña_entry.get()
        confirmar_contraseña = self.contraseña_entry_confirmar.get()
        if contraseña != confirmar_contraseña:
            messagebox.showerror("Recuperación de contraseña", "Las contraseñas no coinciden.")
        if self.bd.actualizarContraseñaBibliotecario(str(celular), contraseña):
            self.withdraw()  # Oculta la ventana de registro 
        self.parent.deiconify()  # Muestra la ventana de login
        self.destroy()

    def volverLogin(self):
        self.destroy()
        self.parent.deiconify()

    # Método para mostrar la contraseña al presionar el Checkbox
    def mostrarContraseñaRegistro(self):
        # Cambia la visibilidad de la contraseña basado en el estado del checkbox
        if self.mostrarContraseña_Registro.get():
            self.contraseña_entry.configure(show="")
            self.contraseña_entry_confirmar.configure(show="")
        else:
            self.contraseña_entry.configure(show="*")
            self.contraseña_entry_confirmar.configure(show="*")

# Ventana Login
class Frame(ck.CTkFrame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.bd = BD()
        self.bd.conectar()

        self.correo_actual = None

        # Crear imagen de fondo como PhotoImage
        imagen_fondo = ImageTk.PhotoImage(Image.open("img\\pattern.png"))

        # Crear etiqueta para la imagen de fondo
        fondo = ck.CTkLabel(master=self.root, image=imagen_fondo)
        fondo.pack()

        frame=ck.CTkFrame(master=fondo, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_log = ck.CTkLabel(master=frame, text="Iniciar Sesión", font=ck.CTkFont(size=30, weight="bold", family="Calibri (body)"))
        label_log.place(x=60, y=40)

        self.correo = ck.CTkEntry(master=frame, placeholder_text='Correo electrónico', width=220, height=40, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.correo.place(x=50, y=80)

        self.contraseña = tk.StringVar()
        self.contraseña_entry = ck.CTkEntry(master=frame, placeholder_text='Contraseña', width=220, height=40, show="*", font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.contraseña_entry.place(x=50, y=130)
        self.contraseña_entry.bind("<Return>", self.login)

        # Checkbox para mostrar/ocultar la contraseña
        self.mostrar_contraseña = tk.BooleanVar()
        self.checkbox_mostrar_contraseña = ck.CTkCheckBox(master=frame, text="Mostrar contraseña", variable=self.mostrar_contraseña, command=self.mostrarContraseña, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"))
        self.checkbox_mostrar_contraseña.place(x=30, y=180)

        iniciar_sesion_photo = ck.CTkImage(Image.open("img\\iniciar_sesion.png"), size=(25, 25))
        self.button_login = ck.CTkButton(master=frame, text="Iniciar sesión", command=self.login, image=iniciar_sesion_photo, font=ck.CTkFont(size=18, weight="bold", family="Calibri (body)"))
        self.button_login.place(x=80, y=220)

        registrarse_photo = ck.CTkImage(Image.open("img\\registrarse.png"), size=(25, 25))
        self.button_registrar = ck.CTkButton(master=frame, text="Registrarse", command=self.abrir_ventana_registro, image=registrarse_photo, font=ck.CTkFont(size=18, weight="bold", family="Calibri (body)"))
        self.button_registrar.place(x=86, y=270)

        self.button_olvido_contraseña = ck.CTkButton(master=frame, text="¿Olvidó su contraseña?", font=ck.CTkFont(size=18, weight="bold", family="Calibri (body)"), command=self.abrir_ventana_recuperar_contraseña)
        self.button_olvido_contraseña.place(x=48, y=320)

    def login(self, event=None):
        correo = self.correo.get()
        contraseña = self.contraseña_entry.get()

        if not correo:
            messagebox.showerror("Error de inicio de sesión", "Debe ingresar un correo.")
            return

        # Verifica si el correo existe en la base de datos
        if self.bd.login(correo, contraseña):
            self.root.withdraw()
            ventana_principal = VentanaPrincipal(self.root, correo)
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

    def abrir_ventana_recuperar_contraseña(self):
        self.root.withdraw()
        ventana_recuperar_contraseña = VentanaRecuperarContraseña(self.root)
        self.root.wait_window(ventana_recuperar_contraseña)

    def limparCampos(self):
        self.correo.delete(0, 'end')
        self.contraseña_entry.delete(0, 'end')
        
# Ventana principal de la aplicación
class VentanaPrincipal(ck.CTkToplevel):
    def __init__(self, parent, correo_actual = None):
        super().__init__(parent)
        self.parent = parent
        self.bd = BD() # Guardar el objeto de la clase BD
        self.correo_actual = correo_actual
        self.iconbitmap('img\\libros.ico')
        self.title("Biblioteca Virtual")
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

        # Variables de texto para el Frame Registrar Usuario
        self.nombre_usuario = ck.StringVar()
        self.apellido_ususario = ck.StringVar()
        self.direccion_usuario = ck.StringVar()
        self.celular_usuario = ck.StringVar()
        self.correo_usuario = ck.StringVar()
        
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
        self.registrar_usuario_image = ck.CTkImage(Image.open("img\\registrar_usuario.png"), size=(450, 120))
        self.realizar_prestamo_icono = ck.CTkImage(Image.open("img\\realizar_prestamo_icono.png"), size=(26, 26))
        self.libros_prestamo_icono = ck.CTkImage(Image.open("img\\libros_prestamo.png"), size=(26, 26))
        self.renovar_libro_icono = ck.CTkImage(Image.open("img\\renovar_libro.png"), size=(26, 26))
        self.catalogo_libro_icono = ck.CTkImage(Image.open("img\\catalogo_libros.png"), size=(26, 26))
        self.renovar_libro_image_titulo = ck.CTkImage(Image.open("img\\renovar_libro_titulo.png"), size=(450, 120))

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
                                        hover_color=("gray70", "gray30"), image=self.catalogo_libro_icono, anchor="w",
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
                                           hover_color=("gray70", "gray30"), image=self.realizar_prestamo_icono, anchor="w",
                                           command=self.realizarPrestamo_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.realizar_prestamo_button.grid(row=5, column=0, sticky="ew")

        # Botón de Frame Libros en Préstamo
        self.frame_libros_en_prestamo_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10,
                                           text="Libros en Préstamo", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), image=self.libros_prestamo_icono, anchor="w",
                                           command=self.frame_libros_en_prestamo_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.frame_libros_en_prestamo_button.grid(row=6, column=0, sticky="ew")
        
        # Botón de Frame Registrar Usuario
        self.frame_registrar_usuario_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10,
                                           text="Registrar Usuario", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), image=self.add_user_image, anchor="w",
                                           command=self.frame_registrar_usuario_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.frame_registrar_usuario_button.grid(row=7, column=0, sticky="ew")

        # Botón de Frame Renovar Libro
        self.frame_renovar_libro_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10,
                                           text="Renovar Libro", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), image=self.renovar_libro_icono, anchor="w",
                                           command=self.frame_renovar_libro_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.frame_renovar_libro_button.grid(row=8, column=0, sticky="ew")

        # Menu de opciones para cambiar de apariencia la app
        self.menu_apariencia = ck.CTkOptionMenu(self.frameNavegacion, font=ck.CTkFont(size=15, weight="bold", family="Calibri (body)"), values=["Dark", "Light"], command=self.evento_cambiar_apariencia)
        self.menu_apariencia.grid(row=9, column=0, padx=20, pady=20, sticky="s")

        # Botón para cerrar sesion
        self.button_cerrarSesion = ck.CTkButton(self.frameNavegacion, font=ck.CTkFont(size=18, weight="bold", family="Calibri (body)"), text="Cerrar sesión", image=self.cerrar_sesion_imagen, command=self.cerrar_sesion)
        self.button_cerrarSesion.grid(row=10, column=0, padx=20, pady=20, sticky="s")

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

        libros = self.bd.obtenerLibrosCatalogo() # Obtener los libros desde la base de datos

        for i, libro in enumerate(libros):
            nombre = libro[0]
            apellido = libro[1]
            nacionalidad = libro[2]
            titulo = libro[3]
            imagen_bytes = libro[4]
            isbn = libro[5]

            if imagen_bytes is not None:
                imagen_flip = self.crear_imagen_flip(imagen_bytes, titulo, f"ISBN: {isbn}\nAutor: {nombre} {apellido}\nNacionalidad: {nacionalidad}")
                imagen_flip.grid(row=i // 4, column=i % 4, padx=10, pady=10)

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

        self.isbn_libro_entry = ck.CTkEntry(self.frame_realizar_prestamo, textvariable=self.isbn, width=140, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.isbn_libro_entry.grid(row=11, column=1, padx=5)

        self.fecha_inicio_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Fecha Inicio de Préstamo: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.fecha_inicio_label.grid(row=12, column=0, pady=5)
        
        self.fecha_inicio = DateEntry(self.frame_realizar_prestamo, width=11,
                          date_pattern='yyyy/mm/dd', font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"),
                          highlightbackground="deep sky blue", highlightthickness=1, corner_radius=10)
        self.fecha_inicio.grid(row=12, column=1, pady=5)

        self.fecha_devolucion_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Fecha Devolución de Préstamo: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.fecha_devolucion_label.grid(row=13, column=0, pady=5)

        self.fecha_devolucion = DateEntry(self.frame_realizar_prestamo, width=11,
                          date_pattern='yyyy/mm/dd', font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"),
                          highlightbackground="deep sky blue", highlightthickness=1, corner_radius=10)
        self.fecha_devolucion.grid(row=13, column=1, pady=5)

        self.tipo_usuario_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Tipo de Usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.tipo_usuario_label.grid(row=14, column=0, pady=5)

        self.tipo_usuario_entry = ck.CTkEntry(self.frame_realizar_prestamo, textvariable=self.tipo_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.tipo_usuario_entry.grid(row=14, column=1, padx=5)

        # Botón que realizara el prestamo
        self.completar_prestamo_button = ck.CTkButton(self.frame_realizar_prestamo, command=self.realizarPrestamo, text="REALIZAR PRÉSTAMO", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.completar_prestamo_button.place(x=280, y=400)

        # Botón para borrar el contenido de todos los campos
        self.borrar_campos_prestamo = ck.CTkButton(self.frame_realizar_prestamo, text="BORRAR TODO", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"), command=self.limpiarCamposPrestamo)
        self.borrar_campos_prestamo.place(x=65, y=400)

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

        # FRAME REGISTRAR USUARIO
        self.frame_registrar_usuario = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_registrar_usuario.grid(row=0, column=0, sticky="nsew")

        self.registrar_usuario_image_label = ck.CTkLabel(self.frame_registrar_usuario, text="", image=self.registrar_usuario_image)
        self.registrar_usuario_image_label.grid(row=0, columnspan=2, padx=20)

        self.nombre_usuario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese el nombre del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.nombre_usuario_label.grid(row=10, column=0, pady=5, padx=5)

        self.nombre_usuario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.nombre_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.nombre_usuario_entry.grid(row=10, column=1, pady=10, padx=5)

        self.apellido_ususario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese el apellido del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.apellido_ususario_label.grid(row=11, column=0, pady=5, padx=5)

        self.apellido_ususario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.apellido_ususario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.apellido_ususario_entry.grid(row=11, column=1, pady=10, padx=5)

        self.direccion_usuario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese la dirección del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.direccion_usuario_label.grid(row=12, column=0, pady=5, padx=5)

        self.direccion_usuario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.direccion_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.direccion_usuario_entry.grid(row=12, column=1, pady=10, padx=5)

        self.rut_usuario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese el RUT del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.rut_usuario_label.grid(row=13, column=0, pady=5, padx=5)

        self.rut_usuario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.rut_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.rut_usuario_entry.grid(row=13, column=1, pady=10, padx=5)

        self.celular_usuario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese el celular del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.celular_usuario_label.grid(row=14, column=0, pady=5, padx=5)

        self.celular_usuario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.celular_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.celular_usuario_entry.grid(row=14, column=1, pady=10, padx=5)

        self.correo_usuario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese el correo electrónico del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.correo_usuario_label.grid(row=15, column=0, pady=5, padx=5)

        self.correo_usuario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.correo_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.correo_usuario_entry.grid(row=15, column=1, pady=10, padx=5)

        self.tipo_usuario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese el tipo de usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.tipo_usuario_label.grid(row=16, column=0, pady=5, padx=5)

        self.tipo_usuario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.tipo_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.tipo_usuario_entry.grid(row=16, column=1, pady=10, padx=5)

        self.registrar_usuario_button = ck.CTkButton(self.frame_registrar_usuario, text="REGISTRAR USUARIO", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"), command=self.registrarUsuario)
        self.registrar_usuario_button.place(x=288, y=480)

        # FRAME RENOVAR LIBRO
        self.frame_renovar_libro = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_renovar_libro.grid(row=0, column=0, sticky="nsew")

        self.renovar_libro_image = ck.CTkLabel(self.frame_renovar_libro, text="", image=self.renovar_libro_image_titulo)
        self.renovar_libro_image.grid(row=0, columnspan=3, padx=20)

        self.rut_usuario_label = ck.CTkLabel(self.frame_renovar_libro, text="Ingrese el rut del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.rut_usuario_label.grid(row=3, column=0, pady=5, padx=5)

        self.rut_usuario_entry = ck.CTkEntry(self.frame_renovar_libro, textvariable=self.rut_usuario, width=200, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.rut_usuario_entry.grid(row=3, column=1, pady=5, padx=5)

        self.isbn_label = ck.CTkLabel(self.frame_renovar_libro, text="Ingrese el ISBN del libro: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.isbn_label.grid(row=4, column=0, pady=5, padx=5)

        self.isbn_entry = ck.CTkEntry(self.frame_renovar_libro, textvariable=self.isbn, width=200, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.isbn_entry.grid(row=4, column=1, pady=5, padx=5)

        self.buscar_usuario = ck.CTkButton(self.frame_renovar_libro, text="BUSCAR USUARIO", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"), command=self.obtenerFechaDevolucion)
        self.buscar_usuario.grid(row=4, column=2, pady=5, padx=5)

        self.fecha_devolucion_label = ck.CTkLabel(self.frame_renovar_libro, text="Fecha Devolución de Préstamo: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"))
        self.fecha_devolucion_label.grid(row=7, column=0, pady=5, padx=5)

        self.fecha_devolucion = DateEntry(self.frame_renovar_libro, width=16,
                          date_pattern='yyyy/mm/dd', font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"),
                          highlightbackground="deep sky blue", highlightthickness=1, corner_radius=10)
        self.fecha_devolucion.grid(row=7, column=1, pady=5, padx=5)

        self.sumar_dias = ck.CTkButton(self.frame_renovar_libro, text="SUMAR DÍAS", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"), command=self.sumarDiasRenovacion)
        self.sumar_dias.grid(row=7, column=2, pady=5, padx=5)

        self.renovar_libro_button = ck.CTkButton(self.frame_renovar_libro, text="RENOVAR LIBRO", font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"), command=self.renovarLibro)
        self.renovar_libro_button.place(x=330, y=260)

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
        self.frame_registrar_usuario.configure(fg_color=("gray75", "gray25") if name == "registrar_usuario" else "transparent")
        self.frame_renovar_libro.configure(fg_color=("gray75", "gray25") if name == "renovar_libro" else "transparent")

        # Mostrar frame seleccionado
        if name == "home":
            self.inicio_frame.grid(row=0, column=0, sticky="nsew")
            self.catalogo.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_registrar_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
        elif name == "catalogo":
            self.inicio_frame.grid_forget()
            self.catalogo.grid(row=0, column=0, sticky="nsew")
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_registrar_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
        elif name == "stock":
            self.inicio_frame.grid_forget()
            self.stock.grid(row=0, column=0, sticky="nsew")
            self.usuario.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_registrar_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
        elif name == "usuarios":
            self.inicio_frame.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid(row=0, column=0, sticky="nsew")
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_registrar_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
        elif name == "realizar_prestamo":
            self.inicio_frame.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.frame_realizar_prestamo.grid(row=0, column=0, sticky="nsew")
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_registrar_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
        elif name == "libros_prestamo":
            self.inicio_frame.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid(row=0, column=0, sticky="nsew")
            self.frame_registrar_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
        elif name == "registrar_usuario":
            self.inicio_frame.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_registrar_usuario.grid(row=0, column=0, sticky="nsew")
            self.frame_renovar_libro.grid_forget()
        elif name == "renovar_libro":
            self.inicio_frame.grid_forget()
            self.stock.grid_forget()
            self.usuario.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_registrar_usuario.grid_forget()
            self.frame_renovar_libro.grid(row=0, column=0, sticky="nsew")

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

    def frame_registrar_usuario_button_evento(self):
        self.seleccion_frame_nombre("registrar_usuario")

    def frame_renovar_libro_button_evento(self):
        self.seleccion_frame_nombre("renovar_libro")

    # Método para cambiar la apariencia de la app
    def evento_cambiar_apariencia(self, new_appearance_mode):
        ck.set_appearance_mode(new_appearance_mode)

    # METODOS PARA EL FRAME STOCK
    # Método para buscar un libro
    def buscarLibroStock(self, event = None):
        isbn = self.buscar_actualiza.get()  # Obtener el ISBN ingresado
        if isbn == "":
            messagebox.showerror("Stock", "Debe de ingresar un ISBN para realizar la busqueda.")
            self.limpiarCamposStock()
        libros = self.bd.buscarLibro(isbn)  # Buscar el libro en la base de datos
        if libros:
            isbn, titulo, num_paginas, stock = libros[0][1:5]  # Tomar los elementos del índice 1 al 4
            self.isbn.set(str(isbn))  # Actualizar el valor del campo ISBN
            self.titulo.set(str(titulo))  # Actualizar el valor del campo Título
            self.numero_paginas.set(int(num_paginas))  # Actualizar el valor del campo Número de Páginas
            self.stockLibro.set(int(stock))  # Actualizar el valor del campo Stock
        else:
            messagebox.showerror("Stock", f"El libro con el ISBN {isbn} no existe.")
            self.limpiarCamposStock()

    # Método para actualizar el stock de un libro
    def actualizarStock(self, event = None):
        isbn = self.isbn.get()
        stock = self.stockLibro.get()
        titulo = self.titulo.get()

        if not isbn:
            messagebox.showerror("Modificar Stock", "El campo ISBN no puede estar vació")
            return

        # Crear instancia de BarraProgreso
        total_elementos = 100
        barra = BarraProgreso(total_elementos)

        # Nostrar barra de progreso en el Frame
        self.barra_progreso_label = ck.CTkLabel(self.stock, text="",
                                                font=ck.CTkFont(size=14, weight="bold", family="Calibri (body)"))
        self.barra_progreso_label.place(x=65, y=450)

        # Realizar el préstamo
        for i in range(total_elementos):
            mensaje_progreso = barra.actualizar()
            self.barra_progreso_label.configure(text=mensaje_progreso)
            self.frame_realizar_prestamo.update() # Actualizar la ventana
            time.sleep(0.1)

        self.bd.actualizarStock(stock, isbn)
        self.limpiarCamposStock()

        # Restablecer el estado de la barra de progreso
        self.barra_progreso_label.configure(text="")
        self.frame_realizar_prestamo.update() # Actualizar la ventana

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
        isbn = self.isbn.get()
        tipo_usuario = self.bd.obtenerTipoUsuario(rut)
        if self.validarRut(rut):
            if tipo_usuario:
                self.tipo_usuario.set(tipo_usuario)
                if tipo_usuario == "Alumno":
                    fecha_devolucion = self.calcularFechaDevolucion(7)
                    messagebox.showinfo("Realizar Préstamo", f"Se han sumado 7 días por ser {tipo_usuario}")
                    if fecha_devolucion:
                        self.fecha_devolucion.set_date(fecha_devolucion)
                elif tipo_usuario == "Docente":
                    fecha_devolucion = self.calcularFechaDevolucion(20)
                    messagebox.showinfo("Realizar Préstamo", f"Se han sumado 20 días por ser {tipo_usuario}")
                    if fecha_devolucion:
                        self.fecha_devolucion.set_date(fecha_devolucion)
                else:
                    self.fecha_devolucion.configure(state="disabled")
        else:
            messagebox.showerror("Realizar Prestamo", f"El RUT {rut} no es valido.")

    def realizarPrestamo(self):
        rut = self.rut_usuario.get()
        isbn = self.isbn_libro_entry.get()
        f_prestamo = self.fecha_inicio.get_date()
        f_devolucion = self.fecha_devolucion.get_date()
        tipo_usuario = self.bd.obtenerTipoUsuario(rut)
        id_bibliotecario = self.bd.obtenerUsuarioLog(self.correo_actual)

        if not rut:
            return
        
        # Verificar la cantidad de libros en préstamo del usuario
        cantidad_prestamos = self.bd.obtenerCantidadLibrosPrestamo(rut)

        if tipo_usuario == "Alumno" and cantidad_prestamos >= 4:
            messagebox.showwarning("Límite de préstamos alcanzado", "El alumno ha alcanzado el límite máximo de préstamos (4 libros).")
            return
        
        # Crear instancia de BarraProgreso
        total_elementos = 100
        barra = BarraProgreso(total_elementos)

        # Nostrar barra de progreso en el Frame
        self.barra_progreso_label = ck.CTkLabel(self.frame_realizar_prestamo, text="",
                                                font=ck.CTkFont(size=14, weight="bold", family="Calibri (body)"))
        self.barra_progreso_label.place(x=65, y=450)

        # Realizar el préstamo
        for i in range(total_elementos):
            mensaje_progreso = barra.actualizar()
            self.barra_progreso_label.configure(text=mensaje_progreso)
            self.frame_realizar_prestamo.update() # Actualizar la ventana
            time.sleep(0.1)

        # Registrar el prestamo en la base de datos
        self.bd.registrarPrestamo(self.correo_actual, rut, isbn, f_prestamo, f_devolucion, tipo_usuario)

        # Restablecer el estado de la barra de progreso
        self.barra_progreso_label.configure(text="")
        self.frame_realizar_prestamo.update() # Actualizar la ventana
             
    def calcularFechaDevolucion(self, dias):
        fecha_actual = datetime.now().date()
        fecha_devolucion = fecha_actual + timedelta(days=dias)
        return fecha_devolucion
    
    # MÉTODOS PARA EL FRAME REGISTRAR USUARIO
    # Método para registrar usuario
    def registrarUsuario(self):
        nombre = self.nombre_usuario.get()
        apellido = self.apellido_ususario.get()
        direccion = self.direccion_usuario.get()
        rut = self.rut_usuario.get()
        celular = self.celular_usuario.get()
        correo = self.correo_usuario.get()
        tipo = self.tipo_usuario.get()

        if rut == "":
            messagebox.showerror("Registrar Usuario", "Debe de ingresar un rut.")

        if self.validarRut(rut):
            if self.validarCorreo(correo):
                # Crear instancia de BarraProgreso
                total_elementos = 100
                barra = BarraProgreso(total_elementos)

                # Nostrar barra de progreso en el Frame
                self.barra_progreso_label = ck.CTkLabel(self.frame_registrar_usuario, text="",
                                                        font=ck.CTkFont(size=14, weight="bold", family="Calibri (body)"))
                self.barra_progreso_label.place(x=80, y=520)

                # Realizar el préstamo
                for i in range(total_elementos):
                    mensaje_progreso = barra.actualizar()
                    self.barra_progreso_label.configure(text=mensaje_progreso)
                    self.frame_registrar_usuario.update() # Actualizar la ventana
                    time.sleep(0.1)

                self.bd.registrarUsuario(nombre, apellido, direccion, rut, celular, correo, tipo)
                self.limpiarCamposUsuario()
                # Restablecer el estado de la barra de progreso
                self.barra_progreso_label.configure(text="")
                self.frame_registrar_usuario.update() # Actualizar la ventana
            else:
                messagebox.showerror("Registrar Usuario", f"El correo {correo} no es valido.")
        else:
            messagebox.showerror("Registrar Usuario", f"El RUT {rut} ingresado no es valido.")

    # METODO PARA EL FRAME RENOVAR PRÉSTAMO
    def renovarLibro(self):
        # Obtener los datos necesarios
        rut = self.rut_usuario.get()
        isbn = self.isbn_entry.get()
        id_bibliotecario = self.bd.obtenerUsuarioLog(self.correo_actual)
        nueva_fecha_devolucion = self.fecha_devolucion.get_date()

        if not rut:
            messagebox.showerror("Renovación de libro", "El campo RUT no debe estar vacío")
            return

        if not isbn:
            messagebox.showerror("Renovación de libro", "El campo ISBN no debe estar vacío")
            return

        # Crear instancia de BarraProgreso
        total_elementos = 100
        barra = BarraProgreso(total_elementos)

        # Mostrar barra de progreso en el Frame
        self.barra_progreso_label = ck.CTkLabel(self.frame_renovar_libro, text="",
                                                font=ck.CTkFont(size=14, weight="bold", family="Calibri (body)"))
        self.barra_progreso_label.grid(row=4, column=0, padx=10, pady=10)

        # Realizar la renovación del libro
        for i in range(total_elementos):
            mensaje_progreso = barra.actualizar()
            self.barra_progreso_label.configure(text=mensaje_progreso)
            self.frame_renovar_libro.update()  # Actualizar la ventana
            time.sleep(0.1)

        # Registrar la renovación del libro
        if self.bd.registrarRenovacion(rut, isbn):
            # Actualizar la fecha de devolución en la base de datos
            if self.bd.actualizarPrestamo(rut, isbn, nueva_fecha_devolucion, id_bibliotecario):
                messagebox.showinfo("Renovación de libro", "El libro ha sido renovado exitosamente.")
                self.limpiarCamposRenovacion()
            else:
                messagebox.showerror("Renovación de libro", "Error al actualizar la fecha de devolución del préstamo.")
        else:
            messagebox.showerror("Renovación de libro", "Error al registrar la renovación del libro.")

        # Restablecer el estado de la barra de progreso
        self.barra_progreso_label.configure(text="")
        self.frame_renovar_libro.update()  # Actualizar la ventana

    def obtenerFechaDevolucion(self):
        rut = self.rut_usuario.get()
        isbn = self.isbn_entry.get()
        tipo_usuario = self.bd.obtenerTipoUsuario(rut)

        if rut == "" and isbn == "":
            messagebox.showerror("Renovación de libro", "Debe de ingresar un RUT.")

        # Verificar si el usuario es "Alumno"
        if tipo_usuario == "Alumno":
            # Verificar si el alumno ya ha realizado una renovación
            if self.bd.haRealizadoRenovacion(rut):
                messagebox.showinfo("Renovación de libro", "El alumno ya ha realizado una renovación y no puede renovar más libros.")
                return

        # Obtener la fecha de devolución actual del préstamo
        fecha_devolucion_actual = self.bd.obtenerFechaDevolucionPrestamo(rut, isbn)
        if fecha_devolucion_actual is None:
            messagebox.showerror("Renovación de libro", "No se encontró un préstamo vigente para el usuario y el libro especificados.")
            return
        
        # Establecer la fecha de devolución actual en el DateEntry
        self.fecha_devolucion.set_date(datetime.strptime(fecha_devolucion_actual, "%Y-%m-%d"))
        messagebox.showinfo("Renovación de libro", f"La fecha de devolución establecida para el alumno por este libro es: {self.fecha_devolucion.get_date()}")

    def sumarDiasRenovacion(self):
        rut = self.rut_usuario.get()
        isbn = self.isbn_entry.get()
        # Obtener la fecha de devolución actual del préstamo
        fecha_devolucion_actual = self.bd.obtenerFechaDevolucionPrestamo(rut, isbn)
        if fecha_devolucion_actual is None:
            messagebox.showerror("Renovación de libro", "No se encontró un préstamo vigente para el usuario y el libro especificados.")
            return
        # Calcular la nueva fecha de devolución sumando 3 días a la fecha actual
        nueva_fecha_devolucion = datetime.strptime(fecha_devolucion_actual, "%Y-%m-%d").date() + timedelta(days=3)
        self.fecha_devolucion.set_date(nueva_fecha_devolucion)
        messagebox.showinfo("Renovación de libro", f"Se han sumado 3 dias a la fecha de devolución, ahora la nueva fecha es: {nueva_fecha_devolucion}") 

    # MÉTODOS PARA FRAME CATALOGO
    def crear_imagen_flip(self, imagen_bytes, titulo, detalle):
        imagen_np = np.frombuffer(imagen_bytes, np.uint8)
        imagen_cv2 = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)

        if imagen_cv2.shape[2] == 3:
            imagen_cv2_rgb = cv2.cvtColor(imagen_cv2, cv2.COLOR_BGR2RGB)
        else:
            imagen_cv2_rgb = cv2.cvtColor(imagen_cv2, cv2.COLOR_GRAY2RGB)

        imagen_pil = Image.fromarray(imagen_cv2_rgb)

        imagen = ck.CTkImage(imagen_pil, size=(150, 200))
        imagen_label = ck.CTkLabel(self.catalogo, text="", image=imagen, font=ck.CTkFont(size=20, weight="bold", family="Calibri (body)"), text_color="blue")
        imagen_label.image = imagen
        imagen_label.bind("<Button-1>", lambda event: self.mostrar_detalle(imagen_label, titulo, detalle))

        return imagen_label

    def mostrar_detalle(self, imagen_label, titulo, detalle):
        imagen_label.configure(text=f"{titulo}\n {detalle}")
        imagen_label.after(2000, lambda: self.ocultar_detalle(imagen_label))

    def ocultar_detalle(self, imagen_label):
        imagen_label.configure(text="")

    # Método para validar el correo electrónico
    def validarCorreo(self, correo):
        patron = r'^[\w\.-]+@\w+\.\w+$'

        if re.match(patron, correo):
            return True
        else:
            return False

    # Método para validar el RUT ingresado
    def validarRut(self, rut):
        rut = rut.replace(".", "").replace("-", "")  # Remover puntos y guiones
        rut = rut.replace("k", "0")  # Reemplazar "k" por "0"
        rutSinDv = rut[:-1]  # Obtener el rut sin dígito verificador
        dv = rut[-1]  # Obtener el dígito verificador

        # Calcular el dígito verificador
        suma = 0
        multiplo = 2
        for i in reversed(rutSinDv):
            suma += int(i) * multiplo
            multiplo += 1
            if multiplo > 7:
                multiplo = 2

        resto = suma % 11
        dvEsperado = str(11 - resto) if resto > 1 else "0"

        return dv == dvEsperado

    def limpiarCamposRenovacion(self):
        self.rut_usuario.set('')
        self.isbn.set('')
        self.fecha_devolucion.set_date(datetime.now().date())
        
    def limpiarCamposUsuario(self):
        self.nombre_usuario.set('')
        self.apellido_ususario.set('')
        self.direccion_usuario.set('')
        self.rut_usuario.set('')
        self.celular_usuario.set('')
        self.correo_usuario.set('')
        self.tipo_usuario.set('')
    
    def limpiarCamposPrestamo(self):
        self.rut_usuario.set('')
        self.isbn.set('')
        self.fecha_inicio.set_date(datetime.now().date())
        self.fecha_devolucion.set_date(datetime.now().date())
        self.tipo_usuario.set('')

    # Método para limpiar los valores en los entry's
    def limpiarCamposStock(self):
        self.buscar_actualiza.set('')
        self.isbn.set('')
        self.titulo.set('')
        self.numero_paginas.set('')
        self.stockLibro.set('')

    # Método para cerrar sesion en la app
    def cerrar_sesion(self):
        self.destroy()
        self.parent.deiconify()