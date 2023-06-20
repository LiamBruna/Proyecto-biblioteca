import sqlite3
from sqlite3 import Error
from tkinter import messagebox
import hashlib

class BD:
    def __init__(self):
        self.base_datos = 'proyecto-biblioteca/database/biblioteca.db'
        self.connect = sqlite3.connect(self.base_datos)
        self.cursor = self.connect.cursor()
        self.conexion_establecida = False

    def conectar(self):
        if not self.conexion_establecida:
            self.connect = sqlite3.connect(self.base_datos)
            self.cursor = self.connect.cursor()
            self.conexion_establecida = True

    def cerrar(self):
        self.cursor.close()
        self.connect.close()
        messagebox.showinfo(f"Mensaje", f"Conexión cerrada")


#Metodos
    def login(self, correo, contraseña):
        try:
            sql = "SELECT * FROM bibliotecario WHERE CORREO_B = ?"
            self.cursor.execute(sql, (correo,))
            result = self.cursor.fetchone()

            if result is not None:
                stored_password_hash = result[4]
                entered_password_hash = hashlib.sha256(contraseña.encode()).hexdigest()
                if stored_password_hash == entered_password_hash:
                    messagebox.showinfo("Inicio de sesión exitoso", f"Bienvenido {correo}")
                    return True
                else:
                    messagebox.showerror("Error de inicio de sesión", "Contraseña incorrecta")
            else:
                messagebox.showerror("Error de inicio de sesión", f"El correo {correo} no está registrado")
        except Error as e:
            print("Error al ejecutar: ", e)

        return False


    def registro(self, nombre, apellido, correo, contraseña, rut):
        sql = "SELECT * FROM bibliotecario WHERE CORREO_B = ?"
        self.cursor.execute(sql, (correo,))
        result = self.cursor.fetchone()

        if result is not None:
            messagebox.showerror("Error de registro", f"El correo {correo} ingresado ya existe, ingrese otro correo.")
            return

        contraHash = hashlib.sha256(contraseña.encode()).hexdigest()
        sql = "INSERT INTO bibliotecario (NOMBRE_B, APELLIDO_B, CORREO_B, CONTRASENA, RUT_B) VALUES (?, ?, ?, ?, ?)"
        vals = (nombre, apellido, correo, contraHash, rut)
        self.cursor.execute(sql, vals)
        self.connect.commit()
        messagebox.showinfo(f"Registro exitoso", f"El usuario {nombre} ha sido registrado correctamente.")