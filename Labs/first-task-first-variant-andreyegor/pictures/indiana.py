from queue import PriorityQueue
import indiana_test


def solution(data: str) -> int:
    lines = ([int(q) for q in e.split()] for e in data.splitlines())
    power, q_nodes, q_edges = next(lines)
    graph = [[float("inf")] * q_nodes for i in range(q_nodes)]
    graph[0][0] = 0
    for i in range(q_edges):
        node1, node2, weight = next(lines)
        graph[node1][node2] = weight
        graph[node2][node1] = weight
    nodes = [next(lines)[0] for i in range(q_nodes)]

    weights = [0] + [float("inf") for i in range(q_nodes - 1)]
    queue = PriorityQueue()
    queue.put((0, 0))
    while not queue.empty():
        weight, node = queue.get()
        if weight > weights[node]:
            continue
        for i in range(q_nodes):
            if weights[i] > weights[node] + graph[node][i]:
                weights[i] = weights[node] + graph[node][i]
                queue.put((weights[i], i))

    return nodes[
        max(range(q_nodes), key=lambda x: nodes[x] if weights[x] <= power else -1)
    ]


if __name__ == "__main__":
    indiana_test.test1()
