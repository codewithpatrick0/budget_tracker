"""
BUDGET TRACKER - Sistema Integral de Gestión Financiera
=========================================================

Aplicación para gestionar gastos, ingresos y ahorros.
Sistema modular y escalable con interfaz de terminal.

Módulos principales:
    - Gastos: Registra dinero gastado
    - Ingresos: Registra dinero recibido
    - Ahorros: Gestiona metas de ahorro
    - Reportes: Resúmenes y análisis financiero

Características:
    ✅ Menú principal intuitivo
    ✅ Validación completa de datos
    ✅ Tablas formateadas
    ✅ Resúmenes mensuales
    ✅ Análisis financiero
    ✅ Persistencia en BD SQLite

Autor: Patrick
Fecha: 2026-04-02
Versión: 2.0 (Refactorizada)
"""

# ============= IMPORTS =============
from src.db import crear_tablas
from src.validators import (
    validar_descripcion,
    validar_monto,
    validar_nombre,
    obtener_opcion
)
from src.formatters import (
    mostrar_desgloze,
    mostrar_resumen_financiero,
    mostrar_tabla_ahorros,
    mostrar_encabezado,
    mostrar_tabla_gastos,
    mostrar_tabla_ingresos
)
from src.utils import pausar, calcular_balance
# Imports de Gestor de Gastos
from src.gestor_gastos import (
    agregar_gasto,
    obtener_todos_gastos,
    obtener_gastos_por_categoria,
    obtener_gasto_por_id,
    eliminar_gasto,
    obtener_resumen_mensual as obtener_resumen_gastos
)

# Imports de Gestor de Ingresos
from src.gestor_ingresos import (
    agregar_ingreso,
    obtener_todos_ingresos,
    obtener_ingresos_por_fuente,
    obtener_ingreso_por_id,
    eliminar_ingreso,
    obtener_resumen_ingresos
)

# Imports de Gestor de Ahorros
from src.gestor_ahorros import (
    agregar_ahorro,
    obtener_todos_ahorros,
    obtener_ahorros_por_meta,
    obtener_ahorro_por_id,
    eliminar_ahorro,
    obtener_resumen_ahorro_por_meta
)


# ============= MENÚ PRINCIPAL =============

def mostrar_menu_principal() :
    
    mostrar_encabezado("BUDGET TRACKER 💰", 60)
    print("\n   MENÚ PRINCIPAL\n")
    print("   1. 🛒 Gestión de Gastos")
    print("   2. 💵 Gestión de Ingresos")
    print("   3. 🏦 Gestión de Ahorros")
    print("   4. 📊 Reportes Financieros")
    print("   5. ❌ Salir del Programa")
    print("\n" + "="*60)
    
# ============= SECCIÓN GASTOS =============
def mostrar_menu_gastos() :
    mostrar_encabezado("GESTIÓN DE GASTOS", 60)
    print("\n   OPCIONES:\n")
    print("   1. ➕ Agregar un nuevo gasto")
    print("   2. 📋 Ver todos los gastos")
    print("   3. 🏷️  Ver gastos por categoría")
    print("   4. 🗑️  Eliminar un gasto")
    print("   5. 📊 Resumen mensual de gastos")
    print("   6. ↩️  Volver al menú principal")
    print("\n" + "="*60)
    
def agregar_gasto_menu() :
    mostrar_encabezado("➕ AGREGAR NUEVO GASTO", 60)
    
    try :
        monto = validar_monto()
        categoria = validar_nombre()
        descripcion = validar_descripcion()
        
        agregar_gasto(monto, categoria, descripcion)
        pausar()
        
    except Exception as e :
        print(f"❌ Error : {str(e)}")
        pausar()