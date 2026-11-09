from normalizacion import clave_codigo


def buscar_documento(registros, codigo):
    codigo = clave_codigo(codigo)

    for registro in registros:
        if clave_codigo(registro.get("codigo", "")) == codigo:
            return registro

    return None
