from datetime import date, timedelta

from models.cita_model import Cita
from services.citas_services import service_obtener_citas_programadas, service_actualizar_cita
from services.usuarias_services import service_obtener_usuaria_por_id
from services.whatsapp_services import obtener_estado_servidor, enviar_mensaje_a_usuaria
from services.notificaciones_services import service_registrar_envio_whatsapp
from threading import Lock

from repositories.catalogos_repository import (
    obtener_configuracion_por_clave,
    actualizar_configuracion,
)


_bloqueo_tarea = Lock()

# Estado IDs
ESTADO_PROGRAMADA = 1
ESTADO_ATENDIDA   = 2


def _dia_siguiente_habil(hoy: date) -> date:
    """
    Devuelve el día siguiente hábil:
    - Si hoy es sábado  → lunes
    - Cualquier otro día → mañana
    """
    if hoy.weekday() == 5:   # sabado
        return hoy + timedelta(days=2)
    else:
        return hoy + timedelta(days=1)


def _procesar_tarea_inicio_dia() -> dict:
    """
    Ejecutar al primer inicio de sesión del día.

    1. Citas programadas con fecha anterior a hoy → estado 'Atendida' (id=2)
    2. Citas programadas con fecha igual al día siguiente hábil → enviar recordatorio

    Returns:
        {
            "atendidas":    int,   # citas marcadas como atendidas
            "recordatorios_enviados": int,
            "recordatorios_fallidos": int,
            "errores":      list   # mensajes de error detallados
        }
    """
    hoy            = date.today()
    dia_recordatorio = _dia_siguiente_habil(hoy)

    print(f"[TareaInicio] Fecha actual:       {hoy}")
    print(f"[TareaInicio] Día de recordatorio: {dia_recordatorio}")

    citas  = service_obtener_citas_programadas()
    print(citas)
    estado_wa = obtener_estado_servidor()
    wa_conectado = estado_wa.get("status") == "connected"

    atendidas             = 0
    recordatorios_enviados = 0
    recordatorios_fallidos = 0
    errores               = []

    for cita in citas:
        if cita.estado_id != ESTADO_PROGRAMADA:
            continue   # solo procesar citas activas

        try:
            fecha_cita = date.fromisoformat(cita.fecha)
        except ValueError:
            errores.append(f"Cita ID {cita.id_cita}: fecha inválida '{cita.fecha}'")
            continue

        # ── 1. Citas vencidas → marcar como Atendida ──────────────────────────
        if fecha_cita < hoy:
            cita_actualizada = Cita(
                fecha        = cita.fecha,
                usuaria_id   = cita.usuaria_id,
                psicologa_id = cita.psicologa_id,
                hora         = cita.hora,
                estado_id    = ESTADO_ATENDIDA,
                id_cita      = cita.id_cita,
            )
            resultado = service_actualizar_cita(cita_actualizada)

            if resultado["success"]:
                atendidas += 1
                print(f"[TareaInicio] Cita ID {cita.id_cita} marcada como Atendida.")
            else:
                errores.append(f"Cita ID {cita.id_cita}: no se pudo actualizar → {resultado['error']}")

        # ── 2. Citas del día siguiente hábil → enviar recordatorio ─────────────
        elif fecha_cita == dia_recordatorio:
            if not wa_conectado:
                recordatorios_fallidos += 1
                errores.append(f"Cita ID {cita.id_cita}: WhatsApp no conectado, recordatorio no enviado.")
                continue

            usuaria = service_obtener_usuaria_por_id(cita.usuaria_id)
            if not usuaria:
                recordatorios_fallidos += 1
                errores.append(f"Cita ID {cita.id_cita}: usuaria ID {cita.usuaria_id} no encontrada.")
                continue

            envio = enviar_mensaje_a_usuaria(usuaria, cita, "recordatorio_cita")

            if envio["success"]:
                service_registrar_envio_whatsapp(
                    cita_id = cita.id_cita,
                    mensaje = envio["mensaje"]
                )
                recordatorios_enviados += 1
                print(f"[TareaInicio] Recordatorio enviado a {usuaria.nombre} (Cita ID {cita.id_cita}).")
            else:
                recordatorios_fallidos += 1
                errores.append(f"Cita ID {cita.id_cita}: error al enviar a {usuaria.nombre} → {envio.get('error')}")

    resumen = {
        "atendidas":              atendidas,
        "recordatorios_enviados": recordatorios_enviados,
        "recordatorios_fallidos": recordatorios_fallidos,
        "errores":                errores,
    }

    print(f"[TareaInicio] Resumen: {resumen}")
    return resumen

def ejecutar_tarea_inicio_dia() -> dict:
    resumen = {
        "atendidas": 0,
        "recordatorios_enviados": 0,
        "recordatorios_fallidos": 0,
        "errores": [],
        "omitida": False,
    }

    # Evita dos ejecuciones simultáneas dentro de la aplicación.
    if not _bloqueo_tarea.acquire(blocking=False):
        resumen["omitida"] = True
        return resumen

    try:
        hoy = date.today().isoformat()

        configuracion = obtener_configuracion_por_clave(
            "dia_envio_recordatorio"
        )

        if configuracion is None:
            raise RuntimeError(
                "No existe la clave dia_envio_recordatorio."
            )

        if configuracion.valor == hoy:
            resumen["omitida"] = True
            print("[TareaInicio] La tarea ya fue iniciada hoy.")
            return resumen

        estado = obtener_estado_servidor()

        if estado.get("status") != "connected":
            resumen["omitida"] = True
            print("[TareaInicio] WhatsApp todavía no está conectado.")
            return resumen

        # Registrar el inicio antes de enviar para evitar repetir el lote.
        filas = actualizar_configuracion(
            "dia_envio_recordatorio",
            hoy
        )

        if filas != 1:
            raise RuntimeError(
                "No se pudo registrar el día de envío."
            )

        return _procesar_tarea_inicio_dia()

    except Exception as e:
        resumen["errores"].append(str(e))
        print(f"[TareaInicio] Error: {e}")
        return resumen

    finally:
        _bloqueo_tarea.release()