from avl import obtener_altura, obtener_balance

def verificar_invariante_avl(nodo):
    """
    Recorre el árbol para garantizar que el balance y las alturas sean consistentes.
    Retorna True si el subárbol cumple la propiedad AVL, False de lo contrario.
    """
    if nodo is None:
        return True
