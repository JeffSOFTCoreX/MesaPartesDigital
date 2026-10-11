# Pruebas manuales adicionales — MesaPartesDigital

## Objetivo y versión probada

Comprobar manualmente el comportamiento del menú ante una opción inválida, la consulta de un código inexistente, la búsqueda sin distinguir mayúsculas y minúsculas, y la persistencia de un expediente al cerrar y volver a abrir el programa.

- **Proyecto:** MesaPartesDigital · Academia Magna Perpetua
- **Rama:** `main`
- **Commit probado:** `0faea42c3455d874d03a2cdc809477b977f52f0a` (`Semana 8: actualizar documentacion y proteccion de datos`)
- **Copia de trabajo:** clon local separado; no se modificaron los módulos Python del proyecto.

## Entorno de ejecución

- **Sistema operativo:** Linux x86_64, kernel `6.18.38+` (Ubuntu 24.04 del entorno de ejecución).
- **Python:** `3.12.3`
- **Ejecución:** `python3 main.py`
- **Datos de prueba:** ficticios; se utilizó `EXP-201`, `Solicitud`, `Usuario Prueba QA` y `10/10/2026`.

## Casos ejecutados

### PM-01 · Menú inválido

- **Entrada:** `9`
- **Pasos:** Se abrió `main.py`, se escribió `9` en el menú y se observó la respuesta.
- **Resultado esperado:** `Opción no válida. Intente nuevamente.`
- **Resultado observado:** `Opción no válida. Intente nuevamente.` El menú volvió a mostrarse y el programa continuó funcionando.
- **Estado final:** **Aprobado**

### PM-02 · Consulta inexistente

- **Entrada:** opción `3`; código `EXP-999`.
- **Pasos:** Se eligió la opción 3 y se consultó el código ficticio `EXP-999`.
- **Resultado esperado:** Aviso de que `EXP-999` no está registrado y continuidad del programa.
- **Resultado observado:** `No se puede consultar: el código 'EXP-999' no está registrado.` El menú volvió a mostrarse y el programa continuó hasta salir correctamente.
- **Estado final:** **Aprobado**

### PM-03 · Búsqueda sin distinguir mayúsculas

- **Entrada:** registro `EXP-201`, tipo `Solicitud`, usuario `Usuario Prueba QA`, fecha `10/10/2026`; búsqueda `exp-201`.
- **Pasos:** Se registró el expediente ficticio, se eligió la opción 2 y se buscó el mismo código escrito en minúsculas.
- **Resultado esperado:** El expediente se encuentra aunque el código se escriba en minúsculas.
- **Resultado observado:** El programa mostró `Documento 'exp-201' encontrado:` y presentó el registro con código `EXP-201`, tipo `Solicitud`, usuario `Usuario Prueba QA`, fecha `10/10/2026` y estado `Pendiente`.
- **Estado final:** **Aprobado**

### PM-04 · Persistencia al salir

- **Entrada:** opción `8` para salir; después, opción `2` y búsqueda `exp-201` en una nueva ejecución.
- **Pasos:** Tras PM-03 se eligió la opción 8, se cerró el programa, se volvió a abrir `main.py` y se buscó `exp-201`.
- **Resultado esperado:** El expediente permanece disponible después de cerrar y abrir el programa.
- **Resultado observado:** En la segunda ejecución el programa mostró nuevamente `Documento 'exp-201' encontrado:` con los datos del expediente. La salida también indicó `Datos guardados. Programa finalizado.`
- **Estado final:** **Aprobado**

## Incidencias y evidencias

No se encontraron incidencias durante los cuatro casos. No se adjuntaron capturas de pantalla; la evidencia quedó registrada mediante las transcripciones de salida de la terminal durante cada ejecución. Los datos introducidos fueron ficticios y no contienen información personal real.

Como comprobación complementaria, se ejecutó `python3 -m unittest pruebas pruebas_semana8 -v`: **17 pruebas automatizadas ejecutadas, todas satisfactorias**.

## Conclusión

Se comprobó que el menú rechaza opciones inválidas sin detener el sistema, que una consulta inexistente muestra un aviso claro, que la búsqueda de códigos no distingue mayúsculas de minúsculas y que los registros se guardan y recuperan al cerrar y abrir el programa. No se probaron en esta actividad la actualización de estados, el ordenamiento de registros, la validación de otros formatos de fecha ni escenarios de error de escritura o permisos del archivo.
