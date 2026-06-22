from models.direccion_model import Direccion
from repositories.direcciones_repository import (
    crear_direccion,
    obtener_direcciones,
    obtener_direccion_por_id,
    actualizar_direccion,
    eliminar_direccion,
)


def service_crear_direccion(direccion: Direccion) -> dict:
    if not direccion.calle_numero or not direccion.calle_numero.strip():
        return {"success": False, "error": "La calle y número son obligatorios."}

    if not direccion.colonia or not direccion.colonia.strip():
        return {"success": False, "error": "La colonia es obligatoria."}

    if not direccion.municipio or not direccion.municipio.strip():
        return {"success": False, "error": "El municipio es obligatorio."}

    try:
        nuevo_id = crear_direccion(direccion)
        return {"success": True, "id_direccion": nuevo_id}
    except Exception as e:
        return {"success": False, "error": f"Error al crear la dirección: {str(e)}"}


def service_obtener_direcciones() -> list[Direccion]:
    try:
        return obtener_direcciones()
    except Exception as e:
        print(f"[direcciones_service] Error al obtener direcciones: {e}")
        return []


def service_obtener_direccion_por_id(id_direccion: int) -> Direccion | None:
    if not id_direccion:
        return None
    try:
        return obtener_direccion_por_id(id_direccion)
    except Exception as e:
        print(f"[direcciones_service] Error al obtener dirección {id_direccion}: {e}")
        return None


def service_actualizar_direccion(direccion: Direccion) -> dict:
    if not direccion.id_direccion:
        return {"success": False, "error": "El ID de la dirección es requerido."}

    if not direccion.calle_numero or not direccion.calle_numero.strip():
        return {"success": False, "error": "La calle y número son obligatorios."}

    existente = obtener_direccion_por_id(direccion.id_direccion)
    if not existente:
        return {"success": False, "error": f"No se encontró una dirección con ID {direccion.id_direccion}."}

    try:
        filas = actualizar_direccion(direccion)
        if filas == 0:
            return {"success": False, "error": "No se realizaron cambios."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al actualizar la dirección: {str(e)}"}


def service_eliminar_direccion(id_direccion: int) -> dict:
    if not id_direccion:
        return {"success": False, "error": "El ID de la dirección es requerido."}

    existente = obtener_direccion_por_id(id_direccion)
    if not existente:
        return {"success": False, "error": f"No se encontró una dirección con ID {id_direccion}."}

    try:
        filas = eliminar_direccion(id_direccion)
        if filas == 0:
            return {"success": False, "error": "No se pudo eliminar la dirección."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al eliminar la dirección: {str(e)}"}