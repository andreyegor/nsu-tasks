import functools
import io
import os
import re
import sys
from pathlib import Path
from typing import TextIO


class environment:
    def __init__(self):
        self.working_dir = Path(__file__).parent

    def __wrapper(f=None, aliases={}, bool_aliases={}):
        def wrapper(f):
            f.__aliases__ = aliases
            f.__bool_aliases__ = bool_aliases
            return f

        if f != None:
            return wrapper(f)
        return wrapper
    
    def engine

    @__wrapper
    def pwd(self, *data):
        return str(self.working_dir)

    @__wrapper
    def cd(self, *data):
        in_dir = Path(data[0])
        if in_dir == "..":
            new_dir = self.working_dir.parent
        elif in_dir.is_absolute():
            new_dir /= in_dir
        else:
            new_dir = in_dir

        if new_dir.is_dir():
            self.working_dir = new_dir
            return False
        raise IsADirectoryError

    @__wrapper
    def mkdir(self, *data):
        in_dir = Path(data[0])
        dir_dir = self.working_dir / in_dir
        os.mkdir(dir_dir)  # рэйсит ошибку

    @__wrapper
    def ls(self, *data):
        return "\n".join(os.listdir(self.working_dir))

    @__wrapper
    def cat(self, *data):
        out = ""
        for file in data:
            path =self.working_dir / file
            if not path.is_file():
                out += f"{path}: No such file or directory"
                continue
            with open(path) as f:
                out += f.read()
        return out

    @__wrapper
    def tac(self, *data):
        return self.cat(*data)[::-1]

    @__wrapper(aliases={"L": "level", "P": "pattern"})
    def tree(self, level=float("inf"), pattern=".*", *data):
        ...


def solution(script: TextIO, output: TextIO) -> None:
    env = environment()
    for line in script:
        commands = line.split("|")
        out = ""
        for command in commands:
            command, *write_to = command.split(">")
            
            олег = iter(command.split())
            func = getattr(env, next(олег))
            data = []
            kwargs = {}
            while True:
                try:
                    word = next(олег)
                    if word.startswith("-"):
                        if word[1] in func.__bool_aliases__:
                            kwargs[word[1:]] = True
                        elif word[1] in func.__aliases__:
                            kwargs[word[1:]] = next(олег)
                        else:
                            ...  # когда нет алиаса
                    data.append(word)
                except StopIteration:
                    break
            
            out = func(*data, **kwargs)
            
            

        output.write(out + "\n")


if __name__ == "__main__":
    print("$ ", end="")
    for line in sys.stdin:
        solution(io.StringIO(line), sys.stdout)
        print("$ ", end="")
