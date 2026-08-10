import sys
import subprocess
from pathlib import Path
import shutil

import customtkinter as ctk
from ui.main_window import MainWindow

# Ruta al servidor WhatsApp
WHATSAPP_SERVER_PATH = Path(__file__).parent / "integrations" / "whatsapp-server"
BASE_DIR = Path(__file__).parent
SERVER_ENTRY = WHATSAPP_SERVER_PATH / "src" / "index.js"


def obtener_node():
    """
    Devuelve la ruta al ejecutable de Node.
    En desarrollo usa el Node instalado.
    En producción usa runtime/node.exe.
    """

    if getattr(sys, "frozen", False):
        return BASE_DIR / "runtime" / "node.exe"

    return shutil.which("node")

def iniciar_servidor_whatsapp() -> subprocess.Popen | None:
    """
    Lanza `npm start` en la carpeta del servidor WhatsApp como proceso hijo.
    Devuelve el proceso para poder terminarlo al cerrar la app.
    """
    if not WHATSAPP_SERVER_PATH.exists():
        print(f"[WhatsApp] Advertencia: no se encontró el servidor en {WHATSAPP_SERVER_PATH}")
        return None

    try:
        NODE = obtener_node()
        proceso = subprocess.Popen(
            [
                str(NODE),
                str(SERVER_ENTRY)
            ],
            cwd=WHATSAPP_SERVER_PATH,
            shell=(sys.platform == "win32"),
            # Redirigir salida
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        print(f"[WhatsApp] Servidor iniciado (PID: {proceso.pid})")
        return proceso
    except FileNotFoundError:
        print("[WhatsApp] Error: npm no encontrado. Asegúrate de que Node.js esté instalado.")
        return None
    except Exception as e:
        print(f"[WhatsApp] Error al iniciar el servidor: {e}")
        return None

def detener_servidor_whatsapp(proceso: subprocess.Popen) -> None:
    """Termina el proceso del servidor WhatsApp y todos sus hijos en Windows/Linux."""
    if proceso and proceso.poll() is None:  # Sigue corriendo
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proceso.pid)], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("[WhatsApp] Servidor y sus subprocesos detenidos en Windows.")
        else:
            #Se ejecuta solo en sistemas diferentes a Windows
            proceso.terminate()
            try:
                proceso.wait(timeout=5)
                print("[WhatsApp] Servidor detenido correctamente.")
            except subprocess.TimeoutExpired:
                proceso.kill()
                print("[WhatsApp] Servidor forzosamente terminado.")


# Entry point
if __name__ == "__main__":
    servidor = iniciar_servidor_whatsapp()

    app = MainWindow()

    # Registrar el cierre del servidor cuando se cierre la ventana
    def al_cerrar():
        detener_servidor_whatsapp(servidor)
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", al_cerrar)
    app.mainloop()