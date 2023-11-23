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
    left, command, right = re.findall("(\w+) (\w+) ({.*}|\S+)", condition)[0]
    # TODO Кажеися что так делать не стоит, лучше отдать это функции чтобы корректно проверить типы
    if right.startswith('"') and right.endswith('"'):
        right = right[1:-1]
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
        condition = next(
            re.finditer("\w+ (contains|is) \S+|\w+ in {.*}", request)
        ).group()
        assert condition
        command = compile(condition)
    return filter(command, walk(db_name))


def solution(requests: TextIO, db_name: str, output: TextIO) -> None:
    for request in requests:
        for out in do(request, db_name):
            output.write(str(out) + "\n")


if __name__ == "__main__":
    print("$ ", end="")
    for line in sys.stdin:
        solution(io.StringIO(line.strip()), "db.txt", sys.stdout)
        print("$ ", end="")
