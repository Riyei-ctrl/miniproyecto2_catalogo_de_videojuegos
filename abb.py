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

    def sucesor(self, nodo):
        """Encuentra el sucesor inorden utilizando el apuntador al padre."""
        if nodo.der is not None:
            return self.minimo(nodo.der)
        
        padre = nodo.padre
        while padre is not None and nodo == padre.der:
            nodo = padre
            padre = padre.padre
        return padre

    def predecesor(self, nodo):
        """
        Encuentra el predecesor inorden utilizando el apuntador al padre.
        """
        if nodo.izq is not None:
            return self.maximo(nodo.izq)

        padre = nodo.padre
        while padre is not None and nodo == padre.izq:
            nodo = padre
            padre = padre.padre
        return padre  

    def obtener_altura_abb(self, nodo):
        """
        Calcula recursivamente la altura máxima de un subárbol en el ABB.
        Sirve para demostrar la degeneración O(n) frente al AVL.
        """
        if nodo is None:
            return 0
            
        altura_izq = self.obtener_altura_abb(nodo.izq)
        altura_der = self.obtener_altura_abb(nodo.der)
        
        return 1 + max(altura_izq, altura_der)

    # RECORRIDOS
    def inorden(self, nodo, resultado=None):
        """Visita: Izquierda, Raíz, Derecha"""
        if resultado is None:
            resultado = []
        if nodo is not None:
            self.inorden(nodo.izq, resultado)
            resultado.append(nodo)
            self.inorden(nodo.der, resultado)
        return resultado

    def preorden(self, nodo, resultado=None):
        """Visita: Raíz, Izquierda, Derecha."""
        if resultado is None:
            resultado = []
        if nodo is not None:
            resultado.append(nodo)
            self.preorden(nodo.izq, resultado)
            self.preorden(nodo.der, resultado)
        return resultado

    def postorden(self, nodo, resultado=None):
        """Visita: Izquierda, Derecha, Raíz."""
        if resultado is None:
            resultado = []
        if nodo is not None:
            self.postorden(nodo.izq, resultado)
            self.postorden(nodo.der, resultado)
            resultado.append(nodo)
        return resultado

    def transplant(self, u, v):
        """
        Reemplaza el subárbol con raíz en 'u' por el subárbol con raíz en 'v'.
        Actualiza correctamente los apuntadores al padre.
        """
        if u.padre is None:
            self.raiz = v
        elif u == u.padre.izq:
            u.padre.izq = v
        else:
            u.padre.der = v
            
        if v is not None:
            v.padre = u.padre         