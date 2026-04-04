"""
MÓDULO GESTOR DE INGRESOS
==========================

Contiene todas las funciones CRUD para gestionar ingresos.

Funciones:
    - agregar_ingreso(): Agregar nuevo ingreso
    - obtener_todos_ingresos(): Obtener todos
    - obtener_ingresos_por_fuente(): Filtrar por fuente
    - obtener_ingreso_por_id(): Buscar por ID
    - eliminar_ingreso(): Eliminar ingreso
    - obtener_resumen_ingresos(): Resumen mensual

Autor: Patrick
Fecha: 2026-04-02
"""

from src.db import SessionLocal, Ingreso
from sqlalchemy import extract, func
from datetime import datetime

def agregar_ingreso(monto, fuente, descripcion=None) :
    
    if monto <= 0 :
        raise ValueError("El monto debe ser mayor a 0")
    
    #Creamos sesion de consultas :
    session = SessionLocal()
    
    try :
        nuevo_ingreso = Ingreso(
            monto = monto, 
            fuente = fuente,
            descripcion = descripcion
        )
        session.add(nuevo_ingreso)
        session.commit()  #Añadimos y guardamos cambios
        
        print("Ingreso añadido correctamente")
        print(f"ID : {nuevo_ingreso.id} | Monto : S/{nuevo_ingreso.monto} | Fuente : {nuevo_ingreso.fuente} | ")
        return nuevo_ingreso
    
    except Exception as e :
        session.rollback()
        print(f"Error al agregar el ingreso : {str(e)}")
        return None
    
    finally :
        session.close()
        
def obtener_todos_gastos() :
    #Sesion de consultas para la bd de ingresos
    session = SessionLocal()
    try :
        ingresos = session.query(Ingreso).order_by(Ingreso.fecha.desc()).all()
        return ingresos
    
    except Exception as e :
        session.rollback()
        print(f"Error al obtener los ingresos : {str(e)}")
        return None
    
    finally :
        session.close()
        
def obtener_ingresos_por_fuente(fuente) :
    session = SessionLocal()
    
    try :
        ingresos = session.query(Ingreso).filter(Ingreso.fuente.ilike(f"%{fuente}%")).order_by(Ingreso.fecha.desc()).all()
        return ingresos
    
    except Exception as e :
        session.rollback()
        print(f"Error al filtrar los ingresos por categoría : {str(e)}")
        return None
    
    finally :
        session.close()
        
def obtener_ingreso_por_id(ingreso_id) :
    session = SessionLocal()
    
    try :
        ingresos = session.query(Ingreso).filter(Ingreso.id == ingreso_id).first()
        return ingresos
    
    except Exception as e :
        session.rollback()
        print(f"Error al obtener el ingreso por ID : {str(e)}")
        return None
    
    finally :
        session.close()
        
def eliminar_ingreso(ingreso_id) :
    session = SessionLocal()
    try :
        ingresos = session.query(Ingreso).filter(Ingreso.id == ingreso_id).first()
        
        if not ingresos :
            print(f"No se encontró ingresos con el ID {ingreso_id}")
            return False
        
        session.delete(ingresos)
        session.commit()
        
        print("Ingreso eliminado correctamente")
        return True
    
    except Exception as e :
        session.rollback()
        print(f"Error al eliminar el ingreso {str(e)}")
        
    finally :
        session.close()
        
def obtener_resumen_ingresos(año=None, mes=None) :
    session = SessionLocal()
    try :
        resultados = session.query(
            func.sum(Ingreso.monto).label("total"),
            func.count(Ingreso.id).label("cantidad"),
            Ingreso.fuente
        ).filter(
            extract('year', Ingreso.fecha) == año,
            extract('mounth', Ingreso.fecha) == mes
        ).group_by(Ingreso.fuente).all()
        
        if not resultados :
            return {
                'total' : 0,
                'cantidad' : 0,
                'promedio' : 0,
                'por_fuente' : {}
            }
        
        total = 0
        cantidad = 0
        por_fuente = {}
        
        for r in resultados :
            fuente = r.fuente
            suma_fuente = float(r.total or 0)
            count_fuente = r.cantidad
            
            por_fuente[fuente] = round(suma_fuente, 2)
            total += suma_fuente
            cantidad += count_fuente
            
        prom = total / cantidad if cantidad > 0 else 0
        
        return {
            'total': round(total, 2),
            'cantidad': cantidad,
            'promedio': round(prom, 2),
            'por_fuente': por_fuente
        }
        
    except Exception as e:
        print(f"❌ Error al obtener resumen: {e}")
        return None
    finally:
        session.close()