from validacion import validar_datos
from busqueda import buscar_documento


def registrar_documento(registros):
    print("\n--- REGISTRO DE DOCUMENTO ---")

    codigo = input("Código: ").strip()

    if buscar_documento(registros, codigo):
        print("Ya existe un documento registrado con ese código.")
        return False

    tipo_documento = input("Tipo de documento: ").strip()
    estudiante = input("Nombre del estudiante/usuario: ").strip()
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
    print("Documento registrado correctamente con estado 'Pendiente'.")
    return True
