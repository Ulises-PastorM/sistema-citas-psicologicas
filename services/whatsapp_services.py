import requests
from repositories.usuarias_repository import obtener_usuarias
from models.usuaria_model import Usuaria

# URL base del servidor WhatsApp local
WHATSAPP_SERVER_URL = "http://localhost:3000"


def obtener_estado_servidor() -> dict:
    """Verifica si el servidor WhatsApp está conectado."""
    try:
        response = requests.get(f"{WHATSAPP_SERVER_URL}/status", timeout=5)
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"status": "error", "detail": "No se pudo conectar al servidor WhatsApp."}


def enviar_mensaje_a_usuaria(usuaria: Usuaria, mensaje: str) -> dict:
    """
    Envía un mensaje de WhatsApp a una usuaria.

    Args:
        usuaria: Diccionario con al menos 'nombre' y 'telefono'.
        mensaje:  Texto del mensaje a enviar.

    Returns:
        Diccionario con el resultado de la operación.
    """

    if not usuaria.telefono:
        return {"success": False, "error": f"La usuaria '{usuaria.nombre}' no tiene teléfono registrado."}

    try:
        response = requests.post(
            f"{WHATSAPP_SERVER_URL}/send-message",
            json={"phone": usuaria.telefono_limpio(), "message": mensaje},
            timeout=15,
        )
        data = response.json()

        if response.status_code == 200 and data.get("success"):
            return {"success": True, "nombre": usuaria.nombre, "telefono": usuaria.telefono_limpio()}
        else:
            return {"success": False, "nombre": usuaria.nombre, "error": data.get("error", "Error desconocido")}

    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No se pudo conectar al servidor WhatsApp."}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "El servidor WhatsApp no respondió a tiempo."}


def enviar_mensaje_a_todas(mensaje: str) -> list[dict]:
    """
    Envía un mensaje a todas las usuarias registradas en la base de datos.

    Args:
        mensaje: Texto del mensaje. Puede usar {nombre} como placeholder.
                Ejemplo: "Hola {nombre}, tienes una cita mañana."

    Returns:
        Lista de resultados por cada usuaria.
    """
    usuarias = obtener_usuarias()

    if not usuarias:
        return [{"success": False, "error": "No hay usuarias registradas en la base de datos."}]

    resultados = []
    for usuaria in usuarias:
        # Personalizar el mensaje con el nombre si el placeholder está presente
        mensaje_personalizado = mensaje.format(nombre=usuaria.get("nombre", ""))
        resultado = enviar_mensaje_a_usuaria(usuaria, mensaje_personalizado)
        resultados.append(resultado)

    return resultados


def enviar_mensaje_por_id(usuaria_id: int, mensaje: str) -> dict:
    """
    Envía un mensaje a una usuaria específica por su ID.

    Args:
        usuaria_id: ID de la usuaria en la base de datos.
        mensaje:    Texto del mensaje.

    Returns:
        Diccionario con el resultado de la operación.
    """
    usuarias = obtener_usuarias()
    usuaria  = next((u for u in usuarias if u.get("id") == usuaria_id), None)

    if not usuaria:
        return {"success": False, "error": f"No se encontró una usuaria con ID {usuaria_id}."}

    mensaje_personalizado = mensaje.format(nombre=usuaria.get("nombre", ""))
    return enviar_mensaje_a_usuaria(usuaria, mensaje_personalizado)
