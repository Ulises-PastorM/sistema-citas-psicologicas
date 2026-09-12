from database.connection import get_connection, enable_foreign_keys
from models.cita_model import Cita


def crear_cita(cita: Cita) -> int:
    """Inserta una nueva cita y devuelve su id_cita generado."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO citas (fecha, hora, estado_id, usuaria_id, psicologa_id)
        VALUES (?, ?, ?, ?, ?)
    """, (cita.fecha, cita.hora, cita.estado_id, cita.usuaria_id, cita.psicologa_id))

    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return nuevo_id


def obtener_citas() -> list[Cita]:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM citas ORDER BY fecha ASC, hora ASC")

    resultados = cursor.fetchall()
    conn.close()

    return [Cita.from_dict(dict(row)) for row in resultados]


def obtener_citas_programadas() -> list[Cita]:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM citas WHERE estado_id = 1 ORDER BY fecha ASC, hora ASC")

    resultados = cursor.fetchall()
    conn.close()

    return [Cita.from_dict(dict(row)) for row in resultados]


def obtener_cita_por_id(id_cita: int) -> Cita | None:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM citas WHERE id_cita = ?",
        (id_cita,)
    )

    resultado = cursor.fetchone()
    conn.close()

    return Cita.from_dict(dict(resultado)) if resultado else None


def obtener_citas_por_usuaria(usuaria_id: int) -> list[Cita]:
    """Devuelve todas las citas asociadas a una usuaria específica."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM citas WHERE usuaria_id = ?",
        (usuaria_id,)
    )

    resultados = cursor.fetchall()
    conn.close()

    return [Cita.from_dict(dict(row)) for row in resultados]


def obtener_citas_por_psicologa(psicologa_id: int) -> list[Cita]:
    """Devuelve todas las citas asociadas a una psicóloga específica."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM citas WHERE psicologa_id = ?",
        (psicologa_id,)
    )

    resultados = cursor.fetchall()
    conn.close()

    return [Cita.from_dict(dict(row)) for row in resultados]


def actualizar_cita(cita: Cita) -> int:
    """Actualiza una cita existente usando el id_cita del objeto. Devuelve filas afectadas."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE citas
        SET fecha = ?, hora = ?, estado_id = ?, usuaria_id = ?, psicologa_id = ?
        WHERE id_cita = ?
    """, (cita.fecha, cita.hora, cita.estado_id, cita.usuaria_id, cita.psicologa_id, cita.id_cita))

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas


def eliminar_cita(id_cita: int) -> int:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM citas WHERE id_cita = ?",
        (id_cita,)
    )

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas