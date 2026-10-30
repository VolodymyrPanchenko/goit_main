from typing import Dict, Hashable, Tuple, List, Any
import heapq
import math

Graph = Dict[Hashable, List[Tuple[Hashable, float]]]

def dijkstra_heap(graph: Graph, start: Hashable) -> Tuple[Dict[Hashable, float], Dict[Hashable, Any]]:
    """
    Алгоритм Дейкстри з бінарною купою (heapq).
    graph: adjacency list, напр. {'A': [('B', 5), ('C', 2)], ...}
    start: стартова вершина

    Повертає:
      dist  — найкоротші відстані від start до кожної вершини
      prev  — попередник у найкоротшому шляху (для відновлення маршруту)
    """
    # 1) Ініціалізація
    dist: Dict[Hashable, float] = {v: math.inf for v in graph}
    dist[start] = 0.0
    prev: Dict[Hashable, Any] = {v: None for v in graph}

    # 2) Мін-купа за відстанню
    heap: List[Tuple[float, Hashable]] = [(0.0, start)]
    visited = set()

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        # Якщо поточна відстань у купі застаріла — пропускаємо
        if d > dist[u]:
            continue

        # 3) Релаксація ребер
        for v, w in graph.get(u, []):
            if w < 0:
                raise ValueError("Дейкстра не підтримує від'ємні ваги ребер.")
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    return dist, prev


def reconstruct_path(prev: Dict[Hashable, Any], start: Hashable, target: Hashable) -> List[Hashable]:
    """Відновити шлях start -> target за словником попередників prev."""
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == start else []


if __name__ == "__main__":
    # Орієнтований чи неорієнтований граф — залежить від того, як додасте ребра.
    # Тут приклад неорієнтованого: додаємо обидва напрямки.
    graph: Graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
        'D': [('B', 5), ('C', 8), ('E', 2), ('F', 6)],
        'E': [('C', 10), ('D', 2), ('F', 2)],
        'F': [('D', 6), ('E', 2)]
    }

    start = 'A'
    dist, prev = dijkstra_heap(graph, start)

    # Вивести найкоротші відстані
    for v in sorted(graph.keys()):
        print(f"dist[{start}->{v}] = {dist[v]}")

    # Відновити шлях A -> F
    target = 'F'
    path = reconstruct_path(prev, start, target)
    print("Шлях:", " -> ".join(path))
