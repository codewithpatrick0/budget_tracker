from src.db import SessionLocal, Gasto

#Defino funcion para agregar gastos a base de datos
def agregar_gasto(monto, categoria, descripcion=None):
    #Generador de sesiones
    session = SessionLocal()
    
    nuevo_gasto = Gasto(
        monto=monto,
        categoria=categoria,
        descripcion=descripcion
    )

    session.add(nuevo_gasto)
    session.commit()
    session.close()

    print("✅ Gasto agregado correctamente")