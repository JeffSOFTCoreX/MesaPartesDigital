from actualizacion import ESTADOS


def normalizar_texto(texto):
    """Ignora mayúsculas y espacios sobrantes, incluso entre palabras."""
    return " ".join(texto.split()).casefold()


def filtrar_expedientes(registros, tipo="", estado=""):
    """Devuelve una lista nueva con las coincidencias, sin alterar registros.

    Un criterio vacío no restringe la consulta. Ambos criterios se combinan
    con AND; si ambos están vacíos se devuelven todos los expedientes.
    """
    tipo = normalizar_texto(tipo)
    estado = normalizar_texto(estado)
    resultados = []
    for registro in registros:
        coincide_tipo = not tipo or normalizar_texto(registro["tipo_documento"]) == tipo
        coincide_estado = not estado or normalizar_texto(registro["estado"]) == estado
        if coincide_tipo and coincide_estado:
            resultados.append(registro)
    return resultados


def mostrar_resultados_filtro(resultados):
    if not resultados:
        print("No existen registros que cumplan los criterios seleccionados.")
        return
    print(f"Expedientes encontrados: {len(resultados)}")
    mostrar_registros(resultados)


def consultar_por_filtros(registros):
    print("\n--- CONSULTA POR FILTROS ---")
    if not registros:
        print("No existen registros almacenados.")
        return

    tipo = input("Tipo de documento (ej.: Matrícula o Constancia; Enter: todos): ")
    print("Estados admitidos: " + ", ".join(ESTADOS.values()))
    estado = input("Estado (Enter: todos): ")
    if normalizar_texto(estado) and normalizar_texto(estado) not in {
        normalizar_texto(valor) for valor in ESTADOS.values()
    }:
        print("El estado ingresado no es válido. Use Pendiente, En proceso o Atendido.")
        return

    mostrar_resultados_filtro(filtrar_expedientes(registros, tipo, estado))


def resumen_por_estado(registros):
    """Cuenta expedientes por estado con un recorrido secuencial O(n)."""
    conteos = {estado: 0 for estado in ESTADOS.values()}
    for registro in registros:
        estado = registro["estado"]
        if estado in conteos:
            conteos[estado] += 1
    return conteos


def consultar_pendientes(registros):
    print("\n--- EXPEDIENTES PENDIENTES ---")
    if not registros:
        print("No existen registros almacenados.")
        return
    conteos = resumen_por_estado(registros)
    print(f"Resumen: {len(registros)} expedientes en total")
    for estado, cantidad in conteos.items():
        print(f"- {estado}: {cantidad}")
    mostrar_resultados_filtro(filtrar_expedientes(registros, estado=ESTADOS["1"]))


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
