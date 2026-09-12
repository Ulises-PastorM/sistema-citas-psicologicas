from pathlib import Path
import sys


def resource_path(relative_path: str) -> Path:
    """
    Obtiene la ruta absoluta de un recurso del sistema.

    En desarrollo:
        proyecto/assets/...

    En PyInstaller:
        dist/main/_internal/assets/...
    """
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent

    return base_path / relative_path