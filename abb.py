import sys
# Aumentamos el límite de recursión por si el ABB degenera a O(n) con 11,000 AppIDs ordenados
sys.setrecursionlimit(15000)

class NodoABB:
    """Estructura base del nodo, incluyendo el apuntador al padre exigido."""
    def _init_(self, clave, datos, padre=None):
        self.clave = clave
        self.datos = datos
        self.izq = None
        self.der = None
        self.padre = padre  

class ABB:
    """Árbol Binario de Búsqueda para el Catálogo de Videojuegos."""
    def _init_(self):
        self.raiz = None

    def insertar(self, clave, datos):
        """Inserción iterativa para evitar desbordamiento de pila en árboles degenerados."""
        nuevo_nodo = NodoABB(clave, datos)
        if self.raiz is None:
            self.raiz = nuevo_nodo
            return

        actual = self.raiz
        padre = None
        while actual is not None:
            padre = actual
            if clave == actual.clave:
                # Política de claves: Rechazar duplicados para AppID
                return 
            elif clave < actual.clave:
                actual = actual.izq
            else:
                actual = actual.der

        nuevo_nodo.padre = padre
        if clave < padre.clave:
            padre.izq = nuevo_nodo
        else:
            padre.der = nuevo_nodo    

    def buscar(self, nodo, clave):
        """Búsqueda recursiva estándar."""
        if nodo is None or clave == nodo.clave:
            return nodo
        if clave < nodo.clave:
            return self.buscar(nodo.izq, clave)
        return self.buscar(nodo.der, clave)

    def minimo(self, nodo):
        """Encuentra el nodo más a la izquierda."""
        while nodo.izq is not None:
            nodo = nodo.izq
        return nodo

    def maximo(self, nodo):
        """Encuentra el nodo más a la derecha."""
        while nodo.der is not None:
            nodo = nodo.der
        return nodo            