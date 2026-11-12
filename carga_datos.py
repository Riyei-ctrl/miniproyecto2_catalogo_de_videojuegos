import os
import csv
from abb import ABB
from avl import AVL

def detectar_archivo_repositorio():
    """
    Busca automáticamente el archivo de datos dentro de la carpeta 'data/'.
    Prioriza archivos CSV disponibles en 'data/'.
    """
    carpeta_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    if os.path.exists(carpeta_data):
        archivos = os.listdir(carpeta_data)
        for arch in archivos:
            if arch.lower().endswith('.csv'):
                return os.path.join('data', arch)
    return os.path.join('data', 'steam_games.csv')

def cargar_dataset(ruta_archivo=None, genero_objetivo="Action", limite=11000):
    """
    Carga el subconjunto de exactamente 11,000 juegos del género indicado
    directamente desde la carpeta 'data/' utilizando la biblioteca estándar csv.
    Construye y devuelve las tres estructuras del proyecto:
      1. ABB por AppID (Problemas 1 y 2)
      2. ABB por Nombre (Problema 1: listado alfabético sin ordenar cada vez)
      3. AVL por AppID (Problema 3: garantiza costo logarítmico con inserción ordenada)
      4. AVL por Precio (Problema 4: consultas por rango, mín, máx y sucesor)
      5. Lista cruda (Problema 5: montículo para cola editorial y top-k)
    """
    if ruta_archivo is None or not str(ruta_archivo).strip():
        ruta_archivo = detectar_archivo_repositorio()

    if not os.path.exists(ruta_archivo):
        posible = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_archivo)
        if os.path.exists(posible):
            ruta_archivo = posible
        else:
            raise FileNotFoundError(f"No se encontro el archivo en la ruta '{ruta_archivo}'.")
    print(f"\n[Cargando repositorio directamente desde: '{ruta_archivo}']")
    print(f"  Genero objetivo : {genero_objetivo}")
    print(f"  Limite exigido  : {limite} juegos")

    arbol_abb_appid = ABB()
    arbol_abb_nombres = ABB()
    arbol_avl_appid = AVL()
    arbol_avl_precios = AVL()
    lista_juegos = []
    contador = 0

    with open(ruta_archivo, mode='r', encoding='utf-8', errors='replace') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            # Normalizar claves a minúsculas para acceso seguro
            fila_norm = {k.strip().lower(): v for k, v in fila.items() if k}
            generos = fila_norm.get('genres', '')

            if genero_objetivo.lower() in generos.lower():
                try:
                    appid = int(fila_norm.get('appid', 0))
                    nombre = fila_norm.get('name', 'Sin nombre').strip()

                    try:
                        precio = float(fila_norm.get('price', 0.0))
                    except ValueError:
                        precio = 0.0

                    try:
                        positivas = int(fila_norm.get('positive', 0))
                    except ValueError:
                        positivas = 0

                    try:
                        negativas = int(fila_norm.get('negative', 0))
                    except ValueError:
                        negativas = 0

                    fecha = fila_norm.get('release date', fila_norm.get('release_date', ''))

                    datos_juego = {
                        'AppID': appid,
                        'Name': nombre,
                        'Price': precio,
                        'Positive': positivas,
                        'Negative': negativas,
                        'Genres': generos,
                        'Release date': fecha
                    }

                    # 1. ABB por AppID (Problemas 1 y 2)
                    arbol_abb_appid.insertar(appid, datos_juego)

                    # 2. ABB por Nombre (Problema 1: listado alfabético sin sorted)
                    if nombre:
                        arbol_abb_nombres.insertar(nombre.lower(), datos_juego)

                    # 3. AVL por AppID (Problema 3: garantiza O(log n))
                    arbol_avl_appid.insertar(appid, datos_juego)

                    # 4. AVL por Precio en centavos (Problema 4: rango, min, max, sucesor)
                    clave_precio = int(round(precio * 100))
                    arbol_avl_precios.insertar(clave_precio, datos_juego)

                    # 5. Lista para el montículo (Problema 5)
                    lista_juegos.append(datos_juego)

                    contador += 1
                    if contador >= limite:
                        break
                except ValueError:
                    continue
