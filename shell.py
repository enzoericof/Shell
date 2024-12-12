"""COMANDOS INICIALES"""

import subprocess
import os
import sys
import pwd
import logging
import socket
import json
from inotify_simple import INotify, flags
from datetime import datetime
from commands.file_ops import copiar, mover, renombrar, cambiar_propietario, cambiar_permisos, validar_permisos, comando_vim, configurar_directorio_usuario, monitorear_directorio
from commands.dir_ops import listar, crear_directorio, ir
from commands.user_ops import agregar_usuario, cambiar_contrasena, validar_acceso,es_ip_permitida, es_horario_permitido, validar_credenciales, solicitar_ips 
from commands.service_ops import iniciar_servicio, detener_servicio
from utils import log_action, log_error, log_horario_fuera_de_rango

LOG_DIR = "/root/Shell-main/LFS-Shell/logs"
USER_DATA_FILE= "/root/Shell-main/LFS-Shell/users/user_data.json"
current_user = None



"""EJECUCION"""

def main():
    session_active = False
    current_user = None


    # Lógica para iniciar sesión con un usuario o crear un usuario nuevo
    while not session_active:
        print("Bienvenido a LFS Shell")
        user_command = input("Para iniciar sesión presione Enter, para registrar un usuario escriba usuario: ").strip()

        # Lógica para crear un usuario nuevo
        if user_command.startswith("usuario"):
            try:
                nombre = input("Nombre de usuario: ").strip().lower()
                contrasena = input("Contraseña: ").strip()
                verificar_contrasena = input("Verificar contraseña: ").strip()
                datos_personales = input("Datos personales: ").strip()
                ips_permitidas = solicitar_ips()
                agregar_usuario(nombre, contrasena, verificar_contrasena, datos_personales, ips_permitidas)
            except Exception as e:
                log_error(f"Error al agregar usuario: {str(e)}")
        
        # Lógica para iniciar sesión con un usuario exitente
        else:
            username = input("Usuario: ").strip().lower()
            password = input("Contraseña: ").strip()

            # Lógica para configurar la sesión del usuario
            if validar_credenciales(username, password):
                session_active = True
                current_user = username
                ip_actual = socket.gethostbyname(socket.gethostname())
                horario_actual = datetime.now().strftime("%H:%M")
                if not es_horario_permitido(username, horario_actual):
                    log_horario_fuera_de_rango(username, ip_actual)
                user_dir = f"/home/{username}"

                # Lógica para configurar directorios del usuario
                if session_active and current_user:
                    monitorear_directorio(current_user, user_dir)
                if not os.path.exists(user_dir):
                    os.makedirs(user_dir)
                os.chdir(user_dir)
                subprocess.run(['chown', f'{username}:{username}', user_dir], check=True)
                subprocess.run(['chmod', 'g+s', user_dir], check=True)
                log_action(f"Usuario {username} inició sesión. IP: {ip_actual}")
                # Cambiar de usuario en un subproceso
                try:
                    user_info = pwd.getpwnam(username)
                    os.setgid(user_info.pw_gid)
                    os.setuid(user_info.pw_uid)
                    os.environ['HOME'] = user_info.pw_dir
                    os.environ['USER'] = user_info.pw_name
                    os.environ['LOGNAME'] = user_info.pw_name
                    os.environ['SHELL'] = user_info.pw_shell
                    os.chdir(user_info.pw_dir)
                except Exception as e:
                    print(f"Error al cambiar de usuario: {e}")
            else:
                print("Credenciales incorrectas. Intente de nuevo.")


    # Lógica de la Shell
    while session_active:
        try:
            command = input(f"{current_user}@lfs-shell> ").strip()
            
            # Lógica para salir
            if command.lower() in ["exit", "quit"]:
                log_action(f"Usuario {current_user} salió de la sesión.")
                print("Adiós!")
                horario_actual = datetime.now().strftime("%H:%M")
                if not es_horario_permitido(username, horario_actual):
                    log_horario_fuera_de_rango(username, ip_actual)
                break

            # A partir de aquí son los llamados a los comandos

            elif command.startswith("copiar"):
                try:
                    _, src, dest = command.split()
                    copiar(src, dest)
                except Exception as e:
                    log_error(f"Error al copiar: {str(e)}")
            
            elif command.startswith("mover"):
                try:
                    _, src, dest = command.split()
                    mover(src, dest)
                except Exception as e:
                    log_error(f"Error al mover: {str(e)}")
            
            elif command.startswith("renombrar"):
                try:
                    _, old_name, new_name = command.split()
                    renombrar(old_name, new_name)
                except Exception as e:
                    log_error(f"Error al renombrar: {str(e)}")
            
            elif command.startswith("listar"):
                try:
                    _, path = command.split()
                    listar(path)
                except Exception as e:
                    log_error(f"Error al listar: {str(e)}")
            
            elif command.startswith("creardir"):
                try:
                    _, path = command.split() 
                    crear_directorio(path, current_user)
                except Exception as e:
                    log_error(f"Error al crear directorio: {str(e)}")

            elif command.startswith("ir"):
                try:
                    _, path = command.split()
                    ir(path)
                except Exception as e:
                    log_error(f"Error al cambiar de directorio: {str(e)}")

            elif command.startswith("propietario"):
                try:
                    args = command.split()
                    if len(args) != 3:
                        print("Error: Formato incorrecto. Usa 'propietario <path> <nuevo_usuario>'.")
                        return
                    _, path, nuevo_usuario = args
                    cambiar_propietario(path, nuevo_usuario, current_user)    
                except FileNotFoundError as e:
                    print(f"Error: {e}")
                except PermissionError as e:
                    print(f"Error: {e}")
                except ValueError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    log_error(f"Error al procesar el comando propietario: {str(e)}")

            elif command.startswith("permisos"):
                try:
                    args = command.split()
                    if len(args) != 3:
                        print("Error: Formato incorrecto. Usa 'permisos <path> <mode>'.")
                        return
                    _, path, mode = args
                    cambiar_permisos(path, mode, current_user)
                except ValueError:
                    print("Error: Formato incorrecto. Usa 'permisos <path> <mode>'.")
                except Exception as e:
                    log_error(f"Error al procesar el comando permisos: {str(e)}")
            elif command.startswith("usuario"):
                try:
                    nombre = input("Nombre de usuario: ").strip().lower()
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
                try:
                    _, action, service_name = command.split()
                    if action == "iniciar":
                        iniciar_servicio(service_name)
                    elif action == "detener":
                        detener_servicio(service_name)
                    else:
                        print("Error: Acción desconocida. Usa 'servicio iniciar|detener <service_name>'.")
                except ValueError:
                    print("Error: Formato incorrecto. Usa 'servicio iniciar|detener <service_name>'.")
                except Exception as e:
                    log_error(f"Error al manejar servicio: {str(e)}")
            else:
                os.system(command)
        except Exception as e:
            log_error(f"Error al ejecutar el comando: {str(e)}")

if __name__ == "__main__":
    main()

