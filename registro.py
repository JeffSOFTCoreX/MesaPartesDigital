from validacion import validar_datos
from busqueda import buscar_documento


def _limpiar(texto):
    """Quita espacios sobrantes al inicio, al final y entre palabras."""
    return " ".join(texto.split())


def registrar_documento(registros):
    print("\n--- REGISTRO DE DOCUMENTO ---")

    codigo = _limpiar(input("Código: "))

    if not codigo:
        print("No se pudo registrar: El campo 'codigo' es obligatorio.")
        return False

    if buscar_documento(registros, codigo):
        print(f"Ya existe un documento registrado con el código '{codigo}'.")
        return False

    tipo_documento = _limpiar(input("Tipo de documento: "))
    estudiante = _limpiar(input("Nombre del estudiante/usuario: "))
    fecha = input("Fecha (DD/MM/AAAA): ").strip()
    estado = "Pendiente"

    datos = {
        "codigo": codigo,
        "tipo_documento": tipo_documento,
        "estudiante": estudiante,
        "fecha": fecha,
        "estado": estado,
    }

    valido, mensaje = validar_datos(datos)

    if not valido:
        print(f"No se pudo registrar: {mensaje}")
        return False

    registros.append(datos)
    print(f"Documento '{codigo}' registrado correctamente con estado '{estado}'.")
    return True
