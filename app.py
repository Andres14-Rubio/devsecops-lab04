import os
import sqlite3
import hashlib
from werkzeug.security import generate_password_hash

# CORREGIDO (Hardcoded Secret / CWE-547):
# Antes: API_KEY = "123456789_SECRET_KEY"
# Ahora: se lee desde una variable de entorno, nunca queda escrita en el código.
API_KEY = os.environ.get("API_KEY")


def buscar_usuario(nombre):
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    # CORREGIDO (SQL Injection / CWE-89):
    # Antes: consulta = "SELECT * FROM usuarios WHERE nombre = '" + nombre + "'"
    #        cursor.execute(consulta)
    # Ahora: se usa una consulta parametrizada. El "?" es reemplazado de forma
    # segura por la librería, nunca se concatena el texto del usuario.
    consulta = "SELECT * FROM usuarios WHERE nombre = ?"
    cursor.execute(consulta, (nombre,))

    resultado = cursor.fetchall()
    conexion.close()

    return resultado


def ejecutar_comando(comando):
    # CORREGIDO (Command Injection / CWE-78):
    # Antes: os.system(comando)  -> ejecutaba cualquier texto en la shell
    # Ahora: en vez de recibir un comando arbitrario, se restringe a una
    # lista fija de acciones permitidas (allowlist). Esto es lo que de
    # verdad elimina el riesgo, no solo "limpiar" el texto.
    comandos_permitidos = {
        "listar": ["ls", "-la"],
        "fecha": ["date"],
    }
    if comando not in comandos_permitidos:
        return "Comando no permitido"

    import subprocess
    resultado = subprocess.run(
        comandos_permitidos[comando], capture_output=True, text=True
    )
    return resultado.stdout


def calcular_hash(password):
    # CORREGIDO (Weak Password Hash / CWE-916):
    # Antes: hashlib.md5(password.encode()).hexdigest()  -> MD5 es inseguro
    # Ahora: se usa generate_password_hash de werkzeug, que aplica un
    # algoritmo lento y con "salt" (pbkdf2/scrypt), pensado para contraseñas.
    return generate_password_hash(password)


def leer_archivo(nombre):
    # CORREGIDO (Path Traversal / CWE-23):
    # Antes: archivo = open("archivos/" + nombre, "r")  -> permitía "../../etc/passwd"
    # Ahora: se resuelve la ruta absoluta y se verifica que siga DENTRO
    # de la carpeta "archivos". Si alguien intenta escapar con "../", se rechaza.
    base_dir = os.path.abspath("archivos")
    ruta_solicitada = os.path.abspath(os.path.join(base_dir, nombre))

    if not ruta_solicitada.startswith(base_dir + os.sep):
        return "Ruta no permitida"

    with open(ruta_solicitada, "r") as archivo:
        contenido = archivo.read()

    return contenido


def main():
    print("=== Aplicación DevSecOps Lab 04 (versión corregida) ===")

    nombre = input("Ingrese usuario: ")
    print(buscar_usuario(nombre))

    comando = input("Ingrese comando (listar/fecha): ")
    print(ejecutar_comando(comando))

    password = input("Ingrese contraseña: ")
    print(calcular_hash(password))


if __name__ == "__main__":
    main()