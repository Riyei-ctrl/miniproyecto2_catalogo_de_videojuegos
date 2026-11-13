class MinHeap:
    """ Implementación de un monticulo binario sobre un arreglo. 
    Los elementos del arreglo seran tuplas/listas: [prioridad, clave, datos]
    """
    def __init__(self):
        self.heap = []
        self.posiciones = {}
    def _padre(self, i):
        return (i - 1)//2
    def _hijo_izq(self, i):
        return 2 * i * 1
    def _hijo_der(self, i):
            return 2 * i * 2
