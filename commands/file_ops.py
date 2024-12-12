import shutil
import os
import argparse
from utils import log_action, log_error
import pwd
import grp
import subprocess
import json

USERS_JSON_PATH = '/root/Shell-main/LFS-Shell/users/user_data.json'

# Copia y pega un archivo desde origen a destino
def copiar(origen, destino):
    try:
        shutil.copy2(origen, destino)
        mensaje = f"Se copió archivo de {origen} a {destino}"
        print(mensaje)
        log_action(mensaje)
    except Exception as e:
        mensaje = f"Error al copiar archivo: {e}"
        print(mensaje)
        log_error(mensaje)

# Mueve un archivo desde origen a destino
def mover(origen, destino):
    try:
        shutil.move(origen, destino)
        mensaje = f"Se movió el archivo de {origen} a {destino}"
        print(mensaje)
        log_action(mensaje)
    except Exception as e:
        mensaje = f"Error al mover archivo: {e}"
        print(mensaje)
        log_error(mensaje)

# Renombra un archivo o directorio
def renombrar(origen, nuevo_nombre):
    try:
        os.rename(origen, nuevo_nombre)
        mensaje = f"Se renombró {origen} a {nuevo_nombre}"
        print(mensaje)
        log_action(mensaje)
    except Exception as e:
        mensaje = f"Error al renombrar: {e}"
        print(mensaje)
        log_error(mensaje)

# Busca datos de usuarios de un Json
def cargar_usuarios():
    try:
        with open('/root/Shell-main/LFS-Shell/users/user_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("El archivo de usuarios no se encontró.")
        return {}
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON de usuarios.")
        return {}

# Cambia permisos de archivos
def cambiar_permisos(path, mode, usuario_actual):
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo o directorio '{path}' no existe.")
        # Obtener propietario y grupo del archivo
        detalles = subprocess.check_output(['ls', '-ld', path]).decode().split()
        propietario = detalles[2]
        grupo = detalles[3]
        # Verificar si el usuario pertenece al grupo
        grupos_usuario = [g.gr_name for g in grp.getgrall() if usuario_actual in g.gr_mem]
        # Verificar permisos para cambiar el archivo
        if usuario_actual != propietario and grupo not in grupos_usuario and usuario_actual != 'root':
            raise PermissionError(f"El usuario '{usuario_actual}' no tiene permisos para cambiar los permisos de '{path}'.")
        # Validar el modo
        if not mode.isdigit() or len(mode) != 3:
            raise ValueError("El modo de permisos debe ser un número octal de tres dígitos.")
        # Cambiar los permisos
        mode_octal = int(mode, 8)
        os.chmod(path, mode_octal)
        print(f"Permisos del archivo o directorio '{path}' cambiados a {mode}.")
    except Exception as e:
        print(f"Error al cambiar los permisos: {e}")

# Cambia el propietario de un archivo o directorio
def cambiar_propietario(path, nuevo_usuario, usuario_actual):
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo o directorio '{path}' no existe.")
        # Obtener propietario y grupo del archivo
        detalles = subprocess.check_output(['ls', '-ld', path]).decode().split()
        propietario_actual = detalles[2]
        grupo = detalles[3]
        # Verificar si el usuario actual es el propietario o pertenece al grupo
        grupos_usuario = [g.gr_name for g in grp.getgrall() if usuario_actual in g.gr_mem]
        if usuario_actual != propietario_actual and grupo not in grupos_usuario and usuario_actual != 'root':
            raise PermissionError(f"El usuario '{usuario_actual}' no puede cambiar el propietario de '{path}'.")
        # Verificar si el nuevo propietario existe
        try:
            subprocess.run(['id', nuevo_usuario], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            raise ValueError(f"El nuevo propietario '{nuevo_usuario}' no existe en el sistema.")
        # Cambiar el propietario
        subprocess.run(['chown', nuevo_usuario, path], check=True)
        print(f"Propietario del archivo '{path}' cambiado a '{nuevo_usuario}'.")
    except Exception as e:
        print(f"Error al cambiar el propietario: {e}")

# Funcion no utilizada
def validar_permisos(path, accion):
    """Verifica si el usuario actual tiene permisos para realizar una acción específica en un archivo o directorio."""
    acciones = {
        'lectura': os.R_OK,
        'escritura': os.W_OK,
        'ejecucion': os.X_OK
    }
    if accion not in acciones:
        raise ValueError(f"Acción no válida: {accion}")
    # Verifica permisos usando os.access
    if not os.access(path, acciones[accion]):
        mensaje = f"El usuario {current_user} no tiene permisos de {accion} sobre {path}."
        print(mensaje)
        return False
    return True


# Función para el comando vim
def comando_vim(path):
    """Simula el comando vim para editar un archivo."""
    try:
        if validar_permisos(path, 'escritura'):
            print(f"Se está editando {path}.")
            # Aquí puedes simular la edición real o registrar la operación
        else:
            print(f"No tienes permisos para editar {path}.")
    except Exception as e:
        print(f"Error al intentar editar {path}: {str(e)}")

# Funcion para configurar directorios
def configurar_directorio_usuario(usuario):
    home_dir = f"/home/{usuario}"
    try:
        # Asegurar que el bit setgid esté habilitado para heredar grupo
        subprocess.run(['chmod', 'g+s', home_dir], check=True)
        # Configurar ACLs predeterminadas para heredar permisos
        subprocess.run(['setfacl', '-d', '-m', f'u:{usuario}:rwx', home_dir], check=True)
        subprocess.run(['setfacl', '-d', '-m', 'g::rwx', home_dir], check=True)
        subprocess.run(['setfacl', '-d', '-m', 'o::rx', home_dir], check=True)
        # Crear un hook para corregir propietarios automáticamente
        hook_script = f"""
#!/bin/bash
chown {usuario}:{usuario} "$@"
"""
        hook_path = "/usr/local/bin/correct_owner"
        with open(hook_path, "w") as hook_file:
            hook_file.write(hook_script)
        
        # Hacer el hook ejecutable
        subprocess.run(['chmod', '+x', hook_path], check=True)
        print(f"Configuración completada para futuros archivos en {home_dir}.")
    except subprocess.CalledProcessError as e:
        print(f"Error al configurar el directorio para {usuario}: {e}")

# Funcion de configuración de directorios
def monitorear_directorio(usuario, directorio):
    home_dir = f"/home/{usuario}"
    
    try:
        # Verificar que el directorio existe
        if not os.path.exists(home_dir):
            raise FileNotFoundError(f"El directorio {home_dir} no existe.")
        
        print(f"Configurando directorio {home_dir} para el usuario {usuario}...")
        
        # Cambiar el propietario del directorio al usuario
        subprocess.run(['chown', usuario, home_dir], check=True)
        print(f"Propietario del directorio cambiado a {usuario}.")
        
        # Configurar permisos del directorio
        subprocess.run(['chmod', '700', home_dir], check=True)
        print("Permisos configurados correctamente (solo usuario tiene acceso completo).")
        
        print(f"Configuración completada para futuros archivos en {home_dir}.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar un comando: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
