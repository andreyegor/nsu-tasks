from random import shuffle
from typing import Self


class BHeap:
    class Node:
        def __init__(
            self,
            priority: int = 4242,
            value: int = 4242,
            parent: Self = None,
            childs: list[Self] = None,
        ) -> None:
            self.priority = priority
            self.value = value
            self._parent = parent
            self._childs = childs if childs else []

        def __str__(self) -> str:
            return str((self.priority, self.value))

        def size(self):
            return len(self._childs)

        def add_child(self, new_child: Self) -> None:
            self._childs.append(new_child)

        def merge(self, other_childs: Self) -> None:
            to, frm = (self._childs, other_childs.copy())
            min(to, frm, key=len).extend([None] * (abs(len(to) - len(frm))))
            carry = None
            for i, (f, t) in enumerate(zip(frm, to)):
                if f and t:
                    to[i] = carry
                    carry = self.__merge_nodes(t, f)
                elif carry and ((e := f) or (e := t)):
                    to[i] = None
                    carry = self.__merge_nodes(carry, e)
                elif carry:
                    to[i] = carry
                    carry = None
                elif f:
                    to[i] = f
                # elif t: уже лежит
            if carry:
                to.append(carry)
            # self._childs = to

        def __merge_nodes(self, first, second):
            to, frm = sorted((first, second), key=lambda x: x.priority)
            to.merge(self.__node_to_childs(frm))
            frm._parent = to
            return to

        def __node_to_childs(self, node: Self):
            out = [None] * (node.size() + 1)
            out[-1] = node
            return out

    def __init__(self, threes: list[Node] = None) -> None:
        self.__root_node = self.Node(4242, 4242, None, threes)

    @property
    def __trees(self):
        return self.__root_node._childs

    def __sift_up(self, node: Node) -> None:
        node_to_swap = None
        while node._parent and node._parent.priority > node.priority:
            node_to_swap = node._parent
            for i, e in enumerate(node_to_swap._childs):
                if node == e:
                    node_to_swap._childs[i] = node_to_swap
                    break
            for i, e in enumerate(
                node_to_swap._parent._childs if node_to_swap._parent else []
            ):
                if node_to_swap == e:
                    node_to_swap._parent._childs[i] = node
                    break
            node_to_swap._childs, node._childs = (
                node._childs,
                node_to_swap._childs,
            )
            node._parent, node_to_swap._parent = (
                node_to_swap._parent,
                node,
            )
        if not node_to_swap:
            return
        for i, e in enumerate(self.__trees):
            if e == node_to_swap:
                self.__trees[i] = node

    def empty(self):
        return not bool(self.__trees)

    def peek_min(self) -> Node:
        out = min(
            self.__trees,
            key=lambda three: three.priority if three else float("inf"),
        )
        if not out:
            raise ValueError()
        return out

    def extract_min(self) -> Node:
        out = self.peek_min()
        self.__trees[out.size()] = None
        if self.__trees[-1] == None:
            del self.__trees[-1]

        for e in out._childs:
            if e:
                e._parent = None
        if out._childs:
            self.merge(BHeap(out._childs))

        out._parent = None
        out._childs = []
        return out

    def delete(self, node: Node) -> None:
        self.decrease_priority(node, -float("inf"))
        self.extract_min()

    def insert(self, priority: int, value: int) -> None:
        self.merge(BHeap([self.Node(priority, value)]))

    def decrease_priority(self, node: Node, new_priority: int) -> None:
        node.priority = new_priority
        self.__sift_up(node)

    def merge(self, other):
        self.__root_node.merge(other.__trees)


heap = BHeap()
heap.insert(10, 1)
heap.insert(1, 2)
node = heap.peek_min()
heap.insert(-1, 3)
heap.insert(999999, 42)
heap.insert(5, 4)
heap.delete(node)

assert heap.extract_min().priority == -1
assert heap.extract_min().priority == 5
assert heap.extract_min().priority == 10
assert heap.extract_min().priority == 999999

priorties = list(range(1, 16))
shuffle(priorties)
for i in priorties:
    heap.insert(i, 55)
heap.insert(0, 55)

assert heap._BHeap__trees[0:4] == [None] * 4 and heap._BHeap__trees[4] != None
for i in range(16):
    assert heap.extract_min().priority == i
