import io
import os
import re
import sys
from collections import deque
from pathlib import Path
from typing import TextIO


def listdir(*args, **kwargs):
    return sorted(os.listdir(*args, **kwargs))


class engine:
    def __init__(self):
        self.working_dir = Path(os.getcwd())

    def __write(self, file: Path, text: str, mode="w"):
        if not file.is_absolute():
            file = self.working_dir / file
        with open(file, mode, encoding="utf-8") as f:
            f.write(text)

    def parse(self, line: str):
        options, data = [], []
        write_add_to, write_add_to_mode = [], False
        command = None
        out = ""
        for e in line.split() + ["|"]:
            match e:
                case "|":
                    correct_files = []
                    for file, mode in write_add_to:
                        try:
                            f = Path(file)
                            self.__write(f, out, mode)
                            correct_files.append(f)
                        except FileNotFoundError:
                            print(f"'{file}': No such file or directory")

                    try:
                        out = getattr(self, "_" + command)(options, data + out.split())
                    except AttributeError:
                        out = f"{command}: command not found"

                    for f in correct_files:
                        self.__write(Path(file), out, "a")
                        out = ""
                    options, data = [], []
                    write_add_to, write_add_to_mode = [], False
                    command = None
                case l if l[0] == "-":
                    options.append(e)
                case ">":
                    write_add_to_mode = "w"
                case ">>":
                    write_add_to_mode = "a"
                case _ if write_add_to_mode:
                    write_add_to.append([e, write_add_to_mode])
                    write_add_to_mode = False
                case _ if not command:
                    command = e
                case _:
                    data.append(e)
        return out

    # ниже записаны сами команды, обязательно в формате def _name(self, options:list, data:list)->str

    def _echo(self, options, data):
        return " ".join(data) + "\n"

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
        _dir = self.working_dir / "".join(data)
        if _dir.is_dir():
            return " ".join(sorted(listdir(_dir)))
        if _dir.is_file():
            return _dir.name
        return f"cannot access '{''.join(data)}': No such file or directory"

    def _cat(self, options, data):
        out = ""
        for file in data:
            path = self.working_dir / file
            if not path.is_file():
                out += f"'{path}': No such file or directory"
                continue
            with open(path, "r", encoding="utf-8") as f:
                out += f.read()
        return out

    def _tac(self, options, data):
        return "\n".join(self._cat(options, data).splitlines()[::-1])

    def _tree(self, options, data):
        out = "."
        pattern = ".*"
        deph_limit = float("inf")
        for option, value in zip(options, data):
            match option:
                case "-L":
                    try:
                        deph_limit = int(value)
                    except:
                        return f"invalid option '{option}' value"
                case "-P":
                    pattern = value
                case _:
                    return f"invalid option '{option}'"

        _dir = in_path = Path("".join(data[len(options) :]))
        if not _dir.is_absolute():
            _dir = self.working_dir / _dir
        if not _dir.is_dir():
            return f"'{in_path}': No such file or directory"

        def dfs(_dir, deph, threads=set(), end=False):
            nonlocal out, in_path
            if deph != 0:
                out += (
                    "\n"
                    + "".join(
                        "│   " if i in threads else "    " for i in range(deph - 1)
                    )
                    + (f"└── {_dir.name}" if end else f"├── {_dir.name}")
                )

            if not _dir.is_dir() or deph >= deph_limit:
                return
            dirs = [e for e in listdir(_dir) if re.match(pattern, e)]
            if not dirs:
                if deph == 0 and in_path:
                    out = str(in_path) + "\n"  # ??? тест 9 и тест 11
                return

            threads.add(deph)
            for e in dirs[:-1]:
                dfs(_dir / e, deph + 1, threads)
            threads.remove(deph)
            dfs(_dir / dirs[-1], deph + 1, threads, True)

        dfs(_dir, 0)
        if not out.endswith("\n"):
            out += "\n"
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
