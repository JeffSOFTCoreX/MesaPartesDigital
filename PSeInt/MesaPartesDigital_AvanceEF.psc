// MODELO ACADEMICO: las operaciones sobre documentos se realizan en memoria.
// GuardarDatos simula el resultado del guardado; Python escribe documentos.txt.

SubProceso MostrarMenu(titulo)
    Escribir "=== ", titulo, " ==="
    Escribir "1 Registrar | 2 Buscar | 3 Listar"
    Escribir "4 Filtrar | 5 Pendientes | 6 Actualizar"
    Escribir "7 Ordenar | 8 Guardar | 9 Salir"
FinSubProceso

SubProceso MostrarUno(datos, fila)
    Escribir "Codigo: ", datos[fila,1], " | Tipo: ", datos[fila,2]
    Escribir "Usuario: ", datos[fila,3], " | Fecha: ", datos[fila,4]
    Escribir "Estado: ", datos[fila,5]
FinSubProceso

SubProceso Localizar(datos, total, codigo, posicion Por Referencia)
    Definir i Como Entero
    posicion <- 0
    Si total > 0 Entonces
        Para i <- 1 Hasta total Con Paso 1 Hacer
            Si Mayusculas(datos[i,1]) = Mayusculas(codigo) Entonces
                posicion <- i
            FinSi
        FinPara
    FinSi
FinSubProceso

SubProceso Registrar(datos, total Por Referencia, cambio Por Referencia)
    Definir codigo, tipo, usuario, fecha Como Cadena
    Definir posicion Como Entero
    cambio <- Falso
    Si total < 100 Entonces
        Escribir "Codigo del documento:" 
        Leer codigo
        Localizar(datos, total, codigo, posicion)
        Si posicion <> 0 Entonces
            Escribir "Error: codigo duplicado"
        SiNo
            Escribir "Tipo:" 
            Leer tipo
            Escribir "Usuario:" 
            Leer usuario
            Escribir "Fecha (DD/MM/AAAA):"
            Leer fecha
            Si codigo <> "" Y tipo <> "" Y usuario <> "" Y Longitud(fecha) = 10 Entonces
                total <- total + 1
                datos[total,1] <- codigo
                datos[total,2] <- tipo
                datos[total,3] <- usuario
                datos[total,4] <- fecha
                datos[total,5] <- "Pendiente"
                cambio <- Verdadero
                Escribir "Expediente registrado"
            SiNo
                Escribir "Error: datos incompletos"
            FinSi
        FinSi
    SiNo
        Escribir "Limite de registros alcanzado"
    FinSi
FinSubProceso

SubProceso Buscar(datos, total)
    Definir codigo Como Cadena
    Definir posicion Como Entero
    Escribir "Codigo a buscar:"
    Leer codigo
    Localizar(datos, total, codigo, posicion)
    Si posicion > 0 Entonces
        MostrarUno(datos, posicion)
    SiNo
        Escribir "Documento no encontrado"
    FinSi
FinSubProceso

SubProceso Listar(datos, total)
    Definir i Como Entero
    Si total = 0 Entonces
        Escribir "No hay documentos"
    SiNo
        Para i <- 1 Hasta total Con Paso 1 Hacer
            MostrarUno(datos, i)
        FinPara
    FinSi
FinSubProceso

SubProceso Filtrar(datos, total)
    Definir tipo, estado Como Cadena
    Definir i, encontrados Como Entero
    Escribir "Tipo (TODOS para omitir filtro):"
    Leer tipo
    Escribir "Estado (TODOS para omitir filtro):"
    Leer estado
    encontrados <- 0
    Si total > 0 Entonces
        Para i <- 1 Hasta total Con Paso 1 Hacer
            Si (Mayusculas(tipo) = "TODOS" O Mayusculas(datos[i,2]) = Mayusculas(tipo)) Y (Mayusculas(estado) = "TODOS" O Mayusculas(datos[i,5]) = Mayusculas(estado)) Entonces
                MostrarUno(datos, i)
                encontrados <- encontrados + 1
            FinSi
        FinPara
    FinSi
    Escribir "Coincidencias: ", encontrados
FinSubProceso

SubProceso VerPendientes(datos, total)
    Definir i, pendientes, enProceso, atendidos Como Entero
    pendientes <- 0
    enProceso <- 0
    atendidos <- 0
    Si total > 0 Entonces
        Para i <- 1 Hasta total Con Paso 1 Hacer
            Segun datos[i,5] Hacer
                "Pendiente":
                    pendientes <- pendientes + 1
                "En proceso":
                    enProceso <- enProceso + 1
                "Atendido":
                    atendidos <- atendidos + 1
            FinSegun
        FinPara
    FinSi
    Escribir "Total: ", total, " | Pendientes: ", pendientes
    Escribir "En proceso: ", enProceso, " | Atendidos: ", atendidos
    Si total > 0 Entonces
        Para i <- 1 Hasta total Con Paso 1 Hacer
            Si datos[i,5] = "Pendiente" Entonces
                MostrarUno(datos, i)
            FinSi
        FinPara
    FinSi
FinSubProceso

SubProceso Actualizar(datos, total, cambio Por Referencia)
    Definir codigo Como Cadena
    Definir posicion, nuevoEstado Como Entero
    cambio <- Falso
    Escribir "Codigo del documento:"
    Leer codigo
    Localizar(datos, total, codigo, posicion)
    Si posicion > 0 Entonces
        Escribir "Estado actual: ", datos[posicion,5]
        Escribir "1 Pendiente | 2 En proceso | 3 Atendido"
        Leer nuevoEstado
        Segun nuevoEstado Hacer
            1:
                datos[posicion,5] <- "Pendiente"
                cambio <- Verdadero
            2:
                datos[posicion,5] <- "En proceso"
                cambio <- Verdadero
            3:
                datos[posicion,5] <- "Atendido"
                cambio <- Verdadero
            De Otro Modo:
                Escribir "Estado no valido"
        FinSegun
        Si cambio Entonces
            Escribir "Estado actualizado"
        FinSi
    SiNo
        Escribir "Documento no encontrado"
    FinSi
FinSubProceso

SubProceso Ordenar(datos, total, cambio Por Referencia)
    Definir criterio, claveA, claveB, auxiliar Como Cadena
    Definir i, j, k Como Entero
    cambio <- Falso
    Escribir "Ordenar por codigo o fecha:"
    Leer criterio
    criterio <- Minusculas(criterio)
    Si criterio = "codigo" O criterio = "fecha" Entonces
        Si total > 1 Entonces
            Para i <- 1 Hasta total - 1 Con Paso 1 Hacer
                Para j <- i + 1 Hasta total Con Paso 1 Hacer
                    Si criterio = "codigo" Entonces
                        claveA <- Minusculas(datos[i,1])
                        claveB <- Minusculas(datos[j,1])
                    SiNo
                        claveA <- SubCadena(datos[i,4],6,9) + SubCadena(datos[i,4],3,4) + SubCadena(datos[i,4],0,1)
                        claveB <- SubCadena(datos[j,4],6,9) + SubCadena(datos[j,4],3,4) + SubCadena(datos[j,4],0,1)
                    FinSi
                    Si claveA > claveB Entonces
                        Para k <- 1 Hasta 5 Con Paso 1 Hacer
                            auxiliar <- datos[i,k]
                            datos[i,k] <- datos[j,k]
                            datos[j,k] <- auxiliar
                        FinPara
                        cambio <- Verdadero
                    FinSi
                FinPara
            FinPara
        FinSi
        Escribir "Ordenamiento terminado"
    SiNo
        Escribir "Criterio no valido"
    FinSi
FinSubProceso

SubProceso GuardarDatos(cambios Por Referencia)
    Definir respuesta Como Cadena
    Escribir "SIMULACION de guardado: S correcto / N error"
    Leer respuesta
    Si Mayusculas(respuesta) = "S" Entonces
        cambios <- Falso
        Escribir "Guardado correcto"
    SiNo
        Escribir "No se guardo. Cambios pendientes"
    FinSi
FinSubProceso

Algoritmo MesaPartesDigitalEF
    Definir datos Como Cadena
    Definir total, opcion Como Entero
    Definir cambios, salir, modificado Como Logico
    Definir respuesta Como Cadena
    Dimension datos[101,6]
    total <- 0
    cambios <- Falso
    salir <- Falso
    Escribir "Modelo PSeInt: los datos se mantienen en memoria"
    Repetir
        MostrarMenu("MESA DE PARTES DIGITAL")
        Escribir "Seleccione una opcion:"
        Leer opcion
        modificado <- Falso
        Segun opcion Hacer
            1:
                Registrar(datos, total, modificado)
            2:
                Buscar(datos, total)
            3:
                Listar(datos, total)
            4:
                Filtrar(datos, total)
            5:
                VerPendientes(datos, total)
            6:
                Actualizar(datos, total, modificado)
            7:
                Ordenar(datos, total, modificado)
            8:
                GuardarDatos(cambios)
            9:
                Si cambios Entonces
                    Escribir "Cambios sin guardar. Reintentar? (S/N)"
                    Leer respuesta
                    Si Mayusculas(respuesta) = "S" Entonces
                        GuardarDatos(cambios)
                    FinSi
                FinSi
                Si NO cambios Entonces
                    salir <- Verdadero
                FinSi
            De Otro Modo:
                Escribir "Opcion no valida"
        FinSegun
        Si modificado Entonces
            cambios <- Verdadero
            GuardarDatos(cambios)
        FinSi
    Hasta Que salir
    Escribir "Programa finalizado"
FinAlgoritmo
