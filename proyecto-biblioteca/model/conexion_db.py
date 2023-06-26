import sqlite3 #Modulo para crear la conexión con la base de datos
from datetime import datetime, timedelta # Modulo para controlar el tiempo en la app
from sqlite3 import Error # Modulo para mostrar errores por si se presentan
from tkinter import messagebox # Modulo para mostrar mensajes en ventanas emergentes
import hashlib # Modulo para hashear las contraseñas ingresadas

from model.classes import Libro

class BD:
    def __init__(self):
        self.base_datos = 'database/biblioteca.db'
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


    # Método para logearse en la app
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
                    self.bibliotecarioId = result[0]
                    return True
                else:
                    messagebox.showerror("Error de inicio de sesión", "Contraseña incorrecta")
            else:
                messagebox.showerror("Error de inicio de sesión", f"El correo {correo} no está registrado")
        except Error as e:
            print("Error al ejecutar: ", e)

        return False

    # Método para registrarse en la app
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

    # Método para registrar un préstamo de libro
    def registrarPrestamo(self, usuario_actual):
        try:
            sql_bibliotecario = "SELECT ID_B FROM bibliotecario WHERE CORREO_B = ?"
            self.cursor.execute(sql_bibliotecario, (usuario_actual,))
            bibliotecario_result = self.cursor.fetchone()

            if bibliotecario_result is None:
                messagebox.showerror("Error de registro de préstamo", "El bibliotecario no esta registrado.")
                return
            
            bibliotecarioId = bibliotecario_result[0]
            f_prestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sql_prestamo = "INSERT INTO prestamo (F_PRESTAMO, F_DEVOLUCION, ID_B) VALUES (?, ? ,?)"
            vals_prestamo = (f_prestamo, '', bibliotecarioId)
            self.cursor.execute(sql_prestamo, vals_prestamo)
            self.connect.commit()

            messagebox.showinfo("Registro de préstamo", "El préstamo ha sido registrado correctamente.")

        except Error as e:
            print(f"Error al ejecutar: {e}")

    # Método para mostrar información personal de los usuarios registrados
    def mostrarUsuarios(self):
        sql = "SELECT * FROM usuario"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            messagebox.showerror("Mostrar usuarios", f"{str(e)}")

    # Método para saber si existe un libro por su código ISBN
    '''def existeLibro(self, isbn):
        sql = "SELECT * FROM libro WHERE ISBN = ?"
        vals = (isbn)
        existe = False
        try:
            self.cursor.execute(sql, vals)
            result = self.cursor.fetchone()
            if result != None:
                existe = True
            else:
                existe = False
        except Exception as e:
            messagebox.showerror("Existe libro", f"{str(e)}")
        return existe'''
    
    # Método para buscar un libro por ISBN
    def buscarLibro(self, isbn):
        sql = "SELECT * FROM libro WHERE ISBN = ?"
        self.cursor.execute(sql, (isbn,))
        results = self.cursor.fetchall()
        return results
        

    # Método para mostrar los libros en el Catalogo
    def modificarStock(self, isbn, stock):
        sql = "UPDATE libro SET STOCK = ? WHERE ISBN = ?"
        vals = (stock, isbn)
        try:
            if self.existeLibro(isbn == False):
                self.cursor.execute(sql, vals)
                self.connect.commit()
                messagebox.showinfo("Modificar stock", f"Stock del libro se ha actualizado.")
            else:
                messagebox.showerror("Modificar stock", f"El codigo {isbn} del libro no existe.")
        except Exception as e:
            messagebox.showerror(f"Modificar stock", f"{str(e)}")