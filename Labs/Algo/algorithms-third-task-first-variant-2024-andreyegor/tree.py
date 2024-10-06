from typing import Generator, List, Callable, Any, Literal, Union


class Tree:
    class Node:
        def __init__(
            self,
            key: Any,
            val: Any,
            _parent=None,
            height: int = 0,
            _left=None,
            _right=None,
        ):
            self.key = key
            self.val = val
            self._parent = _parent
            self._left = _left
            self._right = _right
            self._height = height

    def __init__(self, key=None, val=None) -> None:
        self._root: self.Node = None
        if key:
            self.insert(key, val)

    def __len__(self) -> int:
        return self._root._height if self._root else 0

    def __iter__(self):
        yield from self.__dfs(self._root)

    def insert(self, key, val=None) -> None:
        if not self._root:
            self._root = self.Node(key, val, height=1)
            return

        new = self._root
        while True:
            if new.key < key:
                if not new._right:
                    new._right = self.Node(key, val, new, height=1)
                    break
                new = new._right
            elif new.key > key:
                if not new._left:
                    new._left = self.Node(key, val, new, height=1)
                    break
                new = new._left
            else:
                raise AttributeError("Same key object alrey exists")
        self._root = self.__balance(new, False)

    def extract(self, key) -> Any:
        return self.__extract_node(self._peek(key)).val

    def peek(self, key) -> Any:
        return self._peek(key)

    def set(self, key, val) -> None:
        self._peek(key).val = val

    def __extract_node(self, extractable: Node) -> Node:
        if extractable._left and extractable._right:
            swap = self.__local_min(extractable._right)
            swap.key, extractable.key = extractable.key, swap.key
            swap.val, extractable.val = extractable.val, swap.val
            swap, extractable = extractable, swap
            balance_node = extractable._parent
            self.__kill_child(extractable)
            self.__balance(balance_node)
            if self._root == extractable:
                self._root = swap
        elif self._root == extractable:
            self._root = extractable._left if extractable._left else extractable._right
            self.__kill_child(extractable)
        else:
            balance_node = extractable._parent
            self.__kill_child(extractable)
            self.__balance(balance_node)
        return extractable

    def __dfs(self, node: Node) -> Generator:
        if node == None:
            return
        if node._left:
            yield from self.__dfs(node._left)
        yield node
        if node._right:
            yield from self.__dfs(node._right)

    def _peek(self, key) -> Node:
        this = self._root
        while this and this.key != key:
            if this.key > key:
                this = this._left
            elif this.key < key:
                this = this._right
        if not this:
            raise AttributeError("These aren't the value you're looking for...")
        return this

    def __local_min(self, root) -> Node:
        while root._left:
            root = root._left
        return root

    def __kill_child(self, child: Node) -> None:
        if not (child._left or child._right or child._parent):
            return
        if child._left and child._right:
            raise AttributeError("Too many alive grandsons")
        alive_grandson = child._left if child._left else child._right
        if not child._parent:
            pass
        elif child._parent._left == child:
            child._parent._left = alive_grandson
        else:
            child._parent._right = alive_grandson
        if alive_grandson:
            alive_grandson._parent = child._parent
        child._parent, child._left, child._right = None, None, None

    def __balance(self, node: Node, b_rotate=True) -> Node:
        while True:
            self.__update_height(node)
            diff = self.__diff(node)
            if diff == -2:
                if b_rotate and node._left and self.__diff(node._left) == 1:
                    node = self.__br_rotation(node)
                else:
                    node = self.__sr_rotation(node)
            elif diff == 2:
                if b_rotate and node._right and self.__diff(node._right) == -1:
                    node = self.__bl_rotation(node)
                else:
                    node = self.__sl_rotation(node)
            if node._parent:
                node = node._parent
                continue
            break
        self._root = node
        return node

    def __update_height(self, *nodes: Node) -> None:
        for node in nodes:
            node._height = (
                (node._right._height if node._right else 0)
                + (node._left._height if node._left else 0)
                + 1
            )

    def __diff(self, node: Node) -> int:
        return (node._right._height if node._right else 0) - (
            node._left._height if node._left else 0
        )

    def __rotation(self, root, type) -> Node:
        if type == "sl":
            first, second = "_left", "_right"
        elif type == "sr":
            first, second = "_right", "_left"
        else:
            raise AttributeError("""Attribute 'type' can be "sl" or "sr" only""")
        new_root = root.__getattribute__(second)
        root._parent, new_root._parent = new_root, root._parent

        root.__setattr__(second, new_root.__getattribute__(first))
        new_root.__setattr__(first, root)

        if root.__getattribute__(second):
            root.__getattribute__(second)._parent = root
        self.__update_height(root, new_root)

        if not new_root._parent:
            self._root = new_root
        elif new_root._parent.__getattribute__(first) == root:
            new_root._parent.__setattr__(first, new_root)
        else:
            new_root._parent.__setattr__(second, new_root)

        return new_root

    def __sl_rotation(self, root: Node) -> Node:
        return self.__rotation(root, "sl")

    def __sr_rotation(self, root: Node) -> Node:
        return self.__rotation(root, "sr")

    def __bl_rotation(self, root: Node) -> Node:
        self.__sr_rotation(root._right)
        return self.__sl_rotation(root)

    def __br_rotation(self, root: Node) -> Node:
        self.__sl_rotation(root._left)
        return self.__sr_rotation(root)