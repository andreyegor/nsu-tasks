from primes import Primes
from random import randint
from typing import Any, List, Tuple, Union


class LinkedList:
    class Node:
        def __init__(self, key: Any, val: Any, nxt: Union[object, None] = None) -> None:
            self.key = key
            self.val = val
            self.nxt = nxt

    def __init__(self, now=None) -> None:
        if not now:
            self.length = 0
            self.root = None
        else:
            self.length = 1
            self.root = self.Node(now)
        self.tail = self.root

    def __iter__(self) -> None:
        self.iter_now = self.root
        return self

    def __next__(self) -> Tuple[Any, Any]:
        if not self.iter_now:
            raise StopIteration
        out, self.iter_now = self.iter_now, self.iter_now.nxt
        return (out.key, out.val)

    def add(self, key, val):
        self.length += 1
        if not self.root:
            self.root = self.Node(key, val)
            self.tail = self.root
            return

        self.tail.nxt = self.Node(key, val)
        self.tail = self.tail.nxt

    def remove(self, key) -> Any:
        if not self.root:
            raise KeyError("Nothing to remove")
        prev = None
        now = self.root
        while now.key != key:
            if not now.nxt:
                break
            prev = now
            now = now.nxt
        else:
            self.length -= 1
            if not prev:
                self.root = now.nxt
            else:
                prev.nxt = now.nxt
            return now.val
        raise KeyError("Nothing to remove")

    def includes(self, key) -> Union[Node, None]:
        if not self.root:
            return None
        now = self.root
        while now.key != key:
            now = now.nxt
            if not now:
                break
        else:
            return now
        return None


class UniversalHashingString:
    LIMIT = 2**32
    INITIAL_VALUE = 0

    def __init__(self, func_val=None) -> None:
        self.__primes = Primes()
        self.upd_val(func_val)
        self.__mod = self.__primes.get()

    def hash(self, line: str):
        out = self.INITIAL_VALUE
        for val in line:
            out = ((out * self.__val) + ord(val)) % self.__mod
        return out

    def upd(self, val=None):
        self.upd_val(val)
        return self.upd_mod()

    def upd_val(self, val=None) -> None:
        if val:
            self.__val = val
        else:
            self.__val = randint(1, self.LIMIT)

    def upd_mod(self) -> None:
        self.__mod = self.__primes.next()
        return self.__mod

    def get_mod(self):
        return self.__mod


class Counter:
    LESS_RESIZE=3
    
    def __init__(self) -> None:
        self.__hash = UniversalHashingString()
        self.__length = 0
        self.__data = [LinkedList() for i in range(self.__hash.get_mod())]

    def __len__(self) -> int:
        return self.__length

    def add(self, line: str, cnt: int = 1) -> None:
        if node := self.__data[self.__hash.hash(line)].includes(line):
            node.val += cnt
        else:
            self.__auto_resize()
            self.__length += 1
            self.__data[self.__hash.hash(line)].add(line, cnt)

    def sub(self, line: str, cnt: int = 1) -> None:
        node = self.__data[self.__hash.hash(line)].includes(line)
        if not node:
            raise KeyError("Nothing to sub")
        node.val -= cnt
        if node.val == 0:
            self.destroy(line)  # TODO doublehash итп, несрочно на самом деле

    def destroy(self, line: str) -> None:
        try:
            self.__data[self.__hash.hash(line)].remove(line)
            self.__length -= 1
        except KeyError:
            raise KeyError("Nothing to destroy")

    def get(self, line: str):
        node = self.__data[self.__hash.hash(line)].includes(line)
        if node == None:
            return None
        assert node.val != 0
        return node.val

    def __auto_resize(self) -> None:
        if len(self.__data) - self.__length == 0:
            self.__hash.upd()
            self.__rehash()

    def __rehash(self) -> None:
        old_data = self.__data
        self.__length = 0
        self.__data = [LinkedList() for i in range(self.__hash.get_mod())]
        for llst in old_data:
            for key, val in llst:
                self.add(key, val)


class Interface:
    __LOCATED_IN = "Located rebel base on "
    __GET_IN = "Rebel bases on "
    __INVATED_IN = " invaded"
    __DESTROYED_IN = " destroyed"

    __ROGER_THAT = "Roger that"

    def __init__(self):
        self.__cnt = Counter()

    def do(self, line: str):  # TODO не оч
        if line.startswith(self.__LOCATED_IN):
            return self.__located(line[len(self.__LOCATED_IN) :])
        if line.startswith(self.__GET_IN):
            return self.__get(line[len(self.__GET_IN) :])
        if line.endswith(self.__INVATED_IN):
            return self.__invaded(line[: len(line) - len(self.__INVATED_IN)])
        if line.endswith(self.__DESTROYED_IN):
            return self.__destroyed(line[: len(line) - len(self.__DESTROYED_IN)])
        raise "what"

    def __located(self, line):
        self.__cnt.add(line)
        return self.__ROGER_THAT

    def __invaded(self, line):
        self.__cnt.sub(line)
        return self.__ROGER_THAT

    def __destroyed(self, line):
        try:
            self.__cnt.destroy(line)
        except KeyError:
            pass  # No bases on destroyed planet
        return self.__ROGER_THAT

    def __get(self, line):
        out = self.__cnt.get(line)
        return f"Bases on {line}: {out if out else 0}"


def solution(data: str) -> str:
    out = ""
    intrf = Interface()
    for line in data.splitlines():
        try:
            out += intrf.do(line) + "\n"
        except NotImplementedError:
            out += "Beep-bee-bee-boop-bee-doo-weep\n"
    return out


if __name__ == "__main__":
    # cnt = Counter()
    # cnt.add("a")
    # cnt.add("a")
    # cnt.add("b")
    # cnt.add("c")
    # cnt.add("d")
    # cnt.add("a")
    # print(cnt.get("a"))
    # cnt.sub("a")
    # print(cnt.get("a"))
    # cnt.destroy("a")
    # print(cnt.get("b"))
    # print(cnt.get("a"))

    i = Interface()
    i.do("Located rebel base on hot")
