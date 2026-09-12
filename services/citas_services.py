from models.cita_model import Cita
from repositories.citas_repository import (
    crear_cita,
    obtener_citas,
    obtener_citas_programadas,
    obtener_cita_por_id,
    obtener_citas_por_usuaria,
    obtener_citas_por_psicologa,
    actualizar_cita,
    eliminar_cita,
)
from services.usuarias_services import service_obtener_usuaria_basico
from repositories.catalogos_repository import (
    obtener_estados_cita
)


def service_crear_cita(cita: Cita) -> dict:
    if not cita.fecha or not cita.fecha.strip():
        return {"success": False, "error": "La fecha es obligatoria."}

    if not cita.usuaria_id:
        return {"success": False, "error": "La usuaria es obligatoria."}

    if not cita.psicologa_id:
        return {"success": False, "error": "La psicóloga es obligatoria."}

    try:
        nuevo_id = crear_cita(cita)
        return {"success": True, "id_cita": nuevo_id}
    except Exception as e:
        return {"success": False, "error": f"Error al crear la cita: {str(e)}"}


def service_obtener_citas() -> list[Cita]:
    try:
        return obtener_citas()
    except Exception as e:
        print(f"[citas_service] Error al obtener citas: {e}")
        return []


def service_obtener_citas_programadas() -> list[Cita]:
    try:
        return obtener_citas_programadas()
    except Exception as e:
        print(f"[citas_service] Error al obtener citas: {e}")
        return []


def service_obtener_cita_por_id(id_cita: int) -> Cita | None:
    if not id_cita:
        return None
    try:
        return obtener_cita_por_id(id_cita)
    except Exception as e:
        print(f"[citas_service] Error al obtener cita {id_cita}: {e}")
        return None


def service_obtener_citas_por_usuaria(usuaria_id: int) -> list[Cita]:
    if not usuaria_id:
        return []
    try:
        return obtener_citas_por_usuaria(usuaria_id)
    except Exception as e:
        print(f"[citas_service] Error al obtener citas de usuaria {usuaria_id}: {e}")
        return []


def service_obtener_citas_por_psicologa(psicologa_id: int) -> list[Cita]:
    if not psicologa_id:
        return []
    try:
        return obtener_citas_por_psicologa(psicologa_id)
    except Exception as e:
        print(f"[citas_service] Error al obtener citas de psicóloga {psicologa_id}: {e}")
        return []


def service_actualizar_cita(cita: Cita) -> dict:
    if not cita.id_cita:
        return {"success": False, "error": "El ID de la cita es requerido."}

    existente = obtener_cita_por_id(cita.id_cita)
    if not existente:
        return {"success": False, "error": f"No se encontró una cita con ID {cita.id_cita}."}

    try:
        filas = actualizar_cita(cita)
        if filas == 0:
            return {"success": False, "error": "No se realizaron cambios."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al actualizar la cita: {str(e)}"}


def service_eliminar_cita(id_cita: int) -> dict:
    if not id_cita:
        return {"success": False, "error": "El ID de la cita es requerido."}

    existente = obtener_cita_por_id(id_cita)
    if not existente:
        return {"success": False, "error": f"No se encontró una cita con ID {id_cita}."}

    try:
        filas = eliminar_cita(id_cita)
        if filas == 0:
            return {"success": False, "error": "No se pudo eliminar la cita."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al eliminar la cita: {str(e)}"}
    
def service_obtener_citas_usuarias():
    try:
        citas = obtener_citas()
        estados_cita_list = obtener_estados_cita()
        citas_usuarias = []
        for c in citas:
            u = service_obtener_usuaria_basico(c.usuaria_id)
            citas_usuarias.append([
                u[0],
                c.fecha,
                u[1],
                c.hora,
                _id_a_texto(estados_cita_list, "id_estado_cita", c.estado_id, "estado_cita"),
                c.id_cita
            ])
        return citas_usuarias
    except Exception as e:
        print(f"[citas_service] Error al obtener citas: {e}")
        return []

def _id_a_texto(lista, attr_id, valor_id, attr_texto) -> str:
    item = next((x for x in lista if getattr(x, attr_id) == valor_id), None)
    return getattr(item, attr_texto) if item else "Sin especificar"