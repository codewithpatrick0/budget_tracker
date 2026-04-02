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