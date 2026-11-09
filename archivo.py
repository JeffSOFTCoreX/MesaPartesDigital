from datetime import datetime
from pathlib import Path
import os
import re
import tempfile

from validacion import validar_datos
from normalizacion import clave_codigo

SEPARADOR = "|"
CAMPOS = ["codigo", "tipo_documento", "estudiante", "fecha", "estado"]


def _eliminar_temporal(ruta):
    if ruta is not None:
        try:
            ruta.unlink(missing_ok=True)
        except OSError:
            # La limpieza no debe ocultar el error de guardado original.
            pass


def _escribir_temporal(destino, contenido):
    """Escribe y sincroniza en el mismo directorio para permitir os.replace."""
    temporal = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=destino.parent, prefix=f".{destino.name}.",
            suffix=".tmp", delete=False,
        ) as archivo:
            temporal = Path(archivo.name)
            archivo.write(contenido)
            archivo.flush()
            os.fsync(archivo.fileno())
        return temporal
    except BaseException:
        _eliminar_temporal(temporal)
        raise


def guardar_archivo(registros, ruta="documentos.txt"):
    """Reemplaza el archivo completo y conserva su versión previa en .bak.

    Si falla la escritura, sincronización o preparación del respaldo, no se
    reemplaza el archivo principal. No coordina escritores simultáneos.
    """
    destino = Path(ruta)
    lineas = []
    codigos = set()
    for numero, registro in enumerate(registros, start=1):
        valido, mensaje = validar_datos(registro)
        if not valido:
            raise ValueError(f"Registro {numero} inválido: {mensaje}")
        codigo = clave_codigo(registro["codigo"])
        if codigo in codigos:
            raise ValueError(f"Código duplicado en el registro {numero}: {registro['codigo']}")
        codigos.add(codigo)
        valores = [str(registro[campo]) for campo in CAMPOS]
        lineas.append(SEPARADOR.join(valores) + "\n")
    contenido = "".join(lineas).encode("utf-8")
    temporal = None
    temporal_respaldo = None
    try:
        temporal = _escribir_temporal(destino, contenido)
        if destino.exists():
            respaldo = destino.with_name(destino.name + ".bak")
            temporal_respaldo = _escribir_temporal(respaldo, destino.read_bytes())
            os.replace(temporal_respaldo, respaldo)
        os.replace(temporal, destino)
    finally:
        _eliminar_temporal(temporal)
        _eliminar_temporal(temporal_respaldo)


ESTADOS_VALIDOS = ("Pendiente", "En proceso", "Atendido")


def _estado_canonico(estado):
    """Devuelve el estado con su escritura oficial si coincide sin distinguir mayúsculas."""
    limpio = " ".join(estado.split())
    for oficial in ESTADOS_VALIDOS:
        if limpio.casefold() == oficial.casefold():
            return oficial
    return estado


def _clave_natural(texto):
    """Orden natural: EXP2 va antes que EXP10."""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", texto.strip().casefold())]


def cargar_archivo(ruta="documentos.txt"):
    registros = []
    archivo = Path(ruta)

    if not archivo.exists():
        archivo.touch()
        return registros

    omitidos = 0
    codigos = set()
    with open(archivo, "r", encoding="utf-8-sig") as f:  # tolera BOM de Windows
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue

            partes = linea.split(SEPARADOR)
            if len(partes) != len(CAMPOS):
                omitidos += 1
                continue

            # Tolera archivos editados a mano: espacios alrededor de | y
            # estado escrito en minúsculas ("pendiente").
            registro = {campo: valor.strip() for campo, valor in zip(CAMPOS, partes)}
            registro["estado"] = _estado_canonico(registro["estado"])
            valido, _ = validar_datos(registro)
            # Misma regla de comparación de códigos en carga, registro y búsqueda
            # (normalizacion.clave_codigo). El valor guardado no se altera.
            registro["codigo"] = registro["codigo"].strip()
            codigo_normalizado = clave_codigo(registro["codigo"])
            if not valido or codigo_normalizado in codigos:
                omitidos += 1
                continue

            registros.append(registro)
            codigos.add(codigo_normalizado)

    if omitidos:
        raise ValueError(
            f"Se detectaron {omitidos} registro(s) inválido(s) o duplicado(s) en {archivo}. "
            "Revise el archivo antes de continuar. No se modificaron los datos."
        )
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
        return sorted(registros, key=lambda r: _clave_natural(r.get("codigo", "")))

    else:
        print("Criterio no válido. Use 'codigo' o 'fecha'.")
        return None
