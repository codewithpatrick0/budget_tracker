"""
MÓDULO GESTOR DE AHORROS
=========================

Gestiona los ahorros y metas de ahorro del usuario.

Funciones:
    - agregar_ahorro(): Agregar ahorro
    - obtener_todos_ahorros(): Obtener todos
    - obtener_ahorros_por_meta(): Filtrar por meta
    - obtener_ahorro_por_id(): Buscar por ID
    - eliminar_ahorro(): Eliminar ahorro
    - obtener_total_ahorrado(): Total ahorrado

Autor: Patrick
Fecha: 2026-04-02
"""

from src.db import SessionLocal, Ahorro
from sqlalchemy import extract, func
from datetime import datetime

def agregar_ahorro(monto, meta, descripcion=None) :
    
    if monto <= 0 :
        raise ValueError("El monto debe ser mayor a 0")
        
    session = SessionLocal()
    
    try :
        nuevo_ahorro = Ahorro(
            monto = monto,
            meta = meta,
            descripcion = descripcion
        )
        session.add(nuevo_ahorro)
        session.commit()
    
    except :
        session.rollback()
        print("No se pudo añadir el nuevo ahorro")
        
    finally :
        session.close()
        
def obtener_todos_ahorros() :
    session = SessionLocal()
    try :
        ahorros = session.query(Ahorro).order_by(Ahorro.fecha.desc()).all()
        return ahorros
    except  :
        session.rollback()
        print("No se pudo obtener los ahorros")
        return None
    finally :
        session.close()