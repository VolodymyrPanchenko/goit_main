import heapq
from typing import List, Tuple

def min_cable_cost(lengths: List[int]) -> Tuple[int, List[Tuple[int,int,int]]]:
    if not lengths:
        return 0, []
    if len(lengths) == 1:
        return 0, []

    heap = lengths[:]
    heapq.heapify(heap)

    total = 0
    merges = []
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        c = a + b
        total += c
        merges.append((a, b, c))
        heapq.heappush(heap, c)
    return total, merges

# приклад
cost, plan = min_cable_cost([4,3,2,6])
print(cost)  # 29
print(plan)  # [(2,3,5), (4,5,9), (6,9,15)]
