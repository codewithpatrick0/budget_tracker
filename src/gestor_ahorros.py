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
    
    except Exception as e :
        session.rollback()
        print(f"No se pudo añadir el nuevo ahorro : {str(e)}")
        
    finally :
        session.close()
        
def obtener_todos_ahorros() :
    session = SessionLocal()
    try :
        ahorros = session.query(Ahorro).order_by(Ahorro.fecha.desc()).all()
        return ahorros
    except Exception as e  :
        session.rollback()
        print(f"Error al obtener los ahorros : {str(e)}")
        return None
    finally :
        session.close()
        
def obtener_ahorros_por_meta(meta) :
    session = SessionLocal()
    try :
        ahorros = session.query(Ahorro).filter(
            Ahorro.meta.ilike(f"%{meta}%")
            ).order_by(Ahorro.fecha.desc()).all()
        return ahorros
    except Exception as e :
        session.rollback()
        print(f"Error al obtener el ahorro por meta :  {str(e)}")
        return None
    finally :
        session.close()

def obtener_ahorro_por_id(ahorro_id) :
    session = SessionLocal()
    try :
        ahorro = session.query(Ahorro).filter(Ahorro.id == ahorro_id).first()
        return ahorro
    except Exception as e :
        session.rollback()
        print(f"Error al obtener el ingreso por id : {str(e)}")
        return None
    finally :
        session.close()
        
def eliminar_ahorro(ahorro_id) :
    session = SessionLocal()
    try :
        ahorro = session.query(Ahorro).filter(Ahorro.id == ahorro_id).first()
        
        if not ahorro :
            print(f"No existe un ahorro con el ID {ahorro_id}")
            return False
        
        session.delete(ahorro)
        session.commit
        return True
    
    except Exception as e :
        session.rollback()
        print(f"Error al eliminar el ahorro : {str(e)}")
        
    finally :
        session.close()
        
def obtener_total_ahorrado_por_meta(meta) :
    session = SessionLocal()
    try :
        resultado = session.query(
            func.sum(Ahorro.monto).label("total")
            ).filter(Ahorro.meta.ilike(f"%{meta}%")).first()
        
        total = float(resultado.total or 0)
        return round(total, 2)
    except Exception as e:
        print(f"Error al calcular total : {str(e)}")
        return 0
    finally:
        session.close()
        
def obtener_resumen_ahorro_por_meta() :
    
    session = SessionLocal()
    try :
        resultados = session.query(
            func.sum(Ahorro.monto).label("total"),
            func.count(Ahorro.id).label("cantidad"),
            Ahorro.meta
        ).group_by(Ahorro.meta).all()
        
        if not resultados :
            return {
                'total_ahrorrado' : 0,
                'cantidad_metas' : 0,
                'por_meta' : {}
            }
            
        total = 0
        por_meta = {}
        
        for fila in resultados :
            meta = fila.meta
            sum_meta = float(Ahorro.total or 0)
            por_meta[meta] = round(sum_meta, 2)
            total += sum_meta
            
        return {
            'total_ahrorrado' : total,
                'cantidad_metas' : len(resultados),
                'por_meta' : por_meta
        }
    except Exception as e:
        print(f"Error al obtener resumen : {str(e)}")
        return None
    finally:
        session.close()