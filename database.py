import io
import sys
from typing import TextIO

from constructors import *
from db_classes import *


def tokenize(line):
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


def do(request: str, db_name: str) -> str:
    graph = Node(tokenize(request), db_name)
    out = graph.compile()()
    return out


def solution(requests: TextIO, db_name: str, output: TextIO) -> None:
    for request in requests:
        if request.endswith("\n"):
            request = request[:-1]
        for out in do(request, db_name):
            output.write(str(out) + "\n")


debug_input = (
    """get records where (department is "ММФ" or group is 19301)""".splitlines()
)
debug = 0
if __name__ == "__main__":
    if debug:
        solution(debug_input, "db.txt", sys.stdout)
    print("$ ", end="")
    for line in sys.stdin:
        solution(io.StringIO(line.strip()), "db.txt", sys.stdout)
        print("$ ", end="")
