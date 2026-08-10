from models.agresor_model import Agresor
from repositories.agresores_repository import (
    crear_agresor,
    obtener_agresores,
    obtener_agresor_por_id,
    actualizar_agresor,
    eliminar_agresor,
    vincular_usuaria_agresor,
    desvincular_usuaria_agresor,
    obtener_agresores_de_usuaria,
    obtener_usuarias_de_agresor,
    eliminar_vinculos_de_usuaria,
)


def service_crear_agresor(agresor: Agresor) -> dict:
    if not agresor.nombre_agresor or not agresor.nombre_agresor.strip():
        return {"success": False, "error": "El nombre del agresor es obligatorio."}

    try:
        nuevo_id = crear_agresor(agresor)
        return {"success": True, "id_agresor": nuevo_id}
    except Exception as e:
        return {"success": False, "error": f"Error al crear el agresor: {str(e)}"}


def service_obtener_agresores() -> list[Agresor]:
    try:
        return obtener_agresores()
    except Exception as e:
        print(f"[agresores_service] Error al obtener agresores: {e}")
        return []


def service_obtener_agresor_por_id(id_agresor: int) -> Agresor | None:
    if not id_agresor:
        return None
    try:
        return obtener_agresor_por_id(id_agresor)
    except Exception as e:
        print(f"[agresores_service] Error al obtener agresor {id_agresor}: {e}")
        return None


def service_actualizar_agresor(agresor: Agresor) -> dict:
    if not agresor.id_agresor:
        return {"success": False, "error": "El ID del agresor es requerido."}

    if not agresor.nombre_agresor or not agresor.nombre_agresor.strip():
        return {"success": False, "error": "El nombre del agresor es obligatorio."}

    existente = obtener_agresor_por_id(agresor.id_agresor)
    if not existente:
        return {"success": False, "error": f"No se encontró un agresor con ID {agresor.id_agresor}."}

    try:
        filas = actualizar_agresor(agresor)
        if filas == 0:
            return {"success": False, "error": "No se realizaron cambios."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al actualizar el agresor: {str(e)}"}


def service_eliminar_agresor(id_agresor: int) -> dict:
    if not id_agresor:
        return {"success": False, "error": "El ID del agresor es requerido."}

    existente = obtener_agresor_por_id(id_agresor)
    if not existente:
        return {"success": False, "error": f"No se encontró un agresor con ID {id_agresor}."}

    try:
        eliminar_agresor(id_agresor)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al eliminar el agresor: {str(e)}"}


# ─── Vínculos usuaria ↔ agresor ───────────────────────────────────────────────

def service_vincular_usuaria_agresor(usuaria_id: int, agresor_id: int) -> dict:
    if not usuaria_id or not agresor_id:
        return {"success": False, "error": "usuaria_id y agresor_id son obligatorios."}

    try:
        vincular_usuaria_agresor(usuaria_id, agresor_id)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al vincular: {str(e)}"}


def service_crear_y_vincular_agresor(usuaria_id: int, agresor: Agresor) -> dict:
    """
    Atajo para crear un agresor nuevo y vincularlo a una usuaria en un solo paso.
    Uso típico: formulario de registro donde se capturan datos del agresor.
    """
    resultado = service_crear_agresor(agresor)
    if not resultado["success"]:
        return resultado

    id_agresor = resultado["id_agresor"]
    vinculo    = service_vincular_usuaria_agresor(usuaria_id, id_agresor)
    if not vinculo["success"]:
        return vinculo

    return {"success": True, "id_agresor": id_agresor}


def service_desvincular_usuaria_agresor(usuaria_id: int, agresor_id: int) -> dict:
    if not usuaria_id or not agresor_id:
        return {"success": False, "error": "usuaria_id y agresor_id son obligatorios."}

    try:
        filas = desvincular_usuaria_agresor(usuaria_id, agresor_id)
        if filas == 0:
            return {"success": False, "error": "No se encontró el vínculo."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al desvincular: {str(e)}"}


def service_obtener_agresores_de_usuaria(usuaria_id: int) -> list[Agresor]:
    if not usuaria_id:
        return []
    try:
        return obtener_agresores_de_usuaria(usuaria_id)
    except Exception as e:
        print(f"[agresores_service] Error al obtener agresores de usuaria {usuaria_id}: {e}")
        return []


def service_eliminar_vinculos_de_usuaria(usuaria_id: int) -> dict:
    """Limpia todos los vínculos de una usuaria. Llamar antes de eliminar la usuaria."""
    if not usuaria_id:
        return {"success": False, "error": "El ID de la usuaria es requerido."}
    try:
        eliminar_vinculos_de_usuaria(usuaria_id)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al eliminar vínculos: {str(e)}"}