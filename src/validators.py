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
    

    
            
        