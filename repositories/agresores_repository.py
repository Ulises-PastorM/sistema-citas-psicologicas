from database.connection import get_connection, enable_foreign_keys
from models.agresor_model import Agresor, UsuariaAgresor


# ─── Agresores ────────────────────────────────────────────────────────────────

def crear_agresor(agresor: Agresor) -> int:
    """Inserta un nuevo agresor y devuelve su id_agresor generado."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO agresores (nombre_agresor, parentesco_agresor, ocupacion_agresor, edad_agresor)
        VALUES (?, ?, ?, ?)
    """, (agresor.nombre_agresor, agresor.parentesco_agresor,
          agresor.ocupacion_agresor, agresor.edad_agresor))

    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return nuevo_id


def obtener_agresores() -> list[Agresor]:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agresores")

    resultados = cursor.fetchall()
    conn.close()

    return [Agresor.from_dict(dict(row)) for row in resultados]


def obtener_agresor_por_id(id_agresor: int) -> Agresor | None:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM agresores WHERE id_agresor = ?",
        (id_agresor,)
    )

    resultado = cursor.fetchone()
    conn.close()

    return Agresor.from_dict(dict(resultado)) if resultado else None


def actualizar_agresor(agresor: Agresor) -> int:
    """Actualiza un agresor existente. Devuelve filas afectadas."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE agresores
        SET nombre_agresor = ?, parentesco_agresor = ?, ocupacion_agresor = ?, edad_agresor = ?
        WHERE id_agresor = ?
    """, (agresor.nombre_agresor, agresor.parentesco_agresor,
          agresor.ocupacion_agresor, agresor.edad_agresor, agresor.id_agresor))

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas


def eliminar_agresor(id_agresor: int) -> int:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM agresores WHERE id_agresor = ?",
        (id_agresor,)
    )

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas


# ─── Tabla intermedia usuarias_agresores ──────────────────────────────────────

def vincular_usuaria_agresor(usuaria_id: int, agresor_id: int) -> None:
    """Crea el vínculo entre una usuaria y un agresor."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO usuarias_agresores (usuaria_id, agresor_id)
        VALUES (?, ?)
    """, (usuaria_id, agresor_id))

    conn.commit()
    conn.close()


def desvincular_usuaria_agresor(usuaria_id: int, agresor_id: int) -> int:
    """Elimina el vínculo entre una usuaria y un agresor. Devuelve filas afectadas."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM usuarias_agresores
        WHERE usuaria_id = ? AND agresor_id = ?
    """, (usuaria_id, agresor_id))

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas


def obtener_agresores_de_usuaria(usuaria_id: int) -> list[Agresor]:
    """Devuelve todos los agresores vinculados a una usuaria."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.*
        FROM agresores a
        INNER JOIN usuarias_agresores ua ON a.id_agresor = ua.agresor_id
        WHERE ua.usuaria_id = ?
    """, (usuaria_id,))

    resultados = cursor.fetchall()
    conn.close()

    return [Agresor.from_dict(dict(row)) for row in resultados]


def obtener_usuarias_de_agresor(agresor_id: int) -> list[dict]:
    """Devuelve todos los IDs de usuarias vinculadas a un agresor."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        SELECT usuaria_id FROM usuarias_agresores
        WHERE agresor_id = ?
    """, (agresor_id,))

    resultados = cursor.fetchall()
    conn.close()

    return [row["usuaria_id"] for row in resultados]


def eliminar_vinculos_de_usuaria(usuaria_id: int) -> int:
    """Elimina todos los vínculos de una usuaria (útil al eliminar la usuaria)."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM usuarias_agresores WHERE usuaria_id = ?",
        (usuaria_id,)
    )

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas