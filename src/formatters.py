"""
MÓDULO FORMATTERS - Formateo de Datos
=======================================

Contiene funciones para formatear y mostrar datos en tablas.
Centraliza el formateo visual de la aplicación.

Funciones:
    - mostrar_tabla_gastos(): Tabla de gastos
    - mostrar_tabla_ingresos(): Tabla de ingresos
    - mostrar_tabla_ahorros(): Tabla de ahorros
    - mostrar_resumen(): Resumen financiero
    - mostrar_encabezado(): Encabezado de sección

Autor: Patrick
Fecha: 2026-04-02
"""

def mostrar_encabezado(titulo, ancho=50) :
    #título
    print("\n"+"="*ancho)
    print(titulo)
    print("="*ancho)
    
def mostrar_tabla_gastos(gastos) :
    if not gastos :
        print("No hay gastos registrados")
        return
    #Header
    print(f"\n{'ID':<5} {'Fecha' :<20} {'Monto:<10'}{'Categoría':<15}  {'Descripción':<30}")
    
    #Content
    for gasto in gastos :
        fecha_fmt = gasto.fecha.strftime("%d/%m/%Y %H/%M")
        descripcion = gasto.descripcion[:27] + "..." if gasto.descripcion and len(gasto.descripcion) > 30 else gasto.descripcion or "Sin descripcion" 
        
        print(f"{gasto.id:<5} {gasto.fecha_fmt:<20} S/{gasto.monto:<10.2f} {gasto.categoria:<15} {descripcion}")
        
        print(f"Cantidad de gastos : {len(gastos)}")
        