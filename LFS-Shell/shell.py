import os
import sys
import logging
from commands.file_ops import copiar, mover, renombrar
from utils import log_action, log_error

def cambiar_directorio(ruta):
    """
    Cambia el directorio de trabajo actual.
    """
    try:
        os.chdir(ruta)
        log_action(f"Directorio cambiado a {ruta}")
    except Exception as e:
        log_error(f"Error al cambiar directorio: {e}")

def agregar_usuario():
    """
    Agrega un nuevo usuario al sistema.
    """
    try:
        username = input("Ingrese el nombre del usuario: ")
        os.system(f"useradd {username}")
        log_action(f"Usuario {username} agregado al sistema")
    except Exception as e:
        log_error(f"Error al agregar usuario: {e}")

def cambiar_contrasena():
    """
    Cambia la contrasena de un usuario.
    """
    try:
        username = input("Ingrese el nombre del usuario: ")
        os.system(f"passwd {username}")
        log_action(f"Contrasena cambiada para el usuario {username}")
    except Exception as e:
        log_error(f"Error al cambiar contrasena: {e}")

def iniciar_servicio(servicio):
    """
    Inicia un servicio del sistema.
    """
    try:
        os.system(f"systemctl start {servicio}")
        log_action(f"Servicio {servicio} iniciado")
    except Exception as e:
        log_error(f"Error al iniciar servicio {servicio}: {e}")

def detener_servicio(servicio):
    """
    Detiene un servicio del sistema.
    """
    try:
        os.system(f"systemctl stop {servicio}")
        log_action(f"Servicio {servicio} detenido")
    except Exception as e:
        log_error(f"Error al detener servicio {servicio}: {e}")
def main():
    """
    Función principal que procesa los comandos del usuario.
    """
    while True:
        try:
            command = input("Ingrese un comando: ")
            if command in ["salir", "exit"]:
                log_action("Sesión terminada por el usuario")
                break
            elif command.startswith("copiar"):
                _, origen, destino = command.split()
                copiar(origen, destino)
            elif command.startswith("mover"):
                _, origen, destino = command.split()
                mover(origen, destino)
            elif command.startswith("renombrar"):
                _, origen, nuevo_nombre = command.split()
                renombrar(origen, nuevo_nombre)
            elif command.startswith("cd"):
                _, ruta = command.split()
                cambiar_directorio(ruta)
            elif command.startswith("permisos"):
                _, modo, ruta = command.split()
                os.chmod(ruta, int(modo, 8))
                log_action(f"Cambiados permisos de {ruta} a {modo}")
            elif command.startswith("usuario"):
                agregar_usuario()
            elif command.startswith("contrasena"):
                cambiar_contrasena()
            elif command.startswith("servicio"):
                _, accion, servicio = command.split()
                if accion == "iniciar":
                    iniciar_servicio(servicio)
                elif accion == "detener":
                    detener_servicio(servicio)
            else:
                os.system(command)
        except Exception as e:
            log_error(f"Error al procesar el comando: {str(e)}")

if _name_ == "_main_":
    main()