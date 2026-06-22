from database.connection import get_connection, enable_foreign_keys
from models.psicologa_model import Psicologa


def crear_psicologa(psicologa: Psicologa) -> int:
    """Inserta una nueva psicóloga y devuelve su id_psicologas generado."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO psicologas (nombre, especialidad, horario, activa)
        VALUES (?, ?, ?, ?)
    """, (psicologa.nombre, psicologa.especialidad, psicologa.horario, psicologa.activa))

    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return nuevo_id


def obtener_psicologas() -> list[Psicologa]:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM psicologas")

    resultados = cursor.fetchall()
    conn.close()

    return [Psicologa.from_dict(dict(row)) for row in resultados]


def obtener_psicologa_por_id(id_psicologas: int) -> Psicologa | None:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM psicologas WHERE id_psicologas = ?",
        (id_psicologas,)
    )

    resultado = cursor.fetchone()
    conn.close()

    return Psicologa.from_dict(dict(resultado)) if resultado else None


def obtener_psicologas_activas() -> list[Psicologa]:
    """Devuelve solo las psicólogas marcadas como activas (activa = 1)."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM psicologas WHERE activa = 1")

    resultados = cursor.fetchall()
    conn.close()

    return [Psicologa.from_dict(dict(row)) for row in resultados]


def actualizar_psicologa(psicologa: Psicologa) -> int:
    """Actualiza una psicóloga existente usando el id_psicologas del objeto. Devuelve filas afectadas."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE psicologas
        SET nombre = ?, especialidad = ?, horario = ?, activa = ?
        WHERE id_psicologas = ?
    """, (psicologa.nombre, psicologa.especialidad, psicologa.horario,
          psicologa.activa, psicologa.id_psicologas))

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas


def eliminar_psicologa(id_psicologas: int) -> int:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM psicologas WHERE id_psicologas = ?",
        (id_psicologas,)
    )

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas