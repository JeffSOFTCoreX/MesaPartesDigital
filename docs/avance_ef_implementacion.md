# Avance hacia la Evaluación Final: revisión del 31/10/2026

Esta carpeta parte del ZIP **Entregable_MesaPartesDigital_Mejorado.zip**. No incluye la carpeta `.git`: la publicación en el repositorio de los cambios debe realizarla el equipo. No se han creado commits ni se han publicado cambios por este proceso.

## Diferencia verificable entre versiones

| Aspecto | EP | ZIP mejorado | Avance EF (esta carpeta) |
| --- | --- | --- | --- |
| Opciones de menú | 8 | 9 | 9 |
| Consultas por tipo/estado | No | Sí | Sí |
| Consulta de pendientes | No | Sí | Sí, con conteos |
| Guardado con temporal y `.bak` | No | Sí | Sí |
| Advertencia ante salida con datos sin guardar | No | No | Sí |
| Validación de caracteres incompatibles con `|` | No | No | Sí |
| Duplicidad de códigos con espacios en carga | Inconsistente | Inconsistente | Normalizada |
| Ordenamiento persistente | Requiere guardar | Requiere guardar | Guarda si cambia el orden |
| Pruebas automatizadas aprobadas | 28 | 61 | 75 |

## Cambios aplicados

1. `main.py`: variable `cambios_pendientes`, aviso y opción de reintentar antes de cerrar. Ante una respuesta distinta de sí, el programa vuelve al menú; no descarta cambios silenciosamente. Registro y actualización siguen intentando guardado automático. Ordenamiento guarda cuando efectivamente altera la lista.
2. `validacion.py`: rechaza el separador `|`, saltos de línea y tabulación en los campos persistidos. Evita transformar `|` en `/` sin consentimiento.
3. `archivo.py`: comprueba la validez de los datos también antes del guardado, rechaza códigos duplicados con normalización y escribe los valores sin sustitución. Al cargar, normaliza el código con `strip()` y `casefold()` para detectar duplicados de manera coherente con la búsqueda.
4. `busqueda.py`: usa `casefold()` al comparar códigos, además de quitar espacios al inicio/final.
5. `consulta.py`: integra `resumen_por_estado()` en la opción 5 y muestra el total y los conteos de Pendiente, En proceso y Atendido.
6. `pruebas_avance_ef.py`: 14 pruebas adicionales de caracteres, duplicados, persistencia, recuperación manual, resumen y salida tras error.

## Cómo ejecutar

Desde `Codigo_Python`:

```bash
python main.py
python -m unittest discover -p "pruebas*.py" -v
```

Se ejecutaron las pruebas automatizadas sobre este avance: **75 pruebas, OK**. Incluye las 61 originales del ZIP mejorado y las 14 adicionales. Las pruebas adicionales usan directorios temporales y expedientes ficticios, no datos personales reales. El resultado informa de los escenarios comprobados; no implica ausencia de todo fallo ni recuperación garantizada ante problemas de hardware.

## Demostración sugerida para la sustentación

1. Registrar dos documentos ficticios, mostrar el guardado automático.
2. Intentar ingresar `|` en el tipo de documento; comprobar el rechazo claro.
3. Consultar un código, filtrar por tipo/estado y consultar la opción 5 (pendientes + resumen).
4. Cambiar el estado de un expediente, volver a consultar el resumen.
5. Ordenar por código, cerrar y volver a abrir para mostrar que el orden queda persistido.
6. Mostrar `documentos.txt.bak` en una carpeta de prueba; explicar que la recuperación es manual y que el respaldo puede ser anterior al último cambio.
7. Ejecutar `python -m unittest discover -p "pruebas*.py" -v` y enseñar la salida `Ran 75 tests ... OK`.

## Precauciones y limitaciones

- Si falla el guardado, la aplicación evita la salida **normal por el menú**, pero no puede impedir un cierre forzado, corte de energía o cierre de la terminal.
- El respaldo contiene como máximo una versión anterior y se actualiza en cada guardado sobre un archivo existente, incluso si no hay cambio; no es un historial ni una garantía frente a daños físicos.
- No hay autenticación, control de acceso, notificaciones electrónicas, protección integral de datos, operaciones simultáneas ni medición de tiempos de atención.
- La salida de consola y las pruebas de esta carpeta son evidencias de funcionamiento local, **no** de funcionamiento en la academia.
- Revisar el código y el informe en equipo y declarar la asistencia de IA conforme al formato del curso.
