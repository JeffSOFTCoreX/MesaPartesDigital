"""Autenticación del administrador de la Mesa de Partes Digital.

La contraseña nunca se guarda ni aparece en el código: solo se almacena un
hash PBKDF2-HMAC-SHA256 con sal aleatoria en ``credenciales.json`` (archivo
local, ignorado por Git).

Configurar o cambiar la cuenta del administrador:

    python autenticacion.py
"""

import base64
import getpass
import hashlib
import hmac
import json
import os
import secrets
import tempfile
from pathlib import Path

# Archivo junto a este módulo: no depende de la carpeta de ejecución.
ARCHIVO_CREDENCIALES = str(Path(__file__).resolve().parent / "credenciales.json")

ALGORITMO = "pbkdf2_sha256"
ITERACIONES = 200_000
LONGITUD_SAL = 16
MAX_INTENTOS = 3
MIN_LONGITUD_CONTRASENA = 8
MENSAJE_RECHAZO = "Usuario o contraseña incorrectos."


def _derivar(contrasena, sal, iteraciones):
    return hashlib.pbkdf2_hmac(
        "sha256", contrasena.encode("utf-8"), sal, iteraciones
    )


def normalizar_usuario(usuario):
    """El usuario no distingue mayúsculas ni espacios sobrantes."""
    return " ".join(usuario.split()).casefold()


def generar_credenciales(usuario, contrasena, iteraciones=ITERACIONES):
    """Devuelve el diccionario a guardar: usuario, sal y hash (sin la clave)."""
    usuario = " ".join(usuario.split())
    if not usuario:
        raise ValueError("El usuario no puede estar vacío.")
    if len(contrasena) < MIN_LONGITUD_CONTRASENA:
        raise ValueError(
            f"La contraseña debe tener al menos {MIN_LONGITUD_CONTRASENA} caracteres."
        )
    sal = secrets.token_bytes(LONGITUD_SAL)
    return {
        "usuario": usuario,
        "algoritmo": ALGORITMO,
        "iteraciones": iteraciones,
        "sal": base64.b64encode(sal).decode("ascii"),
        "hash": base64.b64encode(_derivar(contrasena, sal, iteraciones)).decode("ascii"),
    }


def _validar_estructura(datos):
    try:
        if datos["algoritmo"] != ALGORITMO:
            raise ValueError("algoritmo no soportado")
        if not str(datos["usuario"]).strip():
            raise ValueError("usuario vacío")
        iteraciones = int(datos["iteraciones"])
        if iteraciones < 1:
            raise ValueError("iteraciones inválidas")
        sal = base64.b64decode(datos["sal"], validate=True)
        hash_guardado = base64.b64decode(datos["hash"], validate=True)
        if not sal or not hash_guardado:
            raise ValueError("sal o hash vacíos")
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"El archivo de credenciales no es válido: {error}") from error
    return iteraciones, sal, hash_guardado


def verificar_credenciales(usuario, contrasena, datos):
    """True solo si usuario y contraseña coinciden con las credenciales."""
    iteraciones, sal, hash_guardado = _validar_estructura(datos)
    # Se calcula el hash siempre, aunque el usuario no coincida, para que el
    # tiempo de respuesta no revele si el usuario existe.
    calculado = _derivar(contrasena, sal, iteraciones)
    contrasena_ok = hmac.compare_digest(calculado, hash_guardado)
    usuario_ok = hmac.compare_digest(
        normalizar_usuario(usuario).encode("utf-8"),
        normalizar_usuario(str(datos["usuario"])).encode("utf-8"),
    )
    return usuario_ok and contrasena_ok


def cargar_credenciales(ruta=None):
    """Devuelve las credenciales guardadas o None si no se han configurado.

    Lanza ValueError si el archivo existe pero está dañado: en ese caso no se
    debe permitir el acceso.
    """
    archivo = Path(ruta or ARCHIVO_CREDENCIALES)
    if not archivo.exists():
        return None
    try:
        datos = json.loads(archivo.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"No se pudo leer el archivo de credenciales: {error}") from error
    if not isinstance(datos, dict):
        raise ValueError("El archivo de credenciales no es válido.")
    _validar_estructura(datos)
    return datos


def guardar_credenciales(datos, ruta=None):
    """Guarda con archivo temporal + reemplazo para no dejarlo a medias."""
    destino = Path(ruta or ARCHIVO_CREDENCIALES)
    temporal = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destino.parent,
            prefix=f".{destino.name}.", suffix=".tmp", delete=False,
        ) as archivo:
            temporal = Path(archivo.name)
            json.dump(datos, archivo, indent=2)
            archivo.flush()
            os.fsync(archivo.fileno())
        try:
            os.chmod(temporal, 0o600)  # solo el dueño (no aplica en Windows)
        except OSError:
            pass
        os.replace(temporal, destino)
    except BaseException:
        if temporal is not None:
            try:
                temporal.unlink(missing_ok=True)
            except OSError:
                pass
        raise


def _pedir_contrasena(mensaje):
    return getpass.getpass(mensaje)


def configurar_administrador(ruta=None):
    """Crea la cuenta del administrador o cambia la existente.

    Si ya existe una cuenta, exige antes la contraseña actual.
    Devuelve True si quedó guardada una cuenta nueva.
    """
    print("\n--- CONFIGURACIÓN DEL ADMINISTRADOR ---")
    try:
        actuales = cargar_credenciales(ruta)
    except ValueError as error:
        print(error)
        print("Elimine o repare credenciales.json antes de continuar.")
        return False

    if actuales is not None:
        print("Ya existe una cuenta. Confirme la contraseña actual para cambiarla.")
        clave_actual = _pedir_contrasena("Contraseña actual: ")
        if not verificar_credenciales(actuales["usuario"], clave_actual, actuales):
            print("Contraseña actual incorrecta. No se realizaron cambios.")
            return False

    usuario = input("Nuevo usuario administrador: ").strip()
    contrasena = _pedir_contrasena(
        f"Nueva contraseña (mínimo {MIN_LONGITUD_CONTRASENA} caracteres): "
    )
    confirmacion = _pedir_contrasena("Repita la contraseña: ")
    if contrasena != confirmacion:
        print("Las contraseñas no coinciden. No se guardó nada.")
        return False

    try:
        datos = generar_credenciales(usuario, contrasena)
        guardar_credenciales(datos, ruta)
    except ValueError as error:
        print(f"No se pudo configurar: {error}")
        return False
    except OSError as error:
        print(f"No se pudo guardar la cuenta: {error}")
        return False

    print(f"Cuenta del administrador '{datos['usuario']}' guardada correctamente.")
    return True


def iniciar_sesion(ruta=None, max_intentos=MAX_INTENTOS):
    """Pide usuario y contraseña. Devuelve el usuario autenticado o None.

    Devuelve None si se agotan los intentos o si no es posible validar la
    cuenta; nunca permite el acceso por defecto.
    """
    print("\n" + "=" * 62)
    print("                 MESA DE PARTES DIGITAL")
    print("               INICIO DE SESIÓN - ADMINISTRADOR")
    print("=" * 62)

    try:
        datos = cargar_credenciales(ruta)
    except ValueError as error:
        print(error)
        print("Acceso denegado.")
        return None

    if datos is None:
        print("Todavía no hay un administrador configurado.")
        if input("¿Desea crearlo ahora? (S/N): ").strip().casefold() not in {"s", "si", "sí"}:
            print("Sin administrador no se puede ingresar. "
                  "Ejecute: python autenticacion.py")
            return None
        if not configurar_administrador(ruta):
            return None
        datos = cargar_credenciales(ruta)

    for intento in range(1, max_intentos + 1):
        usuario = input("Usuario: ").strip()
        contrasena = _pedir_contrasena("Contraseña: ")
        if verificar_credenciales(usuario, contrasena, datos):
            print(f"Acceso concedido. Bienvenido, {datos['usuario']}.")
            return datos["usuario"]
        restantes = max_intentos - intento
        if restantes:
            print(f"{MENSAJE_RECHAZO} Intentos restantes: {restantes}.")
        else:
            print(f"{MENSAJE_RECHAZO} Se agotaron los intentos. Acceso bloqueado.")
    return None


if __name__ == "__main__":
    try:
        configurar_administrador()
    except (KeyboardInterrupt, EOFError):
        print("\nConfiguración cancelada.")
