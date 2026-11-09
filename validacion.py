from datetime import datetime
import re


LONGITUD_MAXIMA = 100


def validar_longitudes(datos, maximo=LONGITUD_MAXIMA):
    """Límite de longitud para registros nuevos (no se usa al cargar archivos)."""
    for campo, valor in datos.items():
        if len(str(valor)) > maximo:
            return False, f"El campo '{campo}' supera los {maximo} caracteres permitidos."
    return True, "Longitudes válidas."


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

    # El formato de texto utiliza | y un registro por línea: no alterar
    # silenciosamente datos que romperían ese formato al recuperarlos.
    for campo in campos_obligatorios:
        valor = str(datos[campo])
        if any(caracter in valor for caracter in ("|", "\r", "\n", "\t")):
            return False, f"El campo '{campo}' contiene un carácter no permitido (| o salto/tabulación)."

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
