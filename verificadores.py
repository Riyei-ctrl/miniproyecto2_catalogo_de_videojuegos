from avl import obtener_altura, obtener_balance

def verificar_invariante_avl(nodo):
    """
    Recorre el árbol para garantizar que el balance y las alturas sean consistentes.
    Retorna True si el subárbol cumple la propiedad AVL, False de lo contrario.
    """
    if nodo is None:
        return True

    # 1. Verificar alturas correctas internamente
    altura_calculada = 1 + max(obtener_altura(nodo.izq), obtener_altura(nodo.der))
    if nodo.altura != altura_calculada:
        print(f"Error de invariante: Altura inconsistente en nodo clave {nodo.clave}")
        return False

    # 2. Verificar el factor de balance
    balance = obtener_balance(nodo)
    if abs(balance) > 1:
        print(f"Error de invariante: Nodo clave {nodo.clave} desbalanceado (factor: {balance})")
        return False

    # 3. Verificación recursiva de los hijos
    return verificar_invariante_avl(nodo.izq) and verificar_invariante_avl(nodo.der)