import os
from utils import log_action, log_error

def listar(directorio):
    """
    Lista los contenidos de un directorio.
    """
    try:
        contenidos = os.listdir(directorio)
        log_action(f"Listados contenidos de {directorio}")
        return contenidos
    except Exception as e:
        log_error(f"Error al listar directorio {directorio}: {e}")
        return []

def crear_directorio(directorio):
    """
    Crea un nuevo directorio.
    """
    try:
        os.makedirs(directorio, exist_ok=True)
        log_action(f"Creado directorio {directorio}")
    except Exception as e:
        log_error(f"Error al crear directorio {directorio}: {e}")
