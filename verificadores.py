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

def verificar_invariante_abb(nodo, minimo=None, maximo=None):
    """
    Verifica que el subárbol cumple la propiedad de orden del ABB:
    todas las claves del subárbol izquierdo < clave < todas las claves del subárbol derecho.
    """
    if nodo is None:
        return True

    if minimo is not None and nodo.clave <= minimo:
        print(f"Error de invariante ABB: Nodo {nodo.clave} viola el limite inferior {minimo}")
        return False

    if maximo is not None and nodo.clave >= maximo:
        print(f"Error de invariante ABB: Nodo {nodo.clave} viola el limite superior {maximo}")
        return False

    return (verificar_invariante_abb(nodo.izq, minimo, nodo.clave) and
            verificar_invariante_abb(nodo.der, nodo.clave, maximo))

def verificar_invariante_heap(heap):
    """
    Verifica la propiedad min-heap: cada padre tiene prioridad <= que sus hijos.
    Recibe el arreglo interno del montículo.
    """
    n = len(heap)
    for i in range(n):
        hijo_izq = 2 * i + 1
        hijo_der = 2 * i + 2

        if hijo_izq < n and heap[i][0] > heap[hijo_izq][0]:
            print(f"Error de invariante Heap: Padre indice {i} (prioridad {heap[i][0]}) > Hijo izq indice {hijo_izq} (prioridad {heap[hijo_izq][0]})")
            return False

        if hijo_der < n and heap[i][0] > heap[hijo_der][0]:
            print(f"Error de invariante Heap: Padre indice {i} (prioridad {heap[i][0]}) > Hijo der indice {hijo_der} (prioridad {heap[hijo_der][0]})")
            return False

    return True

def verificar_invariante_abb(nodo, minimo=None, maximo=None):
    """
    Verifica que el subárbol cumple la propiedad de orden del ABB:
    todas las claves del subárbol izquierdo < clave < todas las claves del subárbol derecho.
    """
    if nodo is None:
        return True

    if minimo is not None and nodo.clave <= minimo:
        print(f"Error de invariante ABB: Nodo {nodo.clave} viola el limite inferior {minimo}")
        return False

    if maximo is not None and nodo.clave >= maximo:
        print(f"Error de invariante ABB: Nodo {nodo.clave} viola el limite superior {maximo}")
        return False

    return (verificar_invariante_abb(nodo.izq, minimo, nodo.clave) and
            verificar_invariante_abb(nodo.der, nodo.clave, maximo))

def verificar_invariante_heap(heap):
    """
    Verifica la propiedad min-heap: cada padre tiene prioridad <= que sus hijos.
    Recibe el arreglo interno del montículo.
    """
    n = len(heap)
    for i in range(n):
        hijo_izq = 2 * i + 1
        hijo_der = 2 * i + 2

        if hijo_izq < n and heap[i][0] > heap[hijo_izq][0]:
            print(f"Error de invariante Heap: Padre indice {i} (prioridad {heap[i][0]}) > Hijo izq indice {hijo_izq} (prioridad {heap[hijo_izq][0]})")
            return False

        if hijo_der < n and heap[i][0] > heap[hijo_der][0]:
            print(f"Error de invariante Heap: Padre indice {i} (prioridad {heap[i][0]}) > Hijo der indice {hijo_der} (prioridad {heap[hijo_der][0]})")
            return False

    return True