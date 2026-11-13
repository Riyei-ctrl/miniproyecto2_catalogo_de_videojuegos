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

def probar_avl_rotaciones_aisladas():
    """
    Prueba aislada de las cuatro rotaciones con árboles pequeños construidos a mano,
    seguida de inserción y eliminación con rebalanceo en cascada y verificación de invariante.
    (Criterios 6 y 7 de la lista de cotejo).
    """
    print("\n" + "="*55)
    print("  PRUEBA 2: ROTACIONES AVL E INVARIANTE")
    print("="*55)

    # 1. Caso LL (Left-Left) -> Rotación Simple Derecha
    print("\n--- 1. Caso Left-Left (LL) - Requiere Rotacion Derecha ---")
    raiz = NodoAVL(30, "A")
    hijo_izq = NodoAVL(20, "B", padre=raiz)
    nieto_izq = NodoAVL(10, "C", padre=hijo_izq)
    raiz.izq = hijo_izq
    hijo_izq.izq = nieto_izq
    nieto_izq.altura = 1
    hijo_izq.altura = 2
    raiz.altura = 3
    print("  Estado inicial desbalanceado (factor de balance = +2):")
    print(f"    Invariante AVL cumple: {verificar_invariante_avl(raiz)}")
    nueva_raiz = OperacionesAVL.rotacion_derecha(raiz)
    print("  Despues de rotacion derecha (LL):")
    print(f"    Nueva raiz (esperado 20) : {nueva_raiz.clave}")
    print(f"    Hijo izq   (esperado 10) : {nueva_raiz.izq.clave}")
    print(f"    Hijo der   (esperado 30) : {nueva_raiz.der.clave}")
    print(f"    Invariante AVL cumple    : {verificar_invariante_avl(nueva_raiz)}")

    # 2. Caso RR (Right-Right) -> Rotación Simple Izquierda
    print("\n--- 2. Caso Right-Right (RR) - Requiere Rotacion Izquierda ---")
    raiz2 = NodoAVL(10, "A")
    hijo_der = NodoAVL(20, "B", padre=raiz2)
    nieto_der = NodoAVL(30, "C", padre=hijo_der)
    raiz2.der = hijo_der
    hijo_der.der = nieto_der
    nieto_der.altura = 1
    hijo_der.altura = 2
    raiz2.altura = 3
    print("  Estado inicial desbalanceado (factor de balance = -2):")
    print(f"    Invariante AVL cumple: {verificar_invariante_avl(raiz2)}")
    nueva_raiz2 = OperacionesAVL.rotacion_izquierda(raiz2)
    print("  Despues de rotacion izquierda (RR):")
    print(f"    Nueva raiz (esperado 20) : {nueva_raiz2.clave}")
    print(f"    Hijo izq   (esperado 10) : {nueva_raiz2.izq.clave}")
    print(f"    Hijo der   (esperado 30) : {nueva_raiz2.der.clave}")
    print(f"    Invariante AVL cumple    : {verificar_invariante_avl(nueva_raiz2)}")

    # 3. Caso LR (Left-Right) -> Rotación Doble Izquierda-Derecha
    print("\n--- 3. Caso Left-Right (LR) - Requiere Rotacion Doble Izq-Der ---")
    raiz3 = NodoAVL(30, "A")
    hijo_izq3 = NodoAVL(10, "B", padre=raiz3)
    nieto_der3 = NodoAVL(20, "C", padre=hijo_izq3)
    raiz3.izq = hijo_izq3
    hijo_izq3.der = nieto_der3
    nieto_der3.altura = 1
    hijo_izq3.altura = 2
    raiz3.altura = 3
    print("  Estado inicial desbalanceado:")
    print(f"    Invariante AVL cumple: {verificar_invariante_avl(raiz3)}")
    nueva_raiz3 = OperacionesAVL.rotacion_izquierda_derecha(raiz3)
    print("  Despues de rotacion doble LR:")
    print(f"    Nueva raiz (esperado 20) : {nueva_raiz3.clave}")
    print(f"    Hijo izq   (esperado 10) : {nueva_raiz3.izq.clave}")
    print(f"    Hijo der   (esperado 30) : {nueva_raiz3.der.clave}")
    print(f"    Invariante AVL cumple    : {verificar_invariante_avl(nueva_raiz3)}")

    # 4. Caso RL (Right-Left) -> Rotación Doble Derecha-Izquierda
    print("\n--- 4. Caso Right-Left (RL) - Requiere Rotacion Doble Der-Izq ---")
    raiz4 = NodoAVL(10, "A")
    hijo_der4 = NodoAVL(30, "B", padre=raiz4)
    nieto_izq4 = NodoAVL(20, "C", padre=hijo_der4)
    raiz4.der = hijo_der4
    hijo_der4.izq = nieto_izq4
    nieto_izq4.altura = 1
    hijo_der4.altura = 2
    raiz4.altura = 3
    print("  Estado inicial desbalanceado:")
    print(f"    Invariante AVL cumple: {verificar_invariante_avl(raiz4)}")
    nueva_raiz4 = OperacionesAVL.rotacion_derecha_izquierda(raiz4)
    print("  Despues de rotacion doble RL:")
    print(f"    Nueva raiz (esperado 20) : {nueva_raiz4.clave}")
    print(f"    Hijo izq   (esperado 10) : {nueva_raiz4.izq.clave}")
    print(f"    Hijo der   (esperado 30) : {nueva_raiz4.der.clave}")
    print(f"    Invariante AVL cumple    : {verificar_invariante_avl(nueva_raiz4)}")

    # Inserción con rebalanceo en cascada
    print("\n--- 5. Insercion AVL con rebalanceo en cascada hasta la raiz ---")
    avl = AVL()
    secuencia = [10, 20, 30, 25, 28, 5, 3]
    for v in secuencia:
        avl.insertar(v, f"Data_{v}")
    inorden = [n.clave for n in avl.inorden(avl.raiz)]
    print(f"  Secuencia insertada      : {secuencia}")
    print(f"  Inorden resultante       : {inorden}")
    print(f"  Raiz del arbol           : {avl.raiz.clave}")
    print(f"  Altura del arbol         : {avl.raiz.altura}")
    print(f"  Invariante AVL cumple    : {verificar_invariante_avl(avl.raiz)}")

    # Eliminación con rebalanceo en cascada
    print("\n--- 6. Eliminacion AVL con rebalanceo en cascada ---")
    nodo_3 = avl.buscar(avl.raiz, 3)
    avl.eliminar(nodo_3)
    print(f"  Eliminado nodo con clave 3 -> Inorden: {[n.clave for n in avl.inorden(avl.raiz)]}")
    print(f"  Invariante AVL cumple    : {verificar_invariante_avl(avl.raiz)}")

def probar_monticulo():
    """
    Valida el min-heap sobre arreglo: flotar, hundir, inserción,
    extracción del mínimo, decrementar clave y verificador de invariante.
    (Criterio 8 de la lista de cotejo).
    """
    print("\n" + "="*55)
    print("  PRUEBA 3: MONTICULO BINARIO (MIN-HEAP SOBRE ARREGLO)")
    print("="*55)
    heap = MinHeap()
    inserciones = [(10, 101, "Juego A"), (5, 102, "Juego B"), (20, 103, "Juego C"), (1, 104, "Juego D")]

    for prioridad, clave, datos in inserciones:
        heap.insertar(prioridad, clave, {"Name": datos})

    print(f"Prioridades en el arreglo interno: {[elem[0] for elem in heap.heap]}")
    print(f"Invariante min-heap cumple        : {verificar_invariante_heap(heap.heap)}")

    print("\nDecrementando prioridad del Juego C (clave 103) de 20 a 0...")
    heap.decrementar_clave(103, 0)
    print(f"Prioridades tras decrementar      : {[elem[0] for elem in heap.heap]}")
    print(f"Invariante min-heap cumple        : {verificar_invariante_heap(heap.heap)}")

    print("\nExtrayendo en orden de prioridad (debe salir Juego C con prioridad 0 primero):")
    while heap.heap:
        extraido = heap.extraer_minimo()
        print(f"  Prioridad: {extraido[0]}, Juego: {extraido[2]['Name']} (Clave: {extraido[1]})")

def atender_revision_editorial(lista_juegos):
    """
    Problema 5a: Atiende primero al juego con más valoraciones negativas
    usando un MinHeap propio. Contrasta tiempos y resultados con heapq.
    """
    print("\n" + "-"*55)
    print("  COLA DE REVISION EDITORIAL (Juegos con mas valoraciones negativas)")
    print("-"*55)

    heap_propio = MinHeap()

    t0 = time.perf_counter()
    for juego in lista_juegos:
        # Prioridad negativa: el juego con MAS negativas tiene menor número y sale primero
        prioridad = -juego['Negative']
        heap_propio.insertar(prioridad, juego['AppID'], juego)
    t_construccion_propio = time.perf_counter() - t0

    print(f"Monticulo propio construido con {len(lista_juegos)} juegos.")
    print(f"Tiempo de construccion (MinHeap propio) : {t_construccion_propio:.6f} s")
    print(f"Invariante min-heap cumple              : {verificar_invariante_heap(heap_propio.heap)}")

    print("\nLos 10 juegos mas urgentes de revision (mayor cantidad de negativas):")
    for i in range(min(10, len(heap_propio.heap))):
        extraido = heap_propio.extraer_minimo()
        juego = extraido[2]
        print(f"  {i+1}. {juego['Name']} (AppID: {juego['AppID']}) - Negativas: {juego['Negative']}")

    # Contraste con heapq nativo
    print("\n--- Contraste con heapq nativo de Python ---")
    heap_nativo = []
    t0 = time.perf_counter()
    for juego in lista_juegos:
        heapq.heappush(heap_nativo, (-juego['Negative'], juego['AppID'], juego['Name']))
    t_construccion_nativo = time.perf_counter() - t0
    print(f"Tiempo de construccion (heapq nativo)   : {t_construccion_nativo:.6f} s")

    print("Los 10 juegos con mas negativas extraidos con heapq:")
    for i in range(min(10, len(heap_nativo))):
        neg, appid, nombre = heapq.heappop(heap_nativo)
        print(f"  {i+1}. {nombre} (AppID: {appid}) - Negativas: {-neg}")


def obtener_top_k_positivos(lista_juegos, k=10):
    """
    Problema 5b: Obtiene los k juegos con más valoraciones positivas
    mediante un montículo acotado de tamaño k.
    Contrasta tiempos y resultados con heapq.nlargest.
    """
    print("\n" + "-"*55)
    print(f"  TOP-{k} JUEGOS CON MAS VALORACIONES POSITIVAS")
    print("-"*55)

    # Montículo acotado propio de tamaño k (min-heap donde la raíz es el mínimo del top actual)
    heap_topk = MinHeap()

    t0 = time.perf_counter()
    for juego in lista_juegos:
        positivas = juego['Positive']
        if len(heap_topk.heap) < k:
            heap_topk.insertar(positivas, juego['AppID'], juego)
        else:
            if positivas > heap_topk.heap[0][0]:
                heap_topk.extraer_minimo()
                heap_topk.insertar(positivas, juego['AppID'], juego)
    t_propio = time.perf_counter() - t0

    # Extraer y ordenar descendentemente
    top_extraidos = []
    while heap_topk.heap:
        top_extraidos.append(heap_topk.extraer_minimo())
    top_extraidos.reverse()

    print(f"Tiempo de ejecucion (MinHeap acotado k={k}) : {t_propio:.6f} s")
    print(f"Top-{k} juegos con mas valoraciones positivas (Monticulo Propio):")
    for i, elem in enumerate(top_extraidos):
        juego = elem[2]
        print(f"  {i+1}. {juego['Name']} (AppID: {juego['AppID']}) - Positivas: {juego['Positive']}")

    # Contraste con heapq.nlargest
    t0 = time.perf_counter()
    top_nativo = heapq.nlargest(k, lista_juegos, key=lambda j: j['Positive'])
    t_nativo = time.perf_counter() - t0

    print(f"\nTiempo de ejecucion (heapq.nlargest)        : {t_nativo:.6f} s")
    print(f"Top-{k} con heapq.nlargest:")
    for i, juego in enumerate(top_nativo):
        print(f"  {i+1}. {juego['Name']} (AppID: {juego['AppID']}) - Positivas: {juego['Positive']}")

def mostrar_menu():
    print("\n" + "="*60)
    print("      CATALOGO CONSULTABLE DE VIDEOJUEGOS - STEAM")
    print("="*60)
    print("1. Cargar subconjunto de datos (Construir estructuras)")
    print("2. Problema 1: Buscar por AppID y Listar Alfabeticamente")
    print("3. Problema 2: Dar de baja un juego por AppID (con TRANSPLANT)")
    print("4. Problemas 3 y 4: Consultar por rango de precios en AVL")
    print("5. Problema 5: Cola Editorial y Top-K Positivos (Monticulo)")
    print("6. Bateria de pruebas tecnicas completas (Criterios 3-8)")
    print("7. Salir")
    print("="*60)


def main():
    catalogo_cargado = False
    estructuras = None

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opcion (1-7): ").strip()

        if opcion == '1':
            print("\n[Cargando dataset directamente desde la carpeta 'data/' (11,000 juegos)...]")
            try:
                estructuras = cargar_dataset(limite=11000)
                catalogo_cargado = True
                print("\n[Verificando invariantes de las estructuras construidas]")
                print(f"  Invariante ABB por AppID   : {verificar_invariante_abb(estructuras['abb_appid'].raiz)}")
                print(f"  Invariante AVL por AppID   : {verificar_invariante_avl(estructuras['avl_appid'].raiz)}")
                print(f"  Invariante AVL por Precio  : {verificar_invariante_avl(estructuras['avl_precios'].raiz)}")
                print(">>> Estructuras creadas y verificadas correctamente desde la carpeta data/ <<<")
            except Exception as e:
                print(f"\nError al cargar los datos desde data/: {e}")

        elif opcion == '2':
            if not catalogo_cargado:
                print("\nPrimero debes cargar el catalogo (Opcion 1).")
                continue

            print("\n--- PROBLEMA 1: LOCALIZAR POR APPID Y LISTADO ALFABETICO ---")
            entrada_appid = input("Ingresa el AppID a buscar (o presiona ENTER para solo listar): ").strip()

            if entrada_appid:
                try:
                    appid = int(entrada_appid)
                    # Búsqueda en ABB y en AVL para comparar
                    t0 = time.perf_counter()
                    nodo_abb = estructuras['abb_appid'].buscar(estructuras['abb_appid'].raiz, appid)
                    t_busqueda_abb = time.perf_counter() - t0

                    t0 = time.perf_counter()
                    nodo_avl = estructuras['avl_appid'].buscar(estructuras['avl_appid'].raiz, appid)
                    t_busqueda_avl = time.perf_counter() - t0

                    if nodo_abb:
                        juego = nodo_abb.datos
                        print(f"\n  Juego encontrado:")
                        print(f"    AppID       : {juego['AppID']}")
                        print(f"    Nombre      : {juego['Name']}")
                        print(f"    Precio      : ${juego['Price']}")
                        print(f"    Positivas   : {juego['Positive']}")
                        print(f"    Negativas   : {juego['Negative']}")
                        print(f"    Generos     : {juego['Genres']}")
                        print(f"    Fecha       : {juego['Release date']}")
                        print(f"    Tiempo busqueda ABB : {t_busqueda_abb:.8f} s")
                        print(f"    Tiempo busqueda AVL : {t_busqueda_avl:.8f} s")

                        # Sucesor inorden por AppID
                        sucesor = estructuras['abb_appid'].sucesor(nodo_abb)
                        if sucesor:
                            print(f"    Sucesor por AppID   : {sucesor.datos['Name']} (AppID: {sucesor.clave})")
                    else:
                        print(f"\n  No se encontro ningun juego con AppID {appid}.")
                except ValueError:
                    print("El AppID debe ser un numero entero.")

            # Listado alfabético usando el recorrido inorden del ABB de nombres (SIN SORTED)
            print("\n--- Listado alfabético de juegos (recorrido inorden de ABB por Nombre, sin ordenar) ---")
            nodos_alfabeticos = estructuras['abb_nombres'].inorden(estructuras['abb_nombres'].raiz)
            mostrar_k = min(20, len(nodos_alfabeticos))
            for i in range(mostrar_k):
                juego = nodos_alfabeticos[i].datos
                print(f"  {i+1}. {juego['Name']} (AppID: {juego['AppID']}, Precio: ${juego['Price']})")
            if len(nodos_alfabeticos) > mostrar_k:
                print(f"  ... y {len(nodos_alfabeticos) - mostrar_k} juegos mas en el catalogo.")

        elif opcion == '3':
            if not catalogo_cargado:
                print("\nPrimero debes cargar el catalogo (Opcion 1).")
                continue

            print("\n--- PROBLEMA 2: DAR DE BAJA UN JUEGO (RETIRO DE TIENDA) ---")
            try:
                appid = int(input("Ingresa el AppID del juego a dar de baja: ").strip())
                nodo_a_eliminar = estructuras['abb_appid'].buscar(estructuras['abb_appid'].raiz, appid)

                if nodo_a_eliminar:
                    nombre = nodo_a_eliminar.datos['Name']
                    precio = nodo_a_eliminar.datos['Price']

                    # 1. Eliminar del ABB por AppID
                    estructuras['abb_appid'].eliminar(nodo_a_eliminar)
                    print(f"\n  Juego '{nombre}' (AppID: {appid}) eliminado del ABB.")
                    print(f"  Invariante ABB tras eliminar: {verificar_invariante_abb(estructuras['abb_appid'].raiz)}")

                    # 2. Eliminar del ABB por Nombre
                    nodo_nombre = estructuras['abb_nombres'].buscar(estructuras['abb_nombres'].raiz, nombre.lower())
                    if nodo_nombre:
                        estructuras['abb_nombres'].eliminar(nodo_nombre)

                    # 3. Eliminar del AVL por AppID
                    nodo_avl_id = estructuras['avl_appid'].buscar(estructuras['avl_appid'].raiz, appid)
                    if nodo_avl_id:
                        estructuras['avl_appid'].eliminar(nodo_avl_id)
                        print(f"  Invariante AVL por AppID tras eliminar: {verificar_invariante_avl(estructuras['avl_appid'].raiz)}")

                    # 4. Eliminar del AVL por Precio
                    clave_precio = int(round(precio * 100))
                    nodo_precio = estructuras['avl_precios'].buscar(estructuras['avl_precios'].raiz, clave_precio)
                    if nodo_precio:
                        # Si tiene encadenados varios, remover este juego de la lista
                        nodo_precio.lista_datos = [j for j in nodo_precio.lista_datos if j['AppID'] != appid]
                        if not nodo_precio.lista_datos:
                            estructuras['avl_precios'].eliminar(nodo_precio)

                    # 5. Eliminar de la lista cruda
                    estructuras['lista'] = [j for j in estructuras['lista'] if j['AppID'] != appid]
                    print(f"  Baja completada con exito. Capacidad de consulta y orden conservados.")
                else:
                    print(f"  No se encontro el juego con AppID {appid}.")
            except ValueError:
                print("El AppID debe ser un numero entero.")

        elif opcion == '4':
            if not catalogo_cargado:
                print("\nPrimero debes cargar el catalogo (Opcion 1).")
                continue

            print("\n--- PROBLEMAS 3 Y 4: CONSULTA POR RANGO DE PRECIOS EN AVL ---")
            try:
                min_p = float(input("Precio minimo (USD): ").strip())
                max_p = float(input("Precio maximo (USD): ").strip())

                clave_min = int(round(min_p * 100))
                clave_max = int(round(max_p * 100))

                t0 = time.perf_counter()
                nodos_en_rango = estructuras['avl_precios'].rango(estructuras['avl_precios'].raiz, clave_min, clave_max)
                t_rango = time.perf_counter() - t0

                # Desempaquetar juegos encadenados
                todos_juegos_rango = []
                for n in nodos_en_rango:
                    for j in n.lista_datos:
                        todos_juegos_rango.append(j)

                if todos_juegos_rango:
                    print(f"\nSe encontraron {len(todos_juegos_rango)} juegos en el rango [${min_p}, ${max_p}] en {t_rango:.6f} s:")
                    mostrar_k = min(25, len(todos_juegos_rango))
                    for i in range(mostrar_k):
                        jg = todos_juegos_rango[i]
                        print(f"  {i+1}. {jg['Name']} - ${jg['Price']} (AppID: {jg['AppID']})")
                    if len(todos_juegos_rango) > mostrar_k:
                        print(f"  ... y {len(todos_juegos_rango) - mostrar_k} juegos mas en el rango.")

                    # Juego más barato y más caro en el rango
                    mas_barato = nodos_en_rango[0].lista_datos[0]
                    mas_caro = nodos_en_rango[-1].lista_datos[-1]
                    print(f"\n  Juego mas barato en el rango : {mas_barato['Name']} (${mas_barato['Price']})")
                    print(f"  Juego mas caro en el rango   : {mas_caro['Name']} (${mas_caro['Price']})")

                    # Sucesor inorden del más caro (siguiente precio superior al rango)
                    sucesor_caro = estructuras['avl_precios'].sucesor(nodos_en_rango[-1])
                    if sucesor_caro:
                        siguiente_juego = sucesor_caro.lista_datos[0]
                        print(f"  Registro inmediatamente siguiente al rango : {siguiente_juego['Name']} (${siguiente_juego['Price']})")
                    else:
                        print(f"  No hay registro siguiente (el rango alcanza el precio maximo de la tienda).")

                    # Extremos globales del catálogo
                    min_global = estructuras['avl_precios'].minimo(estructuras['avl_precios'].raiz)
                    max_global = estructuras['avl_precios'].maximo(estructuras['avl_precios'].raiz)
                    print(f"\n  Juego mas barato del catalogo: {min_global.lista_datos[0]['Name']} (${min_global.lista_datos[0]['Price']})")
                    print(f"  Juego mas caro del catalogo  : {max_global.lista_datos[0]['Name']} (${max_global.lista_datos[0]['Price']})")
                else:
                    print(f"\nNo se encontraron juegos en el rango [${min_p}, ${max_p}].")
            except ValueError:
                print("Los precios deben ser valores numericos.")

        elif opcion == '5':
            if not catalogo_cargado:
                print("\nPrimero debes cargar el catalogo (Opcion 1).")
                continue

            print("\n--- PROBLEMA 5: COLA DE PRIORIDAD EDITORIAL Y TOP-K ---")
            atender_revision_editorial(estructuras['lista'])
            obtener_top_k_positivos(estructuras['lista'], k=10)

        elif opcion == '6':
            print("\n[Ejecutando bateria de pruebas tecnicas completas...]")
            try:
                probar_abb()
                probar_avl_rotaciones_aisladas()
                probar_monticulo()
                print("\n" + "="*55)
                print(">>> TODAS LAS PRUEBAS TECNICAS FINALIZARON CON EXITO <<<")
                print("="*55)
            except Exception as e:
                print(f"\nError en las pruebas: {e}")
                import traceback
                traceback.print_exc()

        elif opcion == '7':
            print("\nSaliendo del sistema de Catalogo de Videojuegos. ¡Hasta luego!")
            sys.exit(0)

        else:
            print("\nOpcion no valida. Por favor selecciona un numero entre 1 y 7.")


if __name__ == "__main__":
    main()