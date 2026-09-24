import os
import sqlite3
import hashlib

API_KEY = "123456789_SECRET_KEY"


def buscar_usuario(nombre):
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    consulta = "SELECT * FROM usuarios WHERE nombre = '" + nombre + "'"

    cursor.execute(consulta)

    resultado = cursor.fetchall()
    conexion.close()

    return resultado


def ejecutar_comando(comando):
    os.system(comando)


def calcular_hash(password):
    return hashlib.md5(password.encode()).hexdigest()


def leer_archivo(nombre):
    archivo = open("archivos/" + nombre, "r")
    contenido = archivo.read()
    archivo.close()

    return contenido


def main():
    print("=== Aplicación DevSecOps Lab 04 ===")

    nombre = input("Ingrese usuario: ")
    print(buscar_usuario(nombre))

    comando = input("Ingrese comando: ")
    ejecutar_comando(comando)

    password = input("Ingrese contraseña: ")
    print("Hash:", calcular_hash(password))

    archivo = input("Ingrese archivo: ")
    print(leer_archivo(archivo))


if __name__ == "__main__":
    main()
    