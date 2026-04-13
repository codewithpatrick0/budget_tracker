"""
MÓDULO UTILS - Funciones Utilitarias
=====================================

Contiene funciones helper para la aplicación.

Funciones:
    - calcular_balance(): Calcula ingresos - gastos
    - obtener_fecha_actual(): Retorna fecha actual formateada
    - pausar(): Pausa la ejecución

Autor: Patrick
Fecha: 2026-04-02
"""

from datetime import datetime
from src.gestor_gastos import obtener_todos_gastos
from src.gestor_ingresos import obtener_todos_ingresos
from src.gestor_ahorros import obtener_todos_ahorros

def calcular_balance() :
    
    gastos = obtener_todos_gastos()
    ingresos = obtener_todos_ingresos()
    ahorros = obtener_todos_ahorros()
    
    gastos_totales = sum(g.monto for g in gastos)
    ingresos_totales = sum(i.monto for i in ingresos)
    ahorros_totales = sum(a.monto for a in ahorros)
    
    balance = ingresos_totales - gastos_totales
    
    return balance, ingresos_totales, gastos_totales, ahorros_totales

def pausar(mensaje="Presiona ENTER para continuar") :

    input(f"\n{mensaje}")

def obtener_fecha_actual_formateada(formato="%d/%m/%Y") :
    
    return datetime.now.strftime(formato)

def limpiar_pantalla() :
    
    import os
    os.system('clear' if os.name != 'nt' else 'cls')