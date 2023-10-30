import functools
import io
import os
import re
import sys
from pathlib import Path
from typing import TextIO


class engine:
    def __init__(self):
        self.working_dir = Path(__file__).parent

    def __write(self, file: Path, text: str, mode="w"):
        if not file.is_absolute():
            file = self.working_dir / file
        with open(file, mode) as f:
            f.write(text)

    def parse(self, line: str):
        options, data = [], []
        write_add_to, write_add_to_mode = [], False
        command = None
        out = ""
        for e in line.split() + ["|"]:
            if e == "|":
                try:
                    out = getattr(self, "_" + command)(options, data + out.split())
                except AttributeError:
                    out = f"{command}: command not found"
                for file, mode in write_add_to:
                    try:
                        self.__write(file, mode, out)
                    except FileNotFoundError:
                        print(f"'{file}': No such file or directory")
                options, data = [], []
                write_add_to, write_add_to_mode = [], False
                command = None
            elif not command:
                command = e
            elif e[0] == "-":
                options.append(e)
            elif e == ">":
                write_add_to_mode = "w"
            elif e == ">>":
                write_add_to_mode = "r"
            elif write_add_to_mode:
                write_add_to.append([e, write_add_to_mode])
                write_add_to_mode = False
            else:
                data.append(e)
        return out

    # ниже записаны сами команды, обязательно в формате def _name(self, options:list, data:list)->str
    def _pwd(self, options, data):
        return str(self.working_dir)

    def _cd(self, options, data):
        in_dir = Path(data[0])
        if str(in_dir) == "..":
            new_dir = self.working_dir.parent
        elif not in_dir.is_absolute():
            new_dir = self.working_dir / in_dir
        else:
            new_dir = in_dir

        if new_dir.is_dir():
            self.working_dir = new_dir
            return ""
        return f"'{in_dir}': No such file or directory"

    def _mkdir(self, options, data):
        in_dir = Path(data[0])
        if not in_dir.is_absolute():
            new_dir = self.working_dir / in_dir
        else:
            new_dir = in_dir

        try:
            os.mkdir(new_dir)
            return ""
        except FileNotFoundError:
            return f"‘{in_dir}’: No such file or directory"
        except FileExistsError:
            return f"‘{in_dir}’: File or directory alredy exists"

    # рэйсит ошибку

    def _ls(self, options, data):
        return " ".join(sorted(os.listdir(self.working_dir)))

    def _cat(self, options, data):
        out = ""
        for file in data:
            path = self.working_dir / file
            if not path.is_file():
                out += f"'{path}': No such file or directory"
                continue
            with open(path) as f:
                out += f.read()
        return out

    def _tac(self, options, data):
        return self.cat(*data)[::-1]

    def _tree(self, options, data):
        ...

eng = engine()
def solution(script: TextIO, output: TextIO) -> None:
    for line in script:
        out = eng.parse(line)
        output.write(out + "\n" if out else "")

if __name__ == "__main__":
    print("$ ", end="")
    for line in sys.stdin:
        solution(io.StringIO(line), sys.stdout)
        print("$ ", end="")
