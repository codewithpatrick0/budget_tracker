"""
BUDGET TRACKER - Sistema de Gestión de Gastos y Ahorros
========================================================

Este módulo contiene la interfaz principal (menú) de la aplicación.
Permite a los usuarios interactuar con el sistema de gastos mediante
un menú de terminal interactivo.

Funcionalidades:
    - Agregar nuevos gastos con validación
    - Ver gastos registrados
    - Filtrar por categoría
    - Eliminar gastos
    - Salir de la aplicación

Autor: Patrick
Fecha: 2026-04-02
"""

from src.db import crear_tablas
from src.gestor import (
    agregar_gasto,
    obtener_todos_gastos,
    obtener_gastos_por_categoria,
    obtener_gasto_por_id,
    eliminar_gasto,
    obtener_resumen_mensual
)

#Inicializar laa base de datos (crear tablas si aun no hay)
crear_tablas()

#FUNCIONES PARA EL MAIN
def mostrar_menu() :

    #MENU PRINCIPAL
    print("\n" +"=" * 50)
    print("BIENVENIDO A BUDGET TRACKER 💰")
    print("=" * 50)
    print("\n Opciones Disponibles : \n")
    print("   1. ➕ Agregar un nuevo gasto")
    print("   2. 📋 Ver todos los gastos")
    print("   3. 🏷️  Ver gastos por categoría")
    print("   4. 🗑️  Eliminar un gasto")
    print("   5. 📊 Ver resumen mensual")
    print("   6. ❌ Salir del programa")
    print("\n" + "="*50)

def seleccionar_opcion():
    while True:
        try:
            # Pedimos el dato
            opcion = int(input("Selecciona una opción (1-6): "))
            
            # Validamos el rango
            if 1 <= opcion <= 6:
                return opcion
            else:
                print("Error: Opción inválida. Debe estar entre 1 y 6.")
                
        except ValueError:
            print("Error: Debes ingresar un número entero.")

def validar_monto() :
    while True :
        try :
            monto = float(input("Ingresa el monto : "))
            if monto < 1 :
                print("El monto debe ser mayor a 0")
                continue
            return monto
        except ValueError :
            print("El monto debe ser un número entero o decimal")

def validar_categoria() :
    while True :   
        categoria = str(input("Escribe la categoría : ")).strip()

        if not categoria :
            print("La categoría no puede estar vacía")
            continue
        if any(char.isdigit() for char in categoria) :
            print("La categoría no puede contener números")
            continue
        
        return categoria
            
def validar_descripcion() :
    while True :    
        descripcion = str(input("Ingresa la descripción (Opcional) : ")).strip()

        if len(descripcion) >= 60 :
            print("Esta descripción sobrepasa el límite de carácteres (60)")
            continue

        if not descripcion :
            descripcion = "Sin descripción"
        
        return descripcion
    
def agregar_gasto_menu() :
    print("\n--- AGREGAR NUEVO GASTO ---")
    try :
    # Obtener y validar monto
        monto = validar_monto()
        
        # Obtener y validar categoría
        categoria = validar_categoria()
        
        # Obtener y validar descripción
        descripcion = validar_descripcion()
        
        # Guardar en base de datos
        agregar_gasto(monto, categoria, descripcion)
        
    except Exception as e:
        print(f"❌ Error al agregar gasto: {str(e)}")
        
def obtener_todos_gastos_menu() :
    print("\n---OBTENIENDO TODOS LOS GASTOS...---")
    gastos = obtener_todos_gastos()
    
    if not gastos :
        print("Aún no tienes gastos registrados")
        return
    
    #Header
    print(f"\n{'ID':<5} {'Monto':<10} {'Categoria':<15} {'Fecha':<20} {'Descripción':<30}")
    print("="*85)
    
    #Contenido
    for gasto in gastos :
        fecha_fmt = gasto.fecha.strftime("%d/%m/%Y %H:%M")
        descripcion_corta = (
            gasto.descripcion[:30] + "..."
            if gasto.descripcion and len(gasto.descripcion) > 33
            else "Sin descripción"
        )   
        print(f"{gasto.id:<5} S/{gasto.monto:<9.2f} {gasto.categoria:<15} {fecha_fmt:<20} {descripcion_corta:<30}")
        print(f"\n📊 Total de gastos: {len(gastos)}")
        
def ver_gastos_por_categoria() :
    print("\n--- VER GASTOS POR CATEGORÍA ---")
    
    categoria = validar_categoria()
    
    gastos = obtener_gastos_por_categoria(categoria)
    
    if not gastos :
        print(f"No hay gastos registrados en la categoría {categoria}")
        return
    
    print(f"\n📋Gastos de la categoría {categoria} : \n")
    print(f"{'ID':<5} {'Monto':<10} {'Categoria':<15} {'Fecha':<20} {'Descripcion':<30}")
    print("="*70)
    
    total_categoria = 0
    for gasto in gastos :
        fecha_fmt = gasto.fecha.strftime("%d/%m/%Y %H/%M")
        descripcion_corta = (
            gasto.descripcion[:30] + "..."
            if gasto.descripcion and len(gasto.descripcion) > 33
            else "Sin descripción"
        ) 
        print(f"{gasto.id:<5} S/{gasto.monto:<9.2f} {gasto.categoria:<15} {fecha_fmt:<20} {descripcion_corta:<30}")
        print("="*70)
        
        total_categoria += gasto.monto
        
    print(f"\n💰 Total en {categoria}: S/{total_categoria:.2f}")
    print(f"📊 Cantidad de gastos: {len(gastos)}")
    
def eliminar_gasto_menu() :
    gastos = obtener_todos_gastos()
    
    if not gastos:
        print("ℹ️  No hay gastos registrados para eliminar")
        return
    
    print("\n📋 Gastos disponibles:\n")
    print(f"{'ID':<5} {'Monto':<10} {'Categoría':<15} {'Descripción':<30}")
    print("="*65)
    
    for gasto in gastos:
        descripcion_corta = gasto.descripcion[:28] if gasto.descripcion else "Sin descripción"
        print(f"{gasto.id:<5} S/{gasto.monto:<9.2f} {gasto.categoria:<15} {descripcion_corta:<30}")
        
    try :
        gasto_id = int(input("Introduce ID del gasto a eliminar : "))
        gasto = obtener_gasto_por_id(gasto_id)
        
        if not gasto :
            print(f"No se encontró gasto con el ID {gasto_id}")
            return 
        
        print(f"\n⚠️  Vas a eliminar:")
        print(f"   ID: {gasto.id} | Monto: S/{gasto.monto} | Categoría: {gasto.categoria}")
        
        confirmacion = input(f"¿Estas seguro de eliminar el gasto con ID {gasto_id}").strip().lower()
        
        if confirmacion == "sí" or confirmacion == "si" :
            eliminar_gasto(gasto_id)
        else :
            print("Elimiación cancelada")
        
    except ValueError :
        print("Debes ingresar un ID válido (ENTERO)")
        