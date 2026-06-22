from models.sesion_model import Sesion
from repositories.sesiones_repository import (
    crear_sesion,
    obtener_sesiones,
    obtener_sesion_por_id,
    obtener_sesiones_por_cita,
    actualizar_sesion,
    eliminar_sesion,
)


def service_crear_sesion(sesion: Sesion) -> dict:
    if not sesion.cita_id:
        return {"success": False, "error": "El ID de la cita es obligatorio."}

    try:
        nuevo_id = crear_sesion(sesion)
        return {"success": True, "id_sesion": nuevo_id}
    except Exception as e:
        return {"success": False, "error": f"Error al crear la sesión: {str(e)}"}


def service_obtener_sesiones() -> list[Sesion]:
    try:
        return obtener_sesiones()
    except Exception as e:
        print(f"[sesiones_service] Error al obtener sesiones: {e}")
        return []


def service_obtener_sesion_por_id(id_sesion: int) -> Sesion | None:
    if not id_sesion:
        return None
    try:
        return obtener_sesion_por_id(id_sesion)
    except Exception as e:
        print(f"[sesiones_service] Error al obtener sesión {id_sesion}: {e}")
        return None


def service_obtener_sesiones_por_cita(cita_id: int) -> list[Sesion]:
    if not cita_id:
        return []
    try:
        return obtener_sesiones_por_cita(cita_id)
    except Exception as e:
        print(f"[sesiones_service] Error al obtener sesiones de cita {cita_id}: {e}")
        return []


def service_actualizar_sesion(sesion: Sesion) -> dict:
    if not sesion.id_sesion:
        return {"success": False, "error": "El ID de la sesión es requerido."}

    existente = obtener_sesion_por_id(sesion.id_sesion)
    if not existente:
        return {"success": False, "error": f"No se encontró una sesión con ID {sesion.id_sesion}."}

    try:
        filas = actualizar_sesion(sesion)
        if filas == 0:
            return {"success": False, "error": "No se realizaron cambios."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al actualizar la sesión: {str(e)}"}


def service_eliminar_sesion(id_sesion: int) -> dict:
    if not id_sesion:
        return {"success": False, "error": "El ID de la sesión es requerido."}

    existente = obtener_sesion_por_id(id_sesion)
    if not existente:
        return {"success": False, "error": f"No se encontró una sesión con ID {id_sesion}."}

    try:
        filas = eliminar_sesion(id_sesion)
        if filas == 0:
            return {"success": False, "error": "No se pudo eliminar la sesión."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al eliminar la sesión: {str(e)}"}