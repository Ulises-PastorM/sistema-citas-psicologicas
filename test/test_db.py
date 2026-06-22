import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.usuarias_services import service_crear_usuaria, service_obtener_usuarias
from services.psicologas_services import service_crear_psicologa, service_obtener_psicologas
from services.citas_services import service_crear_cita
from services.sesiones_services import service_crear_sesion
from models.usuaria_model import Usuaria
from models.psicologa_model import Psicologa
from models.cita_model import Cita
from models.sesion_model import Sesion

for i in range(1, 5):
    nueva_usuaria = Usuaria(
        nombre="María Fernanda López",
        edad=32,
        telefono="951123456" + str(i),
        fecha_nacimiento="1993-04-15",
        lugar_nacimiento="Oaxaca de Juárez, Oaxaca",
        escolaridad_id=5,
        ocupacion="Docente",
        estado_civil_id=2,
        sexo_id=1,
        lengua_indigena_id=1,
        padecimiento="Ninguno",
        servicio_immujer_id=1,
        servicio_immujer_fecha="2024-06-20",
        terapia_tiempo="6 meses",
        terapia_lugar="Centro de Atención IMMUJER",
        canalizada_por="DIF Municipal",
        red_apoyo="Madre y hermana",
        motivo_consulta="Violencia psicológica y orientación legal",
        estatus_id=1
    )
    resultado = service_crear_usuaria(nueva_usuaria)
    print(resultado)

for i in range(1, 2):
    nueva_psicologa = Psicologa(
        nombre="María Fernanda López",
        especialidad="Violencia",
        horario="10:00-14:00",
        activa=1,
    )
    resultado = service_crear_psicologa(nueva_psicologa)
    print(resultado)

citas = [
    ('2026-07-22', '09:00', 1, 1, 1),
    ('2026-07-22', '10:30', 2, 2, 1),
    ('2026-07-22', '12:00', 1, 3, 1),
    ('2026-07-23', '09:30', 1, 1, 1),
    ('2026-07-23', '11:00', 1, 2, 1)
]

for i in citas:
    nueva_cita = Cita(
        fecha=i[0],
        hora=i[1],
        estado_id=i[2],
        usuaria_id=i[3],
        psicologa_id=i[4],
    )
    resultado = service_crear_cita(nueva_cita)
    print(resultado)

for i in range(4):
    nueva_sesion = Sesion(
        cita_id=i+1,
        fecha_sesion="2026-09-02",
        observaciones="Sufre violencia por parte de su esposo. La paciente cuenta con problemas de autoestima.",
    )
    resultado = service_crear_sesion(nueva_sesion)
    print(resultado)

usuarias = service_obtener_usuarias()

for u in usuarias:
    print(u)