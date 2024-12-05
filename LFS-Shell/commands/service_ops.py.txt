import subprocess
from utils import log_action, log_error

def iniciar_servicio(servicio):
    """
    Inicia un demonio del sistema.
    """
    try:
        subprocess.run(['systemctl', 'start', servicio], check=True)
        log_action(f"Servicio {servicio} iniciado")
    except Exception as e:
        log_error(f"Error al iniciar servicio {servicio}: {e}")

def detener_servicio(servicio):
    """
    Detiene un demonio del sistema.
    """
    try:
        subprocess.run(['systemctl', 'stop', servicio], check=True)
        log_action(f"Servicio {servicio} detenido")
    except Exception as e:
        log_error(f"Error al detener servicio {servicio}: {e}")
