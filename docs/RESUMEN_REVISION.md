# Integrante 2 – Revisión del sistema y corrección de errores

Se revisó el sistema completo con las 75 pruebas existentes y con sesiones reales por consola. Cada problema se reprodujo **antes** de corregirlo (ver `EVIDENCIAS_INTEGRANTE2.md`).

## Errores encontrados y solución
| # | Error | Solución | Archivo |
|---|---|---|---|
| 1 | Ejecutado desde otra carpeta, `documentos.txt` se creaba vacío allí y los expedientes "desaparecían". | Ruta fija junto a `main.py`. | `main.py` |
| 2 | Un `documentos.txt` con BOM (UTF-8 de Windows) impedía encontrar el primer expediente. | Lectura con `utf-8-sig`. | `archivo.py` |
| 3 | Cambiar al mismo estado reescribía el archivo y pisaba el respaldo `.bak`. | Aviso "ya está en ese estado", sin guardar. | `actualizacion.py` |
| 4 | Ctrl+D / Ctrl+C mostraban un traceback. | Punto de entrada `ejecutar()` con salida ordenada. | `main.py` |

## Correcciones adicionales
| # | Problema | Solución | Archivo |
|---|---|---|---|
| 5 | Archivo editado a mano (espacios alrededor de `\|`, estado en minúsculas) impedía iniciar el programa. | Se limpian los campos y se normaliza el estado al cargar. | `archivo.py` |
| 6 | El filtro por tipo distinguía tildes. | Comparación sin tildes. | `consulta.py` |
| 7 | Con código vacío se pedían todos los datos antes de avisar. | Aviso inmediato. | `registro.py` |
| 8 | Orden por código alfabético (`EXP10` antes que `EXP2`). | Orden natural. | `archivo.py` |
| 9 | La opción 7 no mostraba el resultado del orden. | Muestra la lista ordenada. | `main.py` |
| 10 | Espacios internos se guardaban (`Ana    Pérez`). | Se normalizan al registrar. | `registro.py` |
| 11 | Campos sin límite de longitud. | Máximo de 100 caracteres (`LONGITUD_MAXIMA`). | `validacion.py` |

## Funcionalidades revisadas (se conservan todas)
Menú principal, registro de documentos, búsqueda por código, consulta por filtros, actualización de estados, ordenamiento, almacenamiento (temporal + `.bak`), validaciones y persistencia al cerrar y reabrir.

## Pruebas
Sobre el código del paquete revisado: 93 pruebas en `OK` (75 originales + 8 de `pruebas_revision.py` + 10 de `pruebas_mejoras.py`). Tras integrar con el repositorio actual debe volver a correrse la suite completa.

## Observaciones (no modificadas)
Se permite volver de "Atendido" a "Pendiente"; se aceptan fechas futuras o muy antiguas; solo se conserva un respaldo `.bak`.
