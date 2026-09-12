import requests
from datetime import datetime
from repositories.usuarias_repository import obtener_usuarias
from models.usuaria_model import Usuaria
from models.cita_model import Cita

# URL base del servidor WhatsApp local
WHATSAPP_SERVER_URL = "http://localhost:3000"


def obtener_estado_servidor() -> dict:
    """Verifica si el servidor WhatsApp está conectado."""
    try:
        response = requests.get(f"{WHATSAPP_SERVER_URL}/status", timeout=10)
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"status": "error", "detail": "No se pudo conectar al servidor WhatsApp."}
    except requests.exceptions.ReadTimeout:
        return {"status": "error", "detail": "El servidor no respondió a tiempo."}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "detail": str(e)}

def fecha_a_texto(fecha_str: str) -> str:
    meses = [
        "enero", "febrero", "marzo", "abril",
        "mayo", "junio", "julio", "agosto",
        "septiembre", "octubre", "noviembre", "diciembre"
    ]

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        return f"{fecha.day} de {meses[fecha.month - 1]} de {fecha.year}"
    except ValueError:
        raise ValueError("La fecha debe tener el formato AAAA-MM-DD")

def enviar_mensaje_a_usuaria(usuaria: Usuaria, cita: Cita, tipo_mensaje: str) -> dict:
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

    if tipo_mensaje == "cita_agendada":
        mensaje = "¡Hola, " + usuaria.nombre + "!\nTu cita en IMMujer ha sido agendada.\n\nFecha: " + fecha_a_texto(cita.fecha) + "\nHora: " + cita.hora + " hrs.\n\n¡Te esperamos!"
    
    elif tipo_mensaje == "cita_actualizada":
        mensaje = "¡Hola, " + usuaria.nombre + "!\nTu cita en IMMujer ha sido actualizada.\n\nFecha: " + fecha_a_texto(cita.fecha) + "\nHora: " + cita.hora + " hrs.\n\n¡Te esperamos!"
    
    elif tipo_mensaje == "cita_atendida":
        mensaje = "¡Hola, " + usuaria.nombre + "!\nTu cita en IMMujer ha sido atendida.\n\n¡Gracias por confiar en IMMujer!"
    
    elif tipo_mensaje == "cita_cancelada":
        mensaje = "¡Hola, " + usuaria.nombre + "!\nLamentamos informarte que tu cita en IMMujer ha sido cancelada.\n\n¡No te preocupes! En IMMujer siempre serás bienvenida."
    
    elif tipo_mensaje == "no_asistio":
        mensaje = "¡Hola, " + usuaria.nombre + "!\nLamentamos que no hayas podido asistir a tu cita de hoy.\n\n¡No te preocupes! Nos pondremos en contacto contigo para agendar una nueva cita.\n¡Te esperamos!"
    
    elif tipo_mensaje == "recordatorio_cita":
        mensaje =  "¡Hola, " + usuaria.nombre + "!\nTe recordamos que tienes una cita en IMMujer.\n\nFecha: " + fecha_a_texto(cita.fecha) + "\nHora: " + cita.hora + " hrs.\n\n¡Te esperamos!"
    
    else:
        return {"success": False, "error": "Tipo de mensaje no válido."}


    try:
        response = requests.post(
            f"{WHATSAPP_SERVER_URL}/send-message",
            json={"phone": usuaria.telefono_limpio(), "message": mensaje},
            timeout=15,
        )
        data = response.json()

        if response.status_code == 200 and data.get("success"):
            return {"success": True, "nombre": usuaria.nombre, "mensaje": mensaje}
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
