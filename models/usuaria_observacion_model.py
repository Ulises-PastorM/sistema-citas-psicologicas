from dataclasses import dataclass


@dataclass
class Usuaria_Observacion:
    id_usuaria:     int
    nombre:         str
    fecha_sesion:   str
    hora_cita:      str
    observaciones:  str

    def to_dict(self) -> dict:
        return {
            "id_usuaria":       self.id_usuaria,
            "nombre":           self.nombre,
            "fecha_sesion":     self.fecha_sesion,
            "hora_cita":        self.hora_cita,
            "observaciones":    self.observaciones,
        }

    @staticmethod
    def from_dict(data: dict) -> "Usuaria_Observacion":
        return Usuaria_Observacion(
            id_usuaria      = data.get("id_usuaria", 0),
            nombre          = data.get("nombre", ""),
            fecha_sesion    = data.get("fecha_sesion", ""),
            hora_cita       = data.get("hora_cita", ""),
            observaciones   = data.get("observaciones", ""),
        )