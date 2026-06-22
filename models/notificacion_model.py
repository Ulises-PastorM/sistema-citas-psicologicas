from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Notificacion:
    fecha_envio:     str            # Formato: "YYYY-MM-DD HH:MM:SS"
    cita_id:         int
    mensaje:         Optional[str] = field(default=None)
    id_notificacion: Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_notificacion": self.id_notificacion,
            "fecha_envio":     self.fecha_envio,
            "mensaje":         self.mensaje,
            "cita_id":         self.cita_id,
        }

    @staticmethod
    def from_dict(data: dict) -> "Notificacion":
        return Notificacion(
            id_notificacion = data.get("id_notificacion"),
            fecha_envio     = data.get("fecha_envio", ""),
            mensaje         = data.get("mensaje"),
            cita_id         = data.get("cita_id", 0),
        )

    def __str__(self) -> str:
        return f"Notificacion(id={self.id_notificacion}, cita_id={self.cita_id}, fecha_envio='{self.fecha_envio}')"