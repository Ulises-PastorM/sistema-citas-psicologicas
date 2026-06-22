import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.usuarias_services import service_crear_usuaria, service_obtener_usuarias
from services.psicologas_services import service_crear_psicologa, service_obtener_psicologas
from models.usuaria_model import Usuaria
from models.psicologa_model import Psicologa

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

#print(nueva_usuaria)



#crear_usuaria("María López", "25/03/2026", "Centro", 29, "9531234567", 3, 1)
#
usuarias = service_obtener_usuarias()

for u in usuarias:
    print(u)