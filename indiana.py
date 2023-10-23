from itertools import permutations
from collections import deque
import indiana_test


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

    weights = [float("inf")] * q_nodes
    weights[0] = 0
    not_visited = set(range(q_nodes))
    while not_visited:
        node = min(not_visited, key=lambda x: weights[x])
        for i in range(q_nodes):
            if weights[i] > weights[node] + graph[node][i]:
                weights[i] = weights[node] + graph[node][i]
        not_visited.remove(node)

    return nodes[
        max(range(q_nodes), key=lambda x: nodes[x] if weights[x] <= power else -1)
    ]


if __name__ == "__main__":
    indiana_test.test1()