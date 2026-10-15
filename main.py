from archivo import cargar_archivo, guardar_archivo, ordenar_registros
from registro import registrar_documento
from busqueda import buscar_documento
from consulta import consultar_documento, mostrar_registros
from actualizacion import actualizar_estado

ARCHIVO_DATOS = "documentos.txt"


def guardar_automaticamente(registros):
    """Guarda los cambios después de un registro o una actualización válidos."""
    try:
        guardar_archivo(registros, ARCHIVO_DATOS)
    except OSError as error:
        print(f"No se pudieron guardar los cambios: {error}")
        return False

    print("Cambios guardados automáticamente.")
    return True


def mostrar_menu():
    print("\n=== MESA DE PARTES DIGITAL ===")
    print("1. Registrar documento")
    print("2. Buscar documento")
    print("3. Consultar documento")
    print("4. Actualizar estado")
    print("5. Ordenar registros")
    print("6. Guardar registros")
    print("7. Mostrar todos los registros")
    print("8. Salir")


def main():
    try:
        registros = cargar_archivo(ARCHIVO_DATOS)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"No se pudieron cargar los registros: {error}")
        print("El programa no se iniciará para evitar sobrescribir los datos existentes.")
        return

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            if registrar_documento(registros):
                guardar_automaticamente(registros)

        elif opcion == "2":
            codigo = input("Ingrese el código a buscar: ").strip()
            registro = buscar_documento(registros, codigo)
            if registro:
                print(f"\nDocumento '{codigo}' encontrado:")
                consultar_documento(registro)
            else:
                print(f"No se encontró ningún documento con el código '{codigo}'.")

        elif opcion == "3":
            codigo = input("Ingrese el código del documento: ").strip()
            registro = buscar_documento(registros, codigo)
            if registro:
                consultar_documento(registro)
            else:
                print(f"No se puede consultar: el código '{codigo}' no está registrado.")

        elif opcion == "4":
            if actualizar_estado(registros):
                guardar_automaticamente(registros)

        elif opcion == "5":
            criterio = input("Ordenar por 'codigo' o 'fecha': ").strip().lower()
            registros_ordenados = ordenar_registros(registros, criterio)

            if registros_ordenados is not None:
                registros = registros_ordenados
                print("Registros ordenados correctamente.")


        elif opcion == "6":
            try:
                guardar_archivo(registros, ARCHIVO_DATOS)
            except OSError as error:
                print(f"No se pudieron guardar los registros: {error}")
            else:
                print("Información guardada correctamente.")

        elif opcion == "7":
            mostrar_registros(registros)

        elif opcion == "8":
            try:
                guardar_archivo(registros, ARCHIVO_DATOS)
            except OSError as error:
                print(f"No se pudieron guardar los registros: {error}")
                print("El programa seguirá abierto para que puedas reintentar.")
            else:
                print("Datos guardados. Programa finalizado.")
                break

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
