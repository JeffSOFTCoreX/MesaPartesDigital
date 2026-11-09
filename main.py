"""Menú principal del prototipo de mesa de partes digital."""

from pathlib import Path

from archivo import cargar_archivo, guardar_archivo, ordenar_registros
from registro import registrar_documento
from busqueda import buscar_documento
from consulta import (
    consultar_documento, mostrar_registros, consultar_por_filtros,
    consultar_pendientes,
)
from actualizacion import actualizar_estado

# Ruta fija junto a main.py: los expedientes se encuentran sin importar
# desde qué carpeta se ejecute el programa.
ARCHIVO_DATOS = str(Path(__file__).resolve().parent / "documentos.txt")


def guardar_automaticamente(registros):
    """Intenta persistir la lista; el menú administra los cambios pendientes."""
    try:
        guardar_archivo(registros, ARCHIVO_DATOS)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"No se pudieron guardar los cambios: {error}")
        return False

    print("Cambios guardados automáticamente.")
    return True


def mostrar_encabezado(registros):
    """Muestra el encabezado y un resumen actualizado de los expedientes."""
    total = len(registros)
    pendientes = sum(r["estado"] == "Pendiente" for r in registros)
    en_proceso = sum(r["estado"] == "En proceso" for r in registros)
    atendidos = sum(r["estado"] == "Atendido" for r in registros)

    print("\n" + "=" * 62)
    print("                 MESA DE PARTES DIGITAL")
    print("                  ACADEMIA MAGNA PERPETUA")
    print("=" * 62)
    print(f"  Expedientes registrados : {total}")
    print(f"  Pendientes              : {pendientes}")
    print(f"  En proceso              : {en_proceso}")
    print(f"  Atendidos               : {atendidos}")
    print("-" * 62)


def mostrar_menu():
    print("\n  MENÚ PRINCIPAL")
    print("  " + "-" * 40)
    print("  GESTIÓN DE DOCUMENTOS")
    print("   [1] Registrar documento")
    print("   [2] Consultar documento por código")
    print("   [3] Mostrar todos los registros")
    print("   [4] Consultar por tipo y/o estado")
    print("   [5] Consultar expedientes pendientes")
    print()
    print("  ADMINISTRACIÓN")
    print("   [6] Actualizar estado")
    print("   [7] Ordenar registros")
    print("   [8] Guardar registros")
    print()
    print("   [9] Salir")
    print("  " + "-" * 40)


def main():
    try:
        registros = cargar_archivo(ARCHIVO_DATOS)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"No se pudieron cargar los registros: {error}")
        print("El programa no se iniciará para evitar sobrescribir los datos existentes.")
        return

    cambios_pendientes = False

    while True:
        mostrar_encabezado(registros)
        mostrar_menu()
        opcion = input("\n  Seleccione una opción: ").strip()

        if opcion == "1":
            if registrar_documento(registros):
                cambios_pendientes = True
                if guardar_automaticamente(registros):
                    cambios_pendientes = False

        elif opcion == "2":
            codigo = input("Ingrese el código del documento: ").strip()
            registro = buscar_documento(registros, codigo)
            if registro:
                consultar_documento(registro)
            else:
                print(f"No se encontró ningún documento con el código '{codigo}'.")

        elif opcion == "3":
            mostrar_registros(registros)

        elif opcion == "4":
            consultar_por_filtros(registros)

        elif opcion == "5":
            consultar_pendientes(registros)

        elif opcion == "6":
            if actualizar_estado(registros):
                cambios_pendientes = True
                if guardar_automaticamente(registros):
                    cambios_pendientes = False

        elif opcion == "7":
            criterio = input("Ordenar por 'codigo' o 'fecha': ").strip().lower()
            registros_ordenados = ordenar_registros(registros, criterio)
            if registros_ordenados is not None:
                cambio_de_orden = registros_ordenados != registros
                registros = registros_ordenados
                print("Registros ordenados correctamente.")
                mostrar_registros(registros)
                if cambio_de_orden:
                    cambios_pendientes = True
                    if guardar_automaticamente(registros):
                        cambios_pendientes = False

        elif opcion == "8":
            try:
                guardar_archivo(registros, ARCHIVO_DATOS)
            except (OSError, UnicodeError, ValueError) as error:
                print(f"No se pudieron guardar los registros: {error}")
            else:
                cambios_pendientes = False
                print("Información guardada correctamente.")

        elif opcion == "9":
            if cambios_pendientes:
                print("ADVERTENCIA: hay cambios sin guardar tras un error de escritura.")
                decision = input("¿Reintentar el guardado antes de salir? (S/N): ").strip().casefold()
                if decision in {"s", "si", "sí"}:
                    if not guardar_automaticamente(registros):
                        print("El programa seguirá abierto para intentar guardar nuevamente.")
                        continue
                    cambios_pendientes = False
                else:
                    print("El programa seguirá abierto para evitar la pérdida de cambios.")
                    continue
            print("Programa finalizado.")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


def ejecutar():
    """Punto de entrada: Ctrl+C / Ctrl+D salen con un mensaje, sin traceback."""
    try:
        main()
    except EOFError:
        print("\nEntrada finalizada. Programa finalizado.")
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")


if __name__ == "__main__":
    ejecutar()
