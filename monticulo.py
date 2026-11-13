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

    def hundir(self, i):
        """
        Baja un elemento si su prioridad es mayor que la de sus hijos.
        (Sift-Down)
        """
        minimo = i
        izq = self._hijo_izq(i)
        der = self._hijo_der(i)
        n = len(self.heap)

        if izq < n and self.heap[izq][0] < self.heap[minimo][0]:
            minimo = izq
        if der < n and self.heap[der][0] < self.heap[minimo][0]:
            minimo = der

        if minimo != i:
            self._intercambiar(i, minimo)
            self.hundir(minimo)

    def insertar(self, prioridad, clave, datos):
        """Inserta un nuevo elemento al final del arreglo y lo hace flotar."""
        if clave in self.posiciones:
            return  # Evitar duplicados exactos si la clave es AppID
            
        nuevo_elemento = [prioridad, clave, datos]
        self.heap.append(nuevo_elemento)
        
        # El nuevo índice es el último
        indice_actual = len(self.heap) - 1
        self.posiciones[clave] = indice_actual
        
        self.flotar(indice_actual)   

    def extraer_minimo(self):
        """Extrae el juego de mayor prioridad (mínimo valor) y reordena el montículo."""
        if not self.heap:
            return None

        minimo_extraido = self.heap[0]
        del self.posiciones[minimo_extraido[1]] # Eliminar del rastreador

        if len(self.heap) > 1:
            # Movemos el último elemento a la raíz y lo hundimos
            self.heap[0] = self.heap.pop()
            self.posiciones[self.heap[0][1]] = 0
            self.hundir(0)
        else:
            self.heap.pop()

        return minimo_extraido

    def decrementar_clave(self, clave, nueva_prioridad):
        """
        Reduce el valor de prioridad de un elemento existente,
        haciendo que suba en el montículo (aumenta su urgencia).
        """
        if clave not in self.posiciones:
            raise KeyError("La clave no existe en el montículo.")
            
        i = self.posiciones[clave]
        
        if nueva_prioridad > self.heap[i][0]:
            raise ValueError("La nueva prioridad debe ser estrictamente menor que la actual.")
            
        self.heap[i][0] = nueva_prioridad
        self.flotar(i)     

    def incrementar_clave(self, clave, nueva_prioridad):
        """
        Aumenta el valor de prioridad de un elemento existente,
        haciendo que baje en el montículo (disminuye su urgencia).
        (Operación simétrica de decrementar clave - Banco de defensa oral).
        """
        if clave not in self.posiciones:
            raise KeyError("La clave no existe en el montículo.")

        i = self.posiciones[clave]

        if nueva_prioridad < self.heap[i][0]:
            raise ValueError("La nueva prioridad debe ser estrictamente mayor que la actual.")

        self.heap[i][0] = nueva_prioridad
        self.hundir(i)               
