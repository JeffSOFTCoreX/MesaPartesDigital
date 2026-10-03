def buscar_documento(registros, codigo):
    codigo = codigo.strip().lower()

    for registro in registros:
        if registro.get("codigo", "").strip().lower() == codigo:
            return registro

    return None
