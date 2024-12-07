import shutil
import os
from utils import log_action, log_error

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
