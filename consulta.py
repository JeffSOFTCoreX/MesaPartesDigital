def consultar_documento(registro):
    print("\n--- INFORMACIÓN DEL DOCUMENTO ---")
    print(f"Código: {registro['codigo']}")
    print(f"Tipo de documento: {registro['tipo_documento']}")
    print(f"Estudiante/usuario: {registro['estudiante']}")
    print(f"Fecha: {registro['fecha']}")
    print(f"Estado: {registro['estado']}")


def mostrar_registros(registros):
    if not registros:
        print("No existen registros almacenados.")
        return

    print("\n=== REGISTROS ALMACENADOS ===")
    for i, registro in enumerate(registros, start=1):
        print(f"\nRegistro {i}")
        consultar_documento(registro)
