from models.psicologa_model import Psicologa
from repositories.psicologas_repository import (
    crear_psicologa,
    obtener_psicologas,
    obtener_psicologa_por_id,
    obtener_psicologas_activas,
    actualizar_psicologa,
    eliminar_psicologa,
)


def service_crear_psicologa(psicologa: Psicologa) -> dict:
    if not psicologa.nombre or not psicologa.nombre.strip():
        return {"success": False, "error": "El nombre es obligatorio."}

    try:
        nuevo_id = crear_psicologa(psicologa)
        return {"success": True, "id_psicologas": nuevo_id}
    except Exception as e:
        return {"success": False, "error": f"Error al crear la psicóloga: {str(e)}"}


def service_obtener_psicologas() -> list[Psicologa]:
    try:
        return obtener_psicologas()
    except Exception as e:
        print(f"[psicologas_service] Error al obtener psicólogas: {e}")
        return []


def service_obtener_psicologa_por_id(id_psicologas: int) -> Psicologa | None:
    if not id_psicologas:
        return None
    try:
        return obtener_psicologa_por_id(id_psicologas)
    except Exception as e:
        print(f"[psicologas_service] Error al obtener psicóloga {id_psicologas}: {e}")
        return None


def service_obtener_psicologas_activas() -> list[Psicologa]:
    try:
        return obtener_psicologas_activas()
    except Exception as e:
        print(f"[psicologas_service] Error al obtener psicólogas activas: {e}")
        return []


def service_actualizar_psicologa(psicologa: Psicologa) -> dict:
    if not psicologa.id_psicologas:
        return {"success": False, "error": "El ID de la psicóloga es requerido."}

    if not psicologa.nombre or not psicologa.nombre.strip():
        return {"success": False, "error": "El nombre es obligatorio."}

    existente = obtener_psicologa_por_id(psicologa.id_psicologas)
    if not existente:
        return {"success": False, "error": f"No se encontró una psicóloga con ID {psicologa.id_psicologas}."}

    try:
        filas = actualizar_psicologa(psicologa)
        if filas == 0:
            return {"success": False, "error": "No se realizaron cambios."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al actualizar la psicóloga: {str(e)}"}


def service_eliminar_psicologa(id_psicologas: int) -> dict:
    if not id_psicologas:
        return {"success": False, "error": "El ID de la psicóloga es requerido."}

    existente = obtener_psicologa_por_id(id_psicologas)
    if not existente:
        return {"success": False, "error": f"No se encontró una psicóloga con ID {id_psicologas}."}

    try:
        filas = eliminar_psicologa(id_psicologas)
        if filas == 0:
            return {"success": False, "error": "No se pudo eliminar la psicóloga."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al eliminar la psicóloga: {str(e)}"}