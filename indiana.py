from itertools import permutations


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

    chainged = True
    while chainged:
        chainged = False
        for i, j in permutations(range(1, q_nodes), 2):
            if graph[0][i] > graph[0][j] + graph[j][i]:
                graph[0][i] = graph[0][j] + graph[j][i]
                chainged = True

    return nodes[
        max(range(q_nodes), key=lambda x: nodes[x] if graph[0][x] <= power else -1)
    ]
