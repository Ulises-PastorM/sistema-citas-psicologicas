from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Direccion:
    calle_numero:           str
    colonia:                str
    municipio:              str
    domicilio_estatus_id:   Optional[int] = field(default=1)
    id_direccion:           Optional[int] = field(default=None)

    #Utilidades

    def to_dict(self) -> dict:
        """Convierte la instancia a diccionario (útil para la UI y los services)."""
        return {
            "calle_numero":   		    self.calle_numero,
            "colonia":   			    self.colonia,
            "municipio": 				self.municipio,
            "domicilio_estatus_id": 	self.domicilio_estatus_id,
            "id_direccion": 	        self.id_direccion,
        }

    @staticmethod
    def from_dict(data: dict) -> "Direccion":
        """Construye una instancia Direccion desde un dict (lo que devuelve el repository)."""
        return Direccion(
            id_direccion            = data.get("id_direccion"),
            calle_numero            = data.get("calle_numero", ""),
            colonia                 = data.get("colonia", ""),
            municipio               = data.get("municipio", ""),
            domicilio_estatus_id    = data.get("domicilio_estatus_id", 1)
        )