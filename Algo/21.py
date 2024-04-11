from typing import Self


class BHeap:
    class Node:
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
        self.__trees = threes if threes else []

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
        frm, to = sorted((list(self.__trees), list(other.__trees.copy())), key=len)
        frm.extend([None] * (len(to) - len(frm)))
        carry = None
        for i, (f, t) in enumerate(zip(frm, to)):
            if f and t:
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
        self.__trees = to


heap = BHeap()
heap.insert(10, 1)
heap.insert(1, 2)
node = heap.peek_min()
heap.insert(-1, 3)
heap.insert(5, 4)
heap.delete(node)
print(heap.extract_min())
print(heap.extract_min())
