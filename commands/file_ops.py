import shutil
import os
import argparse
from utils import log_action, log_error
import pwd
import json
USERS_JSON_PATH = '/root/Shell-main/LFS-Shell/users/user_data.json'

def copiar(origen, destino):
    """
    Copia un archivo desde 'origen' a 'destino'.
    """
    try:
        shutil.copy2(origen, destino)
        mensaje = f"Se copió archivo de {origen} a {destino}"
        print(mensaje)
        log_action(mensaje)
    except Exception as e:
        mensaje = f"Error al copiar archivo: {e}"
        print(mensaje)
        log_error(mensaje)

def mover(origen, destino):
    """
    Mueve un archivo desde 'origen' a 'destino'.
    """
    try:
        shutil.move(origen, destino)
        mensaje = f"Se movió el archivo de {origen} a {destino}"
        print(mensaje)
        log_action(mensaje)
    except Exception as e:
        mensaje = f"Error al mover archivo: {e}"
        print(mensaje)
        log_error(mensaje)

def cargar_usuarios():
    try:
        with open(USERS_JSON_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo {USERS_JSON_PATH} no existe.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: El archivo {USERS_JSON_PATH} no tiene un formato válido.")
        return {}

def renombrar(origen, nuevo_nombre):
    """
    Renombra un archivo o directorio.
    """
    try:
        os.rename(origen, nuevo_nombre)
        mensaje = f"Se renombró {origen} a {nuevo_nombre}"
        print(mensaje)
        log_action(mensaje)
    except Exception as e:
        mensaje = f"Error al renombrar: {e}"
        print(mensaje)
        log_error(mensaje)

def cambiar_permisos(path, mode, usuario_actual):
    """
    Cambia los permisos de un archivo o directorio solo si el usuario tiene permisos.
    """
    try:
        usuarios = cargar_usuarios()
        # Verificar si el usuario actual está en el archivo JSON
        if usuario_actual not in usuarios:
            mensaje = f"El usuario {usuario_actual} no existe en el sistema."
            print(mensaje)
            log_error(mensaje)
            return
        
        # Obtén la información del archivo
        info = os.stat(path)
        propietario_uid = info.st_uid
        usuario_uid = pwd.getpwnam(usuario_actual).pw_uid

        # Verifica si el usuario actual es el propietario o root
        if usuario_uid != propietario_uid and usuario_uid != 0:
            mensaje = f"No tienes permisos para cambiar los permisos de {path}."
            print(mensaje)
            log_error(mensaje)
            return

        # Cambiar los permisos
        os.chmod(path, int(mode, 8))
        mensaje = f"Permisos de {path} cambiados a {mode}."
        print(mensaje)
        log_action(mensaje)
    except FileNotFoundError:
        mensaje = f"El archivo o directorio {path} no existe."
        print(mensaje)
        log_error(mensaje)
    except PermissionError:
        mensaje = f"No tienes permisos para realizar esta operación."
        print(mensaje)
        log_error(mensaje)
    except Exception as e:
        mensaje = f"Error inesperado al cambiar permisos de {path}: {e}"
        print(mensaje)
        log_error(mensaje)

def cambiar_propietario(path, nuevo_usuario, usuario_actual):
    """
    Cambia el propietario de un archivo o directorio solo si el usuario actual tiene permisos de root.
    """
    try:
        usuarios = cargar_usuarios()

        # Verificar si el usuario actual está en el archivo JSON
        if usuario_actual not in usuarios:
            mensaje = f"El usuario {usuario_actual} no existe en el sistema."
            print(mensaje)
            log_error(mensaje)
            return

        # Verifica si el usuario actual tiene privilegios de root
        usuario_uid = pwd.getpwnam(usuario_actual).pw_uid
        if usuario_uid != 0:
            mensaje = f"Solo el administrador (root) puede cambiar el propietario de {path}."
            print(mensaje)
            log_error(mensaje)
            return

        # Verificar si el nuevo usuario existe en el archivo JSON
        if nuevo_usuario not in usuarios:
            mensaje = f"El usuario {nuevo_usuario} no existe en el sistema."
            print(mensaje)
            log_error(mensaje)
            return

        # Obtener UID y GID del nuevo propietario
        uid = pwd.getpwnam(nuevo_usuario).pw_uid
        gid = pwd.getpwnam(nuevo_usuario).pw_gid

        # Cambiar el propietario
        os.chown(path, uid, gid)
        mensaje = f"Propietario de {path} cambiado a {nuevo_usuario}."
        print(mensaje)
        log_action(mensaje)
    except KeyError:
        mensaje = f"El usuario {nuevo_usuario} no existe."
        print(mensaje)
        log_error(mensaje)
    except FileNotFoundError:
        mensaje = f"El archivo o directorio {path} no existe."
        print(mensaje)
        log_error(mensaje)
    except PermissionError:
        mensaje = f"No tienes permisos para cambiar el propietario de {path}."
        print(mensaje)
        log_error(mensaje)
    except Exception as e:
        mensaje = f"Error inesperado al cambiar propietario de {path}: {e}"
        print(mensaje)
        log_error(mensaje)
