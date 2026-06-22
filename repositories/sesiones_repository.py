from database.connection import get_connection, enable_foreign_keys
from models.sesion_model import Sesion


def crear_sesion(sesion: Sesion) -> int:
    """Inserta una nueva sesión y devuelve su id_sesion generado."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sesiones (fecha_sesion, observaciones, cita_id)
        VALUES (?, ?, ?)
    """, (sesion.fecha_sesion, sesion.observaciones, sesion.cita_id))

    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return nuevo_id


def obtener_sesiones() -> list[Sesion]:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sesiones")

    resultados = cursor.fetchall()
    conn.close()

    return [Sesion.from_dict(dict(row)) for row in resultados]


def obtener_sesion_por_id(id_sesion: int) -> Sesion | None:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM sesiones WHERE id_sesion = ?",
        (id_sesion,)
    )

    resultado = cursor.fetchone()
    conn.close()

    return Sesion.from_dict(dict(resultado)) if resultado else None


def obtener_sesiones_por_cita(cita_id: int) -> list[Sesion]:
    """Devuelve todas las sesiones asociadas a una cita específica."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM sesiones WHERE cita_id = ? ORDER BY fecha_sesion ASC",
        (cita_id,)
    )

    resultados = cursor.fetchall()
    conn.close()

    return [Sesion.from_dict(dict(row)) for row in resultados]


def actualizar_sesion(sesion: Sesion) -> int:
    """Actualiza una sesión existente usando el id_sesion del objeto. Devuelve filas afectadas."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE sesiones
        SET fecha_sesion = ?, observaciones = ?, cita_id = ?
        WHERE id_sesion = ?
    """, (sesion.fecha_sesion, sesion.observaciones, sesion.cita_id, sesion.id_sesion))

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas


def eliminar_sesion(id_sesion: int) -> int:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM sesiones WHERE id_sesion = ?",
        (id_sesion,)
    )

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas