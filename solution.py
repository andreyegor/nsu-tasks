from re import match
from typing import Any, List, Self, Tuple, Union


class LinkedList:
    class Node:
        def __init__(self, key: Any, val: Any, nxt: Union[Self, None] = None) -> None:
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


class Counter:
    def __init__(self, default_length=1, less_resize=3, more_resize=2) -> None:
        self.LESS_RESIZE = less_resize
        self.MORE_RESIZE = more_resize
        self.length = 0
        self.data = [LinkedList() for i in range(default_length)]
        pass

    def __len__(self) -> int:
        return self.length

    def add(self, line: str, cnt: int = 1) -> None:
        if node := self.data[self.__hsh(line)].includes(line):
            node.val += cnt
        else:
            self.__auto_resize()
            self.length += 1
            self.data[self.__hsh(line)].add(line, cnt)

    def sub(self, line: str, cnt: int = 1) -> None:
        node = self.data[self.__hsh(line)].includes(line)
        if not node:
            raise KeyError("Nothing to sub")
        node.val -= cnt
        if node.val == 0:
            self.destroy(line)  # TODO doublehash итп, несрочно на самом деле

    def destroy(self, line: str) -> None:
        try:
            self.data[self.__hsh(line)].remove(line)
            self.length -= 1
        except KeyError:
            raise KeyError("Nothing to destroy")

    def get(self, line: str):
        node = self.data[self.__hsh(line)].includes(line)
        if node == None:
            return None
        assert node.val != 0
        return node.val

    def __auto_resize(self) -> None:  # TODO проверить ужимание
        # if len(self.data) == 1:TODO что-то нужно но не такое
        #     return
        if len(self.data) - self.length == 0:
            self.__rehash(len(self.data) * self.MORE_RESIZE)
        elif len(self.data) - self.length > len(self.data) - (
            len(self.data) // self.LESS_RESIZE
        ):
            self.__rehash(len(self.data) // self.MORE_RESIZE)

    def __rehash(self, new_length) -> None:
        old_data = self.data
        self.length = 0
        self.data = [LinkedList() for i in range(new_length)]
        for llst in old_data:
            for key, val in llst:
                self.add(key, val)

    def __hsh(self, line: str) -> int:  # TODO TODO TODO TODO
        return hash(line) % len(self.data)  # TODO TODO TODO TODO


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
