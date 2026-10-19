from datetime import datetime


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