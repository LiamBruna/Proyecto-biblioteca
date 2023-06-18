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
            sql = "SELECT * FROM bibliotecario WHERE TRIM(CORREO_B) = ? AND CONTRASENA = ?"
            self.cursor.execute(sql, (correo.strip(), contraseña))
            result = self.cursor.fetchone()
            print(result)

            if result is not None:
                messagebox.showinfo("Inicio de sesión exitoso", f"Bienvenido {correo}")
                return True
            else:
                messagebox.showerror("Error de inicio de sesión", "Credenciales incorrectas")
                return False
        except Error as e:
            print("Error al ejecutar: ", e)
            return False


    def registro(self, nombre, apellido, correo, contraseña, rut):
        sql = "INSERT INTO bibliotecario (NOMBRE_B, APELLIDO_B, CORREO_B, CONTRASENA, RUT_B) VALUES (?, ?, ?, ?, ?)"
        vals = (nombre, apellido, correo, contraseña, rut)
        self.cursor.execute(sql, vals)
        self.connect.commit()
        messagebox.showinfo(f"Registro exitoso", f"El usuario {nombre} ha sido registrado correctamente.")