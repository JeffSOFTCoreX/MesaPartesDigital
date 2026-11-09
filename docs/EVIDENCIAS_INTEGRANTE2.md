# Evidencias – Integrante 2: Revisión del sistema y corrección de errores

Cada corrección se probó **antes** (código original) y **después** (código corregido) ejecutando el programa real. Las capturas son la salida de consola.

## Corrección 1: Ruta del archivo dependía de la carpeta de ejecución
- **Archivo modificado:** `main.py`
- **Escenario:** Se registra EXP01 y luego se ejecuta el programa desde otra carpeta.

**Antes**
```
Expedientes registrados : 0
Archivos creados en la otra carpeta: ['documentos.txt']
```

**Después**
```
Expedientes registrados : 1
Archivos creados en la otra carpeta: ninguno
```

## Corrección 2: Archivo con BOM: el primer expediente no se encontraba
- **Archivo modificado:** `archivo.py`
- **Escenario:** documentos.txt guardado como 'UTF-8 con BOM'; se consulta EXP01 (opción 2).

**Antes**
```
No se encontró ningún documento con el código 'EXP01'.
```

**Después**
```
Código: EXP01
```

## Corrección 3: Cambiar al mismo estado reescribía el archivo
- **Archivo modificado:** `actualizacion.py`
- **Escenario:** Se pasa EXP01 a 'En proceso' y se repite la misma operación.

**Antes**
```
Cambios guardados automáticamente.
Estado actualizado a 'En proceso'.
Cambios guardados automáticamente.
```

**Después**
```
Estado actualizado a 'En proceso'.
Cambios guardados automáticamente.
El documento ya está en estado 'En proceso'. No hay cambios.
```

## Corrección 4: Ctrl+D / Ctrl+C mostraban un traceback
- **Archivo modificado:** `main.py`
- **Escenario:** Se corta la entrada en el menú (Ctrl+D en Linux/Mac, Ctrl+Z+Enter en Windows; Ctrl+C).

**Antes**
```
EOFError: EOF when reading a line
```

**Después**
```
Entrada finalizada. Programa finalizado.
Programa interrumpido por el usuario.
```

## Corrección 5: Archivo editado a mano impedía iniciar el programa
- **Archivo modificado:** `archivo.py`
- **Escenario:** documentos.txt con espacios alrededor de | y estado 'pendiente' en minúsculas.

**Antes**
```
No se pudieron cargar los registros: Se detectaron 1 registro(s) inválido(s) o duplicado(s) en documentos.txt. Revise el archivo antes de continuar. No se modificaron los datos.
El programa no se iniciará para evitar sobrescribir los datos existentes.
```

**Después**
```
Código: EXP01
Estado: Pendiente
```

## Corrección 6: Filtro por tipo sensible a tildes
- **Archivo modificado:** `consulta.py`
- **Escenario:** Opción 4, tipo escrito 'matricula' (sin tilde) y estado vacío.

**Antes**
```
No existen registros que cumplan los criterios seleccionados.
```

**Después**
```
Expedientes encontrados: 1
```

## Corrección 7: Código vacío pedía todos los datos antes de avisar
- **Archivo modificado:** `registro.py`
- **Escenario:** Opción 1 con el código en blanco.

**Antes**
```
Preguntas hechas: 4 de 4
No se pudo registrar: El campo 'codigo' es obligatorio.
```

**Después**
```
Preguntas hechas: 1 de 4
No se pudo registrar: El campo 'codigo' es obligatorio.
```

## Corrección 8: Orden por código alfabético (EXP10 antes que EXP2)
- **Archivo modificado:** `archivo.py`
- **Escenario:** Se registran EXP2, EXP10, EXP1 y se ordena por código (opción 7).

**Antes**
```
Orden resultante (opción 3): EXP1, EXP10, EXP2
```

**Después**
```
Orden resultante (opción 3): EXP1, EXP2, EXP10
```

## Corrección 9: La opción 7 no mostraba el resultado
- **Archivo modificado:** `main.py`
- **Escenario:** Opción 7, criterio 'codigo'.

**Antes**
```
Registros ordenados correctamente.
No se muestra la lista
```

**Después**
```
Registros ordenados correctamente.
La lista ordenada se muestra en pantalla
```

## Corrección 10: Espacios internos se guardaban tal cual
- **Archivo modificado:** `registro.py`
- **Escenario:** Nombre ingresado como '  Ana    Pérez  '.

**Antes**
```
documentos.txt → X1|Matrícula|Ana    Pérez|01/01/2026|Pendiente
```

**Después**
```
documentos.txt → X1|Matrícula|Ana Pérez|01/01/2026|Pendiente
```

## Corrección 11: Límite de longitud: solo para registros nuevos, sin afectar datos existentes
- **Archivo modificado:** `validacion.py / registro.py`
- **Escenario:** Se intenta registrar un nombre de 5000 caracteres y se inicia el programa con un documentos.txt que ya tenía un nombre de 150 caracteres.

**Antes**
```
Nuevo registro con nombre de 5000 caracteres → registrado correctamente con estado 'Pendiente'.
Archivo existente con nombre de 150 caracteres → Expedientes registrados : 1
documentos.txt conserva el nombre de 150 caracteres: True
```

**Después**
```
Nuevo registro con nombre de 5000 caracteres → No se pudo registrar: El campo 'estudiante' supera los 100 caracteres permitidos.
Archivo existente con nombre de 150 caracteres → Expedientes registrados : 1
documentos.txt conserva el nombre de 150 caracteres: True
```

## Corrección 12: Una sola regla para comparar códigos (registro, búsqueda y carga)
- **Archivo modificado:** `normalizacion.py, busqueda.py, registro.py, archivo.py`
- **Escenario:** Se registra el código 'A  1' (dos espacios) y se busca como 'A 1' y como 'a   1'.

**Antes**
```
documentos.txt → A  1|T|Ana|01/01/2026|Pendiente
No se encontró ningún documento con el código 'A 1'.
No se encontró ningún documento con el código 'a   1'.
```

**Después**
```
documentos.txt → A 1|T|Ana|01/01/2026|Pendiente
Código: A 1
Código: A 1
```
