"""
A* Pathfinding — Backend Python (Flask)
========================================
Ejecutar:
    pip install flask
    python app.py

Luego abre el navegador en: http://localhost:5000
"""

from flask import Flask, request, jsonify, render_template
import heapq, math
from collections import deque

app = Flask(__name__)

# ══════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════
LIBRE   = 0
BLOQ    = 1
LENTO   = 2
RAPIDO  = 3
COSTES  = {0: 1.0, 1: float('inf'), 2: 3.0, 3: 0.5}
DIRS8   = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]


# ══════════════════════════════════════════
# HEURÍSTICAS
# ══════════════════════════════════════════
def h_euclidea(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def h_manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


# ══════════════════════════════════════════
# ALGORITMO A*
# ══════════════════════════════════════════
def astar(grid, inicio, fin, h_fn=h_euclidea):
    rows = len(grid)
    cols = len(grid[0])
    inicio = tuple(inicio)
    fin    = tuple(fin)

    open_set = []
    heapq.heappush(open_set, (h_fn(inicio, fin), 0, inicio))
    came_from = {}
    g_score   = {inicio: 0}
    visitados = []

    while open_set:
        f, g, actual = heapq.heappop(open_set)
        if actual in came_from and actual != inicio:
            pass
        if actual in [tuple(v) for v in visitados]:
            continue
        visitados.append(list(actual))

        if actual == fin:
            camino = []
            n = fin
            while n in came_from:
                camino.append(list(n))
                n = came_from[n]
            camino.append(list(inicio))
            return camino[::-1], visitados

        r, c = actual
        for dr, dc in DIRS8:
            nr, nc = r+dr, c+dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == BLOQ:
                continue
            mov = COSTES[grid[nr][nc]]
            if dr != 0 and dc != 0:
                mov *= math.sqrt(2)
            nuevo_g = g_score[actual] + mov
            vecino  = (nr, nc)
            if nuevo_g < g_score.get(vecino, float('inf')):
                came_from[vecino] = actual
                g_score[vecino]   = nuevo_g
                heapq.heappush(open_set,
                    (nuevo_g + h_fn(vecino, fin), nuevo_g, vecino))

    return [], visitados


# ══════════════════════════════════════════
# DIJKSTRA
# ══════════════════════════════════════════
def dijkstra(grid, inicio, fin):
    return astar(grid, inicio, fin, h_fn=lambda a, b: 0)


# ══════════════════════════════════════════
# BFS
# ══════════════════════════════════════════
def bfs(grid, inicio, fin):
    rows = len(grid)
    cols = len(grid[0])
    inicio = tuple(inicio)
    fin    = tuple(fin)

    cola      = deque([(inicio, [list(inicio)])])
    visitados = set([inicio])
    vis_list  = [list(inicio)]

    while cola:
        actual, camino = cola.popleft()
        if actual == fin:
            return camino, vis_list
        r, c = actual
        for dr, dc in DIRS8:
            nr, nc  = r+dr, c+dc
            vecino  = (nr, nc)
            if (0 <= nr < rows and 0 <= nc < cols
                    and vecino not in visitados
                    and grid[nr][nc] != BLOQ):
                visitados.add(vecino)
                vis_list.append([nr, nc])
                cola.append((vecino, camino + [[nr, nc]]))

    return [], vis_list


# ══════════════════════════════════════════
# CALCULAR COSTE
# ══════════════════════════════════════════
def calcular_coste(camino, grid):
    total = 0
    for i in range(1, len(camino)):
        r,  c  = camino[i]
        pr, pc = camino[i-1]
        mov = COSTES[grid[r][c]]
        if r != pr and c != pc:
            mov *= math.sqrt(2)
        total += mov
    return round(total, 2)


# ══════════════════════════════════════════
# RUTAS FLASK
# ══════════════════════════════════════════
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/buscar', methods=['POST'])
def buscar():
    data    = request.json
    grid    = data['grid']
    inicio  = data['inicio']
    fin     = data['fin']
    algo    = data.get('algoritmo', 'astar')

    import time
    t0 = time.perf_counter()

    if algo == 'astar':
        camino, visitados = astar(grid, inicio, fin, h_euclidea)
    elif algo == 'astar_m':
        camino, visitados = astar(grid, inicio, fin, h_manhattan)
    elif algo == 'dijkstra':
        camino, visitados = dijkstra(grid, inicio, fin)
    elif algo == 'bfs':
        camino, visitados = bfs(grid, inicio, fin)
    else:
        camino, visitados = astar(grid, inicio, fin, h_euclidea)

    ms    = round((time.perf_counter() - t0) * 1000, 3)
    coste = calcular_coste(camino, grid) if camino else 0

    return jsonify({
        'camino':    camino,
        'visitados': visitados,
        'pasos':     len(camino),
        'coste':     coste,
        'explorados':len(visitados),
        'tiempo_ms': ms,
    })


@app.route('/comparar', methods=['POST'])
def comparar():
    data   = request.json
    grid   = data['grid']
    inicio = data['inicio']
    fin    = data['fin']

    import time
    resultados = {}

    for nombre, fn in [
        ('astar',    lambda: astar(grid, inicio, fin, h_euclidea)),
        ('dijkstra', lambda: dijkstra(grid, inicio, fin)),
        ('bfs',      lambda: bfs(grid, inicio, fin)),
    ]:
        t0 = time.perf_counter()
        cam, vis = fn()
        ms = round((time.perf_counter() - t0) * 1000, 3)
        resultados[nombre] = {
            'camino':     cam,
            'visitados':  vis,
            'pasos':      len(cam),
            'coste':      calcular_coste(cam, grid) if cam else 0,
            'explorados': len(vis),
            'tiempo_ms':  ms,
        }

    return jsonify(resultados)


# ══════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════
if __name__ == '__main__':
    print("\n" + "="*50)
    print("  A* Pathfinding — Servidor iniciado")
    print("  Abre el navegador en: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True)
