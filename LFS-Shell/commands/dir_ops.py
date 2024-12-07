import os
from utils import log_action, log_error

def listar(directorio):
    """
    Lista los contenidos de un directorio.
    """
    try:
        contenidos = os.listdir(directorio)
        log_action(f"Listados contenidos de {directorio}")

        print(f"Contenido de {directorio}:")
        for item in contenidos:
            print(f"- {item}")

        return contenidos
    except Exception as e:
        mensaje = f"Error al listar directorio {directorio}: {e}"
        print(mensaje)
        log_error(mensaje)
        return []

def crear_directorio(directorio):
    """
    Crea un nuevo directorio.
    """
    try:
        os.makedirs(directorio, exist_ok=True)
        mensaje = f"Creado directorio {directorio}"
        print(mensaje)
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
        mensaje = f"Directorio cambiado a: {os.getcwd()}"
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
