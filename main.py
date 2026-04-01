from src.db import crear_tablas


crear_tablas()

#Comienzo del menú
while True :
    print("\nBIENVENIDO A BUDGET TRACKER\n")
    print("1.Agregar gasto")
    try :
        opcion = int(input("Selecciona una opción :"))
        if opcion <= 0 or opcion > 5 :
            print("Opción inválida")
            
    except Exception as e :
        print(f"Error : {e}")
        


