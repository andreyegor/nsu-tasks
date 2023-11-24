import io
import json
import re
import sys
from typing import TextIO

from constructors import *
from data_classes import *


def walk(db_name: str) -> any([Student, Teacher, AssistantStudent, None]):
    with open(db_name, "r", encoding="utf-8") as db:
        while line := db.readline():
            for cls in (Student, Teacher, AssistantStudent):
                try:
                    yield cls.create_from_json(line)
                except ValueError:
                    continue
                break
            else:
                yield None


def compile(condition: str):  # [arg1] [command] [arg2]
    ...



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
            tokens[-1]+=e
        elif e == '"':
            if not (not string and not tokens[-1]):
                tokens.append("")
            string = not string
        elif string:
            tokens[-1]+=e
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

def old_do(request: str, db_name: str) -> str:
    tokens = tokenize(request)
    if len(request)<3:
        command = lambda x: True
    else:
        condition = next(
            re.finditer("\w+ (contains|is) \S+|\w+ in {.*}", request)
        ).group()
        assert condition
        command = compile(condition)
    return filter(command, walk(db_name))


def do(request: str, db_name: str) -> str:
    graph = Node(tokenize(request), db_name)
    graph.create_graph()
    command = graph.compile()
    return command


def solution(requests: TextIO, db_name: str, output: TextIO) -> None:
    for request in requests:
        for out in do(request, db_name):
            output.write(str(out) + "\n")


if __name__ == "__main__":
    print("$ ", end="")
    for line in sys.stdin:
        solution(io.StringIO(line.strip()), "db.txt", sys.stdout)
        print("$ ", end="")
