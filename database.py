import io
import sys
from typing import TextIO

from constructors import *
from data_classes import *


def tokenize(line):
    # TODO хлипенько
    tokens = [""]
    string = False
    arr = False
    for e in line:
        if e in "}{":
            if not (not arr and not tokens[-1]):
                tokens.append("")
            arr = not arr
            tokens[-1 if e == "{" else -2] += e
        elif arr:
            tokens[-1] += e
        elif e == '"':
            if not (not string and not tokens[-1]):
                tokens.append("")
            string = not string
        elif string:
            tokens[-1] += e
        elif e in "().":
            if tokens[-1]:
                tokens.append(e)
            else:
                tokens[-1] = e
            tokens.append("")
        elif e in " ":
            if tokens[-1]:
                tokens.append("")
        else:
            tokens[-1] += e
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
