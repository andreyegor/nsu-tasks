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
            this = new
            if new.key < key:
                if not new._right:
                    new._right = self.Node(key, val, this, height=1)
                    break
                new = new._right
            elif new.key > key:
                if not new._left:
                    new._left = self.Node(key, val, this, height=1)
                    break
                new = new._left
            else:
                raise AttributeError("Same key object alrey exists")
        self._root = self.__balance(new, False)

    def extract(self, key) -> Any:
        return self.__extract_node(self._peek(key)).val

    def peek(self, key) -> Any:
        return self._peek(key).val

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
        yield (node.key, node.val)
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


class RepetableTree(Tree):
    def __init__(self, key=None, val=None):
        super().__init__(key, val)
        self.__len = 1 if key else 0

    def __len__(self):
        return self.__len

    def __next__(self) -> Any:
        raise NotImplementedError

    def insert(self, key, val) -> None:
        try:
            super().peek(key).insert(val)
        except AttributeError:
            super().insert(key, Tree(val))
        self.__len += 1

    def extract(self, key) -> List:
        out = list(super().extract(key))
        self.__len -= len(out)
        return out

    def extarct_one(self, key, val) -> Any:
        tree = super().peek(key)
        tree.extract(val)
        if len(tree) == 0:
            self.extract(key)
        self.__len -= 1
        return val

    def peek(self, val) -> List:
        return [e[1] for e in self.peek(val)]

    def set(self, key, val) -> None:
        raise NotImplementedError

    def range(self, mn: int, mx: int) -> List:
        return self.__range(mn, mx, self._root)

    def top(self, n: int) -> List:
        return self.__top(self._root, n)

    def rank(self, key):
        return self.__rank(self._root, key) + 1

    def __range(self, mn: int, mx: int, root) -> List:
        if not root:
            return []

        if root.key <= mx and root.key >= mn:
            return (
                self.__range(mn, mx, root._right)
                + [[e[0], root.key] for e in list(root.val)]
                + self.__range(mn, mx, root._left)
            )
        elif root.key <= mx:
            return self.__range(mn, mx, root._right)
        elif root.key >= mn:
            return self.__range(mn, mx, root._left)
        return []

    def __top(self, root, n) -> List:
        if not root or n <= 0:
            return []
        out = self.__top(root._right, n)
        n -= len(out)
        for e in list(root.val):
            if n == 0:
                break
            out.append([e[0], root.key])
            n -= 1
        out += self.__top(root._left, n)
        return out

    def __rank(self, root, mn) -> int:
        if not root:
            return 0
        if root.key > mn:
            return (
                len(root.val)
                + self.__rank(root._left, mn)
                + self.__rank(root._right, mn)
            )
        return self.__rank(root._right, mn)


class DataBase:
    def __init__(self) -> None:
        self.__name_tree: Tree[str, int] = Tree()
        self.__bounty_tree: RepetableTree[int, str] = RepetableTree()

    def add_bounty(self, name: str, bounty: int) -> None:
        try:
            self.__name_tree.insert(name, bounty)
            self.__bounty_tree.insert(bounty, name)
        except AttributeError:
            old_bounty = self.__name_tree.peek(name)
            new_bounty = old_bounty + bounty

            self.__name_tree.set(name, new_bounty)
            self.__bounty_tree.extarct_one(old_bounty, name)
            self.__bounty_tree.insert(new_bounty, name)

    def complited(self, name: str) -> None:
        bounty = self.__name_tree.extract(name)
        self.__bounty_tree.extarct_one(bounty, name)

    def bounty(self, name: str) -> int:
        try:
            return self.__name_tree.peek(name)
        except:
            return 0

    def rank(self, name: str) -> int:
        try:
            return self.__bounty_tree.rank(self.__name_tree.peek(name))
        except AttributeError:
            return -1

    def top(self, n: str) -> List[tuple[str, int]]:
        return self.__bounty_tree.top(n)

    def range(self, frm: str, to: str) -> List[tuple[str, int]]:
        return self.__bounty_tree.range(frm, to)


class ProtocolDroid:  #:)
    __roger_that = "Roger that"

    def __init__(self):
        self.__db = DataBase()
        self.__funcs = Tree()
        self.__funcs.insert("ADD BOUNTY", [self.__add_bounty, self.__roger_that])
        self.__funcs.insert("COMPLETED", [self.__complited, self.__roger_that])
        self.__funcs.insert("BOUNTY", [self.__bounty, "Bounty for {name}: {bounty}"])
        self.__funcs.insert("RANK", [self.__rank, "Rank of {name}: {rank}"])
        self.__funcs.insert("TOP", [self.__top, "{name}: {bounty}"])
        self.__funcs.insert("RANGE", [self.__range, "{name}: {bounty}"])

    def ask(self, request: str) -> str:
        last_index = 0
        cmd, local_cmd = "", ""
        for i, e in enumerate(request):
            if e == " ":
                last_index = i + 1
                cmd += local_cmd + " "
                local_cmd = ""
                continue
            if not e.isupper():
                break
            local_cmd += e
        else:
            cmd += local_cmd
            last_index = i + 1

        cmd = cmd.strip()
        args = list(request[last_index:].split(", "))
        func, fstring = self.__funcs.peek(cmd)
        return func(fstring, *args)

    def __add_bounty(self, fstring: str, name: str, bounty: str) -> None:
        self.__db.add_bounty(name, int(bounty))
        return fstring

    def __complited(self, fstring: str, name: str) -> None:
        self.__db.complited(name)
        return fstring

    def __bounty(self, fstring: str, name: str) -> str:
        return fstring.format(name=name, bounty=self.__db.bounty(name))

    def __rank(self, fstring: str, name: str) -> int:
        return fstring.format(name=name, rank=self.__db.rank(name))

    def __top(self, fstring: str, n: str) -> List[tuple[str, int]]:
        out = ""
        for name, bounty in self.__db.top(int(n)):
            out += fstring.format(name=name, bounty=bounty) + "\n"
        return out[:-1]

    def __range(self, fstring: str, frm: str, to: str) -> List[tuple[str, int]]:
        out = ""
        for name, bounty in self.__db.range(int(frm[1:]), int(to[:-1])):
            out += fstring.format(name=name, bounty=bounty) + "\n"
        return out[:-1]


def solution(data: str) -> str:
    out = ""
    IG_88B = ProtocolDroid()  #:)
    for line in data.splitlines():
        try:
            out += IG_88B.ask(line) + "\n"
        except NotImplementedError:
            out += "Beep-bee-bee-boop-bee-doo-weep\n"
    return out


if __name__ == "__main__":
    test_no = 6
    with open(f"tests/{test_no}-input.txt", "r") as inp:
        with open(f"tests/{test_no}-actual.txt", "w") as out:
            data = inp.read()
            result = solution(data)
            print(result)
            out.write(result)
    exit()
