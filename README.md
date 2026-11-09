# MesaPartesDigital

Prototipo académico de consola desarrollado en **Python** para el curso **Fundamentos de Programación**. Permite organizar expedientes mediante registro, validación, búsqueda, consulta, actualización de estado, ordenamiento y almacenamiento en un archivo de texto.

El proyecto utiliza como caso de estudio la gestión documental de la **Academia Magna Perpetua**. Los requerimientos se elaboraron a partir de una entrevista remota sobre sus procesos administrativos. Es una propuesta académica; no constituye una mesa de partes estatal ni implementa notificaciones electrónicas.

## Funciones disponibles

| Opción | Operación |
| --- | --- |
| 1 | Registrar un documento, validar sus datos y guardarlo automáticamente. |
| 2 | Consultar por código: localizar el documento y mostrar todos sus datos. |
| 3 | Mostrar todos los registros cargados. |
| 4 | Consultar por tipo de documento, estado o ambos. |
| 5 | Consultar rápidamente los expedientes pendientes. |
| 6 | Cambiar su estado y guardar automáticamente el cambio válido. |
| 7 | Ordenar registros por código o fecha. |
| 8 | Guardar manualmente los registros. |
| 9 | Salir del programa sin ejecutar un guardado adicional. |
| 10 | Cerrar sesión del administrador y volver al inicio de sesión. |

Los estados admitidos son **Pendiente**, **En proceso** y **Atendido**.

## Estructura del proyecto

```text
MesaPartesDigital/
├── main.py                # Inicio de sesión, menú e integración de funciones
├── autenticacion.py       # Acceso del administrador (hash, intentos, configuración)
├── registro.py            # Registro de expedientes
├── validacion.py          # Validación de campos, fechas y estados
├── busqueda.py            # Búsqueda por código
├── normalizacion.py       # Regla compartida de comparación de códigos
├── consulta.py            # Consulta, filtrado y visualización
├── actualizacion.py       # Cambios de estado
├── archivo.py             # Lectura, validación, ordenamiento y guardado
├── pruebas_autenticacion.py # 31 pruebas de inicio y cierre de sesión
├── pruebas_cierre.py      # 11 pruebas de cierre con cambios pendientes (Ctrl+C / fin de entrada)
├── pruebas_revision.py    # 8 pruebas de la revisión y corrección de errores
├── pruebas_mejoras.py     # 17 pruebas de mejoras y compatibilidad
├── pruebas_menu.py        # 2 pruebas de consulta unificada
├── pruebas_filtros.py     # 21 pruebas de filtros e integración
├── pruebas.py             # 5 pruebas iniciales
├── pruebas_semana8.py     # 12 pruebas adicionales
├── pruebas_semana9.py     # 5 pruebas de guardado automático
├── pruebas_semana10.py    # 6 pruebas de integridad y errores
├── docs/                  # Documentación complementaria
├── README.md
└── .gitignore
```

`documentos.txt` se crea junto a `main.py` (sin importar desde qué carpeta se ejecute el programa) si todavía no existe. Es un archivo de datos de uso local y **no debe subirse a GitHub con expedientes personales**.

## Requisitos y ejecución

- Python 3 instalado y disponible en la terminal.
- No requiere paquetes externos: utiliza la biblioteca estándar de Python.

Desde la carpeta del proyecto:

```bash
python autenticacion.py   # una sola vez: crear la cuenta del administrador
python main.py            # inicia con usuario y contraseña
```

Véase [Inicio de sesión del administrador](#inicio-de-sesión-del-administrador).

Cada expediente contiene cinco campos: código, tipo de documento, estudiante/usuario, fecha (`DD/MM/AAAA`) y estado. Los registros se almacenan en `documentos.txt` separados por `|`.

## Validaciones y persistencia

- Se rechazan campos obligatorios vacíos, fechas con formato incorrecto o inexistentes, estados no admitidos, separadores `|`, saltos de línea y tabulaciones.
- No se permiten códigos duplicados, incluso si cambian mayúsculas o aparecen espacios al inicio/final; se usa la misma normalización en búsqueda, carga y guardado.
- Al registrar un documento o actualizar un estado válido, el programa intenta guardar los cambios automáticamente.
- Al iniciar, se comprueban los registros del archivo. Si hay líneas incompletas, datos inválidos o códigos duplicados, se muestra un error y no se abre el menú para evitar sobrescribir la información existente.
- Los problemas de lectura o escritura se comunican al usuario. Si falla el guardado manual (opción 8), se regresa al menú y se puede reintentar.
- Si un guardado automático falla, el menú conserva una marca de cambios pendientes y la opción 9 advierte y ofrece reintentar; si se rechaza o vuelve a fallar, permanece en el menú. La opción 7 guarda automáticamente cuando cambia el orden de los expedientes.

**Guardado protegido:** se escribe un temporal en la misma carpeta, se vacía el búfer y se ejecuta `os.fsync`. Si existe el archivo principal, su contenido anterior se conserva en `documentos.txt.bak` mediante otro reemplazo completo. Finalmente se utiliza `os.replace` para sustituir el principal. Un fallo al escribir, sincronizar o preparar el respaldo aborta el guardado; un fallo al reemplazar el principal se informa para reintentar.

**Límites:** no garantiza protección absoluta frente a daños físicos, cortes de energía, eliminación externa ni escritores simultáneos. El respaldo conserva una sola versión previa, no un historial. No se sincroniza explícitamente el directorio y las garantías finales dependen del sistema de archivos y el hardware. El prototipo implementa un único administrador (sin roles ni permisos diferenciados) y no envía notificaciones electrónicas.

Ver [procedimiento y recuperación](docs/guardado_seguro.md).

## Pruebas automatizadas

Para ejecutar todas las pruebas:

```bash
python -m unittest discover -p "pruebas*.py" -v
```

| Conjunto | Casos |
| --- | ---: |
| `pruebas.py` | 5 |
| `pruebas_semana8.py` | 12 |
| `pruebas_semana9.py` | 5 |
| `pruebas_semana10.py` | 6 |
| `pruebas_filtros.py` | 21 |
| `pruebas_guardado_seguro.py` | 10 |
| `pruebas_menu.py` | 2 |
| `pruebas_avance_ef.py` | 14 |
| `pruebas_revision.py` | 8 |
| `pruebas_autenticacion.py` | 31 |
| `pruebas_cierre.py` | 11 |
| `pruebas_mejoras.py` | 17 |
| **Total de la versión integrada validada** | **142** |

La versión integrada del commit `ae08ba8645a32ca4424f0ec8136c8ef58ef57492` fue validada con **142 pruebas aprobadas, 0 fallos y 0 errores**. El registro completo y las capturas están en [evidencias de integración final](docs/evidencias_integrante3/README.md). Las cantidades de 28, 61, 75, 83, 100, 114, 117 o 125 citadas en documentos históricos corresponden a etapas o conjuntos anteriores; no son el total final. Si se modifica el código, debe ejecutarse nuevamente la suite y registrar el commit comprobado.

La ejecución documentada para la Evaluación Parcial terminó con **28 pruebas aprobadas (`OK`)**. Entre otras situaciones, se comprueban la validación de fechas, los códigos duplicados, el guardado automático, la recuperación de expedientes y el manejo de errores de archivo.

## Consultas nuevas

Selecciona **4** y escribe el tipo de documento y/o el estado. Pulsa Enter
en un criterio para no restringirlo; ambos vacíos muestran todos los registros.
Por ejemplo, `Matrícula` y `Pendiente` muestran únicamente matrículas pendientes.
También se admiten los demás tipos registrados, sin restringir los anteriores.

Las comparaciones ignoran mayúsculas, minúsculas, tildes y espacios sobrantes al inicio,
al final y entre palabras. Por ejemplo, `Matrícula` y `matricula` coinciden.
Los estados admitidos se reutilizan del módulo de actualización; un estado
desconocido muestra un aviso y regresa al menú.

Selecciona **5** para consultar pendientes sin ingresar criterios y mostrar un resumen contado por estado. Las consultas
no cambian estados, no reordenan registros ni escriben en el archivo. Si la lista
está vacía o no hay coincidencias, se muestra el mensaje correspondiente.

Ver [el registro de revisión](docs/revision_filtros.md),
[los resultados finales de pruebas](docs/evidencias_integrante3/00_resultado_pruebas_automatizadas.txt) y
[las capturas y su alcance](docs/evidencias_integrante3/README.md).

## Control de versiones

El README original identifica estos avances del repositorio de origen:

- [`7f20bf7`](https://github.com/JeffSOFTCoreX/MesaPartesDigital/commit/7f20bf7): guardado automático y pruebas de persistencia.
- [`ff3a6ef`](https://github.com/JeffSOFTCoreX/MesaPartesDigital/commit/ff3a6ef): validación de registros recuperados y manejo de errores de archivos.

El repositorio conserva los commits anteriores para documentar la evolución del prototipo.

## Uso de datos

Las demostraciones y pruebas deben ejecutarse con **datos ficticios**. No publiques archivos de expedientes reales, números de documentos, teléfonos ni otros datos personales. La inclusión de `documentos.txt` en `.gitignore` evita incorporaciones nuevas cuando el archivo ya no está bajo seguimiento, pero no elimina versiones antiguas del historial de Git.

La entrega revisada del 26/10/2026 parte del ZIP proporcionado, que no incluye
la carpeta `.git`. No se generaron commits ni se publicó en GitHub. Las 61 pruebas de aquella revisión terminaron en `OK`; corresponden a esa etapa histórica, no al total final.

## Consulta unificada y guía del desafío

Las antiguas opciones Buscar y Consultar se unificaron en **Consultar documento
por código**. La función `buscar_documento` sigue localizando el expediente y
`consultar_documento` presenta su información. Se conserva la separación de
funciones internas, eliminando únicamente la duplicidad del menú.

Se revisó el documento `Desafio_CIIN1205P.pdf` proporcionado por el usuario:
la página 1 exige consultar registros mediante un código de identificación;
las rúbricas revisadas no prescriben dos opciones separadas ni sus nombres.
El archivo es la guía del desafío, no el sílabo completo ni instrucciones
adicionales del docente. La unificación conserva la funcionalidad requerida.


## Avance hacia la Evaluación Final (31/10/2026)

Se corrigieron escenarios de integridad del texto delimitado, códigos con espacios al cargar, pérdida posible en salida normal tras fallo de guardado, y falta de persistencia del ordenamiento. Se añadió un conteo sencillo por estado a la consulta de pendientes. Las **75 pruebas automatizadas** terminaron en `OK` en la ejecución local. Véase [avance EF: detalles, pruebas y límites](docs/avance_ef_implementacion.md).

La rama `avance-ef-2026` fue integrada en `main` mediante el Pull Request #2. Los cuatro commits del avance quedaron publicados. Este paquete consolidado no contiene la carpeta `.git`; el historial verificable se consulta en el repositorio de GitHub.


## Interfaz de consola

El menú principal muestra un encabezado del sistema y un resumen actualizado de los expedientes por estado. Las opciones están agrupadas por gestión de documentos y administración. La interfaz utiliza únicamente funciones de la biblioteca estándar de Python, por lo que no requiere instalar paquetes adicionales.


## Revisión del sistema y corrección de errores

Se incorporaron las correcciones de menú, registro, búsquedas, actualización de estados, almacenamiento, validaciones y persistencia descritas en [el resumen de revisión](docs/RESUMEN_REVISION.md). Las 25 pruebas de ese aporte forman parte de las **142 pruebas de la versión integrada**, junto con las pruebas originales, de autenticación y de cierre con errores de guardado.

## Inicio de sesión del administrador

Al ejecutar `main.py` se solicita usuario y contraseña **antes** de mostrar el menú. Si las credenciales son correctas se accede al menú principal; si son incorrectas el acceso se rechaza.

- **Configurar la cuenta:** ejecutar `python autenticacion.py`, indicar el usuario y la contraseña (mínimo 8 caracteres) y repetirla. Si ya existe una cuenta, primero se pide la contraseña actual. Si se ejecuta `main.py` sin cuenta configurada, ofrece crearla en ese momento.
- **Almacenamiento seguro:** la contraseña no está en el código ni se guarda en texto plano. Se guarda en `credenciales.json` (junto a `main.py`) solo el hash PBKDF2-HMAC-SHA256 (200 000 iteraciones) con una sal aleatoria. El archivo está en `.gitignore`.
- **Límite de intentos:** 3 intentos por inicio de sesión; al agotarse, el programa termina. El mensaje de error es el mismo si falla el usuario o la contraseña.
- **Cerrar sesión:** opción **10** del menú. Vuelve a pedir credenciales; los expedientes se conservan.
- **Salida con cambios sin guardar:** si el guardado automático falló y se sale con Ctrl+C o con fin de entrada, el programa reintenta guardar. Si vuelve a fallar, muestra `ERROR: los cambios recientes NO se guardaron`, termina con `Programa finalizado con errores.` y devuelve el código de salida 1 (no se presenta como una salida normal).
- **Contraseña olvidada:** borrar `credenciales.json` y volver a configurar la cuenta (los expedientes no se modifican).

**Límites:** hay un solo administrador, sin roles. El bloqueo por intentos vale por ejecución del programa (no persiste si se reinicia). Quien tenga acceso al equipo puede borrar `credenciales.json`; es una protección de acceso al programa, no cifrado de `documentos.txt`.


## Alcance del modelo PSeInt

El archivo `PSeInt/MesaPartesDigital_AvanceEF.psc` y sus capturas documentan el modelo académico anterior de nueve opciones, sin autenticación y con guardado simulado en memoria. La implementación final ejecutable es la versión Python con inicio de sesión y diez opciones; las capturas del modelo previo se conservan como antecedentes.
