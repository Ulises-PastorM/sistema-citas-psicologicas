from database.connection import get_connection, enable_foreign_keys
from models.direccion_model import Direccion


def crear_direccion(direccion: Direccion) -> int:
    """Inserta una nueva dirección y devuelve su id_direccion generado."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO direcciones (calle_numero, colonia, municipio, domicilio_estatus_id)
        VALUES (?, ?, ?, ?)
    """, (direccion.calle_numero, direccion.colonia, direccion.municipio, direccion.domicilio_estatus_id))

    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return nuevo_id


def obtener_direcciones() -> list[Direccion]:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM direcciones")

    resultados = cursor.fetchall()
    conn.close()

    return [Direccion.from_dict(dict(row)) for row in resultados]


def obtener_direccion_por_id(id_direccion: int) -> Direccion | None:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM direcciones WHERE id_direccion = ?",
        (id_direccion,)
    )

    resultado = cursor.fetchone()
    conn.close()

    return Direccion.from_dict(dict(resultado)) if resultado else None


def actualizar_direccion(direccion: Direccion) -> int:
    """Actualiza una dirección existente usando el id_direccion del objeto. Devuelve filas afectadas."""
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE direcciones
        SET calle_numero = ?, colonia = ?, municipio = ?, domicilio_estatus_id = ?
        WHERE id_direccion = ?
    """, (direccion.calle_numero, direccion.colonia, direccion.municipio,
          direccion.domicilio_estatus_id, direccion.id_direccion))

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas


def eliminar_direccion(id_direccion: int) -> int:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM direcciones WHERE id_direccion = ?",
        (id_direccion,)
    )

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas