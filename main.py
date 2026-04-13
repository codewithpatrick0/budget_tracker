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
    mostrar_desglose,
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
        
def ver_todos_gastos_menu() :
    mostrar_encabezado("VER TODOS LOS GASTOS 📋", 60)
    
    gastos = obtener_todos_gastos
    mostrar_tabla_gastos(gastos)
    pausar()
    
def ver_gastos_por_categoria_menu() :
    mostrar_encabezado("VER GASTOS POR CATEGORÍA 🏷️", 60)
    
    categoria = validar_nombre("Categoría a buscar : ")
    gastos = obtener_gastos_por_categoria(categoria)
    
    if not gastos :
        print(f"No hay gastos a mostrar en la caategoría {categoria}")
        pausar()
        return
    
    mostrar_tabla_gastos(gastos)
    
    total = sum(g.monto for g in gastos)
    print(f"\n💰 Total en '{categoria}': S/{total:.2f}")
    print(f"📊 Cantidad: {len(gastos)} gasto(s)")
    pausar()
    
def eliminar_gasto_menu() :
    mostrar_encabezado("ELIMINAR GASTO 🗑️", 60)
    
    gastos = obtener_todos_gastos()
    
    if not gastos:
        print("ℹ️  No hay gastos para eliminar")
        pausar()
        return
    
    mostrar_tabla_gastos(gastos)
    
    try:
        gasto_id = int(input("\nID del gasto a eliminar: "))
        gasto = obtener_gasto_por_id(gasto_id)
        
        if not gasto:
            print(f"❌ No se encontró gasto con ID {gasto_id}")
            pausar()
            return
        
        print(f"\n⚠️  Vas a eliminar:")
        print(f"   ID: {gasto.id} | Monto: S/{gasto.monto} | Categoría: {gasto.categoria}")
        
        confirmacion = input("\n¿Confirmas la eliminación? (sí/no): ").strip().lower()
        
        if confirmacion in ["sí", "si"]:
            eliminar_gasto(gasto_id)
        else:
            print("❌ Eliminación cancelada")
            
    except ValueError:
        print("❌ Error: Debes ingresar un ID válido (número)")
    
    pausar()
    
def ver_resumen_gastos_menu() :
    mostrar_encabezado("RESUMEN MENSUAL DE GASTOS 📊", 60)
    
    resumen = obtener_resumen_gastos()
    
    if resumen is None or resumen['cantidad'] == 0 :
        print("ℹ️  No hay gastos registrados este mes")
        pausar()
        return
    
    print("\n" + "="*60)
    print("RESUMEN DEL MES".center(60))
    print("="*60)
    print(f"{'💰 Total':<30} S/{resumen['total']:>20.2f}")
    print(f"{'📊 Cantidad de gastos':<30} {resumen['cantidad']:>20}")
    print(f"{'📈 Promedio por gasto':<30} S/{resumen['promedio']:>20.2f}")
    print("="*60)
    
    if resumen['por_categoria']:
        mostrar_desglose("\nDESGLOSE POR CATEGORÍA", resumen['por_categoria'])
    
    pausar()
    
def flujo_gastos():
    
    while True:
        mostrar_menu_gastos()
        opcion = obtener_opcion(1, 6, "\nSelecciona una opción: ")
        
        if opcion == 1:
            agregar_gasto_menu()
        elif opcion == 2:
            ver_todos_gastos_menu()
        elif opcion == 3:
            ver_gastos_por_categoria_menu()
        elif opcion == 4:
            eliminar_gasto_menu()
        elif opcion == 5:
            ver_resumen_gastos_menu()
        elif opcion == 6:
            break


# ============= SECCIÓN INGRESOS =============

def mostrar_menu_ingresos():
    """
    Menú principal de gestión de ingresos.
    """
    mostrar_encabezado("GESTIÓN DE INGRESOS 💵", 60)
    print("\n   OPCIONES:\n")
    print("   1. ➕ Agregar un nuevo ingreso")
    print("   2. 📋 Ver todos los ingresos")
    print("   3. 🏷️  Ver ingresos por fuente")
    print("   4. 🗑️  Eliminar un ingreso")
    print("   5. 📊 Resumen mensual de ingresos")
    print("   6. ↩️  Volver al menú principal")
    print("\n" + "="*60)


def agregar_ingreso_menu():
    """
    Flujo completo para agregar un ingreso.
    """
    mostrar_encabezado("AGREGAR NUEVO INGRESO ➕", 60)
    
    try:
        # Obtener datos
        monto = validar_monto("Ingresa el monto del ingreso: S/")
        fuente = validar_nombre("Fuente del ingreso (ej: Trabajo, Negocio): ", permitir_numeros=False)
        descripcion = validar_descripcion(max_caracteres=60)
        
        # Guardar en BD
        agregar_ingreso(monto, fuente, descripcion)
        pausar()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        pausar()


def ver_todos_ingresos_menu():
    """
    Muestra todos los ingresos registrados.
    """
    mostrar_encabezado("VER TODOS LOS INGRESOS 📋", 60)
    
    ingresos = obtener_todos_ingresos()
    mostrar_tabla_ingresos(ingresos)
    pausar()


def ver_ingresos_por_fuente_menu():
    """
    Filtra y muestra ingresos por fuente.
    """
    mostrar_encabezado("VER INGRESOS POR FUENTE 🏷️", 60)
    
    fuente = validar_nombre("Fuente a buscar: ", permitir_numeros=False)
    ingresos = obtener_ingresos_por_fuente(fuente)
    
    if not ingresos:
        print(f"ℹ️  No hay ingresos de la fuente '{fuente}'")
        pausar()
        return
    
    mostrar_tabla_ingresos(ingresos)
    
    # Mostrar desglose
    total = sum(i.monto for i in ingresos)
    print(f"\n💰 Total de '{fuente}': S/{total:.2f}")
    print(f"📊 Cantidad: {len(ingresos)} ingreso(s)")
    pausar()


def eliminar_ingreso_menu():
    """
    Permite eliminar un ingreso con confirmación.
    """
    mostrar_encabezado("ELIMINAR INGRESO 🗑️", 60)
    
    ingresos = obtener_todos_ingresos()
    
    if not ingresos:
        print("ℹ️  No hay ingresos para eliminar")
        pausar()
        return
    
    mostrar_tabla_ingresos(ingresos)
    
    try:
        ingreso_id = int(input("\nID del ingreso a eliminar: "))
        ingreso = obtener_ingreso_por_id(ingreso_id)
        
        if not ingreso:
            print(f"❌ No se encontró ingreso con ID {ingreso_id}")
            pausar()
            return
        
        print(f"\n⚠️  Vas a eliminar:")
        print(f"   ID: {ingreso.id} | Monto: S/{ingreso.monto} | Fuente: {ingreso.fuente}")
        
        confirmacion = input("\n¿Confirmas la eliminación? (sí/no): ").strip().lower()
        
        if confirmacion in ["sí", "si"]:
            eliminar_ingreso(ingreso_id)
        else:
            print("❌ Eliminación cancelada")
            
    except ValueError:
        print("❌ Error: Debes ingresar un ID válido (número)")
    
    pausar()


def ver_resumen_ingresos_menu():
    """
    Muestra el resumen mensual de ingresos.
    """
    mostrar_encabezado("RESUMEN MENSUAL DE INGRESOS 📊", 60)
    
    resumen = obtener_resumen_ingresos()
    
    if resumen is None or resumen['cantidad'] == 0:
        print("ℹ️  No hay ingresos registrados este mes")
        pausar()
        return
    
    print("\n" + "="*60)
    print("RESUMEN DEL MES".center(60))
    print("="*60)
    print(f"{'💰 Total':<30} S/{resumen['total']:>20.2f}")
    print(f"{'📊 Cantidad de ingresos':<30} {resumen['cantidad']:>20}")
    print(f"{'📈 Promedio por ingreso':<30} S/{resumen['promedio']:>20.2f}")
    print("="*60)
    
    if resumen['por_fuente']:
        mostrar_desglose("\nDESGLOSE POR FUENTE", resumen['por_fuente'])
    
    pausar()


def flujo_ingresos():
    """
    Orquesta el flujo completo de gestión de ingresos.
    """
    while True:
        mostrar_menu_ingresos()
        opcion = obtener_opcion(1, 6, "\nSelecciona una opción: ")
        
        if opcion == 1:
            agregar_ingreso_menu()
        elif opcion == 2:
            ver_todos_ingresos_menu()
        elif opcion == 3:
            ver_ingresos_por_fuente_menu()
        elif opcion == 4:
            eliminar_ingreso_menu()
        elif opcion == 5:
            ver_resumen_ingresos_menu()
        elif opcion == 6:
            break


# ============= SECCIÓN AHORROS =============

def mostrar_menu_ahorros():
    """
    Menú principal de gestión de ahorros.
    """
    mostrar_encabezado("GESTIÓN DE AHORROS 🏦", 60)
    print("\n   OPCIONES:\n")
    print("   1. ➕ Agregar un nuevo ahorro")
    print("   2. 📋 Ver todos los ahorros")
    print("   3. 🎯 Ver ahorros por meta")
    print("   4. 🗑️  Eliminar un ahorro")
    print("   5. 📊 Resumen de ahorros por meta")
    print("   6. ↩️  Volver al menú principal")
    print("\n" + "="*60)


def agregar_ahorro_menu():
    """
    Flujo completo para agregar un ahorro.
    """
    mostrar_encabezado("AGREGAR NUEVO AHORRO ➕", 60)
    
    try:
        # Obtener datos
        monto = validar_monto("Ingresa el monto a ahorrar: S/")
        meta = validar_nombre("Meta del ahorro (ej: Viaje, Casa): ", permitir_numeros=False)
        descripcion = validar_descripcion(max_caracteres=60)
        
        # Guardar en BD
        agregar_ahorro(monto, meta, descripcion)
        pausar()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        pausar()


def ver_todos_ahorros_menu():
    """
    Muestra todos los ahorros registrados.
    """
    mostrar_encabezado("VER TODOS LOS AHORROS 📋", 60)
    
    ahorros = obtener_todos_ahorros()
    mostrar_tabla_ahorros(ahorros)
    pausar()


def ver_ahorros_por_meta_menu():
    """
    Filtra y muestra ahorros por meta.
    """
    mostrar_encabezado("VER AHORROS POR META 🎯", 60)
    
    meta = validar_nombre("Meta a buscar: ", permitir_numeros=False)
    ahorros = obtener_ahorros_por_meta(meta)
    
    if not ahorros:
        print(f"ℹ️  No hay ahorros para la meta '{meta}'")
        pausar()
        return
    
    mostrar_tabla_ahorros(ahorros)
    
    # Mostrar desglose
    total = sum(a.monto for a in ahorros)
    print(f"\n💰 Total ahorrado para '{meta}': S/{total:.2f}")
    print(f"📊 Cantidad: {len(ahorros)} ahorro(s)")
    pausar()


def eliminar_ahorro_menu():
    """
    Permite eliminar un ahorro con confirmación.
    """
    mostrar_encabezado("ELIMINAR AHORRO 🗑️", 60)
    
    ahorros = obtener_todos_ahorros()
    
    if not ahorros:
        print("ℹ️  No hay ahorros para eliminar")
        pausar()
        return
    
    mostrar_tabla_ahorros(ahorros)
    
    try:
        ahorro_id = int(input("\nID del ahorro a eliminar: "))
        ahorro = obtener_ahorro_por_id(ahorro_id)
        
        if not ahorro:
            print(f"❌ No se encontró ahorro con ID {ahorro_id}")
            pausar()
            return
        
        print(f"\n⚠️  Vas a eliminar:")
        print(f"   ID: {ahorro.id} | Monto: S/{ahorro.monto} | Meta: {ahorro.meta}")
        
        confirmacion = input("\n¿Confirmas la eliminación? (sí/no): ").strip().lower()
        
        if confirmacion in ["sí", "si"]:
            eliminar_ahorro(ahorro_id)
        else:
            print("❌ Eliminación cancelada")
            
    except ValueError:
        print("❌ Error: Debes ingresar un ID válido (número)")
    
    pausar()


def ver_resumen_ahorros_menu():
    """
    Muestra el resumen de ahorros por meta.
    """
    mostrar_encabezado("RESUMEN DE AHORROS 📊", 60)
    
    resumen = obtener_resumen_ahorro_por_meta()
    
    if resumen is None or resumen['cantidad_metas'] == 0:
        print("ℹ️  No hay ahorros registrados")
        pausar()
        return
    
    print("\n" + "="*60)
    print("RESUMEN GENERAL".center(60))
    print("="*60)
    print(f"{'🏦 Total ahorrado':<30} S/{resumen['total_ahorrado']:>20.2f}")
    print(f"{'🎯 Cantidad de metas':<30} {resumen['cantidad_metas']:>20}")
    print("="*60)
    
    if resumen['por_meta']:
        mostrar_desglose("\nDESGLOSE POR META", resumen['por_meta'])
    
    pausar()


def flujo_ahorros():
    """
    Orquesta el flujo completo de gestión de ahorros.
    """
    while True:
        mostrar_menu_ahorros()
        opcion = obtener_opcion(1, 6, "\nSelecciona una opción: ")
        
        if opcion == 1:
            agregar_ahorro_menu()
        elif opcion == 2:
            ver_todos_ahorros_menu()
        elif opcion == 3:
            ver_ahorros_por_meta_menu()
        elif opcion == 4:
            eliminar_ahorro_menu()
        elif opcion == 5:
            ver_resumen_ahorros_menu()
        elif opcion == 6:
            break


# ============= SECCIÓN REPORTES =============

def mostrar_reportes():
    """
    Muestra un reporte financiero completo.
    """
    mostrar_encabezado("REPORTES FINANCIEROS 📊", 60)
    
    # Calcular totales
    ingresos_total, gastos_total, balance, ahorros_total = calcular_balance()
    
    # Mostrar resumen
    mostrar_resumen_financiero(ingresos_total, gastos_total, ahorros_total)
    
    # Mostrar detalles
    print("\n" + "="*60)
    print("DETALLES POR CATEGORÍA".center(60))
    print("="*60)
    
    # Gastos por categoría
    resumen_gastos = obtener_resumen_gastos()
    if resumen_gastos and resumen_gastos['por_categoria']:
        mostrar_desglose("\n🛒 GASTOS POR CATEGORÍA", resumen_gastos['por_categoria'])
    
    # Ingresos por fuente
    resumen_ingresos = obtener_resumen_ingresos()
    if resumen_ingresos and resumen_ingresos['por_fuente']:
        mostrar_desglose("\n💵 INGRESOS POR FUENTE", resumen_ingresos['por_fuente'])
    
    # Ahorros por meta
    resumen_ahorros = obtener_resumen_ahorro_por_meta()
    if resumen_ahorros and resumen_ahorros['por_meta']:
        mostrar_desglose("\n🏦 AHORROS POR META", resumen_ahorros['por_meta'])
    
    pausar()


# ============= PROGRAMA PRINCIPAL =============

def main():
    """
    Punto de entrada principal de la aplicación.
    
    Inicializa la BD y ejecuta el bucle principal del menú.
    """
    print("🚀 Inicializando Budget Tracker...\n")
    crear_tablas()
    print("✅ Base de datos lista\n")
    
    while True:
        mostrar_menu_principal()
        opcion = obtener_opcion(1, 5, "\nSelecciona una opción: ")
        
        if opcion == 1:
            flujo_gastos()
        elif opcion == 2:
            flujo_ingresos()
        elif opcion == 3:
            flujo_ahorros()
        elif opcion == 4:
            mostrar_reportes()
        elif opcion == 5:
            print("\n" + "="*60)
            print("👋 ¡Hasta luego, Patrick!".center(60))
            print("Gracias por usar Budget Tracker 💰".center(60))
            print("="*60 + "\n")
            break


if __name__ == "__main__":
    """
    Punto de entrada del script.
    """
    main()
