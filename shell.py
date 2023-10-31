import io
import os
import sys
from collections import deque
from pathlib import Path
from typing import TextIO


class engine:
    def __init__(self):
        self.working_dir = Path(os.getcwd())

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
                        self.__write(Path(file), out, mode)
                    except FileNotFoundError:
                        print(f"'{file}': No such file or directory")
                    out = ""
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
        return "\n".join(self._cat(options, data).splitlines()[::-1])

    def _tree(self, options, data):
        out = "."

        def dfs(_dir, deph, threads=set(), end=False):
            nonlocal out
            if deph != 0:
                out += (
                    "\n"
                    + "".join(
                        "│   " if i in threads else "    " for i in range(deph - 1)
                    )
                    + (f"└── {_dir.name}" if end else f"├── {_dir.name}")
                )

            if not _dir.is_dir():
                return
            dirs = os.listdir(_dir)
            if not dirs:
                return

            threads.add(deph)
            for e in dirs[:-1]:
                dfs(_dir / e, deph + 1, threads)
            threads.remove(deph)
            dfs(_dir / dirs[-1], deph + 1, threads, True)

        dfs(self.working_dir, 0)
        return out


eng = engine()


def solution(script: TextIO, output: TextIO) -> None:
    global eng
    if __name__ != "__main__":
        eng = engine()
    for line in script:
        out = eng.parse(line)
        output.write(out + "\n" if out and len(out) > 1 and out[-1:] != "\n" else out)


if __name__ == "__main__":
    print("$ ", end="")
    for line in sys.stdin:
        solution(io.StringIO(line), sys.stdout)
        print("$ ", end="")
