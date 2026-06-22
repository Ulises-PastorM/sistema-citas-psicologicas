from database.connection import get_connection, enable_foreign_keys
from models.notificacion_model import Notificacion


def crear_notificacion(notificacion: Notificacion) -> int:
    """Inserta una nueva notificación y devuelve su id_notificacion generado."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notificaciones (fecha_envio, mensaje, cita_id)
        VALUES (?, ?, ?)
    """, (notificacion.fecha_envio, notificacion.mensaje, notificacion.cita_id))

    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return nuevo_id


def obtener_notificaciones() -> list[Notificacion]:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notificaciones")

    resultados = cursor.fetchall()
    conn.close()

    return [Notificacion.from_dict(dict(row)) for row in resultados]


def obtener_notificacion_por_id(id_notificacion: int) -> Notificacion | None:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM notificaciones WHERE id_notificacion = ?",
        (id_notificacion,)
    )

    resultado = cursor.fetchone()
    conn.close()

    return Notificacion.from_dict(dict(resultado)) if resultado else None


def obtener_notificaciones_por_cita(cita_id: int) -> list[Notificacion]:
    """Devuelve todas las notificaciones asociadas a una cita específica."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM notificaciones WHERE cita_id = ? ORDER BY fecha_envio DESC",
        (cita_id,)
    )

    resultados = cursor.fetchall()
    conn.close()

    return [Notificacion.from_dict(dict(row)) for row in resultados]


def eliminar_notificacion(id_notificacion: int) -> int:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM notificaciones WHERE id_notificacion = ?",
        (id_notificacion,)
    )

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas