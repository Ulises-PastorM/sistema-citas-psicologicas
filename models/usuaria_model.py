from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Usuaria:
    nombre:                 str
    edad:                   int
    telefono:               str
    fecha_nacimiento:       str
    lugar_nacimiento:       str
    escolaridad_id:         int
    ocupacion:              str
    estado_civil_id:        int
    sexo_id:                int
    lengua_indigena_id:     int
    padecimiento:           str
    servicio_immujer_id:    int
    servicio_immujer_fecha: str
    terapia_tiempo:         str
    terapia_lugar:          str
    canalizada_por:         str
    red_apoyo:              str
    motivo_consulta:        str
    estatus_id:             int
    id_usuaria:             Optional[int] = field(default=None)  # None al crear, asignado por la BD

    # Utilidades

    def telefono_limpio(self) -> str:
        """Devuelve el teléfono sin +, espacios ni guiones. Listo para WhatsApp."""
        return "521" + self.telefono.replace(" ", "").replace("-", "").replace("+", "")

    def to_dict(self) -> dict:
        """Convierte la instancia a diccionario (útil para la UI y los services)."""
        return {
            "id_usuaria":   		    self.id_usuaria,
            "nombre":   			    self.nombre,
            "edad": 				    self.edad,
            "telefono": 			    self.telefono,
            "fecha_nacimiento": 	    self.fecha_nacimiento,
            "lugar_nacimiento": 	    self.lugar_nacimiento,
            "escolaridad_id":   	    self.escolaridad_id,
            "ocupacion":    		    self.ocupacion,
            "estado_civil_id":  	    self.estado_civil_id,
            "sexo_id":  			    self.sexo_id,
            "lengua_indigena_id":       self.lengua_indigena_id,
            "padecimiento": 		    self.padecimiento,
            "servicio_immujer_id":      self.servicio_immujer_id,
            "servicio_immujer_fecha":   self.servicio_immujer_fecha,
            "terapia_tiempo":   	    self.terapia_tiempo,
            "terapia_lugar":    	    self.terapia_lugar,
            "canalizada_por":   	    self.canalizada_por,
            "red_apoyo":    		    self.red_apoyo,
            "motivo_consulta":  	    self.motivo_consulta,
            "estatus_id":   		    self.estatus_id,
        }

    @staticmethod
    def from_dict(data: dict) -> "Usuaria":
        """Construye una instancia Usuaria desde un dict (lo que devuelve el repository)."""
        return Usuaria(
            id_usuaria              = data.get("id_usuaria"),
            nombre                  = data.get("nombre", ""),
            edad                    = data.get("edad", 0),
            telefono                = data.get("telefono", ""),
            fecha_nacimiento        = data.get("fecha_nacimiento", ""),
            lugar_nacimiento        = data.get("lugar_nacimiento", ""),
            escolaridad_id          = data.get("escolaridad_id", 0),
            ocupacion               = data.get("ocupacion", ""),
            estado_civil_id         = data.get("estado_civil_id", 0),
            sexo_id                 = data.get("sexo_id", 0),
            lengua_indigena_id      = data.get("lengua_indigena_id", 0),
            padecimiento            = data.get("padecimiento", ""),
            servicio_immujer_id     = data.get("servicio_immujer_id", 0),
            servicio_immujer_fecha  = data.get("servicio_immujer_fecha", ""),
            terapia_tiempo          = data.get("terapia_tiempo", ""),
            terapia_lugar           = data.get("terapia_lugar", ""),
            canalizada_por          = data.get("canalizada_por", ""),
            red_apoyo               = data.get("red_apoyo", ""),
            motivo_consulta         = data.get("motivo_consulta", ""),
            estatus_id              = data.get("estatus_id", 0),
        )

    def __str__(self) -> str:
        return f"Usuaria(id={self.id_usuaria}, nombre='{self.nombre}', tel='{self.telefono}')"
