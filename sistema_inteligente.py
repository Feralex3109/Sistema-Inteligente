import heapq

class Nodo:
    def __init__(self, nombre, coordenadas, vecinos=None):
        self.nombre = nombre
        self.coordenadas = coordenadas
        self.vecinos = vecinos if vecinos else {}
        self.g = float('inf')  # Costo acumulado desde el inicio
        self.f = float('inf')  # Costo total estimado (g + h)
        self.padre = None      # Nodo previo en la mejor ruta encontrada

    def __lt__(self, otro):
        return self.f < otro.f

def heuristica(nodo_actual, nodo_objetivo):
    # Heurística basada en distancia Manhattan
    x1, y1 = nodo_actual.coordenadas
    x2, y2 = nodo_objetivo.coordenadas
    return abs(x1 - x2) + abs(y1 - y2)

def a_estrella(inicio, objetivo):
    inicio.g = 0
    inicio.f = heuristica(inicio, objetivo)
    abiertos = []
    heapq.heappush(abiertos, inicio)
    cerrados = set()

    while abiertos:
        nodo_actual = heapq.heappop(abiertos)

        # Si se alcanza el objetivo, reconstruir la ruta
        if nodo_actual == objetivo:
            ruta = []
            while nodo_actual:
                ruta.append(nodo_actual.nombre)
                nodo_actual = nodo_actual.padre
            return ruta[::-1]

        cerrados.add(nodo_actual)
        
        # Evaluar vecinos
        for vecino, costo in nodo_actual.vecinos.items():
            if vecino in cerrados:
                continue

            tentativo_g = nodo_actual.g + costo
            if tentativo_g < vecino.g:
                vecino.padre = nodo_actual
                vecino.g = tentativo_g
                vecino.f = tentativo_g + heuristica(vecino, objetivo)

                # Añadir vecino a abiertos si no está ya
                if vecino not in abiertos:
                    heapq.heappush(abiertos, vecino)

    return None  # Si no se encuentra ruta

# Definición del grafo (sistema de transporte) con coordenadas
nodo_a = Nodo('A', (0, 0))
nodo_b = Nodo('B', (1, 0))
nodo_c = Nodo('C', (0, 1))
nodo_d = Nodo('D', (1, 1))
nodo_e = Nodo('E', (2, 1))

# Conexiones entre nodos y sus costos
nodo_a.vecinos = {nodo_b: 1, nodo_c: 3}
nodo_b.vecinos = {nodo_d: 1}
nodo_c.vecinos = {nodo_d: 1, nodo_e: 5}
nodo_d.vecinos = {nodo_e: 2}

# Ejecución del algoritmo A*
inicio = nodo_a
objetivo = nodo_e
ruta = a_estrella(inicio, objetivo)

print("La mejor ruta es:", ruta)
