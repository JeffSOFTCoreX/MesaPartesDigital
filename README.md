# MesaPartesDigital

Prototipo académico de consola desarrollado en **Python** para el curso **Fundamentos de Programación**. Permite organizar expedientes mediante registro, validación, búsqueda, consulta, actualización de estado, ordenamiento y almacenamiento en un archivo de texto.

El proyecto utiliza como caso de estudio la gestión documental de la **Academia Magna Perpetua**. Los requerimientos se elaboraron a partir de una entrevista remota sobre sus procesos administrativos. Es una propuesta académica; no constituye una mesa de partes estatal ni implementa notificaciones electrónicas.

## Funciones disponibles

| Opción | Operación |
| --- | --- |
| 1 | Registrar un documento, validar sus datos y guardarlo automáticamente. |
| 2 | Buscar un documento por su código. |
| 3 | Consultar la información de un documento. |
| 4 | Cambiar su estado y guardar automáticamente el cambio válido. |
| 5 | Ordenar registros por código o fecha. |
| 6 | Guardar manualmente los registros. |
| 7 | Mostrar todos los registros cargados. |
| 8 | Guardar y salir. Si falla el guardado, se permite reintentar. |

Los estados admitidos son **Pendiente**, **En proceso** y **Atendido**.

## Estructura del proyecto

```text
MesaPartesDigital/
├── main.py                # Menú e integración de funciones
├── registro.py            # Registro de expedientes
├── validacion.py          # Validación de campos, fechas y estados
├── busqueda.py            # Búsqueda por código
├── consulta.py            # Consulta y visualización
├── actualizacion.py       # Cambios de estado
├── archivo.py             # Lectura, validación, ordenamiento y guardado
├── pruebas.py             # 5 pruebas iniciales
├── pruebas_semana8.py     # 12 pruebas adicionales
├── pruebas_semana9.py     # 5 pruebas de guardado automático
├── pruebas_semana10.py    # 6 pruebas de integridad y errores
├── docs/                  # Documentación complementaria
├── README.md
└── .gitignore
```

`documentos.txt` se crea en la carpeta desde la que se ejecuta el programa si todavía no existe. Es un archivo de datos de uso local y **no debe subirse a GitHub con expedientes personales**.

## Requisitos y ejecución

- Python 3 instalado y disponible en la terminal.
- No requiere paquetes externos: utiliza la biblioteca estándar de Python.

Desde la carpeta del proyecto:

```bash
python main.py
```

Cada expediente contiene cinco campos: código, tipo de documento, estudiante/usuario, fecha (`DD/MM/AAAA`) y estado. Los registros se almacenan en `documentos.txt` separados por `|`.

## Validaciones y persistencia

- Se rechazan campos obligatorios vacíos, fechas con formato incorrecto o inexistentes y estados no admitidos.
- No se permiten códigos duplicados, incluso si solo cambia el uso de mayúsculas y minúsculas.
- Al registrar un documento o actualizar un estado válido, el programa intenta guardar los cambios automáticamente.
- Al iniciar, se comprueban los registros del archivo. Si hay líneas incompletas, datos inválidos o códigos duplicados, se muestra un error y no se abre el menú para evitar sobrescribir la información existente.
- Los problemas de lectura o escritura se comunican al usuario. Si el guardado al salir falla, el programa permanece abierto para permitir otro intento.

**Límites:** la escritura no dispone de copia de seguridad automática ni de guardado transaccional. Un fallo de escritura podría comprometer los datos. El prototipo tampoco implementa autenticación, permisos de usuario, acceso concurrente ni notificaciones electrónicas. No debe utilizarse para gestionar datos personales reales sin adoptar medidas de seguridad adicionales.

## Pruebas automatizadas

Para ejecutar todas las pruebas:

```bash
python -m unittest pruebas pruebas_semana8 pruebas_semana9 pruebas_semana10 -v
```

| Conjunto | Casos |
| --- | ---: |
| `pruebas.py` | 5 |
| `pruebas_semana8.py` | 12 |
| `pruebas_semana9.py` | 5 |
| `pruebas_semana10.py` | 6 |
| **Total** | **28** |

La ejecución documentada para la Evaluación Parcial terminó con **28 pruebas aprobadas (`OK`)**. Entre otras situaciones, se comprueban la validación de fechas, los códigos duplicados, el guardado automático, la recuperación de expedientes y el manejo de errores de archivo.

## Control de versiones

El desarrollo se encuentra en la rama `main`. Dos avances recientes son:

- [`7f20bf7`](https://github.com/JeffSOFTCoreX/MesaPartesDigital/commit/7f20bf7): guardado automático y pruebas de persistencia.
- [`ff3a6ef`](https://github.com/JeffSOFTCoreX/MesaPartesDigital/commit/ff3a6ef): validación de registros recuperados y manejo de errores de archivos.

El repositorio conserva los commits anteriores para documentar la evolución del prototipo.

## Uso de datos

Las demostraciones y pruebas deben ejecutarse con **datos ficticios**. No publiques archivos de expedientes reales, números de documentos, teléfonos ni otros datos personales. La inclusión de `documentos.txt` en `.gitignore` evita incorporaciones nuevas cuando el archivo ya no está bajo seguimiento, pero no elimina versiones antiguas del historial de Git.
