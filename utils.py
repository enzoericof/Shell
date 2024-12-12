import os
import logging
from datetime import datetime

# Directorios de logs
LOG_DIR = "/var/log/shell"
LOG_ERROR = f"{LOG_DIR}/sistema_error.log"
LOG_HORARIOS = f"{LOG_DIR}/usuario_horarios_log.log"
LOG_TRANSFERENCIAS = f"{LOG_DIR}/shell_transferencias.log"

# Configuración inicial de logs
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configuración de logging principal
logging.basicConfig(
    filename=f"{LOG_DIR}/shell.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Logs normales
def log_action(message):
    """
    Registra acciones normales del shell en el log principal.
    """
    logging.info(message)

# Logs de errores
def log_error(message):
    """
    Registra errores en el archivo sistema_error.log y también en el log principal.
    """
    logging.error(message)
    with open(LOG_ERROR, "a") as error_log:
        error_log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR - {message}\n")

# Logs cuando un usuario ingresa fuera de sus horarios permitidos
def log_horario_fuera_de_rango(usuario, ip):
    """
    Registra accesos fuera del horario permitido en el log usuario_horarios_log.log.
    """
    with open(LOG_HORARIOS, "a") as horario_log:
        horario_log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - FUERA DE HORARIO - Usuario: {usuario}, IP: {ip}\n")

# Logs cuando ocurren transferencias
def log_transferencia(tipo, archivo, destino):
    """
    Registra transferencias (ftp/scp) en el archivo shell_transferencias.log.
    """
    with open(LOG_TRANSFERENCIAS, "a") as transferencia_log:
        transferencia_log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {tipo.upper()} - Archivo: {archivo}, Destino: {destino}\n")
