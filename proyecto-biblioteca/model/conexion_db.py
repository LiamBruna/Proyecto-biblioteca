import sqlite3 #Modulo para crear la conexión con la base de datos
from datetime import datetime, timedelta # Modulo para controlar el tiempo en la app
from sqlite3 import Error # Modulo para mostrar errores por si se presentan
from tkinter import messagebox # Modulo para mostrar mensajes en ventanas emergentes
import hashlib # Modulo para hashear las contraseñas ingresadas


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

    def obtenerUsuarioLog(self, correo):
        sql = "SELECT ID_B FROM bibliotecario WHERE CORREO_B = ?"
        self.cursor.execute(sql, (correo,))
        results = self.cursor.fetchone()

        if results is None:
            messagebox.showerror("Registro de préstamo", "El bibliotecario no está logeado")
        else:
            id_b = results[0]
            return id_b

    # MÉTODOS PARA FRAME INICIO
    def obtenerPrestamosConRetraso(self):
        fecha_actual = datetime.today()

        sql = """
        SELECT p.ID_P, u.NOMBRE_U, u.APELLIDO_U, p.RUT_U, u.TIPO_U, p.F_DEVOLUCION, p.ISBN, l.TITULO, u.MULTA, u.MONTO
        FROM prestamo p
        LEFT JOIN usuario u ON p.RUT_U = u.RUT_U
        LEFT JOIN libro l ON p.ISBN = l.ISBN
        WHERE p.F_DEVOLUCION < date('now');
        """

        self.cursor.execute(sql)
        resultados = self.cursor.fetchall()

        for resultado in resultados:
            id_prestamo = resultado[0]
            rut_usuario = resultado[3]
            f_devolucion = datetime.strptime(resultado[5], "%Y-%m-%d")

            dias_retraso = (fecha_actual - f_devolucion).days
            multa = "No pagado"
            monto = dias_retraso * 1000

            # Actualizar la multa y el monto en la tabla usuario
            sql_actualizar = "UPDATE usuario SET MULTA = ?, MONTO = ? WHERE RUT_U = ?"
            self.cursor.execute(sql_actualizar, (multa, monto, rut_usuario))
            self.connect.commit()

        return resultados   
    
    def retrasoDeFecha(self, rut):
        sql = "SELECT COUNT(*) FROM prestamo WHERE RUT_U = ? AND F_DEVOLUCION < DATE('now')"
        try:
            self.cursor.execute(sql, (rut,))
            results = self.cursor.fetchone()
            cantidad_retrasos = results[0]
            return cantidad_retrasos > 0
        except Exception as e:
            messagebox.showerror("Realizar Préstamo", f"{str(e)}")
            return False

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
            messagebox.showinfo("Modificar Stock", f"El stock del libro ha sido actualizado")
        except Exception as e:
            messagebox.showerror(f"Modificar stock", f"{str(e)}")

    # Método para mostrar los libros en prestamo
    def mostrarLibrosPrestamo(self):
        sql = "SELECT libro.ISBN, libro.TITULO, ejemplar.Estado FROM libro LEFT JOIN ejemplar ON libro.ISBN = ejemplar.ISBN LEFT JOIN prestamo ON libro.ISBN = prestamo.ISBN WHERE libro.ISBN = prestamo.ISBN"
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
        except Exception as e:
            messagebox.showerror("Realizar Préstamo", f"{str(e)}")
        
    def verificarISBN(self, isbn):
        sql = "SELECT COUNT(*) FROM libro WHERE ISBN = ?"
        try:
            self.cursor.execute(sql, (isbn,))
            result = self.cursor.fetchone()
            cantidad = result[0]
            return cantidad > 0
        except Exception as e:
            messagebox.showerror("Verificar ISBN", f"Error al verificar el ISBN: {str(e)}")
            return False

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

    def registrarPrestamo(self, bibliotecario, rut, isbn, f_prestamo, f_devolucion, tipo_usuario):
        sql = "INSERT INTO prestamo (RUT_U, ISBN, F_PRESTAMO, F_DEVOLUCION, TIPO_U, ID_B) VALUES (?, ?, ?, ?, ?, ?)"
        try:
            self.cursor.execute(sql, (rut, isbn, f_prestamo, f_devolucion, tipo_usuario, bibliotecario))
            self.connect.commit()
            messagebox.showinfo("Registro de Préstamo", "El préstamo se ha registrado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el préstamo: {str(e)}")

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

    # MÉTODOS PARA FRAME CATALOGO
    # Método para obtener los libros y autores de la base de datos
    def obtenerLibrosCatalogo(self):
        sql = "SELECT a.NOMBRE_A, a.APELLIDO_A, a.NACIONALIDAD, l.TITULO, l.IMAGEN, l.ISBN FROM libro l LEFT JOIN autor a ON a.ID_A = l.ID_L"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            messagebox.showerror("Catalogo", f"{str(e)}")

    # Método para obtener todas las categorías
    def obtenerCategorias(self):
        sql = "SELECT DISTINCT CATEGORIA FROM categoria"
        try:
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()

            if resultados:
                categorias = [categoria[0] for categoria in resultados]
                categorias_limpias = [categoria.strip().replace("{", "").replace("}", "") for categoria in categorias]
                return categorias_limpias
            else:
                return []
        except Exception as e:
            messagebox.showerror("Categorías", f"{str(e)}")

    # Método para obtener el libro por la categoría
    def obtenerLibroCategoria(self, categoria):
        sql = "SELECT a.NOMBRE_A, a.APELLIDO_A, a.NACIONALIDAD, l.TITULO, l.IMAGEN, l.ISBN FROM libro l INNER JOIN libro_categoria cl ON l.ID_L = cl.ID_L INNER JOIN categoria c ON cl.ID_C = c.ID_C INNER JOIN autor a ON a.ID_A = l.ID_L WHERE c.CATEGORIA = ?"
        try:
            self.cursor.execute(sql, (categoria,))
            result = self.cursor.fetchall()
            return result
        except Exception as e:
           messagebox.showerror("Error al obtener libros por categoría", f"{str(e)}") 

    # Método para obtener el libro por su nombre
    def obtenerLibroNombre(self, nombre):
        sql = "SELECT a.NOMBRE_A, a.APELLIDO_A, a.NACIONALIDAD, l.TITULO, l.IMAGEN, l.ISBN FROM libro l INNER JOIN 	autor a ON a.ID_A = l.ID_L WHERE l.TITULO = ?"
        try:
            self.cursor.execute(sql, (nombre,))
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            messagebox.showerror("Error al obtener libros por nombre", f"{str(e)}")

    # Método para obtener el libro por su isbn
    def obtenerLibroIsbn(self, isbn):
        sql = "SELECT a.NOMBRE_A, a.APELLIDO_A, a.NACIONALIDAD, l.TITULO, l.IMAGEN, l.ISBN FROM libro l INNER JOIN 	autor a ON a.ID_A = l.ID_L WHERE l.ISBN = ?"
        try:
            self.cursor.execute(sql, (isbn,))
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            messagebox.showerror("Error al obtener libros por ISBN", f"{str(e)}")

    # MÉTODOS PARA FRAME PRESTAMOS POR USUARIO
    def verificarRutEnBaseDeDatos(self, rut):
        sql = "SELECT COUNT(*) FROM usuario WHERE RUT_U = ?"
        try:
            self.cursor.execute(sql, (rut,))
            result = self.cursor.fetchone()
            if result[0] > 0:
                return True
            else:
                return False
        except Exception as e:
            messagebox.showerror("Error al verificar el RUT en la base de datos", f"{str(e)}")
            return False

    def obtenerPrestamoUsuarioRut(self, rut):
        if not self.verificarRutEnBaseDeDatos(rut):
            return None

        sql = "SELECT l.ISBN, l.TITULO, u.NOMBRE_U, u.APELLIDO_U, u.RUT_U FROM libro l LEFT JOIN prestamo p ON l.ISBN = p.ISBN LEFT JOIN usuario u ON u.RUT_U = p.RUT_U WHERE u.RUT_U = ?"
        try:
            self.cursor.execute(sql, (rut,))
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            messagebox.showerror("Error al obtener el prestamo por RUT", f"{str(e)}")
            return None

    # MÉTODOS PARA EL FRAME PAGAR MULTA
    def obtenerUsuarioMulta(self, rut):
        sql = "SELECT U.NOMBRE_U, U.APELLIDO_U, U.DIRECCION_U, U.RUT_U, U.CELULAR_U, U.CORREO_U, U.TIPO_U, U.MULTA, SUM(U.MONTO) AS MONTO FROM usuario U LEFT JOIN prestamo P ON U.RUT_U = P.RUT_U WHERE U.RUT_U = ? AND P.F_DEVOLUCION < date('now') GROUP BY U.RUT_U"
        try:
            self.cursor.execute(sql, (rut,))
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            messagebox.showerror("Error al obtener el usuario por RUT", f"{str(e)}")

    def marcarMultaPagada(self, rut):
        sql = "UPDATE usuario SET MULTA = 'Pagado' WHERE RUT_U = ?"
        try:
            self.cursor.execute(sql, (rut,))
            self.connect.commit()
        except Exception as e:
            messagebox.showerror("Error al marcar multa como pagada", f"{str(e)}")

    def eliminarPrestamo(self, rut):
        sql = "DELETE FROM prestamo WHERE RUT_U = ?"
        try:
            self.cursor.execute(sql, (rut,))
            self.connect.commit()
        except Exception as e:
            messagebox.showerror("Error al eliminar préstamo", f"{str(e)}")