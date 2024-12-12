import os
import subprocess
from utils import log_action, log_error

def listar(directorio):
    """
    Lista los contenidos de un directorio.
    """
    try:
        contenidos = os.listdir(directorio)
        log_action(f"Listado de contenidos de {directorio}")

        print(f"Este es el listado de contenidos de {directorio}:")
        for item in contenidos:
            print(f"- {item}")

        return contenidos
    except Exception as e:
        mensaje = f"Error al listar directorio {directorio}: {e}"
        print(mensaje)
        log_error(mensaje)
        return []

def crear_directorio(directorio, usuario):
    """
    Crea un nuevo directorio y cambia su propiedad al usuario especificado.
    """
    try:
        # Crear el directorio
        os.makedirs(directorio, exist_ok=True)
        mensaje = f"Se creó el directorio: {directorio}"
        print(mensaje)
        
        # Cambiar la propiedad del directorio al usuario
        subprocess.run(['chown', f'{usuario}:{usuario}', directorio], check=True)
        print(f"Propiedad cambiada a {usuario} para el directorio: {directorio}")

        log_action(mensaje)
    except Exception as e:
        mensaje = f"Error al crear directorio {directorio}: {e}"
        print(mensaje)
        log_error(mensaje)

def ir(nuevo_directorio):
    """
    Cambia el directorio actual al especificado.
    :param nuevo_directorio: Ruta del directorio al que se desea cambiar.
    """
    try:
        os.chdir(nuevo_directorio)
        mensaje = f"Se cambió al directorio: {os.getcwd()}"
        print(mensaje)
        log_action(mensaje)
    except FileNotFoundError:
        mensaje = f"Error: El directorio '{nuevo_directorio}' no existe."
        print(mensaje)
        log_error(mensaje)
    except PermissionError:
        mensaje = f"Error: No tienes permiso para acceder a '{nuevo_directorio}'."
        print(mensaje)
        log_error(mensaje)
    except Exception as e:
        mensaje = f"Error inesperado: {str(e)}"
        print(mensaje)
        log_error(mensaje)
