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
    pass

class Gasto(Base) :
    __tablename__ = "gastos" #DEFINO NOMBRE INDEPENDIENTE DE LA TABLA
    
    #CREAMOS LAS COLUMNAS CON LOS ATRIBUTOS DE LA TABLA
    id = Column(Integer, primary_key=True, autoincrement=True)
    monto = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    categoria = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    
#EJECUCION AL CREAR TABLAS
def crear_tablas() :
    Base.metadata.create_all(bind=engine)
    