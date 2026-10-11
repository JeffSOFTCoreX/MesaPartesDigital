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

## Mejoras implementadas en la semana 8

- Se corrigió el uso de `Path.touch()` para permitir la creación de `documentos.txt` cuando el archivo no existe.
- Se reforzó la validación de fechas en formato `DD/MM/AAAA`, incluyendo el rechazo de fechas inexistentes.
- Se incorporó `pruebas_semana8.py`, con doce pruebas adicionales que, junto con las cinco originales, suman 17 pruebas automatizadas satisfactorias.
- Las mejoras fueron publicadas en GitHub mediante el commit `60a6dfd`.

Ejecutar en el directorio del proyecto:

```bash
python -m unittest pruebas pruebas_semana8 -v
```

**Protección de datos:** El sistema utiliza datos ficticios durante las pruebas para evitar la exposición de información personal. El archivo `documentos.txt` debe mantenerse libre de datos personales reales al compartir el proyecto públicamente. Antes de realizar nuevas publicaciones en GitHub, se recomienda revisar los archivos modificados y verificar que no contengan información confidencial de los usuarios.
