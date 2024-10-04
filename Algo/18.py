"""
Реализовать алгоритм сортировочной станции для
преобразования выражения в инфиксной нотации к обратной
польской записи.

Приоритеты и ассоциативность операторов взять отсюда:
https://en.cppreference.com/w/c/language/operator_precedence
В алгоритме поддержать:
1. Базовые арифметические, битовые и логические операторы
2. Подвыражения в скобках
"""

from typing import Any


class Stack:
    class Item:
        def __init__(self, val, prev=None) -> None:
            self.val = val
            self.prev = prev

    def __init__(self) -> None:
        self.tail = None

    def push(self, val: Any) -> None:
        if self.tail:
            self.tail = self.Item(val, self.tail)
            return
        self.tail = self.Item(val)

    def pop(self) -> Any:
        if self.tail == None:
            raise KeyError()  # чет не то вроде
        val = self.tail.val
        self.tail = self.tail.prev
        return val

    def peek(self) -> Any:
        if self.tail == None:
            raise KeyError()  # тоже не то вроде
        return self.tail.val

    def empty(self):
        return not bool(self.tail)


operators = {
    "(": [1, "obr"],
    ")": [1, "cbr"],
    "!": [2, "u"],
    "~": [2, "u"],
    "*": [3, "b"],
    "/": [3, "b"],
    "%": [3, "b"],
    "+": [4, "b"],
    "-": [4, "b"],
    ">>": [5, "b"],
    "<<": [5, "b"],
    "&": [8, "b"],
    "^": [9, "b"],
    "|": [10, "b"],
    "&&": [11, "b"],
    "||": [12, "b"],
}

max_ln = len(max(operators.keys(), key=len))

numbers = set([str(i) for i in range(10)] + ["."])  # ?

if __name__ == "__main__":
    st = Stack()
    inp = "x+(y*z+x)*z"
    out = ""
    i = 0
    while i < len(inp):
        op = None
        l = i
        i += 1
        if inp[l] == " ":
            continue

        while inp[l:i] not in operators:
            if i - l == max_ln:
                i = l + 1
                out += inp[l]
                break
            i += 1
        else:
            op = [inp[l:i]] + operators[inp[l:i]]

        if not op:
            continue
        if out and out[-1] != " ":
            out += " "

        if op[2] in ("u", "obr"):
            st.push(op)
        elif op[2] == "cbr":
            while (this := st.pop())[2] != "obr":
                out += this[0]
                out += " "
        elif op[2] == "b":
            while not st.empty() and st.peek()[1] <= op[1] and st.peek()[2] != "obr":
                out += st.pop()[0]
                out += " "
            st.push(op)

    if out and out[-1] != " ":
        out += " "

    while not st.empty():
        out += st.pop()[0]
        out += " "
    print(out[:-1])
