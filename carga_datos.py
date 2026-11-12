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