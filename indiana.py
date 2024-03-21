from typing import Iterable, Any
from math import ceil, log2

class DList:
    class Node:
        def __init__(self, value: Any, prev: Self = None, next: Self = None) -> None:
            self.value = value

            self._prev = prev
            self._next = next

        def next(self):
            return self._next

        def prev(self):
            return self._prev

    def __init__(self, values: Iterable = None) -> None:
        self._len = 0
        self._root = None
        self._tail = None
        if not values:
            return
        for value in values:
            self.add(value)

    def __iter__(self) -> Self:
        self.__iter_now = self._root
        return self

    def __next__(self) -> Node:
        if not self.__iter_now:
            raise StopIteration
        out = self.__iter_now
        self.__iter_now = self.__iter_now._next
        return out

    def root(self):
        return self._root

    def tail(self):
        return self._tail

    def len(self):
        return self._len

    def add(self, value: Any) -> Node:
        self._len += 1
        if self._len == 1:
            self._root = self.Node(value)
            self._tail = self._root
        else:
            self._tail._next = self.Node(value, self._tail)
            self._tail = self._tail._next
        return self._tail

    def remove(self, node: Node) -> None:
        self._len -= 1

        if node._prev:
            node._prev._next = node._next
        else:
            self._root = node._next
        if node._next:
            node._next._prev = node._prev
        else:
            self._tail = node._prev

        node._prev, node._next = None, None

    def merge(self, other: Self) -> Self:
        if not other._root:
            return self
        if not self._root:
            return other

        self._len += other._len
        self._tail._next = other._root
        self._tail = other._tail

        other._root, other._tail, other._len = None, None, 0

        return self

    def empty(self):
        return not bool(self._root)


class FibonacciHeap:
    class Node:
        def __init__(
            self,
            priority: int,
            value: int,
            childs: DList = None,
        ) -> None:
            self.priority = priority
            self.value = value
            self._childs = childs if childs else DList()

        def degree(self):
            return self._childs.len()

        def merge(self, other: Self):
            self, other = sorted((self, other), key=lambda node: node.priority)
            self._childs.add(other)
            return self

    def __init__(self) -> None:
        self._trees: DList = DList()
        self._min: DList.Node = None
        self._len = 0
        pass

    def insert(self, priority: int, value: int) -> None:
        self._len += 1
        new_dlist_node = self._trees.add(self.Node(priority, value))
        self._min = min(self._min, new_dlist_node, key=self.__min_trees_key)

    def extract(self) -> tuple[int, int]:
        if self._len == 0:
            raise IndexError()
        self._len -= 1
        self._trees.remove(self._min)
        self._trees = self._trees.merge(self._min.value._childs)

        out = (self._min.value.priority, self._min.value.value)
        self.__consolidate()
        return out

    def empty(self) -> bool:
        return self._trees.empty()

    def __consolidate(self):
        if self._len == 0:
            self._min = None
            return
        new_trees = [None for i in range(ceil(log2(self._len))+1)]  # O(logn) возможно не лучшее значение
        this_tree = self._trees.root()
        while this_tree:
            if not new_trees[this_tree.value.degree()]:
                new_trees[this_tree.value.degree()] = this_tree
                this_tree = this_tree.next()
                continue
            other_tree = new_trees[this_tree.value.degree()]
            new_trees[this_tree.value.degree()] = None
            this_tree.value = this_tree.value.merge(other_tree.value)

        self._trees = DList((tree.value for tree in new_trees if tree))
        self._min = min(self._trees, key=self.__min_trees_key)

    def __min_trees_key(self, node: DList.Node) -> int:
        return node.value.priority if node else float("inf")


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
    queue = FibonacciHeap()
    queue.insert(0, 0)
    while not queue.empty():
        weight, node = queue.extract()
        if weight > weights[node]:
            continue
        for i in range(q_nodes):
            if weights[i] > weights[node] + graph[node][i]:
                weights[i] = weights[node] + graph[node][i]
                queue.insert(weights[i], i)

    return nodes[
        max(range(q_nodes), key=lambda x: nodes[x] if weights[x] <= power else -1)
    ]


if __name__ == "__main__":
    with open("tests/12-input.txt") as inp:
        with open("tests/12-expected.txt") as out:
            data = inp.read()
            excepted = int(out.read())
            result = solution(data)
            print(result)
            assert result == int(excepted)
