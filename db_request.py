from dataclasses import dataclass
from typing import Callable

import constructors


class Database:
    def __init__(self, db_name, dataclasses, variables=None) -> None:
        if variables == None:
            variables = dict()
        self.env = Enviroment(db_name, dataclasses, variables)

    def request(self, request) -> str:
        graph = Node(self.__tokenize(request), self.env)
        return graph.compile()()

    def __tokenize(self, line):
        tokens = [""]
        string = False
        arr = False
        for char in line:
            match char:
                case "{":
                    arr = True
                    tokens[-1] += char
                case "}":
                    arr = False
                    tokens[-1] += char
                    tokens.append("")
                case _ if arr:
                    tokens[-1] += char
                case '"' if not string:
                    string = True
                case '"' if string:
                    string = False
                    tokens.append("")
                case _ if string:
                    tokens[-1] += char
                case char if char in "().":
                    if tokens[-1]:
                        tokens.append(char)
                    else:
                        tokens[-1] = char
                    tokens.append("")
                case " ":
                    if tokens[-1]:
                        tokens.append("")
                case _:
                    tokens[-1] += char
        if tokens[-1] == "":
            del tokens[-1]
        return tokens


@dataclass
class Enviroment:
    db_name: str
    dataclasses: list
    variables: dict


class Node:
    def __init__(self, tokens: [str], env: Enviroment) -> None:
        self.env = env
        self.tokens = tokens
        self.action = []
        self.__create_graph()

    def __create_graph(self) -> None:
        cnt = 0
        left = -1
        for i, token in enumerate(self.tokens):
            if token == "(":
                if not cnt:
                    left = i
                cnt += 1
            elif token == ")":
                cnt -= 1
            if cnt == 0:
                if left != -1:
                    nd = Node(self.tokens[left + 1 : i], self.env)
                    self.action.append(nd)
                    left = -1
                else:
                    self.action.append(token)

    def compile(self) -> Callable:
        for i in range(len(self.action)):
            if type(self.action[i]) == Node:
                self.action[i] = self.action[i].compile()
            if (
                type(self.action[i]) == str
                and self.action[i].startswith("{")
                and self.action[i].endswith("}")
            ):
                self.action[i] = constructors.str_to_iter_constructor(self.action[i])

        dot = {".": constructors.dot_constructor}
        commands = {
            "is": constructors.is_constructor,
            "in": constructors.in_constructor,
            "contains": constructors.contains_constructor,
        }
        logicals = {
            "and": constructors.and_constructor,
            "or": constructors.or_constructor,
        }
        self.replace_bin_op(dot)
        self.replace_bin_op(commands)
        self.replace_bin_op(logicals)

        if self.action == ["get", "records"] or self.action[:3] == [
            "get",
            "records",
            "as",
        ]:
            out = self.walk(lambda x: True)
        elif self.action[:2] == ["get", "records"] and len(self.action) > 3:
            if self.action[2] == "from":
                db_var = self.action[3]
                if len(self.action) > 5 and self.action[4] == "where":
                    out = self.walk(self.action[5], self.env.variables[db_var])
                else:
                    out = self.walk(lambda x: True, self.env.variables[db_var])
            elif self.action[:3] == ["get", "records", "where"]:
                out = self.walk(self.action[3])
        else:
            out = self.action[0]

        for i, e in enumerate(self.action):
            if e == "as":
                self.env.variables[self.action[i + 1]] = out
                out = lambda: []
        return out

    def replace_bin_op(self, keywords) -> None:
        i = 0
        while i < len(self.action):
            if self.action[i] in keywords:
                self.action[i] = keywords[self.action[i]](
                    self.action[i - 1], self.action[i + 1]
                )
                del self.action[i + 1]
                del self.action[i - 1]
            i += 1

    def walk(self, function, from_variable=None) -> Callable:
        def fvinner():
            yield from filter(function, from_variable())

        def inner():
            with open(self.env.db_name, "r", encoding="utf-8") as db:
                while line := db.readline():
                    for cls in self.env.dataclasses:
                        try:
                            if function(cls.create_from_json(line)):
                                yield cls.create_from_json(line)
                        except ValueError:
                            continue
                        break
                    else:
                        yield None

        return fvinner if from_variable else inner
