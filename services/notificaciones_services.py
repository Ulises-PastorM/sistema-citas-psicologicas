from datetime import datetime
from models.notificacion_model import Notificacion
from repositories.notificaciones_repository import (
    crear_notificacion,
    obtener_notificaciones,
    obtener_notificacion_por_id,
    obtener_notificaciones_por_cita,
    eliminar_notificacion,
)


def service_crear_notificacion(notificacion: Notificacion) -> dict:
    if not notificacion.cita_id:
        return {"success": False, "error": "El ID de la cita es obligatorio."}

    # Si no se pasa fecha_envio, se asigna la fecha y hora actual automáticamente
    if not notificacion.fecha_envio:
        notificacion.fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        nuevo_id = crear_notificacion(notificacion)
        return {"success": True, "id_notificacion": nuevo_id}
    except Exception as e:
        return {"success": False, "error": f"Error al registrar la notificación: {str(e)}"}


def service_registrar_envio_whatsapp(cita_id: int, mensaje: str) -> dict:
    """
    Atajo para registrar en BD que se envió una notificación de WhatsApp.
    Se llama después de un envío exitoso en whatsapp_service.

    Ejemplo de uso:
        resultado = enviar_mensaje_a_usuaria(usuaria, mensaje)
        if resultado["success"]:
            service_registrar_envio_whatsapp(cita_id, mensaje)
    """
    notificacion = Notificacion(
        fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        mensaje     = mensaje,
        cita_id     = cita_id,
    )
    return service_crear_notificacion(notificacion)


def service_obtener_notificaciones() -> list[Notificacion]:
    try:
        return obtener_notificaciones()
    except Exception as e:
        print(f"[notificaciones_service] Error al obtener notificaciones: {e}")
        return []


def service_obtener_notificacion_por_id(id_notificacion: int) -> Notificacion | None:
    if not id_notificacion:
        return None
    try:
        return obtener_notificacion_por_id(id_notificacion)
    except Exception as e:
        print(f"[notificaciones_service] Error al obtener notificación {id_notificacion}: {e}")
        return None


def service_obtener_notificaciones_por_cita(cita_id: int) -> list[Notificacion]:
    if not cita_id:
        return []
    try:
        return obtener_notificaciones_por_cita(cita_id)
    except Exception as e:
        print(f"[notificaciones_service] Error al obtener notificaciones de cita {cita_id}: {e}")
        return []


def service_eliminar_notificacion(id_notificacion: int) -> dict:
    if not id_notificacion:
        return {"success": False, "error": "El ID de la notificación es requerido."}

    existente = obtener_notificacion_por_id(id_notificacion)
    if not existente:
        return {"success": False, "error": f"No se encontró una notificación con ID {id_notificacion}."}

    try:
        filas = eliminar_notificacion(id_notificacion)
        if filas == 0:
            return {"success": False, "error": "No se pudo eliminar la notificación."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al eliminar la notificación: {str(e)}"}