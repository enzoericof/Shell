import crypt
import subprocess
from utils import log_action, log_error

def agregar_usuario(nombre, contrasena, datos_personales):
    """
    Agrega un usuario al sistema con una contraseña y datos adicionales.
    """
    try:
        # Crear usuario en el sistema
        subprocess.run(['useradd', '-m', nombre], check=True)
        # Configurar contraseña
        hashed_passwd = crypt.crypt(contrasena)
        subprocess.run(['usermod', '-p', hashed_passwd, nombre], check=True)
        log_action(f"Usuario {nombre} agregado con datos: {datos_personales}")
    except Exception as e:
        log_error(f"Error al agregar usuario {nombre}: {e}")

def cambiar_contrasena(usuario, nueva_contrasena):
    """
    Cambia la contraseña de un usuario.
    """
    try:
        hashed_passwd = crypt.crypt(nueva_contrasena)
        subprocess.run(['usermod', '-p', hashed_passwd, usuario], check=True)
        log_action(f"Cambiada contraseña para el usuario {usuario}")
    except Exception as e:
        log_error(f"Error al cambiar contraseña de {usuario}: {e}")
