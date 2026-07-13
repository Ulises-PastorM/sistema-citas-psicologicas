from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Agresor:
    nombre_agresor:     str
    parentesco_agresor: Optional[str] = field(default=None)
    ocupacion_agresor:  Optional[str] = field(default=None)
    edad_agresor:       Optional[int] = field(default=None)
    id_agresor:         Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_agresor":         self.id_agresor,
            "nombre_agresor":     self.nombre_agresor,
            "parentesco_agresor": self.parentesco_agresor,
            "ocupacion_agresor":  self.ocupacion_agresor,
            "edad_agresor":       self.edad_agresor,
        }

    @staticmethod
    def from_dict(data: dict) -> "Agresor":
        return Agresor(
            id_agresor         = data.get("id_agresor"),
            nombre_agresor     = data.get("nombre_agresor", ""),
            parentesco_agresor = data.get("parentesco_agresor"),
            ocupacion_agresor  = data.get("ocupacion_agresor"),
            edad_agresor       = data.get("edad_agresor"),
        )

    def __str__(self) -> str:
        return f"Agresor(id={self.id_agresor}, nombre='{self.nombre_agresor}', parentesco='{self.parentesco_agresor}')"


@dataclass
class UsuariaAgresor:
    usuaria_id: int
    agresor_id: int

    def to_dict(self) -> dict:
        return {
            "usuaria_id": self.usuaria_id,
            "agresor_id": self.agresor_id,
        }

    @staticmethod
    def from_dict(data: dict) -> "UsuariaAgresor":
        return UsuariaAgresor(
            usuaria_id = data.get("usuaria_id", 0),
            agresor_id = data.get("agresor_id", 0),
        )

    def __str__(self) -> str:
        return f"UsuariaAgresor(usuaria_id={self.usuaria_id}, agresor_id={self.agresor_id})"