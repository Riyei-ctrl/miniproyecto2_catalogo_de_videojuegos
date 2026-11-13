import random
import time
import sys
import math
import heapq
from abb import ABB
from avl import AVL
from monticulo import MinHeap

# Aumentar límite de recursión por si el ABB colapsa en inserciones ordenadas
sys.setrecursionlimit(20000)

def altura_y_tiempo(tamanos_entrada=[1000, 5000, 11000]):
    """
    Realiza las inserciones ordenadas y aleatorias solicitadas para comparar
    degeneración (altura) y tiempos de búsqueda.
    Contrasta ABB, AVL y las estructuras nativas de Python (dict y heapq).
    """
    for n in tamanos_entrada:
        print(f"\n{'='*50}")
        print(f" TAMAÑO DE ENTRADA (N): {n}")
        print(f"{'='*50}")

        datos_ordenados = list(range(1, n + 1))
        datos_aleatorios = datos_ordenados.copy()
        random.shuffle(datos_aleatorios)

        # Objetivo de búsqueda (el peor caso para inserción ordenada es buscar el último)
        clave_a_buscar = n

        for nombre_prueba, dataset in [("INSERCION ORDENADA", datos_ordenados), ("INSERCION ALEATORIA", datos_aleatorios)]:
            print(f"\n--- {nombre_prueba} ---")

            arbol_bb = ABB()
            arbol_avl = AVL()
            heap_propio = MinHeap()
            diccionario_nativo = {}   # Para comparar con la estructura nativa 'dict' de Python
            heap_nativo = []          # Para comparar con heapq

            # --- MEDICIÓN DE INSERCIÓN ---
            # Inserción en ABB
            t0 = time.perf_counter()
            for val in dataset:
                arbol_bb.insertar(val, f"Data_{val}")
            t_ins_abb = time.perf_counter() - t0

            # Inserción en AVL
            t0 = time.perf_counter()
            for val in dataset:
                arbol_avl.insertar(val, f"Data_{val}")
            t_ins_avl = time.perf_counter() - t0

            # Inserción en Montículo propio (MinHeap)
            t0 = time.perf_counter()
            for val in dataset:
                heap_propio.insertar(val, val, f"Data_{val}")
            t_ins_heap_propio = time.perf_counter() - t0

            # Inserción en dict nativo
            t0 = time.perf_counter()
            for val in dataset:
                diccionario_nativo[val] = f"Data_{val}"
            t_ins_dict = time.perf_counter() - t0

            # Inserción en heapq nativo
            t0 = time.perf_counter()
            for val in dataset:
                heapq.heappush(heap_nativo, (val, f"Data_{val}"))
            t_ins_heapq = time.perf_counter() - t0

            # --- MEDICIÓN DE ALTURA ---
            altura_abb = arbol_bb.obtener_altura_abb(arbol_bb.raiz)
            altura_avl = arbol_avl.raiz.altura
            cota_teorica_avl = 1.44 * math.log2(n) if n > 0 else 0

            print(f"\nAlturas:")
            print(f"  Altura ABB            : {altura_abb}")
            print(f"  Altura AVL            : {altura_avl}")
            print(f"  Cota teorica AVL ~    : {cota_teorica_avl:.1f}")
            print(f"  Cota teorica log2(n)  : {math.log2(n):.1f}")

            print(f"\nTiempos de Insercion (N={n}):")
            print(f"  ABB (propio)          : {t_ins_abb:.6f} s")
            print(f"  AVL (propio)          : {t_ins_avl:.6f} s")
            print(f"  MinHeap (propio)      : {t_ins_heap_propio:.6f} s")
            print(f"  dict (nativo)         : {t_ins_dict:.6f} s")
            print(f"  heapq (nativo)        : {t_ins_heapq:.6f} s")

            # --- MEDICIÓN DE TIEMPO DE BÚSQUEDA ---
            # Búsqueda en ABB
            t0 = time.perf_counter()
            arbol_bb.buscar(arbol_bb.raiz, clave_a_buscar)
            t_abb = time.perf_counter() - t0

            # Búsqueda en AVL
            t0 = time.perf_counter()
            arbol_avl.buscar(arbol_avl.raiz, clave_a_buscar)
            t_avl = time.perf_counter() - t0

            # Búsqueda en Python Nativo (O(1) teórico promedio mediante hash table)
            t0 = time.perf_counter()
            _ = diccionario_nativo.get(clave_a_buscar)
            t_nativo = time.perf_counter() - t0

            print(f"\nTiempos de Busqueda (clave={clave_a_buscar}):")
            print(f"  ABB (propio)          : {t_abb:.6f} s")
            print(f"  AVL (propio)          : {t_avl:.6f} s")
            print(f"  dict (nativo)         : {t_nativo:.6f} s")

            # --- MEDICIÓN DE EXTRACCIÓN (MONTÍCULO VS HEAPQ) ---
            t0 = time.perf_counter()
            heap_propio.extraer_minimo()
            t_ext_propio = time.perf_counter() - t0

            t0 = time.perf_counter()
            heapq.heappop(heap_nativo)
            t_ext_heapq = time.perf_counter() - t0

            print(f"\nTiempos de Extraccion Minimo:")
            print(f"  MinHeap (propio)      : {t_ext_propio:.6f} s")
            print(f"  heapq (nativo)        : {t_ext_heapq:.6f} s")

if __name__ == "__main__":
    print("\nIniciando modulo de experimentacion independiente...")
    try:
        altura_y_tiempo([1000, 5000, 11000])
        print("\nPruebas experimentales finalizadas con exito.")
    except Exception as e:
        print(f"\nError en la comparativa: {e}")
        import traceback
        traceback.print_exc()