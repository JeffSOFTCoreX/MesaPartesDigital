# Revisión e implementación de filtros

Fecha: 26/10/2026. Alcance: código Python de la propuesta de mejora.

## Resultado

Se incorporó `filtrar_expedientes(registros, tipo="", estado="")` en
`consulta.py`, con una lista nueva de resultados, recorrido de registros y
condiciones combinadas mediante AND. Se normalizan criterios y valores con
`split()`, `join()` y `casefold()`. Los diccionarios encontrados son referencias
a los originales; la consulta no los modifica. La función no promete copias
profundas para ediciones posteriores realizadas por otro código.

`consultar_por_filtros` solicita criterios y valida el estado reutilizando
`ESTADOS` de `actualizacion.py`. `consultar_pendientes` reutiliza el mismo filtro.
El menú de `main.py` se ordenó por operación: registro (1), consultas
(2–5), actualización (6), ordenamiento (7), guardado (8) y salir (9).
Se actualizaron las rutas de las pruebas al nuevo menú y se conservó el formato
de almacenamiento existente. Para el filtrado no se modificó `validacion.py`. Posteriormente se reforzó
`archivo.py` con el guardado protegido; la carga se verifica mediante integración.

## Verificación real

Antes del cambio: 28 pruebas existentes aprobadas. Después del filtrado: 49 pruebas aprobadas, incluyendo 21 nuevas.
Con la protección de guardado: 59 aprobadas, incluidas 10 pruebas adicionales. La salida completa está en `resultados_pruebas.txt`.

| Caso propuesto | Resultado comprobado |
| --- | --- |
| CP01: Matrícula | EXP-101, EXP-103, EXP-105 |
| CP02: Constancia | EXP-102, EXP-104 |
| CP03: Pendiente | EXP-101, EXP-104 |
| CP04: Matrícula y Pendiente | EXP-101 |
| CP05: Sin coincidencias | Lista vacía y aviso en consola |
| CP06: Mayúsculas y espacios adicionales | Mismas coincidencias; incluye espacios internos |
| CP07: Sin expedientes | Lista vacía y aviso, sin solicitar entradas adicionales |
| CP08: Persistencia | Guardado/carga y dos inicios del menú con filtros correctos |
| CP09: Consulta sin cambios | Datos y orden conservados; las consultas no llaman al guardado |

También se probaron los tres estados, criterios vacíos, tipos personalizados,
estado inválido, consulta rápida sin pendientes e integración de ambas opciones.
Las pruebas existentes conservan la cobertura de validación, duplicados,
actualización, ordenamiento, guardado automático y errores de archivo.

La demostración adicional ejecuta el programa como proceso de consola con datos
ficticios, carga cinco expedientes y recorre las opciones nuevas; se registra
en `demostracion_filtros.txt`. No se presentan capturas de pantalla ni datos de
campo originales. Los resultados no demuestran una reducción de tiempos reales.

## Hallazgos y límites

Se confirmó la ausencia de filtros en la versión inicial. No fallaron las pruebas
originales ni las nuevas durante esta revisión; no se atribuyen correcciones a
errores inexistentes. El guardado se reforzó con temporales, sincronización, reemplazo y respaldo.
Se mantienen los demás límites descritos en README, incluida la falta de
autenticación y la ausencia de notificaciones. La consulta rápida incluye solamente el estado Pendiente,
no En proceso, de acuerdo con los casos de aceptación.

El ZIP de origen no contiene historial Git; esta entrega no publica cambios ni
afirma nuevos commits. Se incluye un parche de texto para revisión e integración
en el repositorio real. El informe DOCX y las diapositivas PPTX originales se
conservan sin modificaciones; este registro documenta la implementación nueva.

## Reflexión técnica y ética

La función con parámetros y retorno permite probar el algoritmo separado de la
entrada por consola. Reutilizar el estado existente evita introducir valores
incompatibles con la persistencia. Las pruebas de regresión y de integración
permitieron comprobar la ampliación junto con las operaciones previas.

Los cinco expedientes de prueba son ficticios, inspirados en los tipos de trámite
descritos en la propuesta. No proceden de archivos institucionales. El sistema
continúa siendo un prototipo académico y no se midió su impacto operativo en la
academia. La entrevista remota y los datos simulados no equivalen a observación
presencial ni a validación institucional.

La opción 9 únicamente finaliza el programa; no llama al guardado. La opción 8
permite guardar y reintentar si ocurre un error. Se conserva el guardado automático
al registrar o actualizar. Se verificó que salir no escribe ni cambia el archivo.

Se unificaron búsqueda y consulta en la opción 2, Consultar documento por código.
La guía del desafío exige la capacidad de consulta por código, sin imponer
opciones separadas. Se añadieron dos casos de integración: expediente existente
con espacios y minúsculas en el código, y expediente inexistente. Total: 61 pruebas.
