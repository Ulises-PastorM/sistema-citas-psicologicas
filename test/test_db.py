import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repositories.usuarias_repository import crear_usuaria, obtener_usuarias

crear_usuaria("María López", "25/03/2026", "Centro", 29, "9531234567", 3, 1)

usuarios = obtener_usuarias()

for u in usuarios:
    print(u)