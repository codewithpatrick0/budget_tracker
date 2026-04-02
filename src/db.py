"""
MÓDULO DE BASE DE DATOS - Database Configuration
==================================================
Configuración y modelos de SQLAlchemy para la base de datos SQLite
Este módulo define:
    - Configuración de conexión a SQLite
    - Modelo de datos (tabla Gasto)
    - Sesiones de base de datos

Las tablas se crean automáticamente al ejecutar crear_tablas().

Autor: Patrick
Fecha: 2026-04-02
"""

import os
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase
#LIBRERIAS PARA CONECTAR A BASE DE DATOS
from datetime import datetime
from pathlib import Path

#RUTA BASE DEL PROYECTO
BASE_DIR = Path(__file__).resolve().parent.parent

#RUTA A LA BASE DE DATOS
DB_PATH = BASE_DIR/"data"/"budget.db"

#Creacion de carpeta
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

#MOTOR DE CONEXION
engine = create_engine(f"sqlite:///{DB_PATH}")

#SESSION (CONSULTAS | INTERACTUAR)
SessionLocal = sessionmaker(bind=engine)
#SessionLocal va primero en mayus para verlo como una clase y no un objeto común.

#BASE PARA LOS MODELOS
class Base(DeclarativeBase) :
    """
    Clase base para todos los modelos de SQLAlchemy.
    ! TODOS los modelos de la aplicación deben heredar de esta clase.
    """
    pass

class Gasto(Base) :
    __tablename__ = "gastos" #DEFINO NOMBRE INDEPENDIENTE DE LA TABLA
    
    #CREAMOS LAS COLUMNAS CON LOS ATRIBUTOS DE LA TABLA
    id = Column(Integer, primary_key=True, autoincrement=True, doc="Identificador único del gasto")
    monto = Column(Float, nullable=False, doc="Monto gastado en dinero")
    fecha = Column(DateTime, default=datetime.now, doc="Fecha y hora del gasto")
    categoria = Column(String, nullable=False, doc="Categoría del gasto")
    descripcion = Column(String, nullable=True, doc="Descripción adicional del gasto")
    
    def __repr__(self):
        """Representación legible del objeto Gasto"""
        return (
            f"Gasto(id={self.id}, monto=S/{self.self.monto},"
            f"Categoría='{self.categoria}', fecha={self.fecha.strftime('%Y-%m-%d %H:%M')})"
        )
            
#FUNCIONES DE BASE DE DATOS
def crear_tablas() :
    """
    Crea todas las tablas en la base de datos.
    
    Esta función debe ejecutarse al iniciar la aplicación para garantizar
    que las tablas existan. Si ya existen, no hace nada.
    
    Utiliza:
        Base.metadata.create_all(bind=engine)
        
    Nota:
        Se ejecuta automáticamente en main.py al iniciar la aplicación.
    """
    Base.metadata.create_all(bind=engine)
    print("Base de datos lista.")