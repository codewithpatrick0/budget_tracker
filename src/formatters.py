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
    print(f"\n{'ID':<5} {'Fecha' :<20} {'Monto:<10'}{'Categoría':<15}{'Descripción':<30}")
    
    #Content
    for gasto in gastos :
        fecha_fmt = gasto.fecha.strftime("%d/%m/%Y %H/%M")
        descripcion = gasto.descripcion[:27] + "..." if gasto.descripcion and len(gasto.descripcion) > 30 else gasto.descripcion or "Sin descripcion" 
        
        print(f"{gasto.id:<5} {fecha_fmt:<20} S/{gasto.monto:<10.2f} {gasto.categoria:<15} {descripcion}")
        
    print(f"Cantidad de gastos : {len(gastos)} gasto(s)")
        
def mostrar_tabla_ingresos(ingresos) :
    if not ingresos :
        print("No hay ingresos registrados")
        return
    
    print(f"\n{'ID':<5} {'Fecha' :<20} {'Monto:<10'} {'Fuente':<15}  {'Descripción':<30}")
    
    #Content
    for ingreso in ingresos :
        fecha_fmt = ingreso.fecha.strftime("%d/%m/%Y %H/%M")
        descripcion = ingreso.descripcion[:27] + "..." if ingreso.descripcion and ingreso.descripcion > 30 else ingreso.descripcion or "Sin descripcion" 
        print(f"{ingreso.id:<5} {fecha_fmt:<20} S/{ingreso.monto:<10.2f} {ingreso.fuente:<15} {descripcion}")
        
    print(f"Cantidad de ingresos : {len(ingresos)} ingreso(s)")
        
def mostrar_tabla_ahorros(ahorros) :
    if not ahorros :
        print("No hay ingresos registrados")
        return
    
    print(f"\n{'ID':<5} {'Fecha' :<20} {'Monto:<10'} {'Meta':<15}  {'Descripción':<30}")
    
    #Content
    for ahorro in ahorros :
        for ahorro in ahorros :
            fecha_fmt = ahorro.fecha.strftime("%d/%m/%Y %H/%M")
            descripcion = ahorro.descripcion[:27] + "..." if ahorro.descripcion and ahorro.descripcion > 30 else ahorro.descripcion or "Sin descripcion" 
            print(f"{ahorro.id:<5} {fecha_fmt:<20} S/{ahorro.monto:<10.2f} {ahorro.fuente:<15} {descripcion}")
        
        print(f"Cantidad de ahorros : {len(ahorros)} ahorro(s)")
        
def mostrar_resumen_financiero(ingresos_total, gastos_total, ahorros_total) :
    
    #Ingresamos balance (Resto)
    balance = ingresos_total - gastos_total
    porcentaje_ahorro = (ahorros_total / ingresos_total * 100) if ingresos_total > 0 else 0
    
    print(f"💰 Ingresos totales:     S/{ingresos_total:>10.2f}")
    print(f"🛒 Gastos totales:       S/{gastos_total:>10.2f}")
    print(f"🏦 Ahorros totales:      S/{ahorros_total:>10.2f}")
    print("-"*50)
    print(f"✨ Balance neto:         S/{balance:>10.2f}")
    print(f"📈 % de ahorro:          {porcentaje_ahorro:>9.1f}%")
    print("="*50)
    
def mostrar_desglose(titulo, diccionario, es_dinero=True):
    """
    Muestra un desglose de datos en formato tabla.
    """
    # ✅ VALIDACIÓN IMPORTANTE
    if not diccionario:
        print("ℹ️  No hay datos para mostrar")
        return
    
    # ✅ Si es string, no hacer nada
    if isinstance(diccionario, str):
        print(f"ℹ️  Error: {diccionario}")
        return
    
    # ✅ Si no es diccionario, no hacer nada
    if not isinstance(diccionario, dict):
        print(f"ℹ️  Formato incorrecto: {type(diccionario)}")
        return
    
    print(f"\n{titulo}")
    print("-"*40)
    
    total = sum(diccionario.values())
    
    for clave, valor in sorted(diccionario.items(), key=lambda x: x[1], reverse=True):
        if es_dinero:
            porcentaje = (valor/total) * 100 if total > 0 else 0
            print(f"{clave:<20} S/{valor:<10.2f} ({porcentaje:.1f}%)")
        else:
            print(f"{clave:<20} {valor}")
    
    print("-"*40)
    if es_dinero:
        print(f"{'TOTAL':<20} S/{total:.2f}")