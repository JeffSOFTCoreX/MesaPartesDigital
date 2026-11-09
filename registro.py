from validacion import validar_datos, validar_longitudes
from busqueda import buscar_documento
from normalizacion import limpiar_texto


def registrar_documento(registros):
    print("\n--- REGISTRO DE DOCUMENTO ---")

    codigo = limpiar_texto(input("Código: "))

    if not codigo:
        print("No se pudo registrar: El campo 'codigo' es obligatorio.")
        return False

    if buscar_documento(registros, codigo):
        print(f"Ya existe un documento registrado con el código '{codigo}'.")
        return False

    tipo_documento = limpiar_texto(input("Tipo de documento: "))
    estudiante = limpiar_texto(input("Nombre del estudiante/usuario: "))
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
    if valido:
        # El límite de longitud se aplica solo a registros NUEVOS: los datos
        # existentes en documentos.txt se cargan y guardan sin truncarse.
        valido, mensaje = validar_longitudes(datos)

    if not valido:
        print(f"No se pudo registrar: {mensaje}")
        return False

    registros.append(datos)
    print(f"Documento '{codigo}' registrado correctamente con estado '{estado}'.")
    return True
