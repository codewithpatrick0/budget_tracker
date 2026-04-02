"""
MÓDULO GESTOR - Operaciones de Gastos
=====================================

Contiene todas las funciones para interactuar con los gastos en la BD.
Incluye operaciones CRUD (Create, Read, Update, Delete).

Funciones principales:
    - agregar_gasto(): Agregar un nuevo gasto
    - obtener_todos_gastos(): Obtener todos los gastos
    - obtener_gastos_por_categoria(): Filtrar por categoría
    - eliminar_gasto(): Eliminar un gasto por ID
    - obtener_gasto_por_id(): Buscar un gasto específico

Autor: Patrick
Fecha: 2026-04-02
"""

from src.db import SessionLocal, Gasto
from sqlalchemy import extract, func 
from datetime import datetime
#Defino funcion para agregar gastos a base de datos
def agregar_gasto(monto, categoria, descripcion=None):
    if monto <= 0 :
        raise ValueError("El monto debe ser mayor a 0")
    
    #Creamos una sesión en la base de datos
    session = SessionLocal()
    
    try :
        nuevo_gasto = Gasto(
            monto=monto,
            categoria=categoria,
            descripcion=descripcion
        )
        #AÑADIMOS EL GASTO A LA SESION
        session.add(nuevo_gasto)
        
        #GUARDAMOS LOS CAMBIOS EN LA BASE DE DATOS
        session.commit()
        
        #Mostrar confirmación
        print("✅Gasto añadido correctamente")
        print(f"ID : {nuevo_gasto.id} | Monto : S/{nuevo_gasto.monto} | Categoría : {nuevo_gasto.categoria}")
        
        return nuevo_gasto
    
    except Exception as e :
        #Si hay error, revertimos cambios
        session.rollback()
        print(f"Error al agregar el gasto : {str(e)}")
        return None
    finally :
        #SI o SI terminamos de cerrar la sesión
        session.close()
        
def obtener_gastos() :
    """Obtiene todos los gastos registrados en la base de datos"""
    
    session = SessionLocal() # Creamos sesion de consulta
    try:
        # Consultar todos los gastos, ordenados por fecha (más recientes primero
        gastos = session.query(Gasto).order_by(Gasto.fecha.desc()).all()
        return gastos
    
    except Exception as e :
        print(f"Error al obtener gastos : {str(e)}")
        return []
    
    finally :
        session.close()
        
def obtener_gastos_por_categoria(categoria) :
    """Obtiene gastos por categoria de la base de datos"""
    
    session = SessionLocal()
    try :
        gastos = session.query(Gasto).filter(Gasto.categoria.ilike(f"%{categoria}%)")).order_by(Gasto.fecha.desc()).all()
        return gastos
    
    except Exception as e :
        print(f"Error al filtrar por categoria : {str(e)}")
        return []
    finally :
        session.close()
        
def obtener_gasto_por_id(id) :
    """Obtener el gastor por ID ingresado según base de datos"""
    
    session = SessionLocal()
    try :
        gasto = session.query(Gasto).filter(Gasto.id == id).first()
        return gasto
    
    except Exception as e :
        print(f"Error al encontrar el gasto : {str(e)}")
        return None
    
    finally :
        session.close()

def eliminar_gasto(id) :
    """Eliminar gasto de la base de datos por ID"""
    
    session = SessionLocal()
    try :
        gasto = session.query(Gasto).filter(Gasto.id == id).first()
        
        if not gasto :
            print(f"No se encontró el gasto por la ID {id}")
            return False
        
        #Eliminar el gasto
        session.delete(gasto)
        session.commit()
        
        print("Gasto eliminado correctamente")
        return True
    
    except Exception as e :
        session.rollback()
        print(f"Error al eliminar el gasto : {str(e)}")
        return False
    
    finally :
        session.close()
        
def obtener_resumen_mensual(mes=None, año=None) :
    if mes is None :
        mes = datetime.now().month
    if año is None :
        año = datetime.now().year
        
    session = SessionLocal()
    
    try :
        resultados = session.query(
            func.sum(Gasto.monto).label("total"),
            func.count(Gasto.id).label("cantidad"),
            Gasto.categoria
        ).filter(
            extract('year', Gasto.fecha) == año,
            extract('month', Gasto.fecha) == mes  
        ).group_by(Gasto.categoria).all()
        
        if not resultados :
            return {
                'total' : 0,
                'cantidad' : 0,
                'promedio' : 0,
                'por_categoria' : []
            }
            
        #PROCESAR RESULTADOS
        total = 0
        cantidad = 0
        por_categoria = {}
        
        for fila in resultados:
            categoria = fila.categoria
            suma_categoria = float(fila.total or 0)
            count_categoria = fila.cantidad

            por_categoria[categoria] = round(suma_categoria, 2)
            total += suma_categoria
            cantidad += count_categoria

        promedio = total / cantidad if cantidad > 0 else 0

        return {
            'total': round(total, 2),
            'cantidad': cantidad,
            'promedio': round(promedio, 2),
            'por_categoria': por_categoria
        }

    except Exception as e:
        print(f"❌ Error al obtener resumen: {e}")
        return None  # mejor que {}

    finally:
        session.close()