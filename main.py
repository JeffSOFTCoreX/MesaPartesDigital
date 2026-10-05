from archivo import cargar_archivo, guardar_archivo, ordenar_registros
from registro import registrar_documento
from busqueda import buscar_documento
from consulta import consultar_documento, mostrar_registros
from actualizacion import actualizar_estado

ARCHIVO_DATOS = "documentos.txt"


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
    registros = cargar_archivo(ARCHIVO_DATOS)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_documento(registros)

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
            actualizar_estado(registros)

        elif opcion == "5":
            criterio = input("Ordenar por 'codigo' o 'fecha': ").strip().lower()
            registros = ordenar_registros(registros, criterio)
            print("Registros ordenados correctamente.")

        elif opcion == "6":
            guardar_archivo(registros, ARCHIVO_DATOS)
            print("Información guardada correctamente.")

        elif opcion == "7":
            mostrar_registros(registros)

        elif opcion == "8":
            guardar_archivo(registros, ARCHIVO_DATOS)
            print("Datos guardados. Programa finalizado.")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
