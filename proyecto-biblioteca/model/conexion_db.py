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
        except Exception as e:
            messagebox.showerror("Error de inicio de sesión", f"{str(e)}")

        return False

    # Método para registrarse en la app
    def registro(self, nombre, apellido, correo, contraseña, rut, celular):
        sql = "SELECT * FROM bibliotecario WHERE CORREO_B = ?"
        self.cursor.execute(sql, (correo,))
        result = self.cursor.fetchone()

        if result is not None:
            messagebox.showerror("Error de registro", f"El correo {correo} ingresado ya existe, ingrese otro correo.")
            return

        contraHash = hashlib.sha256(contraseña.encode()).hexdigest()
        sql = "INSERT INTO bibliotecario (NOMBRE_B, APELLIDO_B, CORREO_B, CONTRASENA, RUT_B, CELULAR_B) VALUES (?, ?, ?, ?, ?, ?)"
        vals = (nombre, apellido, correo, contraHash, rut, celular)
        self.cursor.execute(sql, vals)
        self.connect.commit()
        messagebox.showinfo(f"Registro exitoso", f"El usuario {nombre} ha sido registrado correctamente.")

    # MÉTODOS PARA FRAME REGISTRAR PRÉSTAMO
    # Método para registrar un préstamo de libro
    def registrarPrestamo(self, correo, rut_u, isbn, f_prestamo, f_devolucion, tipo_u):
        try:
            # Obtener el id del bibliotecario logeado
            bibliotecarioId = self.obtenerUsuarioLog(correo)

            sql_prestamo = "INSERT INTO prestamo (RUT_U, ISBN, F_PRESTAMO, F_DEVOLUCION, TIPO_U, ID_B) VALUES (?, ?, ?, ?, ?, ?)"
            vals_prestamo = (rut_u, isbn, f_prestamo, f_devolucion, tipo_u, bibliotecarioId)
            self.cursor.execute(sql_prestamo, vals_prestamo)
            self.connect.commit()

            # Obtener el stock actual del libro
            stock_actual = self.obtenerStockLibro(isbn)

            # Hacemos la resta en el stock actual en caso de que se realice el prestamo de un libro
            nuevo_stock = stock_actual - 1

            # Actualizamos el stock actual
            self.actualizarStockLibro(nuevo_stock, isbn)

            messagebox.showinfo("Registro de préstamo", "El préstamo ha sido registrado correctamente.")
        except Error as e:
            messagebox.showerror("Registro de préstamo", str(e))

    def obtenerUsuarioLog(self, correo):
        sql = "SELECT ID_B FROM bibliotecario WHERE CORREO_B = ?"
        self.cursor.execute(sql, (correo,))
        results = self.cursor.fetchone()

        if results is None:
            messagebox.showerror("Registro de préstamo", "El bibliotecario no está logeado")
        else:
            id_b = results[0]
            return id_b

    def actualizarStockLibro(self, nuevo_stock, isbn):
        try:
            sql = "UPDATE libro SET STOCK = ? WHERE ISBN = ?"
            vals = (nuevo_stock, isbn)
            self.cursor.execute(sql, vals)
            self.connect.commit()
        except Exception as e:
            messagebox.showerror("Registro de préstamo", f"{str(e)}")

    def obtenerStockLibro(self, isbn):
        try:
            sql = "SELECT STOCK FROM libro WHERE ISBN = ?"
            self.cursor.execute(sql, (isbn,))
            resultado = self.cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                messagebox.showerror("Registro de préstamo", f"Libro con ISBN {isbn} no encontrado.")
                return 0  # O cualquier otro valor predeterminado en caso de no encontrar el libro
        except Exception as e:
            messagebox.showerror("Registro de préstamo", str(e))
            return 0  # O cualquier otro valor predeterminado en caso de error

    # Método para mostrar información personal de los usuarios registrados
    def mostrarUsuarios(self):
        sql = "SELECT * FROM usuario"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            messagebox.showerror("Mostrar usuarios", f"{str(e)}")
 
    # Método para buscar un libro por ISBN
    def buscarLibro(self, isbn):
        sql = "SELECT * FROM libro WHERE ISBN = ?"
        self.cursor.execute(sql, (isbn,))
        results = self.cursor.fetchall()
        return results

    # Método para actualizar el stock del libro
    def actualizarStock(self, stock, isbn):
        sql = "UPDATE libro SET STOCK = ? WHERE ISBN = ?"
        try:
            self.cursor.execute(sql, (stock, isbn))
            self.connect.commit()
            messagebox.showinfo("Stock", f"El stock del libro ha sido actualizado")
        except Exception as e:
            messagebox.showerror(f"Modificar stock", f"{str(e)}")

    # Método para mostrar los libros en prestamo
    def mostrarLibrosPrestamo(self):
        sql = "SELECT libro.ID_L, libro.TITULO, ejemplar.Estado FROM libro LEFT JOIN ejemplar ON libro.ISBN = ejemplar.ISBN LEFT JOIN prestamo ON libro.ISBN = prestamo.ISBN WHERE libro.ISBN = prestamo.ISBN"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            messagebox.showerror("Mostrar Libros en Préstamo", f"{str(e)}")

    # MÉTODOS PARA FRAME REALIZAR PRÉSTAMO
    # Método para obtener el tipo de usuario mediante el RUT
    def obtenerTipoUsuario(self, rut):
        sql = "SELECT TIPO_U FROM usuario WHERE RUT_U = ?"
        try:
            self.cursor.execute(sql, (rut,))
            results = self.cursor.fetchone()
            if results:
                tipo_usuario = results[0]
                return tipo_usuario
            else:
                messagebox.showerror("Realizar Préstamo", f"El RUT {rut} no esta registrado en la base de datos.")
        except Exception as e:
            messagebox.showerror("Realizar Préstamo", f"{str(e)}")

    def obtenerCantidadLibrosPrestamo(self, rut_u):
        try:
            sql = "SELECT COUNT(*) FROM prestamo WHERE RUT_U = ?"
            self.cursor.execute(sql, (rut_u,))
            results = self.cursor.fetchone()
            cantidad = results[0]
            return cantidad
        except Exception as e:
            messagebox.showerror("Realizar Préstamo", f"{str(e)}")
            return 0

    # MÉTODO PARA FRAME REGISTRAR USUARIO
    # Método para registrar un usuario
    def registrarUsuario(self, nombre, apellido, direccion, rut, celular, correo, tipo):
        sql = "SELECT * FROM usuario WHERE CORREO_U = ?"
        self.cursor.execute(sql, (correo,))
        result = self.cursor.fetchone()

        if result is not None:
            messagebox.showerror("Error de registro", f"El correo {correo} ingresado ya existe, ingrese otro correo.")
            return

        sql = "INSERT INTO usuario (NOMBRE_U, APELLIDO_U, DIRECCION_U, RUT_U, CELULAR_U, CORREO_U, TIPO_U) VALUES (?, ?, ?, ?, ?, ?, ?)"
        try:
            self.cursor.execute(sql, (nombre, apellido, direccion, rut, celular, correo, tipo))
            self.connect.commit()
            messagebox.showinfo("Registrar Usuario", f"El usuario {nombre} ha sido registrado correctamente.")
        except Exception as e:
            messagebox.showerror("Registrar Usuario", f"{str(e)}")

    # MÉTODO PARA ACTUALIZAR LA CONTRASEÑA DEL BIBLIOTECARIO
    def actualizarContraseñaBibliotecario(self, celular, contraseña):
        sql = "UPDATE bibliotecario SET CONTRASENA = ? WHERE CELULAR_B = ?"
        try:
            contraHash = hashlib.sha256(contraseña.encode()).hexdigest()
            self.cursor.execute(sql, (contraHash, celular))
            self.connect.commit()
            messagebox.showinfo("Recuperación de contraseña", f"Su contraseña ha sido actualizada.")
        except Exception as e:
            messagebox.showerror(f"Recuperación de contraseña", f"{str(e)}")

    # MÉTODOS PARA RENOVAR LIBRO
    def actualizarPrestamo(self, rut, isbn, nueva_fecha_devolucion, id_bibliotecario):
        try:
            sql_actualizar = "UPDATE prestamo SET F_DEVOLUCION = ?, ID_B = ? WHERE RUT_U = ? AND ISBN = ?"
            vals_actualizar = (nueva_fecha_devolucion, id_bibliotecario, rut, isbn)
            self.cursor.execute(sql_actualizar, vals_actualizar)
            self.connect.commit()
            return True  # Devolver True si la actualización es exitosa
        except Exception as e:
            messagebox.showerror("Error al actualizar préstamo", str(e))
            return False  # Devolver False en caso de error

    def obtenerFechaDevolucionPrestamo(self, rut, isbn):
        try:
            sql = "SELECT F_DEVOLUCION FROM prestamo WHERE RUT_U = ? AND ISBN = ?"
            vals = (rut, isbn)
            self.cursor.execute(sql, vals)
            result = self.cursor.fetchone()
            if result:
                fecha_devolucion = result[0]
                return fecha_devolucion
            else:
                return None
        except Error as e:
            messagebox.showerror("Error al obtener la fecha de devolución del préstamo:", str(e))
            return None
        
    def haRealizadoRenovacion(self, rut):
        # Consultar la cantidad de renovaciones realizadas por el alumno
        query = "SELECT COUNT(*) FROM prestamo WHERE RUT_U = ? AND Renovado = 1"
        params = (rut,)
        self.cursor.execute(query, params)
        result = self.cursor.fetchone()

        # Verificar si se encontró un registro de renovación
        if result is not None and result[0] > 0:
            return True
        else:
            return False
        
    def registrarRenovacion(self, rut, isbn):
        try:
            # Verificar si el alumno ya ha realizado una renovación
            if self.haRealizadoRenovacion(rut):
                return False

            # Actualizar el campo "Renovado" a 1 para el libro específico prestado por el alumno
            query = "UPDATE prestamo SET RENOVADO = 1 WHERE RUT_U = ? AND ISBN = ?"
            params = (rut, isbn)
            self.cursor.execute(query, params)
            self.connect.commit()

            return True
        except Exception as e:
            messagebox.showerror("Error al registrar la renovación", str(e))
            return False
