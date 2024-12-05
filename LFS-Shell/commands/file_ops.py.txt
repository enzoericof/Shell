import shutil
import os
from utils import log_action, log_error

def copiar(origen, destino):
    """
    Copia un archivo desde 'origen' a 'destino'.
    """
    try:
        shutil.copy2(origen, destino)
        log_action(f"Copiado archivo de {origen} a {destino}")
    except Exception as e:
        log_error(f"Error al copiar archivo: {e}")

def mover(origen, destino):
    """
    Mueve un archivo desde 'origen' a 'destino'.
    """
    try:
        shutil.move(origen, destino)
        log_action(f"Movido archivo de {origen} a {destino}")
    except Exception as e:
        log_error(f"Error al mover archivo: {e}")

def renombrar(origen, nuevo_nombre):
    """
    Renombra un archivo o directorio.
    """
    try:
        os.rename(origen, nuevo_nombre)
        log_action(f"Renombrado {origen} a {nuevo_nombre}")
    except Exception as e:
        log_error(f"Error al renombrar: {e}")
