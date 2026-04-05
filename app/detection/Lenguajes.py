
def limpiar_lenguaje(lista_cadenas):
    """Convierte la entrada en un conjunto y maneja la cadena vacía."""
    # Representaremos la cadena vacía como una cadena de longitud cero ""
    # Si el usuario ingresa 'epsilon', 'lambda' o '', se trata como cadena vacía.
    lenguaje = set()
    for s in lista_cadenas:
        s = s.strip()
        if s.lower() in ["epsilon", "lambda", "ε", "λ", ""]:
            lenguaje.add("")
        else:
            lenguaje.add(s)
    return lenguaje

def union(L1, L2):
    """Operación de Unión: L1 ∪ L2"""
    return L1.union(L2)

def concatenacion(L1, L2):
    """Operación de Concatenación: L1L2"""
    # Si alguno es conjunto vacío (Ø), el resultado es vacío
    if not L1 or not L2:
        return set()
    resultado = set()
    for s1 in L1:
        for s2 in L2:
            resultado.add(s1 + s2)
    return resultado

def potencia(L, n):
    """Operación de Potencia: L^n"""
    if n == 0:
        return {""}  # L^0 siempre es {epsilon}
    
    res = L
    for _ in range(n - 1):
        res = concatenacion(res, L)
    return res

def kleene_star(L, limite=3):
    """Cerradura de Kleene: L* (Generado hasta el límite indicado)"""
    resultado = {""} # L^0
    for i in range(1, limite + 1):
        resultado = union(resultado, potencia(L, i))
    return resultado

def formatear_salida(L):
    """Formatea el conjunto para mostrar 'ε' en lugar de cadena vacía."""
    if not L: return "∅ (Conjunto Vacío)"
    elementos = [f"'{s}'" if s != "" else "ε" for s in sorted(list(L))]
    return "{ " + ", ".join(elementos) + " }"

def main():
    print("--- Operaciones de Lenguajes Formales ---")
    print("Nota: Para representar la cadena vacía use 'epsilon', 'lambda' o deje vacío.")
    
    # a. Solicitar cadenas al usuario
    input_l1 = input("Ingrese los elementos de L1 separados por comas: ").split(",")
    input_l2 = input("Ingrese los elementos de L2 separados por comas: ").split(",")
    
    L1 = limpiar_lenguaje(input_l1)
    L2 = limpiar_lenguaje(input_l2)
    
    print(f"\nL1 = {formatear_salida(L1)}")
    print(f"L2 = {formatear_salida(L2)}")
    print("-" * 30)

    # c. Realizar operaciones solicitadas
    
    # 1. L1(L2^3 ∪ L1)
    op1 = concatenacion(L1, union(potencia(L2, 3), L1))
    
    # 2. (L1 ∪ L2)L2
    op2 = concatenacion(union(L1, L2), L2)
    
    # 3. L1* ∪ L2*
    op3 = union(kleene_star(L1), kleene_star(L2))
    
    # 4. L1L2 ∪ L2L1
    op4 = union(concatenacion(L1, L2), concatenacion(L2, L1))

    # Mostrar resultados
    print("RESULTADOS DE LAS OPERACIONES:")
    print(f"1. L1(L2³ ∪ L1) = {formatear_salida(op1)}")
    print(f"2. (L1 ∪ L2)L2  = {formatear_salida(op2)}")
    print(f"3. L1* ∪ L2*    = {formatear_salida(op3)}")
    print(f"4. L1L2 ∪ L2L1  = {formatear_salida(op4)}")

if __name__ == "__main__":
    main()