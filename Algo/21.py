from typing import Self


class BHeap:
    class Node:  # как будто лишний
        def __init__(
            self,
            priority: int,
            value: int,
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

        def merge(self, other: Self) -> Self:
            self, other = sorted((self, other), key=lambda node: node.priority)
            self._childs.append(other)
            other._parent = self
            return self

    def __init__(self, threes: list[Node] = None) -> None:
        self.__threes = threes if threes else []

    def __sift_up(self, node: Node) -> None:
        while node._parent and node._parent.priority > node.priority:
            node._parent._childs, node._childs = (
                node._childs,
                node._parent._childs,
            )
            node._parent, node._parent._parent = (
                node._parent._parent,
                node._parent,
            )

    def empty(self):
        return not bool(self.__threes)

    def peek_min(self) -> Node:
        out = min(
            self.__threes,
            key=lambda three: three.priority if three else float("inf"),
        )
        if not out:
            raise ValueError()
        return out

    def extract_min(self) -> Node:
        out = self.peek_min()
        self.__threes[out.size()] = None
        if self.__threes[-1] == None:
            del self.__threes[-1]

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

    def merge(self, other: Self) -> None:
        frm, to = sorted((self.__threes, other.__threes), key=len)
        carry = None
        for i, (f, t) in enumerate(zip(frm, to)):
            if f and t:  # проверить объеденение if
                to[i] = carry
                carry = t.merge(f)
            elif carry and ((e := f) or (e := t)):
                to[i] = None
                carry.merge(e)
            elif carry:
                to[i] = carry
                carry = None
            elif f:
                to[i] = f
            # elif t: уже лежит
        if carry:
            to.append(carry)
        self.__threes = to


heap = BHeap()
heap.insert(10, 1)
heap.insert(1, 1)
node = heap.peek_min()
heap.insert(-1, 1)
heap.delete(node)
print(heap.extract_min())
print(heap.extract_min())
