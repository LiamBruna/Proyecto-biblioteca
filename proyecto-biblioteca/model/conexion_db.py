import sqlite3
from sqlite3 import Error
from tkinter import messagebox

class BD:
    def __init__(self):
        self.base_datos = 'database/biblioteca.db'
        self.connect = sqlite3.connect(self.base_datos)
        self.cursor = self.connect.cursor()
        messagebox.showinfo(f"Mensaje", f"Conectado a la base de datos")

    def cerrar(self):
        self.cursor.close()
        self.connect.close()
        messagebox.showinfo(f"Mensaje", f"Conexión cerrada")


#Metodos
    def login(self, correo, contraseña):
        try:
            sql = "SELECT * FROM bibliotecario WHERE CORREO_B = ? AND CONTRASENA = ?"
            self.cursor.execute(sql, (correo, contraseña))
            result = self.cursor.fetchone()

            if result is not None:
                messagebox.showinfo(f"Inicio de sesion exitoso", f"Bienvenido {correo}")
            else:
                messagebox.showerror("Error de inicio de sesión", "Credenciales invalidas")
        except Error as e:
            print("Error al ejecutar: ", e)
        finally:
            self.cursor.close()
            self.connect.close()
            print("Conexion cerrada")