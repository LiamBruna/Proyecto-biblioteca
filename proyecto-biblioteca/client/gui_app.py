import tkinter as tk
import customtkinter as ck
import tkinter.ttk as ttk
from tkinter import messagebox

from model.conexion_db import *

class Frame(tk.Frame):
    def __init__(self, root = None):
        super().__init__(root)
        self.root = root
        self.pack()
        self.config(bg="red") #Color de la ventana
        
        #self.login()
        self.loginWindow()

    #Campos a mostrar en el Frame
    def login(self):
        correo = self.correo.get()
        password = self.contraseña.get()
        bd = BD()
        bd.login(correo, password)

    def loginWindow(self):
        # Correo electrónico
        self.correo = ck.CTkEntry(self, font=('sans rerif', 12), placeholder_text='Correo electrónico', border_color='green', fg_color='black', width=220, height=40)
        self.correo.grid(columnspan=2, row=1, padx=4, pady=4)

        # Contraseña
        self.contraseña = ck.CTkEntry(self, font=('sans rerif', 12), placeholder_text='Contraseña', border_color='green', fg_color='black', width=220, height=40)
        self.contraseña.grid(columnspan=2, row=2, padx=4, pady=4)

        # Botón
        button_login = tk.Button(self, text="Iniciar sesión", command=self.login)
        button_login.grid(columnspan=2, row=3, padx=4, pady=4)

