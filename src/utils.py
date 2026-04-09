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
"""from src.gestor_ahorros import obtener_todos_ahorros"""

