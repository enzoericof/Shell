import crypt
import subprocess
import os
from utils import log_action, log_error

def agregar_usuario(nombre, contrasena, verificar_contrasena, datos_personales, ips_permitidas):
    """
    Agrega un usuario al sistema con una contraseña, datos adicionales y doble verificación de contraseña.
    Registra también las IPs permitidas.
    """
    try:
        # Verificar contraseñas
        if contrasena != verificar_contrasena:
            mensaje = "Error: Las contraseñas no coinciden."
            print(mensaje)
            log_error(mensaje)
            return

        # Crear usuario en el sistema
        subprocess.run(['useradd', '-m', nombre], check=True)

        # Configurar contraseña
        hashed_passwd = crypt.crypt(contrasena)
        subprocess.run(['usermod', '-p', hashed_passwd, nombre], check=True)

        # Crear directorios y archivos si no existen
        user_data_file = "/root/Shell-main/LFS-Shell/users/user_data.txt"
        ips_file = f"/root/Shell-main/{nombre}_ips.txt"

        os.makedirs(os.path.dirname(user_data_file), exist_ok=True)

        # Guardar datos personales
        with open(user_data_file, "a") as file:
            file.write(f"Usuario: {nombre}\nDatos personales: {datos_personales}\n\n")

        # Guardar IPs permitidas
        with open(ips_file, "w") as file:
            file.write("\n".join(ips_permitidas) + "\n")

        mensaje = f"Usuario {nombre} agregado con éxito. IPs permitidas registradas."
        print(mensaje)
        log_action(f"{mensaje} Datos: {datos_personales}, IPs: {ips_permitidas}")

    except subprocess.CalledProcessError as e:
        mensaje = f"Error al agregar usuario {nombre}: {e}"
        print(mensaje)
        log_error(mensaje)
    except Exception as e:
        mensaje = f"Error inesperado al agregar usuario {nombre}: {e}"
        print(mensaje)
        log_error(mensaje)

def cambiar_contrasena(usuario, contrasena_actual, nueva_contrasena, verificar_nueva_contrasena):
    """
    Cambia la contraseña de un usuario con doble verificación y validación de contraseña actual.
    """
    try:
        # Verificar contraseñas nuevas
        if nueva_contrasena != verificar_nueva_contrasena:
            mensaje = "Error: Las nuevas contraseñas no coinciden."
            print(mensaje)
            log_error(mensaje)
            return

        # Verificar contraseña actual (simulado para este entorno)
        resultado = subprocess.run(['passwd', '--status', usuario], capture_output=True, text=True)
        if resultado.returncode != 0 or contrasena_actual not in resultado.stdout:
            mensaje = "Error: Contraseña actual incorrecta o usuario no encontrado."
            print(mensaje)
            log_error(mensaje)
            return

        # Cambiar la contraseña
        hashed_passwd = crypt.crypt(nueva_contrasena)
        subprocess.run(['usermod', '-p', hashed_passwd, usuario], check=True)

        mensaje = f"Contraseña cambiada con éxito para el usuario {usuario}."
        print(mensaje)
        log_action(mensaje)

    except subprocess.CalledProcessError as e:
        mensaje = f"Error al cambiar la contraseña para {usuario}: {e}"
        print(mensaje)
        log_error(mensaje)
    except Exception as e:
        mensaje = f"Error inesperado al cambiar la contraseña para {usuario}: {e}"
        print(mensaje)
        log_error(mensaje)
