import sqlite3

def insertar_imagen(ruta_imagen, id):
    try:
        # Leer el archivo de imagen como datos binarios
        with open(ruta_imagen, 'rb') as file:
            imagen_data = file.read()

        # Establecer conexión a la base de datos
        conexion = sqlite3.connect('C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\database\\biblioteca.db')
        cursor = conexion.cursor()

        # Insertar la imagen en la base de datos
        cursor.execute("UPDATE libro SET IMAGEN = ? WHERE ID_L = ?", (imagen_data, id))

        # Guardar los cambios y cerrar la conexión
        conexion.commit()
        conexion.close()
        
        print("Imagen insertada correctamente en la base de datos.")

    except Exception as e:
        print("Error al insertar la imagen en la base de datos:", str(e))

# Llamar a la función insertar_imagen y pasar la ruta de la imagen
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\thelastofus.png", 1)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\tokillamochkingbird.png", 2)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\thegreatgatsby.png", 3)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\george-orwell-1984.png", 4)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\where_the_wild-things-are.png", 5)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\charlottes_web.png", 6)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\holes.png", 7)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\harry_potter_stone.png", 8)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\the_hunger_games.png", 9)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\the-hobbit-.png", 10)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\the_fault_in_our_stars.png", 11)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\the_chronicles_of_narnia.png", 12)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\the_alchemist.png", 13)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\pride_and_prejudice.png", 14)
insertar_imagen("C:\\workspace\\Proyecto-biblioteca\\proyecto-biblioteca\\img\\The_Book_Thief.png", 15)