from busqueda import buscar_documento


ESTADOS = {
    "1": "Pendiente",
    "2": "En proceso",
    "3": "Atendido",
}


def cambiar_estado(registro, opcion):
    """Cambia el estado del registro si la opción es válida."""
    if opcion not in ESTADOS:
        return False
    registro["estado"] = ESTADOS[opcion]
    return True


def actualizar_estado(registros):
    print("\n--- ACTUALIZACIÓN DE ESTADO ---")

    codigo = input("Código del documento: ").strip()
    registro = buscar_documento(registros, codigo)

    if not registro:
        print("No se encontró un documento con ese código.")
        return False

    print(f"Estado actual: {registro['estado']}")
    print("1. Pendiente")
    print("2. En proceso")
    print("3. Atendido")

    opcion = input("Seleccione el nuevo estado: ").strip()

    if not cambiar_estado(registro, opcion):
        print("Opción de estado no válida.")
        return False

    print(f"Estado actualizado a '{registro['estado']}'.")
    return True
