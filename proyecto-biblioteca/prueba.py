import customtkinter
import os
from PIL import Image


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("image_example.py")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Image Example", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

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
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()



#************************************************************************************************************
#importing required modules
import tkinter
import customtkinter
from PIL import ImageTk,Image

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


app = customtkinter.CTk()  #creating cutstom tkinter window
app.geometry("600x440")
app.title('Login')



def button_function():
    app.destroy()            # destroy current window and creating new one 
    w = customtkinter.CTk()  
    w.geometry("1280x720")
    w.title('Welcome')
    l1=customtkinter.CTkLabel(master=w, text="Home Page",font=('Century Gothic',60))
    l1.place(relx=0.5, rely=0.5,  anchor=tkinter.CENTER)
    w.mainloop()
    


img1=ImageTk.PhotoImage(Image.open("pattern.png"))
l1=customtkinter.CTkLabel(master=app,image=img1)
l1.pack()

#creating custom frame
frame=customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l2=customtkinter.CTkLabel(master=frame, text="Log into your Account",font=('Century Gothic',20))
l2.place(x=50, y=45)

entry1=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
entry1.place(x=50, y=110)

entry2=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
entry2.place(x=50, y=165)

l3=customtkinter.CTkLabel(master=frame, text="Forget password?",font=('Century Gothic',12))
l3.place(x=155,y=195)

#Create custom button
button1 = customtkinter.CTkButton(master=frame, width=220, text="Login", command=button_function, corner_radius=6)
button1.place(x=50, y=240)


img2=customtkinter.CTkImage(Image.open("Google__G__Logo.svg.webp").resize((20,20), Image.ANTIALIAS))
img3=customtkinter.CTkImage(Image.open("124010.png").resize((20,20), Image.ANTIALIAS))
button2= customtkinter.CTkButton(master=frame, image=img2, text="Google", width=100, height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF')
button2.place(x=50, y=290)

button3= customtkinter.CTkButton(master=frame, image=img3, text="Facebook", width=100, height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF')
button3.place(x=170, y=290)




self.destroy()
self.parent.deiconify()

'''self.parent.withdraw()
ventana_login = Frame(self.parent)
self.parent.wait_window(ventana_login)'''




# You can easily integrate authentication system 

app.mainloop()

# FRAME MOSTRAR USUARIOS REGISTRADOS
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


# Método para mostrar los datos en la tabla de usuarios
    def mostrarDatosUsuario(self):
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


# Método para mostrar información personal de los usuarios registrados
    def mostrarUsuarios(self):
        sql = "SELECT * FROM usuario"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            messagebox.showerror("Mostrar usuarios", f"{str(e)}")


        # FRAME LIBROS EN PRÉSTAMO
        self.frame_libros_en_prestamo = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_libros_en_prestamo.grid(row=0, column=0, sticky="nsew")
        self.frame_libros_en_prestamo.grid_columnconfigure(0, weight=1) # Expansión horizontal
        self.frame_libros_en_prestamo.grid_rowconfigure(1, weight=1) # Expansión vertical

        actualizar_librosPrestamo_button = ck.CTkButton(self.frame_libros_en_prestamo, text='ACTUALIZAR TABLA LIBROS EN PRÉSTAMO', font=('Arial', 11, 'bold'), command=self.mostrarDatosLibros) # FALTA EL COMMAND
        actualizar_librosPrestamo_button.grid(columnspan=1, row=2, pady=5)

        # Estilo de la tabla para mostrar los datos
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font=('Helvetica', 10, 'bold'), foreground='black', background='white')
        estilo_tabla.map('Treeview', background=[('selected', 'green')], foreground=[('selected', 'black')])
        estilo_tabla.configure('Heading', background='white', foreground='navy', padding=3, font=('Calibri (body)', 10, 'bold'))
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

        self.tabla_dos.bind("<<TreeviewSelect>>", self.obtener_filaLibros) #AUN NO USARRRRRRR

        # Ajustar expansión del marco principal
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.rut_usuario_entry.bind("<KeyRelease>", self.obtenerTipoUsuario)

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
        self.buscar_libro_isbn_entry.bind("<Return>", self.buscarLibroStock)

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

        
contraseña = self.contraseña_entry.get()
        confirmarContraseña = self.contraseña_entry_confirmar.get()


 # Método para actualizar el stock de un libro
    def actualizarStock(self, event = None):
        isbn = self.isbn.get()
        stock = self.stockLibro.get()
        titulo = self.titulo.get()
        self.bd.actualizarStock(stock, isbn)  
        self.limpiarCamposStock()