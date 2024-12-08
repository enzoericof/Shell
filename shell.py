import os
import sys
import logging
import json
from commands.file_ops import copiar, mover, renombrar
from commands.dir_ops import listar, crear_directorio, ir
from commands.user_ops import agregar_usuario, cambiar_contrasena
from commands.service_ops import iniciar_servicio, detener_servicio
from utils import log_action, log_error

LOG_DIR = "/root/Shell-main/LFS-Shell/logs"

# Configurar logging
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
logging.basicConfig(
    filename=f"{LOG_DIR}/shell.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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

def main():
    print("Bienvenido a LFS Shell")
    while True:
        try:
            command = input("shell> ").strip()
            if command.lower() in ["exit", "quit"]:
                log_action("Usuario salió de la sesión.")
                print("Adiós!")
                break
            elif command.startswith("copiar"):
                _, src, dest = command.split()
                copiar(src, dest)
            elif command.startswith("mover"):
                _, src, dest = command.split()
                mover(src, dest)
            elif command.startswith("renombrar"):
                _, old_name, new_name = command.split()
                renombrar(old_name, new_name)
            elif command.startswith("listar"):
                _, path = command.split()
                listar(path)
            elif command.startswith("creardir"):
                _, path = command.split()
                crear_directorio(path)
            elif command.startswith("ir"):
                _, path = command.split()
                ir(path)
            elif command.startswith("permisos"):
                _, mode, path = command.split()
                os.chmod(path, int(mode, 8))
                log_action(f"Cambiados permisos de {path} a {mode}")
            elif command.startswith("usuario"):
                 try:
                     nombre = input("Nombre de usuario: ").strip()
                     contrasena = input("Contraseña: ").strip()
                     verificar_contrasena = input("Verificar contraseña: ").strip()
                     datos_personales = input("Datos personales: ").strip()
                     ips_permitidas = input("IPs permitidas (separadas por comas): ").strip().split(",")
                     agregar_usuario(nombre, contrasena, verificar_contrasena, datos_personales, ips_permitidas)
                 except Exception as e:
                     log_error(f"Error al agregar usuario: {str(e)}")
            elif command.startswith("contraseña"):
                 try:
                     usuario = input("Nombre de usuario: ").strip()
                     contrasena_actual = input("Contraseña actual: ").strip()
                     nueva_contrasena = input("Nueva contraseña: ").strip()
                     verificar_nueva_contrasena = input("Verificar nueva contraseña: ").strip()
                     cambiar_contrasena(usuario, contrasena_actual, nueva_contrasena, verificar_nueva_contrasena)
                 except Exception as e:
                     log_error(f"Error al cambiar contraseña: {str(e)}")
            elif command.startswith("servicio"):
                _, action, service_name = command.split()
                if action == "iniciar":
                    iniciar_servicio(service_name)
                elif action == "detener":
                    detener_servicio(service_name)
            else:
                os.system(command)
        except Exception as e:
            log_error(f"Error al procesar el comando: {str(e)}")

if __name__ == "__main__":
    main()
