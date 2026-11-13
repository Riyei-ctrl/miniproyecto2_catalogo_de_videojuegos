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
    
    def _intercambiar(self, i, j):
        """Intercambia dos elementos y actualiza el diccionario de posiciones."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        # Actualizar posiciones en el mapa de rastreo
        self.posiciones[self.heap[i][1]] = i
        self.posiciones[self.heap[j][1]] = j

    def flotar(self, i):
        """
        Sube un elemento si su prioridad es menor que la de su padre.
        (Sift-Up)
        """
        while i > 0 and self.heap[i][0] < self.heap[self._padre(i)][0]:
            self._intercambiar(i, self._padre(i))
            i = self._padre(i)
