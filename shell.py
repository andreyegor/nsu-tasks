import io
import sys
from typing import TextIO


def solution(script: TextIO, output: TextIO) -> None:
    pass


if __name__ == '__main__':
    print("$ ", end="")
    for line in sys.stdin:
        solution(io.StringIO(line), sys.stdout)
        print("$ ", end="")
