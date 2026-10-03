# Mesa de Partes Digital

Prototipo desarrollado para el curso **Fundamentos de Programación**.

El proyecto representa una solución básica para el registro, validación, búsqueda, consulta,
actualización, ordenamiento y almacenamiento de documentos administrativos.

## Estructura

```text
MesaPartesDigital/
├── main.py
├── registro.py
├── validacion.py
├── busqueda.py
├── consulta.py
├── actualizacion.py
├── archivo.py
├── documentos.txt
├── README.md
└── .gitignore
```

## Módulos

- `main.py`: integra todos los módulos y presenta el menú principal.
- `registro.py`: registra nuevos documentos.
- `validacion.py`: valida campos obligatorios y formato de fecha.
- `busqueda.py`: busca documentos por código.
- `consulta.py`: muestra la información de uno o varios registros.
- `actualizacion.py`: permite cambiar el estado del trámite.
- `archivo.py`: carga, guarda y ordena registros.
- `documentos.txt`: archivo de persistencia de datos.

## Ejecución

Se requiere Python 3.

```bash
python main.py
```

## Estados disponibles

- Pendiente
- En proceso
- Atendido

## Flujo principal

1. Registrar documento.
2. Validar la información.
3. Buscar o consultar registros.
4. Actualizar el estado del trámite.
5. Ordenar registros por código o fecha.
6. Guardar la información en `documentos.txt`.
