from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DomicilioEstatus:
    domicilio_estatus:    str
    id_domicilio_estatus: Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_domicilio_estatus": self.id_domicilio_estatus,
            "domicilio_estatus":    self.domicilio_estatus,
        }

    @staticmethod
    def from_dict(data: dict) -> "DomicilioEstatus":
        return DomicilioEstatus(
            id_domicilio_estatus = data.get("id_domicilio_estatus"),
            domicilio_estatus    = data.get("domicilio_estatus", ""),
        )

    def __str__(self) -> str:
        return f"DomicilioEstatus(id={self.id_domicilio_estatus}, domicilio_estatus='{self.domicilio_estatus}')"


@dataclass
class Escolaridad:
    escolaridad:    str
    id_escolaridad: Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_escolaridad": self.id_escolaridad,
            "escolaridad":    self.escolaridad,
        }

    @staticmethod
    def from_dict(data: dict) -> "Escolaridad":
        return Escolaridad(
            id_escolaridad = data.get("id_escolaridad"),
            escolaridad    = data.get("escolaridad", ""),
        )

    def __str__(self) -> str:
        return f"Escolaridad(id={self.id_escolaridad}, escolaridad='{self.escolaridad}')"


@dataclass
class EstadoCita:
    estado_cita:    str
    id_estado_cita: Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_estado_cita": self.id_estado_cita,
            "estado_cita":    self.estado_cita,
        }

    @staticmethod
    def from_dict(data: dict) -> "EstadoCita":
        return EstadoCita(
            id_estado_cita = data.get("id_estado_cita"),
            estado_cita    = data.get("estado_cita", ""),
        )

    def __str__(self) -> str:
        return f"EstadoCita(id={self.id_estado_cita}, estado_cita='{self.estado_cita}')"


@dataclass
class EstadoCivil:
    estado_civil:    str
    id_estado_civil: Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_estado_civil": self.id_estado_civil,
            "estado_civil":    self.estado_civil,
        }

    @staticmethod
    def from_dict(data: dict) -> "EstadoCivil":
        return EstadoCivil(
            id_estado_civil = data.get("id_estado_civil"),
            estado_civil    = data.get("estado_civil", ""),
        )

    def __str__(self) -> str:
        return f"EstadoCivil(id={self.id_estado_civil}, estado_civil='{self.estado_civil}')"


@dataclass
class Estatus:
    estatus:    str
    id_estatus: Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_estatus": self.id_estatus,
            "estatus":    self.estatus,
        }

    @staticmethod
    def from_dict(data: dict) -> "Estatus":
        return Estatus(
            id_estatus = data.get("id_estatus"),
            estatus    = data.get("estatus", ""),
        )

    def __str__(self) -> str:
        return f"Estatus(id={self.id_estatus}, estatus='{self.estatus}')"


@dataclass
class LenguaIndigena:
    lengua_indigena:    str
    id_lengua_indigena: Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_lengua_indigena": self.id_lengua_indigena,
            "lengua_indigena":    self.lengua_indigena,
        }

    @staticmethod
    def from_dict(data: dict) -> "LenguaIndigena":
        return LenguaIndigena(
            id_lengua_indigena = data.get("id_lengua_indigena"),
            lengua_indigena    = data.get("lengua_indigena", ""),
        )

    def __str__(self) -> str:
        return f"LenguaIndigena(id={self.id_lengua_indigena}, lengua_indigena='{self.lengua_indigena}')"


@dataclass
class Rol:
    rol:    str
    id_rol: Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_rol": self.id_rol,
            "rol":    self.rol,
        }

    @staticmethod
    def from_dict(data: dict) -> "Rol":
        return Rol(
            id_rol = data.get("id_rol"),
            rol    = data.get("rol", ""),
        )

    def __str__(self) -> str:
        return f"Rol(id={self.id_rol}, rol='{self.rol}')"


@dataclass
class ServicioImmujer:
    servicio_immujer:    str
    id_servicio_immujer: Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_servicio_immujer": self.id_servicio_immujer,
            "servicio_immujer":    self.servicio_immujer,
        }

    @staticmethod
    def from_dict(data: dict) -> "ServicioImmujer":
        return ServicioImmujer(
            id_servicio_immujer = data.get("id_servicio_immujer"),
            servicio_immujer    = data.get("servicio_immujer", ""),
        )

    def __str__(self) -> str:
        return f"ServicioImmujer(id={self.id_servicio_immujer}, servicio_immujer='{self.servicio_immujer}')"


@dataclass
class Sexo:
    sexo:    str
    id_sexo: Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_sexo": self.id_sexo,
            "sexo":    self.sexo,
        }

    @staticmethod
    def from_dict(data: dict) -> "Sexo":
        return Sexo(
            id_sexo = data.get("id_sexo"),
            sexo    = data.get("sexo", ""),
        )

    def __str__(self) -> str:
        return f"Sexo(id={self.id_sexo}, sexo='{self.sexo}')"