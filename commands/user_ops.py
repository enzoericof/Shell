import crypt
import subprocess
import os
import json
import socket
from commands.file_ops import cambiar_permisos, cambiar_propietario
from datetime import datetime
from utils import log_action, log_error, log_horario_fuera_de_rango

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

        # Crear nuevo usuario
        usuarios[nombre] = {
            "password": contrasena,
            "datos_personales": datos_personales,
            "horarios_permitidos": ["08:00-18:00"],
            "ips_permitidas": ips_permitidas,
        }
        guardar_datos_usuarios(usuarios)

        mensaje = f"Usuario {nombre} agregado con éxito."
        print(mensaje)
        log_action(f"{mensaje} Datos: {datos_personales}, IPs: {ips_permitidas}")

        # Configurar directorio del usuario
        user_dir = f"/root/Shell-main/LFS-Shell/users/{nombre}"
        os.makedirs(user_dir, exist_ok=True)
        cambiar_propietario(user_dir, nombre)
        cambiar_permisos(user_dir, "0700")

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
        if usuarios[usuario]["password"] != contrasena_actual:
            mensaje = "Error: Contraseña actual incorrecta."
            print(mensaje)
            log_error(mensaje)
            return

        # Cambiar la contraseña
        usuarios[usuario]["password"] = nueva_contrasena
        guardar_datos_usuarios(usuarios)

        mensaje = f"Contraseña cambiada con éxito para el usuario {usuario}."
        print(mensaje)
        log_action(mensaje)

    except Exception as e:
        mensaje = f"Error inesperado al cambiar la contraseña para {usuario}: {e}"
        print(mensaje)
        log_error(mensaje)

def validar_acceso(usuario, contrasena):
    usuarios = cargar_datos_usuarios()
    print(f"Usuarios cargados: {usuarios}")

    if usuario not in usuarios:
        print(f"Usuario no encontrado: {usuario}")
        return False, "Usuario incorrecto."
    if usuarios[usuario]["password"] != contrasena:
        print(f"Contraseña incorrecta para el usuario: {usuario}")
        return False, "Contraseña incorrecta."

    # Validar horario
    horarios_permitidos = usuarios[usuario]["horarios_permitidos"]
    hora_actual = datetime.now().strftime("%H:%M")
    print(f"Hora actual: {hora_actual}, Horarios permitidos: {horarios_permitidos}")
    permitido = any(
        hora_inicio <= hora_actual <= hora_fin
        for horario in horarios_permitidos
        for hora_inicio, hora_fin in [horario.split("-")]
    )
    print(f"Acceso permitido por horario: {permitido}")

    # Validar IP
    ip_actual = socket.gethostbyname(socket.gethostname())
    print(f"IP actual: {ip_actual}, IPs permitidas: {usuarios[usuario]['ips_permitidas']}")
    ip_permitida = ip_actual in usuarios[usuario]["ips_permitidas"]

    print(f"Acceso permitido por IP: {ip_permitida}")

    return permitido and ip_permitida, ip_actual



