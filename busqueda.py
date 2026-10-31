def buscar_documento(registros, codigo):
    codigo = codigo.strip().casefold()

    for registro in registros:
        if registro.get("codigo", "").strip().casefold() == codigo:
            return registro

    return None
