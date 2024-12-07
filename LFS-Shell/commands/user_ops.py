import crypt
import subprocess
import os
from utils import log_action, log_error

USER_DATA_FILE = "/root/Shell-main/LFS-Shell/users/user_data.json"

def cargar_datos_usuarios():
    """Carga los datos de los usuarios desde un archivo JSON."""
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, "r") as file:
        return json.load(file)

def guardar_datos_usuarios(data):
    """Guarda los datos de los usuarios en un archivo JSON."""
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def agregar_usuario(nombre, contrasena, verificar_contrasena, datos_personales, ips_permitidas):
    """
    Agrega un usuario al sistema con una contraseña, datos adicionales y doble verificación de contraseña.
    Registra también las IPs permitidas.
    """
    try:
        if contrasena != verificar_contrasena:
            mensaje = "Error: Las contraseñas no coinciden."
            print(mensaje)
            log_error(mensaje)
            return

        # Cargar datos actuales
        usuarios = cargar_datos_usuarios()
        if nombre in usuarios:
            mensaje = f"Error: El usuario {nombre} ya existe."
            print(mensaje)
            log_error(mensaje)
            return

        # Guardar datos
        hashed_passwd = crypt.crypt(contrasena)
        usuarios[nombre] = {
            "password": hashed_passwd,
            "datos_personales": datos_personales,
            "horarios_permitidos": [],
            "ips_permitidas": ips_permitidas
        }
        guardar_datos_usuarios(usuarios)

        mensaje = f"Usuario {nombre} agregado con éxito."
        print(mensaje)
        log_action(f"{mensaje} Datos: {datos_personales}, IPs: {ips_permitidas}")

    except Exception as e:
        mensaje = f"Error inesperado al agregar usuario {nombre}: {e}"
        print(mensaje)
        log_error(mensaje)

def cambiar_contrasena(usuario, contrasena_actual, nueva_contrasena, verificar_nueva_contrasena):
    """
    Cambia la contraseña de un usuario con doble verificación y validación de contraseña actual.
    """
    try:
        if nueva_contrasena != verificar_nueva_contrasena:
            mensaje = "Error: Las nuevas contraseñas no coinciden."
            print(mensaje)
            log_error(mensaje)
            return

        # Cargar datos actuales
        usuarios = cargar_datos_usuarios()
        if usuario not in usuarios:
            mensaje = f"Error: El usuario {usuario} no existe."
            print(mensaje)
            log_error(mensaje)
            return

        # Verificar contraseña actual
        hashed_actual = crypt.crypt(contrasena_actual)
        if usuarios[usuario]["password"] != hashed_actual:
            mensaje = "Error: Contraseña actual incorrecta."
            print(mensaje)
            log_error(mensaje)
            return

        # Cambiar la contraseña
        hashed_nueva = crypt.crypt(nueva_contrasena)
        usuarios[usuario]["password"] = hashed_nueva
        guardar_datos_usuarios(usuarios)

        mensaje = f"Contraseña cambiada con éxito para el usuario {usuario}."
        print(mensaje)
        log_action(mensaje)

    except Exception as e:
        mensaje = f"Error inesperado al cambiar la contraseña para {usuario}: {e}"
        print(mensaje)
        log_error(mensaje)
                    