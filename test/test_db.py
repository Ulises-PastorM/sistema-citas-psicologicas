import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.usuarias_services import service_crear_usuaria
from services.psicologas_services import service_crear_psicologa
from services.citas_services import service_crear_cita
from services.usuarios_sistema_services import service_crear_usuario
from models.usuaria_model import Usuaria
from models.psicologa_model import Psicologa
from models.cita_model import Cita

# Agrega 4 usuarias
nombres = ["María Hernández", "Lucía Ramírez", "Julia Martínez", "Gabriela Márquez", "Daniela Ortíz", "Fernanda Cruz", "Brenda Gutierrez"]
for i in range(7):
    nueva_usuaria = Usuaria(
        nombre=nombres[i],
        edad=25+i,
        telefono="953276944" + str(i),
        fecha_nacimiento="1993-04-15",
        lugar_nacimiento="Oaxaca de Juárez, Oaxaca",
        escolaridad_id=5,
        ocupacion="Docente",
        estado_civil_id=2,
        sexo_id=1,
        lengua_indigena_id=1,
        padecimiento="Violencia física",
        servicio_immujer_id=1,
        servicio_immujer_fecha="2024-06-20",
        terapia_tiempo="6 meses",
        terapia_lugar="Centro de Atención IMMUJER",
        canalizada_por="Vicefiscalía",
        red_apoyo="Madre y hermana",
        motivo_consulta="Violencia psicológica y orientación legal",
        estatus_id=1
    )
    resultado = service_crear_usuaria(nueva_usuaria)
    print(resultado)

# Agrega 1 psicologa
for i in range(1):
    nueva_psicologa = Psicologa(
        nombre="Nayeli Cabrera",
        especialidad="Violencia",
        horario="10:00-14:00",
        activa=1,
    )
    resultado = service_crear_psicologa(nueva_psicologa)
    print(resultado)

# Agrega 5 citas
citas = [
    ('2026-07-07', '13:00', 1, 2, 1),
    ('2026-07-07', '10:00', 1, 3, 1),

    ('2026-07-14', '11:00', 1, 4, 1),
    ('2026-07-15', '09:00', 1, 5, 1),
    ('2026-07-17', '12:00', 1, 3, 1),

    ('2026-07-10', '09:00', 1, 6, 1),

    ('2026-07-09', '10:00', 1, 7, 1),
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


# Ingresa un usuario admin
resultado = service_crear_usuario("admin", "123456", 1)
print(resultado)

if resultado["success"]:
    print("Nuevo usuario agregado!")
