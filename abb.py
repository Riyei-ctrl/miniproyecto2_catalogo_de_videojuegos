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
        self.padre = padre  # Requisito de los principios de trabajo