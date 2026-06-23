import hashlib
from models.usuario_sistema_model import UsuarioSistema
from repositories.usuarios_sistema_repository import (
    crear_usuario,
    obtener_usuarios,
    obtener_usuario_por_id,
    obtener_usuario_por_nombre,
    actualizar_usuario,
    eliminar_usuario,
)


# Utilidad de contraseña
def _hashear(contrasena: str) -> str:
    """Devuelve el SHA-256 de la contraseña en hexadecimal."""
    return hashlib.sha256(contrasena.encode()).hexdigest()


# Autenticación
def service_login(nombre: str, contrasena: str) -> dict:
    """
    Valida las credenciales de un usuario.

    Returns:
        { "success": True, "usuario": UsuarioSistema } si las credenciales son correctas.
        { "success": False, "error": "..." }            si no lo son.
    """
    if not nombre or not contrasena:
        return {"success": False, "error": "Usuario y contraseña son obligatorios."}

    usuario = obtener_usuario_por_nombre(nombre.strip())

    if not usuario:
        return {"success": False, "error": "Usuario o contraseña incorrectos."}

    if usuario.activa != 1:
        return {"success": False, "error": "Esta cuenta está desactivada."}

    if usuario.contrasena != _hashear(contrasena):
        return {"success": False, "error": "Usuario o contraseña incorrectos."}

    return {"success": True, "usuario": usuario}


# CRUD 

def service_crear_usuario(nombre: str, contrasena: str, rol_id: int, activa: int = 1) -> dict:
    """
    Crea un nuevo usuario hasheando la contraseña antes de guardarla.

    Returns:
        { "success": True, "id_usuario": int } o { "success": False, "error": "..." }
    """
    if not nombre or not nombre.strip():
        return {"success": False, "error": "El nombre es obligatorio."}

    if not contrasena or len(contrasena) < 6:
        return {"success": False, "error": "La contraseña debe tener al menos 6 caracteres."}

    if not rol_id:
        return {"success": False, "error": "El rol es obligatorio."}

    # Verificar que no exista otro usuario con el mismo nombre
    existente = obtener_usuario_por_nombre(nombre.strip())
    if existente:
        return {"success": False, "error": f"Ya existe un usuario con el nombre '{nombre}'."}

    usuario = UsuarioSistema(
        nombre     = nombre.strip(),
        contrasena = _hashear(contrasena),
        rol_id     = rol_id,
        activa     = activa,
    )

    try:
        nuevo_id = crear_usuario(usuario)
        return {"success": True, "id_usuario": nuevo_id}
    except Exception as e:
        return {"success": False, "error": f"Error al crear el usuario: {str(e)}"}


def service_obtener_usuarios() -> list[UsuarioSistema]:
    try:
        return obtener_usuarios()
    except Exception as e:
        print(f"[usuarios_sistema_service] Error al obtener usuarios: {e}")
        return []


def service_obtener_usuario_por_id(id_usuario: int) -> UsuarioSistema | None:
    if not id_usuario:
        return None
    try:
        return obtener_usuario_por_id(id_usuario)
    except Exception as e:
        print(f"[usuarios_sistema_service] Error al obtener usuario {id_usuario}: {e}")
        return None


def service_actualizar_usuario(id_usuario: int, nombre: str, rol_id: int, activa: int,
                                nueva_contrasena: str = None) -> dict:
    """
    Actualiza los datos de un usuario. Si se pasa `nueva_contrasena`, se hashea y reemplaza.
    Si no se pasa, se conserva la contraseña actual.
    """
    if not id_usuario:
        return {"success": False, "error": "El ID del usuario es requerido."}

    if not nombre or not nombre.strip():
        return {"success": False, "error": "El nombre es obligatorio."}

    existente = obtener_usuario_por_id(id_usuario)
    if not existente:
        return {"success": False, "error": f"No se encontró un usuario con ID {id_usuario}."}

    # Verificar nombre duplicado en otro usuario
    por_nombre = obtener_usuario_por_nombre(nombre.strip())
    if por_nombre and por_nombre.id_usuario != id_usuario:
        return {"success": False, "error": f"Ya existe otro usuario con el nombre '{nombre}'."}

    contrasena_final = _hashear(nueva_contrasena) if nueva_contrasena else existente.contrasena

    usuario = UsuarioSistema(
        id_usuario = id_usuario,
        nombre     = nombre.strip(),
        contrasena = contrasena_final,
        rol_id     = rol_id,
        activa     = activa,
    )

    try:
        filas = actualizar_usuario(usuario)
        if filas == 0:
            return {"success": False, "error": "No se realizaron cambios."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al actualizar el usuario: {str(e)}"}


def service_eliminar_usuario(id_usuario: int) -> dict:
    if not id_usuario:
        return {"success": False, "error": "El ID del usuario es requerido."}

    existente = obtener_usuario_por_id(id_usuario)
    if not existente:
        return {"success": False, "error": f"No se encontró un usuario con ID {id_usuario}."}

    try:
        filas = eliminar_usuario(id_usuario)
        if filas == 0:
            return {"success": False, "error": "No se pudo eliminar el usuario."}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al eliminar el usuario: {str(e)}"}


def service_cambiar_contrasena(id_usuario: int, contrasena_actual: str, nueva_contrasena: str) -> dict:
    """
    Cambia la contraseña verificando primero la actual.
    """
    if not contrasena_actual or not nueva_contrasena:
        return {"success": False, "error": "Ambas contraseñas son requeridas."}

    if len(nueva_contrasena) < 6:
        return {"success": False, "error": "La nueva contraseña debe tener al menos 6 caracteres."}

    usuario = obtener_usuario_por_id(id_usuario)
    if not usuario:
        return {"success": False, "error": f"No se encontró un usuario con ID {id_usuario}."}

    if usuario.contrasena != _hashear(contrasena_actual):
        return {"success": False, "error": "La contraseña actual es incorrecta."}

    usuario.contrasena = _hashear(nueva_contrasena)

    try:
        actualizar_usuario(usuario)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Error al cambiar la contraseña: {str(e)}"}