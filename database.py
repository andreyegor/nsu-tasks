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
    left, command, *right = condition.split()
    "".join(right)
    commands = {
        "is": is_constructor,
        "in": in_constructor,
        "contains": contains_constructor,
    }
    assert command in commands
    return commands[command](left, right)


def do(request: str, db_name: str) -> str:
    assert request.startswith("get records")
    if "where" not in request:
        command = lambda x: True
    else:
        condition = [e.group() for e in re.finditer("(\w+ (contains|is) \w+)|\w+ in {.*}", request)]
        assert condition
        command = compile(condition[0])
    return filter(command, walk(db_name))


def solution(requests: TextIO, db_name: str, output: TextIO) -> None:
    for request in requests:
        for out in do(request, db_name):
            output.write(str(out)+'\n')


if __name__ == "__main__":
    print("$ ", end="")
    for line in sys.stdin:
        solution(io.StringIO(line.strip()), "db.txt", sys.stdout)
        print("$ ", end="")
