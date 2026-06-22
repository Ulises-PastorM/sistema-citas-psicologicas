from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Psicologa:
    nombre:        str
    especialidad:  Optional[str] = field(default=None)
    horario:       Optional[str] = field(default=None)
    activa:        Optional[int] = field(default=1)   # 1 = activa, 0 = inactiva
    id_psicologas: Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_psicologas": self.id_psicologas,
            "nombre":        self.nombre,
            "especialidad":  self.especialidad,
            "horario":       self.horario,
            "activa":        self.activa,
        }

    @staticmethod
    def from_dict(data: dict) -> "Psicologa":
        return Psicologa(
            id_psicologas = data.get("id_psicologas"),
            nombre         = data.get("nombre", ""),
            especialidad   = data.get("especialidad"),
            horario        = data.get("horario"),
            activa         = data.get("activa", 1),
        )

    def __str__(self) -> str:
        return f"Psicologa(id={self.id_psicologas}, nombre='{self.nombre}', especialidad='{self.especialidad}')"