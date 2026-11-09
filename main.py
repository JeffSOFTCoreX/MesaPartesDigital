"""Menú principal del prototipo de mesa de partes digital."""



import sys

from pathlib import Path



from archivo import cargar_archivo, guardar_archivo, ordenar_registros

from registro import registrar_documento

from busqueda import buscar_documento

from consulta import (

    consultar_documento, mostrar_registros, consultar_por_filtros,

    consultar_pendientes,

)

from actualizacion import actualizar_estado

from autenticacion import iniciar_sesion



# Ruta fija junto a main.py: así los expedientes se encuentran sin importar

# desde qué carpeta se ejecute el programa.

ARCHIVO_DATOS = str(Path(__file__).resolve().parent / "documentos.txt")



# Valores de control del flujo de autenticación y persistencia.

CERRAR_SESION = "cerrar_sesion"

ERROR_PERSISTENCIA = "error_persistencia"





def guardar_automaticamente(registros):
    
    """Intenta persistir la lista; el menú administra los cambios pendientes."""
    
    try:
        
        guardar_archivo(registros, ARCHIVO_DATOS)
        
    except (OSError, UnicodeError, ValueError) as error:
        
        print(f"No se pudieron guardar los cambios: {error}")
        
        return False
        


    print("Cambios guardados automáticamente.")
    
    return True
    




def resolver_cambios_pendientes(registros):
    
    """Último intento de guardado al salir con cambios sin persistir."""
    
    print("Hay cambios sin guardar. Reintentando el guardado antes de salir...")
    
    try:
        
        guardado = guardar_automaticamente(registros)
        
    except KeyboardInterrupt:
        
        print("Reintento de guardado interrumpido.")
        
        guardado = False
        
    if not guardado:
        
        print("ERROR: los cambios recientes NO se guardaron en "
              
              f"'{ARCHIVO_DATOS}'.")
        
        print("Revise el archivo o la carpeta y vuelva a registrar esos cambios.")
        
    return guardado
    




def mostrar_encabezado(registros, usuario=None):
    
    """Muestra el encabezado y un resumen actualizado de los expedientes."""
    
    total = len(registros)
    
    pendientes = sum(r["estado"] == "Pendiente" for r in registros)
    
    en_proceso = sum(r["estado"] == "En proceso" for r in registros)
    
    atendidos = sum(r["estado"] == "Atendido" for r in registros)
    


    print("\n" + "=" * 62)
    
    print("                 MESA DE PARTES DIGITAL")
    
    print("                  ACADEMIA MAGNA PERPETUA")
    
    print("=" * 62)
    
    if usuario:
        
        print(f"  Administrador           : {usuario}")
        
    print(f"  Expedientes registrados : {total}")
    
    print(f"  Pendientes              : {pendientes}")
    
    print(f"  En proceso              : {en_proceso}")
    
    print(f"  Atendidos               : {atendidos}")
    
    print("-" * 62)
    




def mostrar_menu():
    
    print("\n  MENÚ PRINCIPAL")
    
    print("  " + "-" * 40)
    
    print("  GESTIÓN DE DOCUMENTOS")
    
    print("   [1] Registrar documento")
    
    print("   [2] Consultar documento por código")
    
    print("   [3] Mostrar todos los registros")
    
    print("   [4] Consultar por tipo y/o estado")
    
    print("   [5] Consultar expedientes pendientes")
    
    print()
    
    print("  ADMINISTRACIÓN")
    
    print("   [6] Actualizar estado")
    
    print("   [7] Ordenar registros")
    
    print("   [8] Guardar registros")
    
    print()
    
    print("   [9] Salir")
    
    print("  [10] Cerrar sesión")
    
    print("  " + "-" * 40)
    




def main(usuario=None):
    
    """Ejecuta el menú para un usuario autenticado."""
    
    try:
        
        registros = cargar_archivo(ARCHIVO_DATOS)
        
    except (OSError, UnicodeError, ValueError) as error:
        
        print(f"No se pudieron cargar los registros: {error}")
        
        print("El programa no se iniciará para evitar sobrescribir los datos existentes.")
        
        return 































































