from itertools import permutations
from collections import deque

def solution(data: str) -> int:
    lines = ([int(q) for q in e.split()] for e in data.split("\n"))
    power, q_nodes, q_edges = next(lines)
    graph = [[float("inf")] * q_nodes for i in range(q_nodes)]
    graph[0][0] = 0
    for i in range(q_edges):
        node1, node2, weight = next(lines)
        graph[node1][node2] = weight
        graph[node2][node1] = weight
    nodes = [next(lines)[0] for i in range(q_nodes)]

    queue = deque(permutations(range(1, q_nodes), 2))
    while queue:
        i,j = queue.popleft()
        if graph[0][i] > graph[0][j] + graph[j][i]:
            graph[0][i] = graph[0][j] + graph[j][i]
            queue.extend((i,j) for j in range(1, q_nodes))

    return nodes[
        max(range(q_nodes), key=lambda x: nodes[x] if graph[0][x] <= power else -1)
    ]
