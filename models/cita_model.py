from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Cita:
    fecha:        str            # Formato: "YYYY-MM-DD"
    usuaria_id:   int
    psicologa_id: int
    hora:         Optional[str] = field(default=None)   # Formato: "HH:MM"
    estado:       Optional[str] = field(default="pendiente")
    id_cita:      Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_cita":      self.id_cita,
            "fecha":        self.fecha,
            "hora":         self.hora,
            "estado":       self.estado,
            "usuaria_id":   self.usuaria_id,
            "psicologa_id": self.psicologa_id,
        }

    @staticmethod
    def from_dict(data: dict) -> "Cita":
        return Cita(
            id_cita      = data.get("id_cita"),
            fecha        = data.get("fecha", ""),
            hora         = data.get("hora"),
            estado       = data.get("estado", "pendiente"),
            usuaria_id   = data.get("usuaria_id", 0),
            psicologa_id = data.get("psicologa_id", 0),
        )

    def __str__(self) -> str:
        return f"Cita(id={self.id_cita}, fecha='{self.fecha}', hora='{self.hora}', estado='{self.estado}')"