from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UsuarioSistema:
    nombre:      str
    contrasena:  str
    rol_id:      int
    activa:      Optional[int] = field(default=1)   # 1 = activo, 0 = inactivo
    id_usuario:  Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return {
            "id_usuario": self.id_usuario,
            "nombre":     self.nombre,
            "contrasena": self.contrasena,
            "rol_id":     self.rol_id,
            "activa":     self.activa,
        }

    @staticmethod
    def from_dict(data: dict) -> "UsuarioSistema":
        return UsuarioSistema(
            id_usuario = data.get("id_usuario"),
            nombre     = data.get("nombre", ""),
            contrasena = data.get("contrasena", ""),
            rol_id     = data.get("rol_id", 0),
            activa     = data.get("activa", 1),
        )

    def __str__(self) -> str:
        return f"UsuarioSistema(id={self.id_usuario}, nombre='{self.nombre}', rol_id={self.rol_id})"