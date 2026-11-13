class NodoAVL:
   """
    Extension del nodo base para el AVL
    Guarda el apuntador al padre y la altura del nodo
    Politica de duplicados: Encadenar en una lista (self.lista_datos)
    """
def __init__(self, clave, datos, padre=None):
        self.clave = clave
        self.datos = datos  # Primer registro asociado
        self.lista_datos = [datos]  # Lista para encadenar duplicados con la misma clave
        self.izq = None
        self.der = None
        self.padre = padre
        self.altura = 1  # Los nodos nuevos se insertan como hojas con altura 1

def obtener_altura(nodo):
    """Devuelve la altura de un nodo de forma segura."""
    if not nodo:
        return 0
    return nodo.altura

def obtener_balance(nodo):
    """
    Calcula el factor de balance del nodo.
    Factor de balance = Altura(Subarbol Izquierdo) - Altura(Subarbol Derecho).
    """
    if not nodo:
        return 0
    return obtener_altura(nodo.izq) - obtener_altura(nodo.der)

def actualizar_altura(nodo):
    """Actualiza la altura de un nodo basandose en sus hijos."""
    if nodo:
        nodo.altura = 1 + max(obtener_altura(nodo.izq), obtener_altura(nodo.der))

class OperacionesAVL:
    """
    Clase contenedora de las rotaciones AVL aisladas para pruebas.
    """
    def rotacion_derecha(y):
        """
        Rotacion simple a la derecha, aplica para el caso Left-Left (LL).
        """
        x = y.izq
        T2 = x.der

        # Realizar la rotacion
        x.der = y
        y.izq = T2

        # Actualizar padres
        x.padre = y.padre
        if y.padre is not None:
            if y == y.padre.der:
                y.padre.der = x
            else:
                y.padre.izq = x
                
        y.padre = x
        if T2 is not None:
            T2.padre = y

        # Actualizar alturas
        actualizar_altura(y)
        actualizar_altura(x)

        # Retornar la nueva raíz del subárbol
        return x

    def rotacion_izquierda(x):
        """
        Rotacion simple a la izquierda, aplica para el caso Right-Right (RR).
        """
        y = x.der
        T2 = y.izq

        # Realizar la rotacion
        y.izq = x
        x.der = T2

        # Actualizar padres
        y.padre = x.padre
        if x.padre is not None:
            if x == x.padre.izq:
                x.padre.izq = y
            else:
                x.padre.der = y
                
        x.padre = y
        if T2 is not None:
            T2.padre = x

        # Actualizar alturas
        actualizar_altura(x)
        actualizar_altura(y)

        return y

    def rotacion_izquierda_derecha(z):
        """
        Rotacion doble Left-Right (LR)
        Se aplica rotacion izquierda al hijo izquierdo, luego derecha a la raiz.
        """
        z.izq = OperacionesAVL.rotacion_izquierda(z.izq)
        return OperacionesAVL.rotacion_derecha(z)

    def rotacion_derecha_izquierda(z):
        """
        Rotacion doble Right-Left (RL).
        Se aplica rotacion derecha al hijo derecho, luego izquierda a la raiz.
        """
        z.der = OperacionesAVL.rotacion_derecha(z.der)
        return OperacionesAVL.rotacion_izquierda(z)

class AVL:
    def __init__(self):
        self.raiz = None

    def rebalancear_cascada(self, nodo):
        """
        Sube por el arbol desde el nodo dado hasta la raiz,
        actualizando alturas y aplicando rotaciones si hay desbalance.
        """
        while nodo is not None:
            actualizar_altura(nodo)
            balance = obtener_balance(nodo)

            # Caso Desbalanceado por la Izquierda
            if balance > 1:
                # Verificar si es caso LR o LL
                if obtener_balance(nodo.izq) < 0:
                    nodo = OperacionesAVL.rotacion_izquierda_derecha(nodo) # LR
                else:
                    nodo = OperacionesAVL.rotacion_derecha(nodo) # LL

            # Caso Desbalanceado por la Derecha
            elif balance < -1:
                # Verificar si es caso RL o RR
                if obtener_balance(nodo.der) > 0:
                    nodo = OperacionesAVL.rotacion_derecha_izquierda(nodo) # RL
                else:
                    nodo = OperacionesAVL.rotacion_izquierda(nodo) # RR

            # Si la rotacion modificó la raiz del arbol completo, la actualizamos
            if nodo.padre is None:
                self.raiz = nodo

            # Subir al padre para continuar la cascada hacia la raiz
            nodo = nodo.padre

    def insertar(self, clave, datos):
        """
        Insercion iterativa estilo ABB, seguida del rebalanceo en cascada.
        """
        nuevo_nodo = NodoAVL(clave, datos)
        if self.raiz is None:
            self.raiz = nuevo_nodo
            return

        actual = self.raiz
        padre = None
        while actual is not None:
            padre = actual
            if clave == actual.clave:
                # Politica de duplicados: Encadenar en el mismo nodo
                actual.lista_datos.append(datos)
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

        # Rebalancear desde el padre del nuevo nodo hasta la raiz
        self.rebalancear_cascada(nuevo_nodo.padre)

    def buscar(self, nodo, clave):
        """Busqueda recursiva estandar en el AVL."""
        if nodo is None or clave == nodo.clave:
            return nodo
        if clave < nodo.clave:
            return self.buscar(nodo.izq, clave)
        return self.buscar(nodo.der, clave)

    def minimo(self, nodo):
        """Encuentra el nodo mas a la izquierda."""
        while nodo.izq is not None:
            nodo = nodo.izq
        return nodo

    def maximo(self, nodo):
        """Encuentra el nodo mas a la derecha."""
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

    def inorden(self, nodo, resultado=None):
        """Recorrido Inorden: Izquierda, Raiz, Derecha."""
        if resultado is None:
            resultado = []
        if nodo is not None:
            self.inorden(nodo.izq, resultado)
            resultado.append(nodo)
            self.inorden(nodo.der, resultado)
        return resultado

    def preorden(self, nodo, resultado=None):
        """Recorrido Preorden: Raiz, Izquierda, Derecha."""
        if resultado is None:
            resultado = []
        if nodo is not None:
            resultado.append(nodo)
            self.preorden(nodo.izq, resultado)
            self.preorden(nodo.der, resultado)
        return resultado

    def postorden(self, nodo, resultado=None):
        """Recorrido Postorden: Izquierda, Derecha, Raiz."""
        if resultado is None:
            resultado = []
        if nodo is not None:
            self.postorden(nodo.izq, resultado)
            self.postorden(nodo.der, resultado)
            resultado.append(nodo)
        return resultado

    def transplant(self, u, v):
        """
        Reemplaza el subarbol con raiz en 'u' por el subarbol con raiz en 'v'
        Actualiza los apuntadores al padre.
        """
        if u.padre is None:
            self.raiz = v
        elif u == u.padre.izq:
            u.padre.izq = v
        else:
            u.padre.der = v

        if v is not None:
            v.padre = u.padre

    def eliminar(self, nodo_z):
        """
        Elimina el nodo_z del AVL manejando los tres casos clasicos
        y aplicando rebalanceo en cascada despues de la eliminacion.
        """
        if nodo_z is None:
            return

        # Guardar referencia al nodo desde donde se hara el rebalanceo
        nodo_afectado = None

        # Caso 1: No tiene hijo izquierdo
        if nodo_z.izq is None:
            nodo_afectado = nodo_z.padre
            self.transplant(nodo_z, nodo_z.der)

        # Caso 2: No tiene hijo derecho
        elif nodo_z.der is None:
            nodo_afectado = nodo_z.padre
            self.transplant(nodo_z, nodo_z.izq)

        # Caso 3: Tiene dos hijos
        else:
            nodo_y = self.minimo(nodo_z.der)

            if nodo_y.padre != nodo_z:
                nodo_afectado = nodo_y.padre
                self.transplant(nodo_y, nodo_y.der)
                nodo_y.der = nodo_z.der
                nodo_y.der.padre = nodo_y
            else:
                nodo_afectado = nodo_y

            self.transplant(nodo_z, nodo_y)
            nodo_y.izq = nodo_z.izq
            nodo_y.izq.padre = nodo_y

        # Rebalanceo en cascada desde el nodo afectado hasta la raiz
        if nodo_afectado is not None:
            self.rebalancear_cascada(nodo_afectado)

    def rango(self, nodo, clave_min, clave_max, resultado=None):
        """
        Recupera todos los nodos cuya clave esta en [clave_min, clave_max].
        Poda ramas que no pueden contener resultados.
        """
        if resultado is None:
            resultado = []
        if nodo is None:
            return resultado

        # Si la clave del nodo es mayor que el minimo, explorar izquierda
        if nodo.clave > clave_min:
            self.rango(nodo.izq, clave_min, clave_max, resultado)

        # Si la clave esta en rango, agregarla
        if clave_min <= nodo.clave <= clave_max:
            resultado.append(nodo)

        # Si la clave del nodo es menor que el maximo, explorar derecha
        if nodo.clave < clave_max:
            self.rango(nodo.der, clave_min, clave_max, resultado)

        return resultado