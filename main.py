from src.db import crear_tablas
from src.gestor import agregar_gasto

crear_tablas()

#Comienzo del menú
while True :
    print("\nBIENVENIDO A BUDGET TRACKER\n")
    print("1.Agregar gasto")
    try :
        opcion = int(input("Selecciona una opción :"))
    except ValueError :
        print(f"Error : Debes ingresar un número")
        continue
    
    if opcion <= 0 or opcion > 5 :
        print("Opción inválida. Fuera de rango de opciones")
        continue
    
    if opcion == 1 :
        #Validar monto
        while True :
            try :
                monto = float(input("Ingresa el monto : "))
                if monto <= 1 :
                    print("El monto necesita ser mayor a 0")
                    continue
                break
            except ValueError :
                print("Monto ingresado inválido, necesita ser entero o decimal")

        #Validar categoría
        while True :
            categoria = input("Categoría : ").strip()
            if not categoria :
                print("Este campo no puede estar vacío")
                continue
            if any(char.isdigit() for char in categoria) :
                print("La categoría no puede contener números")
            else : break

        #Validar descrpción
        while True :
            descripcion = input("Descripción : ").strip()
            if len(descripcion) > 60 :
                print("El máximo de caracteres es de 60, sobrepasaste el límite")
                continue
            if not descripcion :
                descripcion = "Sin descripción"
            break
        agregar_gasto(monto, categoria, descripcion)