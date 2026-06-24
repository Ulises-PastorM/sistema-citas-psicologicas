from database.connection import get_connection, enable_foreign_keys
from models.usuaria_model import Usuaria

def crear_usuaria(usuaria: Usuaria) -> int:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarias (
            nombre,
            edad,
            telefono,
            fecha_nacimiento,
            lugar_nacimiento,
            escolaridad_id,
            ocupacion,
            estado_civil_id,
            sexo_id,
            lengua_indigena_id,
            padecimiento,
            servicio_immujer_id,
            servicio_immujer_fecha,
            terapia_tiempo,
            terapia_lugar,
            canalizada_por,
            red_apoyo,
            motivo_consulta,
            estatus_id
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        usuaria.nombre,
        usuaria.edad,
        usuaria.telefono,
        usuaria.fecha_nacimiento,
        usuaria.lugar_nacimiento,
        usuaria.escolaridad_id,
        usuaria.ocupacion,
        usuaria.estado_civil_id,
        usuaria.sexo_id,
        usuaria.lengua_indigena_id,
        usuaria.padecimiento,
        usuaria.servicio_immujer_id,
        usuaria.servicio_immujer_fecha,
        usuaria.terapia_tiempo,
        usuaria.terapia_lugar,
        usuaria.canalizada_por,
        usuaria.red_apoyo,
        usuaria.motivo_consulta,
        usuaria.estatus_id
    ))
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return nuevo_id


def obtener_usuarias() -> list[Usuaria]:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarias")

    resultados = cursor.fetchall()
    conn.close()

    return [Usuaria.from_dict(dict(row)) for row in resultados]


def obtener_usuaria_por_id(id_usuaria) -> Usuaria | None:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarias WHERE id_usuaria = ?",
        (id_usuaria,)
    )

    resultado = cursor.fetchone()
    conn.close()

    return Usuaria.from_dict(dict(resultado)) if resultado else None


def actualizar_usuaria(usuaria: Usuaria):
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarias
        SET
            nombre = ?,
            edad = ?,
            telefono = ?,
            fecha_nacimiento = ?,
            lugar_nacimiento = ?,
            escolaridad_id = ?,
            ocupacion = ?,
            estado_civil_id = ?,
            sexo_id = ?,
            lengua_indigena_id = ?,
            padecimiento = ?,
            servicio_immujer_id = ?,
            servicio_immujer_fecha = ?,
            terapia_tiempo = ?,
            terapia_lugar = ?,
            canalizada_por = ?,
            red_apoyo = ?,
            motivo_consulta = ?,
            estatus_id = ?
        WHERE id_usuaria = ?
    """, (
        usuaria.nombre,
        usuaria.edad,
        usuaria.telefono,
        usuaria.fecha_nacimiento,
        usuaria.lugar_nacimiento,
        usuaria.escolaridad_id,
        usuaria.ocupacion,
        usuaria.estado_civil_id,
        usuaria.sexo_id,
        usuaria.lengua_indigena_id,
        usuaria.padecimiento,
        usuaria.servicio_immujer_id,
        usuaria.servicio_immujer_fecha,
        usuaria.terapia_tiempo,
        usuaria.terapia_lugar,
        usuaria.canalizada_por,
        usuaria.red_apoyo,
        usuaria.motivo_consulta,
        usuaria.estatus_id,
        usuaria.id_usuaria
    ))

    conn.commit()
    conn.close()
    return cursor.rowcount  # útil para saber si se actualizó algo


def eliminar_usuaria(id_usuaria):
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM usuarias WHERE id_usuaria = ?",
        (id_usuaria,)
    )

    conn.commit()
    conn.close()

    return cursor.rowcount  # indica si se eliminó algún registro

def obtener_usuaria_basico(id_usuaria):
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT nombre, telefono FROM usuarias WHERE id_usuaria = ?",
        (id_usuaria,)
    )

    resultado = cursor.fetchone()
    conn.close()

    return resultado if resultado else None

def obtener_usuaria_por_telefono(telefono) -> Usuaria | None:
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarias WHERE telefono = ?",
        (telefono,)
    )

    resultado = cursor.fetchone()
    conn.close()

    return Usuaria.from_dict(dict(resultado)) if resultado else None

def crear_usuaria_direccion(usuaria_id, direccion_id):
    conn = get_connection()
    enable_foreign_keys(conn)

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarias_direcciones (usuaria_id, direccion_id) VALUES (?, ?)",
        (usuaria_id, direccion_id,)
    )
    conn.commit()
    conn.close()

