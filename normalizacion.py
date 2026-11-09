"""Normalización de texto compartida por registro, búsqueda y carga."""


def limpiar_texto(texto):
    """Quita espacios sobrantes al inicio, al final y entre palabras."""
    return " ".join(texto.split())


def clave_codigo(codigo):
    """Clave para comparar códigos: sin espacios sobrantes y sin distinguir mayúsculas.

    Es la única regla de comparación de códigos: la usan el registro (duplicados),
    la búsqueda y la carga/guardado del archivo, así `A  1`, `a 1` y ` A 1 `
    son el mismo código en todas partes.
    """
    return limpiar_texto(codigo).casefold()
