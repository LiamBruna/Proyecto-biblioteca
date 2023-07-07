import sqlite3

def insertar_imagen(ruta_imagen):
    try:
        # Leer el archivo de imagen como datos binarios
        with open(ruta_imagen, 'rb') as file:
            imagen_data = file.read()

        # Establecer conexión a la base de datos
        conexion = sqlite3.connect('C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\database\\biblioteca.db')
        cursor = conexion.cursor()

        # Insertar la imagen en la base de datos
        cursor.execute("INSERT INTO libro (IMAGEN) VALUES (?)", (imagen_data,))

        # Guardar los cambios y cerrar la conexión
        conexion.commit()
        conexion.close()
        
        print("Imagen insertada correctamente en la base de datos.")

    except Exception as e:
        print("Error al insertar la imagen en la base de datos:", str(e))

# Llamar a la función insertar_imagen y pasar la ruta de la imagen
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\thelastofus.jpg")