import mysql.connector as db
import json
import os

# Cargar las claves de conexión de la base de datos desde el archivo JSON
with open('keys.json') as json_file:
    keys = json.load(json_file)

def write_file(data, path):
    """Escribe los datos binarios de una imagen en un archivo en disco"""
    try:
        with open(path, 'wb') as file:
            file.write(data)
    except Exception as e:
        print(f"Error al escribir el archivo: {e}")

def registerUser(name, photo_path):
    """Registra a un nuevo usuario en la base de datos, guardando la imagen como archivo"""
    id = 0
    inserted = 0

    try:
        # Convertir la imagen en un archivo binario (solo si quieres almacenarlo como binario en DB)
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as file:
                photo = file.read()
        else:
            print(f"El archivo {photo_path} no existe.")
            return {"id": id, "affected": inserted}

        # Establecer conexión con la base de datos
        con = db.connect(
            host=keys["host"],
            user=keys["user"],
            password=keys["password"],
            database=keys["database"]
        )
        with con.cursor() as cursor:
            # Insertar el nuevo usuario en la base de datos
            sql = "INSERT INTO `user`(name, photo) VALUES (%s,%s)"
            cursor.execute(sql, (name, photo))
            con.commit()
            inserted = cursor.rowcount
            id = cursor.lastrowid

    except db.Error as e:
        print(f"Error en la base de datos: {e}")
    except Exception as e:
        print(f"Error desconocido: {e}")
    finally:
        if con.is_connected():
            con.close()

    return {"id": id, "affected": inserted}

def getUser(name, path):
    """Obtiene los datos de un usuario desde la base de datos y guarda la imagen en el sistema de archivos"""
    id = 0
    rows = 0

    try:
        # Establecer conexión con la base de datos
        con = db.connect(
            host=keys["host"],
            user=keys["user"],
            password=keys["password"],
            database=keys["database"]
        )
        with con.cursor() as cursor:
            # Buscar al usuario por nombre
            sql = "SELECT * FROM `user` WHERE name = %s"
            cursor.execute(sql, (name,))
            records = cursor.fetchall()

            # Si el usuario existe, recuperar la imagen y escribirla en el archivo
            for row in records:
                id = row[0]
                photo_data = row[2]
                if photo_data:
                    write_file(photo_data, os.path.join(path, f"{name}.jpg"))
                rows = len(records)

    except db.Error as e:
        print(f"Error en la base de datos: {e}")
    except Exception as e:
        print(f"Error desconocido: {e}")
    finally:
        if con.is_connected():
            con.close()

    return {"id": id, "affected": rows}
