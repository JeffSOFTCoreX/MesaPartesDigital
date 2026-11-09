# Integrante 2 – Revisión del sistema y corrección de errores (PR #5)

Describe exactamente lo que contiene la rama. Cada cambio se probó antes (código de `main`) y después ejecutando el programa real: ver `EVIDENCIAS_INTEGRANTE2.md`.

## Correcciones
| # | Problema | Solución | Archivo |
|---|---|---|---|
| 1 | Ejecutado desde otra carpeta, `documentos.txt` se creaba vacío allí y los expedientes "desaparecían". | Ruta fija junto a `main.py`. | `main.py` |
| 2 | Un `documentos.txt` con BOM impedía encontrar el primer expediente. | Lectura con `utf-8-sig`. | `archivo.py` |
| 3 | Cambiar al mismo estado reescribía el archivo y pisaba el `.bak`. | Aviso "ya está en ese estado", sin guardar. | `actualizacion.py` |
| 4 | Ctrl+D / Ctrl+C mostraban un traceback. | Punto de entrada `ejecutar()`: Ctrl+C y fin de entrada salen con mensaje. | `main.py` |
| 5 | Un `documentos.txt` editado a mano (espacios alrededor de `\|`, estado en minúsculas) impedía iniciar. | Se limpian los campos y se normaliza el estado al cargar; un estado inexistente se sigue rechazando. | `archivo.py` |
| 6 | El filtro por tipo distinguía tildes. | Comparación sin tildes. | `consulta.py` |
| 7 | Con código vacío se pedían todos los datos antes de avisar. | Aviso inmediato. | `registro.py` |
| 8 | Orden por código alfabético (`EXP10` antes que `EXP2`). | Orden natural. | `archivo.py` |
| 9 | La opción 7 no mostraba el resultado del orden. | Muestra la lista ordenada. | `main.py` |
| 10 | Espacios internos se guardaban (`Ana    Pérez`). | Se normalizan al registrar. | `registro.py` |
| 11 | Campos sin límite de longitud. | Máximo de 100 caracteres **solo para registros nuevos** (`validar_longitudes`). Los datos existentes se cargan y guardan sin truncar. | `validacion.py`, `registro.py` |
| 12 | Registrar `A  1` guardaba `A 1`, pero buscar con la entrada original no lo encontraba. | Regla única de comparación de códigos (`normalizacion.clave_codigo`) usada por registro, búsqueda, carga y guardado. | `normalizacion.py` (nuevo), `busqueda.py`, `registro.py`, `archivo.py` |

## Decisiones de compatibilidad
- **Límite de 100 caracteres:** no está en `validar_datos`, que también se usa al cargar y guardar. Un archivo válido para la versión anterior sigue cargando; no se trunca ni se pierde nada.
- **Códigos:** al cargar no se modifica el valor guardado (solo se recorta el borde). Dos códigos que difieren únicamente en espacios internos o mayúsculas ahora cuentan como duplicados al cargar, igual que ya ocurría con las mayúsculas; en ese caso el programa avisa y no modifica el archivo.

## Pruebas
- Pruebas propias de esta rama: **25** (`pruebas_revision.py`: 8, `pruebas_mejoras.py`: 17), ubicadas en la raíz junto a las demás para que las encuentre `python -m unittest discover -p "pruebas*.py"`.
- Resultado total de la suite: **Ran 100 tests ... OK** (comando: `py -m unittest discover -p "pruebas*.py"`, ejecutado sobre la rama `integrante2`).

## Funcionalidades revisadas (se conservan todas)
Menú principal, registro, búsqueda por código, consulta por filtros, actualización de estados, ordenamiento, almacenamiento (temporal + `.bak`), validaciones y persistencia al cerrar y reabrir.

## Fuera de alcance de esta rama
El reintento de guardado al cerrar con cambios pendientes (Ctrl+C / fin de entrada) y la adaptación de las pruebas a la autenticación corresponden al PR #4.
