import crypt
import spwd
import subprocess
import os
import pwd
import json
import socket
from commands.file_ops import cambiar_permisos, cambiar_propietario
from datetime import datetime
from utils import log_action, log_error, log_horario_fuera_de_rango

USER_DATA_FILE = "/root/Shell-main/LFS-Shell/users/user_data.json"
USER_UID_MAP = "/root/Shell-main/LFS-Shell/users/user_uid.json"

def obtener_uid(usuario):
    return USER_UID_MAP.get(usuario)

def agregar_usuario(nombre, contrasena, verificar_contrasena, datos_personales, ips_permitidas):
    try:
        if contrasena != verificar_contrasena:
            raise ValueError("Las contraseñas no coinciden.")

        # Verificar si el usuario ya existe en el sistema real
        try:
            pwd.getpwnam(nombre)
            raise ValueError(f"El usuario {nombre} ya existe en el sistema.")
        except KeyError:
            pass  # El usuario no existe, podemos crearlo

        # Crear usuario en el sistema real (como root)
        subprocess.run(['useradd', '-m', '-s', '/bin/bash', nombre], check=True)

        # Cambiar la contraseña del usuario
        subprocess.run(['chpasswd'], input=f"{nombre}:{contrasena}".encode(), check=True)

        # Configurar datos adicionales en el archivo JSON
        usuarios = cargar_datos_usuarios()
        usuarios[nombre] = {
            "datos_personales": datos_personales,
            "horarios_permitidos": ["08:00-10:00"],
            "ips_permitidas": ips_permitidas,
        }
        guardar_datos_usuarios(usuarios)

        print(f"Usuario {nombre} agregado con éxito.")
    except Exception as e:
        log_error(f"Error al agregar usuario {nombre}: {e}")
        print(f"Error: {e}")

def validar_credenciales(username, password):
    try:
        # Verifica si el usuario existe
        try:
            pwd.getpwnam(username)
        except KeyError:
            print(f"Usuario {username} no encontrado en el sistema.")
            return False

        # Obtén la contraseña cifrada desde /etc/shadow
        shadow_entry = spwd.getspnam(username)
        hashed_password = shadow_entry.sp_pwdp

        # Compara la contraseña ingresada con la cifrada
        if crypt.crypt(password, hashed_password) == hashed_password:
            print(f"Credenciales de {username} verificadas correctamente ")
            return True
        else:
            print("Credenciales incorrectas.")
            return False

    except PermissionError:
        print("Este script debe ejecutarse con privilegios de superusuario para acceder a /etc/shadow.")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False


def guardar_datos_usuarios(usuarios):
    """Guarda los datos de los usuarios en un archivo JSON."""
    with open(USER_DATA_FILE, "w") as file:
        json.dump(usuarios, file)

def solicitar_ips():
    """Solicitar al usuario las IPs permitidas."""
    ips = []
    print("Ingrese las IPs permitidas para este usuario. Escriba 'done' para finalizar:")
    while True:
        ip = input("IP: ").strip()
        if ip.lower() == 'done':
            break
        ips.append(ip)
    return ips


def es_horario_permitido(username, horario_actual):
    """
    Verifica si el horario actual está dentro del rango permitido para el usuario.
    """
    try:
        with open(USER_DATA_FILE, "r") as f:
            usuarios = json.load(f)
        horarios_permitidos = usuarios[username]["horarios_permitidos"]
        for rango in horarios_permitidos:
            inicio, fin = rango.split("-")
            if inicio <= horario_actual <= fin:
                return True
    except Exception as e:
        log_error(f"Error al verificar horario para {username}: {e}")
    return False

def cargar_datos_usuarios():
    """Carga los datos de los usuarios desde un archivo JSON."""
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, "r") as file:
        return json.load(file)

import subprocess

def cambiar_contrasena(usuario, contrasena_actual, nueva_contrasena, verificar_nueva_contrasena):
    try:
        # Validar que las nuevas contraseñas coincidan
        if nueva_contrasena != verificar_nueva_contrasena:
            print("Error: Las nuevas contraseñas no coinciden.")
            return

        # Validar las credenciales actuales
        if not validar_credenciales(usuario, contrasena_actual):
            print("Error: La contraseña actual es incorrecta.")
            return

        # Usar chpasswd para cambiar la contraseña
        comando = f"{usuario}:{nueva_contrasena}"
        subprocess.run(
            ['chpasswd'],
            input=comando.encode(),  # Convertir el comando a bytes
            check=True  # Asegurarse de que el comando se ejecute correctamente
        )

        print(f"Contraseña cambiada con éxito para el usuario {usuario}.")

    except subprocess.CalledProcessError as e:
        print(f"Error al cambiar la contraseña: {e}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")


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


def es_ip_permitida(username, ip_actual):
    """
    Verifica si la IP actual está dentro de las IPs permitidas para el usuario.
    """
    try:
        with open(USER_DATA_FILE, "r") as f:
            usuarios = json.load(f)
        ips_permitidas = usuarios[username]["ips_permitidas"]
        if ip_actual in ips_permitidas:
            return True
    except Exception as e:
        log_error(f"Error al verificar IP para {username}: {e}")
    return False
