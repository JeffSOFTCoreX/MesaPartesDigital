# Integrante 1 – Inicio de sesión, autenticación y cierre seguro
Proyecto: MesaPartesDigital (consola, Python).

## Archivos de este aporte
| Archivo | Cambio |
|---|---|
| `autenticacion.py` | **Nuevo.** Hash PBKDF2-HMAC-SHA256 con sal, verificación, configuración de cuenta e inicio de sesión (3 intentos). |
| `main.py` | `ejecutar()` pide login antes del menú; opción **[10] Cerrar sesión**; encabezado con el administrador; **cierre seguro con cambios pendientes** (ver abajo). |
| `pruebas_autenticacion.py` | **Nuevo.** 31 pruebas. |
| `pruebas_cierre.py` | **Nuevo.** 11 pruebas de Ctrl+C / fin de entrada con fallo de guardado y de `ejecutar()` sin pedir contraseña. |
| `pruebas_revision.py` | Se ajusta la prueba de Ctrl+C que llama a `ejecutar()`: simula el login, bloquea `getpass` (si pidiera contraseña, la prueba falla) y comprueba el menú y los datos. |
| `.gitignore`, `README.md` | `credenciales.json` ignorado; documentación del inicio de sesión. |

## Cierre cuando falla el guardado (corrección del PR #4)
Antes: Ctrl+C terminaba sin reintentar guardar; el fin de entrada reintentaba pero terminaba igual aunque fallara.
Ahora, con cambios pendientes por un error de escritura previo:
- **Ctrl+C y fin de entrada** reintentan el guardado.
- Si el reintento funciona: se conservan los cambios y la salida es normal (código 0).
- Si el reintento falla (o se interrumpe): se muestra `ERROR: los cambios recientes NO se guardaron en '<ruta>'`, `Programa finalizado con errores.` y el código de salida es **1**. No aparece `Programa finalizado.` como si todo hubiera ido bien.
- Sin cambios pendientes no hay reintento y la salida es normal.
- Si no se pueden cargar los datos al iniciar, `main()` devuelve error y `ejecutar()` sale con código 1.

## Cantidad de pruebas (medida, no estimada)
| Escenario | Pruebas | Resultado |
|---|---:|---|
| Esta rama sola (`main` + #4, sin `pruebas_revision.py`) | 117 (75 + 31 + 11) | OK |
| Esta rama + las 8 de `pruebas_revision.py` de #5 | 125 | OK |

Estas cifras son parciales: el total definitivo se publica después de integrar #5 → #4 → #3 y ejecutar `python -m unittest discover -p "pruebas*.py"` sobre `main` ya integrado (incluyendo lo que se mueva desde `docs/`). Las evidencias de "114 pruebas" no corresponden a ninguna rama actual.

## Configurar la cuenta del administrador
1. `python autenticacion.py` (usuario, contraseña de mínimo 8 caracteres y repetirla; si ya existe cuenta, pide la actual).
2. `python main.py` e ingresar. Si no hay cuenta, ofrece crearla. Contraseña olvidada: borrar `credenciales.json` y repetir el paso 1.

## Límites conocidos
Un solo administrador, sin roles; el bloqueo por intentos vale por ejecución; la contraseña protege el acceso al programa, no cifra `documentos.txt`.
