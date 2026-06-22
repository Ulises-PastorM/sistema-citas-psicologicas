from models.usuaria_model import Usuaria
from repositories.usuarias_repository import (
    crear_usuaria,
    obtener_usuarias,
    obtener_usuaria_por_id,
    actualizar_usuaria,
    eliminar_usuaria,
)


# Crear
def service_crear_usuaria(usuaria: Usuaria) -> dict:
    """
    Valida los datos y crea una nueva usuaria.

    Returns:
        { "success": True } o { "success": False, "error": "..." }
    """
    # Validaciones básicas
    if not usuaria.nombre or not usuaria.nombre.strip():
        return {"success": False, "error": "El nombre es obligatorio."}

    if not usuaria.telefono or not usuaria.telefono.strip():
        return {"success": False, "error": "El teléfono es obligatorio."}

    if not usuaria.telefono_limpio().isdigit():
        return {"success": False, "error": "El teléfono solo debe contener dígitos."}

    if not usuaria.estatus_id:
        return {"success": False, "error": "El estatus es obligatorio."}

    try:
        crear_usuaria(usuaria)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al crear la usuaria: {str(e)}"}


# Obtener usuarias
def service_obtener_usuarias() -> list[Usuaria]:
    """
    Devuelve la lista de todas las usuarias.

    Returns:
        Lista de dicts con los datos de cada usuaria.
        Lista vacía si no hay registros o si ocurre un error.
    """
    try:
        return obtener_usuarias()
    except Exception as e:
        print(f"[usuarias_service] Error al obtener usuarias: {e}")
        return []


# Obtener usuaria por id
def service_obtener_usuaria_por_id(id_usuaria) -> dict | None:
    """
    Busca una usuaria por su ID.

    Returns:
        Dict con los datos de la usuaria, o None si no existe.
    """
    if not id_usuaria:
        return None

    try:
        return obtener_usuaria_por_id(id_usuaria)
    except Exception as e:
        print(f"[usuarias_service] Error al obtener usuaria {id_usuaria}: {e}")
        return None


# Actualizar usuaria por id
def service_actualizar_usuaria(usuaria: Usuaria) -> dict:
    """
    Valida y actualiza los datos de una usuaria existente.

    Returns:
        { "success": True } o { "success": False, "error": "..." }
    """
    if not usuaria.id_usuaria:
        return {"success": False, "error": "El ID de la usuaria es requerido."}

    if not usuaria.nombre or not usuaria.nombre.strip():
        return {"success": False, "error": "El nombre es obligatorio."}

    if not usuaria.telefono or not usuaria.telefono.strip():
        return {"success": False, "error": "El teléfono es obligatorio."}

    if not usuaria.telefono_limpio().isdigit():
        return {"success": False, "error": "El teléfono solo debe contener dígitos."}

    # Verificar que la usuaria existe antes de actualizar
    existente = obtener_usuaria_por_id(usuaria.id_usuaria)
    if not existente:
        return {"success": False, "error": f"No se encontró una usuaria con ID {usuaria.id_usuaria}."}

    try:
        filas = actualizar_usuaria(usuaria)
        if filas == 0:
            return {"success": False, "error": "No se realizaron cambios."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al actualizar la usuaria: {str(e)}"}


# Eliminar usuaria
def service_eliminar_usuaria(id_usuaria) -> dict:
    """
    Elimina una usuaria por su ID.

    Returns:
        { "success": True } o { "success": False, "error": "..." }
    """
    if not id_usuaria:
        return {"success": False, "error": "El ID de la usuaria es requerido."}

    existente = obtener_usuaria_por_id(id_usuaria)
    if not existente:
        return {"success": False, "error": f"No se encontró una usuaria con ID {id_usuaria}."}

    try:
        filas = eliminar_usuaria(id_usuaria)
        if filas == 0:
            return {"success": False, "error": "No se pudo eliminar la usuaria."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al eliminar la usuaria: {str(e)}"}
