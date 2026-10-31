# Guardado protegido y recuperación

## Funcionamiento

Todos los guardados usan `guardar_archivo`: registro automático, actualización
automática, ordenamiento cuando cambia el orden y opción 8. La opción 9 cierra sin escribir si no hay cambios pendientes; ante un guardado fallido, advierte y ofrece reintentar antes de permitir la salida normal.

1. Preparar el contenido completo sin abrir el archivo principal para escritura.
2. Escribir un temporal único en la misma carpeta; ejecutar flush y fsync y cerrarlo.
3. Si existe el principal, copiar sus bytes a otro temporal, sincronizarlo y
   reemplazar el respaldo `documentos.txt.bak` mediante os.replace.
4. Reemplazar el principal mediante os.replace con el temporal ya completo.
5. Limpiar los temporales restantes al terminar o ante un error controlable.

El principal no se vacía previamente. Si falla la preparación, la escritura o
la sincronización, se propaga el error y se conserva el principal anterior.
Si falla el respaldo, tampoco se reemplaza el principal. Si el reemplazo final
falla, el principal conserva la versión anterior y el respaldo ya contiene esa
misma versión. El principal y el respaldo no se actualizan como una transacción
única: pueden existir estados intermedios entre ambos reemplazos.

El respaldo contiene la versión inmediatamente anterior al intento de reemplazo;
se renueva en cada guardado sobre un archivo existente, incluso sin cambios.
En el primer guardado, si el principal no existe, no se inventa un respaldo.
Si la aplicación creó previamente un archivo vacío, ese puede ser el primer
contenido respaldado. Los datos y temporales habituales se excluyen en .gitignore.

## Recuperación manual

1. Cerrar todas las ejecuciones del programa.
2. Copiar el principal dañado a otro nombre para conservarlo antes de intervenir.
3. Revisar `documentos.txt.bak` y comprobar que contiene los registros esperados.
4. Copiar el respaldo a `documentos.txt` en la carpeta desde la que se ejecuta
   el programa. Conservar también el respaldo original.
5. Iniciar el programa; la carga valida campos, fechas, estados y duplicados.

No se restaura automáticamente para evitar ocultar problemas o reemplazar datos
sin revisión. El respaldo puede ser una versión anterior, no necesariamente la
última que se veía en pantalla. Los cambios que nunca se guardaron no aparecen
en el respaldo. Este mecanismo tampoco sustituye copias en otro dispositivo.

## Verificación y límites

El avance EF terminó con 75 pruebas aprobadas: 61 heredadas del ZIP mejorado y 14 adicionales (pruebas_avance_ef.py). Se verificaron escritura parcial
simulada, error de creación de temporal, error de fsync, fallo del reemplazo del
respaldo, fallo del reemplazo principal, primera escritura, respaldo exacto,
rotación de versión previa, lista vacía y fallo inicial sin publicar un archivo.
En los fallos simulados el principal conserva sus bytes y se limpian temporales.

La sustitución en la misma carpeta permite usar el reemplazo del sistema operativo
sin transferir entre discos. La protección depende del sistema de archivos.
No se garantiza supervivencia absoluta frente a corte de energía, avería física,
eliminación externa ni dos procesos guardando a la vez. No se sincroniza
explícitamente el directorio. Un cierre forzado puede dejar temporales huérfanos;
se pueden borrar con la aplicación cerrada tras revisar el principal y el respaldo.
Los errores de limpieza no ocultan el error original. No se hicieron pruebas de
corte físico de energía ni de avería de hardware.
