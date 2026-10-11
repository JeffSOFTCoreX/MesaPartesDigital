from datetime import datetime
import re


def validar_datos(datos):
    campos_obligatorios = [
        "codigo",
        "tipo_documento",
        "estudiante",
        "fecha",
        "estado",
    ]

    for campo in campos_obligatorios:
        if not str(datos.get(campo, "")).strip():
            return False, f"El campo '{campo}' es obligatorio."

    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", datos["fecha"]):
        return False, "La fecha debe tener el formato DD/MM/AAAA."

    try:
        datetime.strptime(datos["fecha"], "%d/%m/%Y")
    except ValueError:
        return False, "La fecha ingresada no es válida."

    estados_permitidos = {"Pendiente", "En proceso", "Atendido"}
    if datos["estado"] not in estados_permitidos:
        return False, "El estado ingresado no es válido."

    return True, "Datos válidos."
