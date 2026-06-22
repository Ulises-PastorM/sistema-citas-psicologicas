from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Sesion:
    cita_id:        Optional[int] = field(default=None)
    fecha_sesion:   Optional[str] = field(default=None)   # Formato: "YYYY-MM-DD"
    observaciones:  Optional[str] = field(default=None)
    id_sesion:      Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_sesion":     self.id_sesion,
            "fecha_sesion":  self.fecha_sesion,
            "observaciones": self.observaciones,
            "cita_id":       self.cita_id,
        }

    @staticmethod
    def from_dict(data: dict) -> "Sesion":
        return Sesion(
            id_sesion      = data.get("id_sesion"),
            fecha_sesion   = data.get("fecha_sesion"),
            observaciones  = data.get("observaciones"),
            cita_id        = data.get("cita_id"),
        )

    def __str__(self) -> str:
        return f"Sesion(id={self.id_sesion}, cita_id={self.cita_id}, fecha_sesion='{self.fecha_sesion}')"