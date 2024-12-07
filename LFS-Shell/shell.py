shell.py
import os
import sys
import logging
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
                agregar_usuario()
            elif command.startswith("contraseña"):
                cambiar_contrasena()
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
if _name_ == "_main_":
    main()