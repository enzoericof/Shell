import subprocess
from utils import log_action, log_error

import dbus

"""
def iniciar_servicio(servicio):
    try:
        bus = dbus.SystemBus()
        systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')
        
        # Importante: Debes asegurar que tu servicio termine con .service
        # Si el usuario ingresa algo como "sshd" deberías agregar el sufijo ".service"
        if not servicio.endswith('.service'):
            servicio += '.service'
        
        # Iniciar el servicio con el modo 'replace'
        manager.StartUnit(servicio, 'replace')
        
        # Aquí puedes loguear la acción
        log_action(f"Servicio {servicio} iniciado")
    except Exception as e:
        # Aquí se registra el error
        log_error(f"Error al iniciar servicio {servicio}: {e}")

def detener_servicio(servicio):
    try:
        bus = dbus.SystemBus()
        systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')
        
        if not servicio.endswith('.service'):
            servicio += '.service'
        
        manager.StopUnit(servicio, 'replace')
        
        # Loguear la acción
        log_action(f"Servicio {servicio} detenido")
    except Exception as e:
        # Loguear el error
        log_error(f"Error al detener servicio {servicio}: {e}")
"""

import dbus

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

