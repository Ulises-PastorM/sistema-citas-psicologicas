from database.connection import get_connection, enable_foreign_keys
from models.usuario_sistema_model import UsuarioSistema


def crear_usuario(usuario: UsuarioSistema) -> int:
    """Inserta un nuevo usuario y devuelve su id_usuario generado."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios_sistema (nombre, contrasena, rol_id, activa)
        VALUES (?, ?, ?, ?)
    """, (usuario.nombre, usuario.contrasena, usuario.rol_id, usuario.activa))

    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return nuevo_id


def obtener_usuarios() -> list[UsuarioSistema]:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios_sistema")

    resultados = cursor.fetchall()
    conn.close()

    return [UsuarioSistema.from_dict(dict(row)) for row in resultados]


def obtener_usuario_por_id(id_usuario: int) -> UsuarioSistema | None:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarios_sistema WHERE id_usuario = ?",
        (id_usuario,)
    )

    resultado = cursor.fetchone()
    conn.close()

    return UsuarioSistema.from_dict(dict(resultado)) if resultado else None


def obtener_usuario_por_nombre(nombre: str) -> UsuarioSistema | None:
    """Busca un usuario por nombre exacto. Útil para el login."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarios_sistema WHERE nombre = ?",
        (nombre,)
    )

    resultado = cursor.fetchone()
    conn.close()

    return UsuarioSistema.from_dict(dict(resultado)) if resultado else None


def actualizar_usuario(usuario: UsuarioSistema) -> int:
    """Actualiza un usuario existente. Devuelve filas afectadas."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios_sistema
        SET nombre = ?, contrasena = ?, rol_id = ?, activa = ?
        WHERE id_usuario = ?
    """, (usuario.nombre, usuario.contrasena, usuario.rol_id, usuario.activa, usuario.id_usuario))

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas


def eliminar_usuario(id_usuario: int) -> int:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM usuarios_sistema WHERE id_usuario = ?",
        (id_usuario,)
    )

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas