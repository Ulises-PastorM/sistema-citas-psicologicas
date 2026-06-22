import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.whatsapp_services import enviar_mensaje_a_usuaria
from services.notificaciones_services import service_registrar_envio_whatsapp
from services.usuarias_services import service_obtener_usuaria_por_id, service_crear_usuaria
from services.citas_services import service_crear_cita, obtener_cita_por_id
from models.usuaria_model import Usuaria
from models.cita_model import Cita

nueva_usuaria = Usuaria(
    nombre="Julieta Salazar",
    edad=25,
    telefono="9532769440",
    fecha_nacimiento="2000-10-26",
    lugar_nacimiento="Huajuapan de León, Oaxaca",
    escolaridad_id=3,
    ocupacion="Ama de casa",
    estado_civil_id=2,
    sexo_id=1,
    lengua_indigena_id=1,
    padecimiento="Ninguno",
    servicio_immujer_id=1,
    servicio_immujer_fecha="2024-06-20",
    terapia_tiempo="1 mes",
    terapia_lugar="Psicologa Wendy",
    canalizada_por="Ninguno",
    red_apoyo="Abuela",
    motivo_consulta="Violencia psicológica y orientación legal",
    estatus_id=1
)
resultado = service_crear_usuaria(nueva_usuaria)

nueva_cita = Cita(
    fecha="2026-06-24",
    hora="14:00",
    estado_id=1,
    usuaria_id=5,
    psicologa_id=1,
)
resultado = service_crear_cita(nueva_cita)

if resultado["success"]:
    cita = obtener_cita_por_id(resultado["id_cita"])
    usuaria_info = service_obtener_usuaria_por_id(cita.usuaria_id)
    msg = "¡Hola, " + usuaria_info.nombre + "!\nTu cita en IMMujer ha sido agendada.\nFecha: " + cita.fecha + "\nHora: " + cita.hora + "\n¡Te esperamos!"
    envio_mensaje = enviar_mensaje_a_usuaria(usuaria_info, msg)
    if envio_mensaje["success"]:
        resultado = service_registrar_envio_whatsapp(cita_id=cita.id_cita, mensaje=msg)
        print(resultado)
