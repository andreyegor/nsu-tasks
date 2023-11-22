import io
import sys
from typing import TextIO


def solution(requests: TextIO, db_name: str, output: TextIO) -> None:
    pass


if __name__ == '__main__':
    print("$ ", end="")
    for line in sys.stdin:
        solution(io.StringIO(line.strip()), "db.txt", sys.stdout)
        print("$ ", end="")
