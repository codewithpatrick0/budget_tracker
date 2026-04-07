"""
MÓDULO VALIDATORS - Validaciones de Entrada
=============================================

Contiene funciones para validar entrada del usuario.
Evita repetir código en múltiples menús.

Funciones:
    - validar_monto(): Valida montos positivos
    - validar_nombre(): Valida nombres sin números
    - validar_descripcion(): Valida descripciones
    - obtener_opcion(): Obtiene opción numérica

Autor: Patrick
Fecha: 2026-04-02
"""

def validar_monto(prompt="Ingresa el monto: S/") :

    
    while True :
        try :
            monto = float(input(prompt))
            if monto <= 0 :
                print("El monto debe ser mayor a 0")
                continue
            return monto
        except ValueError :
            print("Error : Monto inválido")

def validar_nombre(prompt="Ingresa el nombre: ", permitir_numeros=False) :
    while True :
        valor = str(input(prompt)).strip()

        if not permitir_numeros and any(char.isdigit() for char in valor) :
            print("Este campo no puede contener números")
            continue

        return valor
    
def validar_descripcion(max_caracteres=60) :

    while True :
        descripcion = input(f"Ingresa la descripción (OPCIONAL) : ")

        if len(descripcion) > max_caracteres :
            print("Su descripción sobrepasa el límite de carácteres (60)")
            continue

        if not descripcion :
            descripcion = "Sin descripción"
        return descripcion

def obtener_opcion(min_opcion=1, max_opcion=6, prompt="Seleccione una opcion") :

    while True :
        try :
            opcion = int(input(prompt))
            if opcion >= min_opcion or opcion <= max_opcion :
               return opcion
            else :
                 print(f"Opción fuera de rango, la opción debe estar entre {min_opcion} y {max_opcion}")
                 
        except ValueError :
            print("Error : Solo números por favor")


