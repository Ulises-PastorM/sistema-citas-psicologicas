import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.citas_services import service_obtener_citas, service_obtener_citas_usuarias

citas = service_obtener_citas_usuarias()

for c in citas:
    print(c)