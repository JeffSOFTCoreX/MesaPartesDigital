from datetime import datetime
from pathlib import Path

SEPARADOR = "|"
CAMPOS = ["codigo", "tipo_documento", "estudiante", "fecha", "estado"]


def guardar_archivo(registros, ruta="documentos.txt"):
    with open(ruta, "w", encoding="utf-8") as archivo:
        for registro in registros:
            valores = [str(registro.get(campo, "")).replace(SEPARADOR, "/") for campo in CAMPOS]
            archivo.write(SEPARADOR.join(valores) + "\n")


def cargar_archivo(ruta="documentos.txt"):
    registros = []
    archivo = Path(ruta)

    if not archivo.exists():
        archivo.touch()
        return registros

    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue

            partes = linea.split(SEPARADOR)

            if len(partes) == len(CAMPOS):
                registros.append(dict(zip(CAMPOS, partes)))

    return registros


def ordenar_registros(registros, criterio="codigo"):
    if criterio == "fecha":
        def clave_fecha(registro):
            try:
                return datetime.strptime(registro["fecha"], "%d/%m/%Y")
            except ValueError:
                return datetime.max

        return sorted(registros, key=clave_fecha)

    elif criterio == "codigo":
        return sorted(registros, key=lambda r: r.get("codigo", "").lower())

    else:
        print("Criterio no válido. Use 'codigo' o 'fecha'.")
        return None