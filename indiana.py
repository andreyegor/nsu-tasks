from typing import Iterable, Any
from math import ceil, log2
import dis


class DList:
    class Node:
        def __init__(
            self, value: Any, prev: object = None, next: object = None
        ) -> None:
            self.value = value
            self._prev = prev
            self._next = next
            self._exists = True

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

    def __len__(self):
        return self._len

    def __iter__(self) -> object:
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
        if self._len == 0 or node._exists == False:
            raise KeyError
        self._len -= 1

        if node._prev:
            node._prev._next = node._next
        else:
            self._root = node._next
        if node._next:
            node._next._prev = node._prev
        else:
            self._tail = node._prev

        node._prev, node._next, node._exists = None, None, False

    def merge(self, other: object) -> object:
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
            where: DList.Node = None,
            childs: DList = None,
            parent: object = None,
        ) -> None:
            self.priority = priority
            self.value = value
            self.where = where
            self._childs = childs if childs else DList()
            self.parent = parent
            self.decreaced = 0

        def degree(self):
            return self._childs.__len__()

        def merge(self, other: object, root_parent=None):
            self, other = sorted((self, other), key=lambda node: node.priority)
            other.where = self._childs.add(other)
            self.parent = root_parent
            other.parent = self
            return self

    class ReturnableNode:
        def __init__(self, node):
            self._node = node

        def exists(self):
            return self._node.where._exists

        @property
        def priority(self):
            return self._node.priority
        
        @property
        def value(self):
            return self._node.value

        def __eq__(self, other: int):
            return self.priority == other

        def __lt__(self, other: int):
            return self.priority < other

        def __le__(self, other: int):
            return self.priority <= other

        def __gt__(self, other: int):
            return self.priority > other

        def __ge__(self, other: int):
            return self.priority >= other

        def __int__(self):
            return self.priority

    def __init__(self) -> None:
        self._trees: DList = DList()
        self._min: DList.Node = None
        self._len = 0
        pass

    def insert(self, priority: int, value: int) -> ReturnableNode:
        self._len += 1
        return self.__insert_node(self.Node(priority, value))

    def __insert_node(self, node: Node) -> ReturnableNode:
        new_dlist_node = self._trees.add(node)
        node.where = new_dlist_node
        self._min = min(self._min, new_dlist_node, key=self.__min_trees_key)
        return self.ReturnableNode(new_dlist_node.value)

    def extract(self) -> tuple[int, int]:
        if self._len == 0:
            raise KeyError()
        self._len -= 1
        self._trees.remove(self._min)
        for node in self._min.value._childs:
            node.value.parent = None
        self._trees = self._trees.merge(self._min.value._childs)

        out = (self._min.value.priority, self._min.value.value)
        self.__consolidate()
        return out

    def decreace_key(self, node: ReturnableNode, new_key):
        return self.__actual_decreace_key(node._node, new_key)

    def __actual_decreace_key(self, node: Node, new_key):
        node.decreaced = 0
        if not node.parent:
            node.priority = new_key
            self._min = min(self._min, node.where, key=self.__min_trees_key)
            return self.ReturnableNode(node)
        parent = node.parent
        parent._childs.remove(node.where)
        node.priority = new_key
        node.parent = None
        out = self.__insert_node(node)
        if parent.decreaced == 1:
            self.__actual_decreace_key(parent, parent.priority)
            return out
        parent.decreaced += 1
        return out

    def empty(self) -> bool:
        return self._trees.empty()

    def __consolidate(self):
        if self._len == 0:
            self._min = None
            return
        new_trees = [None for i in range(ceil(log2(self._len)) + 1)]  # O(logn)
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
        for node in self._trees:
            node.value.where = node
        self._min = min(self._trees, key=self.__min_trees_key)

    def __min_trees_key(self, node: DList.Node) -> int:
        return node.value.priority if node else float("inf")


def solution(data: str) -> int:
    lines = ([int(q) for q in e.split()] for e in data.splitlines())
    power, q_nodes, q_edges = next(lines)
    graph = [[(i, 0)] for i in range(q_nodes)]  # (node, weight)
    for i in range(q_edges):
        node1, node2, weight = next(lines)
        graph[node1].append((node2, weight))
        graph[node2].append((node1, weight))
    nodes = [next(lines)[0] for i in range(q_nodes)]

    weights = [float("inf") for i in range(q_nodes)]
    queue = FibonacciHeap()
    weights[0] = queue.insert(0, 0)
    while not queue.empty():
        weight, node = queue.extract()
        for i, weight in graph[node]:
            if weights[i] > int(weights[node]) + weight:
                if weights[i] != float("inf") and weights[i].exists():
                    weights[i] = queue.decreace_key(
                        weights[i], int(weights[node]) + weight
                    )
                else:
                    weights[i] = queue.insert(int(weights[node]) + weight, i)

    return nodes[
        max(
            range(q_nodes),
            key=lambda x: (nodes[x] if weights[x] <= power else -1),
        )
    ]


if __name__ == "__main__":
    with open("tests/2-input.txt") as inp:
        with open("tests/2-expected.txt") as out:
            data = inp.read()
            excepted = int(out.read())
            result = solution(data)
            print(result, excepted)
            assert result == int(excepted)
