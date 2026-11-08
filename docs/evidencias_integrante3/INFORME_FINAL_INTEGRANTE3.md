# Informe final de pruebas e integración

**Proyecto:** Mesa de Partes Digital  
**Responsable:** Integrante 3 — Pruebas e integración final  
**Fecha:** 08/11/2026

## 1. Alcance

Se revisó el proyecto base, el avance del integrante 1 y el avance del integrante 2. La entrega final conserva la estructura del proyecto y reúne la autenticación del administrador con las correcciones de revisión del sistema.

La copia original se mantuvo separada y sin modificaciones. La integración se realizó en una copia de trabajo independiente.

## 2. Cambios integrados

El integrante 2 incorporó correcciones en `main.py`, `archivo.py`, `actualizacion.py` y `validacion.py`. Estas correcciones fijan la ruta de datos junto al programa, permiten leer archivos con BOM, evitan reescribir cuando el estado no cambia, manejan la salida por Ctrl+D/Ctrl+C y restringen las fechas a dígitos ASCII.

El integrante 1 incorporó `autenticacion.py`, integró el inicio de sesión en `main.py`, añadió el cierre de sesión como opción 10, agregó `pruebas_autenticacion.py` y actualizó la configuración para ignorar `credenciales.json`. La contraseña se almacena como hash PBKDF2-HMAC-SHA256 con sal aleatoria; no se guarda en texto plano.

La entrega del integrante 1 fue construida sobre la versión corregida del integrante 2. Se verificó que sus archivos Python compartieran las correcciones del integrante 2 y que las diferencias adicionales correspondieran a autenticación y a sus pruebas de integración.

## 3. Resultados de pruebas automatizadas

| Prueba | Resultado | Observación |
|---|---|---|
| Suite original | APROBADA | 75 pruebas ejecutadas. |
| Revisión del sistema | APROBADA | 8 pruebas nuevas del integrante 2. |
| Autenticación | APROBADA | 31 pruebas nuevas del integrante 1. |
| Integración completa | APROBADA | 114 pruebas ejecutadas en total. |
| Sintaxis Python | APROBADA | Compilación de módulos completada sin errores. |

Resultado real de la ejecución integrada:

```text
Ran 114 tests in 0.620s
OK
```

## 4. Validación funcional

Se generaron registros de evidencia separados para el inicio de sesión correcto, rechazo de credenciales y límite de tres intentos, cierre y reingreso de sesión, registro de expediente, búsqueda por código, actualización de estado y recuperación de datos después del reinicio.

Los escenarios funcionales utilizaron datos ficticios. La evidencia de persistencia confirmó la recuperación de un expediente con estado `En proceso` después de cerrar el programa.

## 5. Archivos de evidencia

El paquete separado de evidencias contiene:

- Resultado completo de las 114 pruebas.
- Inicio de sesión correcto y acceso al menú.
- Rechazo de credenciales y bloqueo después de tres intentos.
- Cierre de sesión y reingreso.
- Registro, búsqueda y actualización de un expediente.
- Recuperación de información después del reinicio.
- Esta matriz y este informe.

## 6. Observación para la entrega

Las capturas antiguas incluidas en los paquetes de los integrantes muestran el menú de 9 opciones y 75 pruebas. Después de la integración, la versión actual tiene 10 opciones porque incluye `Cerrar sesión` y cuenta con 114 pruebas. Por eso, para la evidencia final se deben utilizar los registros generados en este paquete y no presentar las capturas antiguas como si reflejaran la versión final.

## 7. Conclusión

La integración queda validada técnicamente en la copia final: las funciones existentes se conservan, la autenticación se ejecuta antes del menú, el cierre de sesión funciona, las credenciales incorrectas son rechazadas con límite de intentos y las 114 pruebas automatizadas terminan correctamente.
