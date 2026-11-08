# Integrante 1 – Inicio de sesión y autenticación
Proyecto: MesaPartesDigital (consola, Python). Trabajado sobre `MesaPartesDigital_corregido.zip` (versión con las correcciones del Integrante 2).

## Archivos
| Archivo | Cambio |
|---|---|
| `autenticacion.py` | **Nuevo.** Hash, verificación, configuración de cuenta, inicio de sesión con límite de intentos. |
| `main.py` | `ejecutar()` pide login antes del menú; `main(usuario=None)`; opción **[10] Cerrar sesión**; el encabezado muestra el administrador. Ninguna función anterior se eliminó. |
| `pruebas_autenticacion.py` | **Nuevo.** 31 pruebas. |
| `pruebas_revision.py` | 1 prueba ajustada (la de Ctrl+C llama a `ejecutar()`, que ahora pasa por el login: se simula sesión iniciada). |
| `.gitignore` | Se agrega `credenciales.json`. |
| `README.md` | Opción 10, estructura, tabla de pruebas, sección de autenticación. |

## Diseño
- Hash **PBKDF2-HMAC-SHA256**, 200 000 iteraciones, sal aleatoria de 16 bytes (biblioteca estándar, sin instalar nada).
- Comparación con `hmac.compare_digest`; mensaje único "Usuario o contraseña incorrectos".
- Contraseña con `getpass` (no se ve al escribir). Mínimo 8 caracteres al crearla.
- 3 intentos; luego se termina el programa. Archivo de credenciales dañado → acceso denegado.
- Guardado de credenciales con temporal + `os.replace`.

## Configurar la cuenta del administrador
1. `python autenticacion.py`
2. Escribir usuario, contraseña y repetirla. (Si ya existe cuenta, pide la actual.)
3. `python main.py` e ingresar.
Si `main.py` se abre sin cuenta, ofrece crearla. Contraseña olvidada: borrar `credenciales.json` y repetir el paso 1.

## Resultado
114 pruebas en `OK` (83 previas + 31 nuevas). Además se probó el programa real en terminal: configuración, 3 intentos fallidos, ingreso, registro, cerrar sesión, reingreso y persistencia de expedientes.

## Pendiente para Integrante 3 / 4
- Las capturas de Evidencias_EF muestran el menú de 9 opciones y "75 pruebas": quedan desactualizadas (ahora 10 opciones y 114 pruebas).
- No se tocaron `docs/`, PSeInt ni el informe.
