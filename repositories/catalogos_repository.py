from database.connection import get_connection, enable_foreign_keys
from models.catalogos_model import (
    DomicilioEstatus,
    Escolaridad,
    EstadoCita,
    EstadoCivil,
    Estatus,
    LenguaIndigena,
    Rol,
    ServicioImmujer,
    Sexo,
)


# ─── Helpers internos ─────────────────────────────────────────────────────────

def _fetchall(query: str, params: tuple = ()) -> list[dict]:
    conn = get_connection()
    enable_foreign_keys(conn)
    cursor = conn.cursor()
    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()
    return [dict(row) for row in resultados]


def _fetchone(query: str, params: tuple = ()) -> dict | None:
    conn = get_connection()
    enable_foreign_keys(conn)
    cursor = conn.cursor()
    cursor.execute(query, params)
    resultado = cursor.fetchone()
    conn.close()
    return dict(resultado) if resultado else None


# ─── DomicilioEstatus ─────────────────────────────────────────────────────────

def obtener_domicilio_estatus() -> list[DomicilioEstatus]:
    rows = _fetchall("SELECT * FROM domicilio_estatus")
    return [DomicilioEstatus.from_dict(r) for r in rows]


def obtener_domicilio_estatus_por_id(id_domicilio_estatus: int) -> DomicilioEstatus | None:
    row = _fetchone(
        "SELECT * FROM domicilio_estatus WHERE id_domicilio_estatus = ?",
        (id_domicilio_estatus,)
    )
    return DomicilioEstatus.from_dict(row) if row else None


# ─── Escolaridades ────────────────────────────────────────────────────────────

def obtener_escolaridades() -> list[Escolaridad]:
    rows = _fetchall("SELECT * FROM escolaridades")
    return [Escolaridad.from_dict(r) for r in rows]


def obtener_escolaridad_por_id(id_escolaridad: int) -> Escolaridad | None:
    row = _fetchone(
        "SELECT * FROM escolaridades WHERE id_escolaridad = ?",
        (id_escolaridad,)
    )
    return Escolaridad.from_dict(row) if row else None


# ─── EstadosCita ──────────────────────────────────────────────────────────────

def obtener_estados_cita() -> list[EstadoCita]:
    rows = _fetchall("SELECT * FROM estados_cita")
    return [EstadoCita.from_dict(r) for r in rows]


def obtener_estado_cita_por_id(id_estado_cita: int) -> EstadoCita | None:
    row = _fetchone(
        "SELECT * FROM estados_cita WHERE id_estado_cita = ?",
        (id_estado_cita,)
    )
    return EstadoCita.from_dict(row) if row else None


# ─── EstadosCiviles ───────────────────────────────────────────────────────────

def obtener_estados_civiles() -> list[EstadoCivil]:
    rows = _fetchall("SELECT * FROM estados_civiles")
    return [EstadoCivil.from_dict(r) for r in rows]


def obtener_estado_civil_por_id(id_estado_civil: int) -> EstadoCivil | None:
    row = _fetchone(
        "SELECT * FROM estados_civiles WHERE id_estado_civil = ?",
        (id_estado_civil,)
    )
    return EstadoCivil.from_dict(row) if row else None


# ─── Estatus ──────────────────────────────────────────────────────────────────

def obtener_estatus() -> list[Estatus]:
    rows = _fetchall("SELECT * FROM estatus")
    return [Estatus.from_dict(r) for r in rows]


def obtener_estatus_por_id(id_estatus: int) -> Estatus | None:
    row = _fetchone(
        "SELECT * FROM estatus WHERE id_estatus = ?",
        (id_estatus,)
    )
    return Estatus.from_dict(row) if row else None


# ─── LenguasIndígenas ─────────────────────────────────────────────────────────

def obtener_lenguas_indigenas() -> list[LenguaIndigena]:
    rows = _fetchall("SELECT * FROM lenguas_indigenas")
    return [LenguaIndigena.from_dict(r) for r in rows]


def obtener_lengua_indigena_por_id(id_lengua_indigena: int) -> LenguaIndigena | None:
    row = _fetchone(
        "SELECT * FROM lenguas_indigenas WHERE id_lengua_indigena = ?",
        (id_lengua_indigena,)
    )
    return LenguaIndigena.from_dict(row) if row else None


# ─── Roles ────────────────────────────────────────────────────────────────────

def obtener_roles() -> list[Rol]:
    rows = _fetchall("SELECT * FROM roles")
    return [Rol.from_dict(r) for r in rows]


def obtener_rol_por_id(id_rol: int) -> Rol | None:
    row = _fetchone(
        "SELECT * FROM roles WHERE id_rol = ?",
        (id_rol,)
    )
    return Rol.from_dict(row) if row else None


# ─── ServiciosImmujer ─────────────────────────────────────────────────────────

def obtener_servicios_immujer() -> list[ServicioImmujer]:
    rows = _fetchall("SELECT * FROM servicios_immujer")
    return [ServicioImmujer.from_dict(r) for r in rows]


def obtener_servicio_immujer_por_id(id_servicio_immujer: int) -> ServicioImmujer | None:
    row = _fetchone(
        "SELECT * FROM servicios_immujer WHERE id_servicio_immujer = ?",
        (id_servicio_immujer,)
    )
    return ServicioImmujer.from_dict(row) if row else None


# ─── Sexos ────────────────────────────────────────────────────────────────────

def obtener_sexos() -> list[Sexo]:
    rows = _fetchall("SELECT * FROM sexos")
    return [Sexo.from_dict(r) for r in rows]


def obtener_sexo_por_id(id_sexo: int) -> Sexo | None:
    row = _fetchone(
        "SELECT * FROM sexos WHERE id_sexo = ?",
        (id_sexo,)
    )
    return Sexo.from_dict(row) if row else None