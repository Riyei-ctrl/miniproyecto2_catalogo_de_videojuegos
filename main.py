import sys
import heapq
import time
from abb import ABB
from avl import AVL, NodoAVL, OperacionesAVL
from monticulo import MinHeap
from verificadores import (
    verificar_invariante_avl,
    verificar_invariante_abb,
    verificar_invariante_heap
)
from carga_datos import cargar_dataset

def probar_abb():
    """
    Valida la inserción, los 3 recorridos, las búsquedas,
    mínimo, máximo, sucesor y la eliminación en los 3 casos.
    (Criterios 3, 4 y 5 de la lista de cotejo).
    """
    print("\n" + "="*55)
    print("  PRUEBA 1: ARBOL BINARIO DE BUSQUEDA (ABB)")
    print("="*55)
    arbol = ABB()
    claves = [50, 30, 70, 20, 40, 60, 80]
    for c in claves:
        arbol.insertar(c, {"Name": f"Juego_{c}"})

    # Verificación del invariante
    print(f"Invariante ABB cumple: {verificar_invariante_abb(arbol.raiz)}")

    # Criterio 5: Los tres recorridos
    inorden = [nodo.clave for nodo in arbol.inorden(arbol.raiz)]
    preorden = [nodo.clave for nodo in arbol.preorden(arbol.raiz)]
    postorden = [nodo.clave for nodo in arbol.postorden(arbol.raiz)]
    print(f"Recorrido Inorden   (ordenado) : {inorden}")
    print(f"Recorrido Preorden  (raiz-i-d) : {preorden}")
    print(f"Recorrido Postorden (i-d-raiz) : {postorden}")

    # Criterio 3: Mínimo, máximo, búsqueda y sucesor
    min_nodo = arbol.minimo(arbol.raiz)
    max_nodo = arbol.maximo(arbol.raiz)
    nodo_40 = arbol.buscar(arbol.raiz, 40)
    suc_40 = arbol.sucesor(nodo_40)
    print(f"Minimo (esperado 20)           : {min_nodo.clave}")
    print(f"Maximo (esperado 80)           : {max_nodo.clave}")
    print(f"Busqueda de 40                 : {'Encontrado' if nodo_40 else 'Fallo'}")
    print(f"Sucesor de 40 (esperado 50)    : {suc_40.clave if suc_40 else 'None'}")
    print(f"Altura del ABB                 : {arbol.obtener_altura_abb(arbol.raiz)}")

    # Criterio 4: Eliminación en los tres casos con TRANSPLANT
    print("\n--- Eliminacion en ABB (3 casos con TRANSPLANT) ---")
    # Caso 1: Nodo sin hijos (hoja)
    nodo_20 = arbol.buscar(arbol.raiz, 20)
    arbol.eliminar(nodo_20)
    print(f"Caso 1 (Hoja: 20)          -> Inorden: {[n.clave for n in arbol.inorden(arbol.raiz)]}")
    print(f"  Invariante ABB cumple    : {verificar_invariante_abb(arbol.raiz)}")

    # Caso 2: Nodo con un solo hijo
    nodo_30 = arbol.buscar(arbol.raiz, 30)
    arbol.eliminar(nodo_30)
    print(f"Caso 2 (Un solo hijo: 30)  -> Inorden: {[n.clave for n in arbol.inorden(arbol.raiz)]}")
    print(f"  Invariante ABB cumple    : {verificar_invariante_abb(arbol.raiz)}")

    # Caso 3: Nodo con dos hijos (sustituye por sucesor)
    nodo_50 = arbol.buscar(arbol.raiz, 50)
    arbol.eliminar(nodo_50)
    print(f"Caso 3 (Dos hijos: 50)     -> Inorden: {[n.clave for n in arbol.inorden(arbol.raiz)]}")
    print(f"  Invariante ABB cumple    : {verificar_invariante_abb(arbol.raiz)}")