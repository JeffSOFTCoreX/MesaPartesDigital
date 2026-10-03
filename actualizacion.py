from busqueda import buscar_documento


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

    estados = {
        "1": "Pendiente",
        "2": "En proceso",
        "3": "Atendido",
    }

    if opcion not in estados:
        print("Opción de estado no válida.")
        return False

    registro["estado"] = estados[opcion]
    print(f"Estado actualizado a '{registro['estado']}'.")
    return True
