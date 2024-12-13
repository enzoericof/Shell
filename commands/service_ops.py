import subprocess
from utils import log_action, log_error, log_transferencia
from datetime import datetime
import dbus

# Inicia demonios
def iniciar_servicio(servicio):
    """
    Inicia un servicio del sistema mediante D-Bus en systemd.
    """
    try:
        # Conexión al bus del sistema
        bus = dbus.SystemBus()
        systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')
        # Asegurar que el nombre del servicio termine en .service
        if not servicio.endswith('.service'):
            servicio += '.service'
        # Iniciar el servicio en modo 'replace'
        manager.StartUnit(servicio, 'replace')
        # Loguear la acción
        log_action(f"Servicio {servicio} iniciado correctamente.")
    except dbus.DBusException as e:
        # Manejar errores específicos de D-Bus
        log_error(f"Error de D-Bus al iniciar servicio {servicio}: {e.get_dbus_message()}")
    except Exception as e:
        # Manejar cualquier otro tipo de error
        log_error(f"Error desconocido al iniciar servicio {servicio}: {e}")

# Detiene demonios
def detener_servicio(servicio):
    """
    Detiene un servicio del sistema mediante D-Bus en systemd.
    """
    try:
        # Conexión al bus del sistema
        bus = dbus.SystemBus()
        systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')

        # Asegurar que el nombre del servicio termine en .service
        if not servicio.endswith('.service'):
            servicio += '.service'

        # Detener el servicio en modo 'replace'
        manager.StopUnit(servicio, 'replace')

        # Loguear la acción
        log_action(f"Servicio {servicio} detenido correctamente.")
    except dbus.DBusException as e:
        # Manejar errores específicos de D-Bus
        log_error(f"Error de D-Bus al detener servicio {servicio}: {e.get_dbus_message()}")
    except Exception as e:
        # Manejar cualquier otro tipo de error
        log_error(f"Error desconocido al detener servicio {servicio}: {e}")

# Función para realizar una transferencia SCP
def transferencia_scp(archivo_origen, servidor_destino, archivo_destino):
    """
    Realiza una transferencia SCP y utiliza el log_transferencia para registrar la operación.
    """
    try:
        # Comando para transferencia SCP
        comando = f"scp {archivo_origen} {servidor_destino}:{archivo_destino}"
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)

        if resultado.returncode == 0:
            log_transferencia("scp", archivo_origen, f"{servidor_destino}:{archivo_destino}")
            log_action(f"Transferencia SCP exitosa - Archivo: {archivo_origen}, Destino: {servidor_destino}:{archivo_destino}")
        else:
            log_error(f"Transferencia SCP fallida - Archivo: {archivo_origen}, Destino: {servidor_destino}:{archivo_destino} - Error: {resultado.stderr}")
    except Exception as e:
        log_error(f"Excepción durante transferencia SCP: {str(e)}")
