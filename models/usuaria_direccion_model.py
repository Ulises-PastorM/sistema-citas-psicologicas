from dataclasses import dataclass


@dataclass
class Usuaria_Direccion:
    usuaria_id:     int
    direccion_id:   int

    def to_dict(self) -> dict:
        return {
            "usuaria_id":   self.usuaria_id,
            "direccion_id": self.direccion_id,
        }

    @staticmethod
    def from_dict(data: dict) -> "Usuaria_Direccion":
        return Usuaria_Direccion(
            usuaria_id   = data.get("usuaria_id", 0),
            direccion_id = data.get("direccion_id", 0),
        )