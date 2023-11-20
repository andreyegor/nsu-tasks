import functools
import io
import os
import re
import sys
from collections import deque
from functools import reduce
from pathlib import Path
from queue import Queue
from typing import TextIO


class Engine:
    def __init__(self):
        pass

    def _write(self, file: Path, text: str, mode="w"):
        with open(file, mode, encoding="utf-8") as f:
            f.write(text)

    def _command(options=None):
        def inner(f):
            f.__command_options__ = {} if options == None else options
            return f

        return inner

    def parse(self, line: str):
        def read_command(token):
            nonlocal command
            try:
                command = getattr(self, token)
                command.__command_options__
                return False
            except AttributeError:
                return f"{token}: command not found"

        def read_option(token):
            nonlocal wait_for_opt, options
            if token not in command.__command_options__:
                return f"invalid option '{token}'"
            wait_for_opt = command.__command_options__[token]
            options[token] = []
            return False

        command = None
        out = ""
        data, options = [], {}
        write_data, write_mode = [], False
        wait_for_opt = 0
        for pipe in line.split("|"):
            left, middle, right = pipe, [], ""
            if '"' in pipe:
                left, *middle, right = pipe.split('"')
            for token in left.split() + middle + right.split():
                match token:
                    case _ if not command:
                        if _out := read_command(token):
                            return _out
                    case _ if wait_for_opt:
                        options[list(options.keys())[-1]].append(token)
                        wait_for_opt -= 1
                    case ">":
                        write_mode = "w"
                    case ">>":
                        write_mode = "a"
                    case _ if write_mode:
                        write_data.append([token, write_mode])
                        write_mode = False
                    case _ if write_data:
                        break
                    case token if token in command.__command_options__:
                        if _out := read_option(token):
                            return _out
                    case _:
                        data.append(token)
            correct_files = []
            for file, mode in write_data:
                f = Path(file)
                if not Path(f.parent).is_dir or (not f.is_file() and (mode == "a")):
                    print(f"'{file}': No such file or directory")
                    continue
                self._write(f, out, mode)
                correct_files.append(f)
            try:
                out = command(options, data)
            except Exception:
                out = "Unknown error"

            for f in correct_files:
                self._write(Path(file), out, "a")
                out = ""
            options, data = [], []
            write_data, write_mode = [], False
            command = None
        return out

    # ниже записаны сами команды, обязательно в формате def _name(self, options:list, data:list)->str
    @_command()
    def echo(self, options, data):
        return " ".join(data) + "\n"

    @_command()
    def pwd(self, options, data):
        return os.getcwd()

    @_command()
    def cd(self, options, data):
        try:
            os.chdir(data[0])
            return ""
        except FileNotFoundError:
            return f"'{data[0]}': No such file or directory"

    @_command()
    def mkdir(self, options, data):
        in_dir = Path(data[0])
        try:
            os.mkdir(in_dir)
            return ""
        except FileNotFoundError:
            return f"‘{in_dir}’: No such file or directory"
        except FileExistsError:
            return f"‘{in_dir}’: File or directory alredy exists"

    @_command()
    def ls(self, options, data):
        try:
            return " ".join(sorted(os.listdir(data[0]) if data else os.listdir()))
        except FileNotFoundError:
            return f"cannot access '{''.join(data)}': No such file or directory"

    @_command()
    def cat(self, options, data):
        out = ""
        for file in data:
            path = Path(file)
            if not path.is_file():
                out += f"'{path}': No such file or directory"
                continue
            with open(path, "r", encoding="utf-8") as f:
                out += f.read()
        return out

    @_command()
    def tac(self, options, data):
        return "\n".join(self.cat(options, data).splitlines()[::-1])

    @_command(options={"-L": 1, "-P": 1})
    def tree(self, options, data):
        out = "."
        pattern = ".*"
        deph_limit = float("inf")
        for option, value in options.items():
            match option:
                case "-L":
                    try:
                        deph_limit = int(value[0])
                    except:
                        return f"invalid option '{option}' value"
                case "-P":
                    pattern = value[0]

        _dir = in_path = Path("".join(data[len(options) :]))
        if not _dir.is_dir():
            return f"'{in_path}': No such file or directory"

        def dfs(_dir, deph, branches=set(), end=False):
            nonlocal out, in_path
            space = "    "
            branch = "│   "
            middle = "├── "
            last = "└── "
            if deph != 0:
                out += (
                    "\n"
                    + "".join(
                        branch if i in branches else space for i in range(deph - 1)
                    )
                    + (last + _dir.name if end else middle + _dir.name)
                )

            if not _dir.is_dir() or deph >= deph_limit:
                return
            dirs = [
                e
                for e in sorted(os.listdir(_dir))
                if (_dir / e).is_dir() or re.match(pattern, str(e))
            ]
            if not dirs:
                if deph == 0 and in_path:
                    out = str(in_path) + "\n"
                return

            branches.add(deph)
            for e in dirs[:-1]:
                dfs(_dir / e, deph + 1, branches)
            branches.remove(deph)
            dfs(_dir / dirs[-1], deph + 1, branches, True)

        dfs(_dir, 0)
        if not out.endswith("\n"):
            out += "\n"
        return out

    @_command(options={"-c": 1, "-r": 1})
    def grep(self, options, data):
        pattern = data[0]
        count = False
        recursive = False
        for option in options:
            match option:
                case "-c":
                    count = True
                case "-r":
                    recursive = True
                case _:
                    return f"invalid option '{option}'"

        path = Path("".join(data[1:]))

        files = Queue()
        if path.is_file():
            files.put(path)
        elif not recursive or not path.is_absolute():
            return f"'{path}': No such file or directory"
        else:
            _dirs = Queue()
            _dirs.put(path)
            while not _dirs.empty():
                _dir = _dirs.get()
                for e in sorted(os.listdir(_dir)):
                    new_path = _dir / e
                    if new_path.is_file():
                        files.put(new_path)
                    else:
                        _dirs.put(new_path)
        out = ""
        while not files.empty():
            cnt = 0
            file = files.get()
            with open(file, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if re.search(pattern, line):
                        cnt += 1
                        if count:
                            continue
                        if not line.endswith("\n"):
                            line += "\n"
                        if recursive:
                            out += f"{file.name}:{line}"
                        else:
                            out += f"{line}"
                if cnt > 1:
                    out += f"{cnt}\n"
                if count:
                    out += f"{file.name}:{cnt}\n"
        return out


eng = Engine()


def solution(script: TextIO, output: TextIO) -> None:
    global eng
    if __name__ != "__main__":
        eng = Engine()
    for line in script:
        out = eng.parse(line)
        output.write(out + "\n" if out and len(out) > 1 and out[-1:] != "\n" else out)


if __name__ == "__main__":
    print("$ ", end="")
    for line in sys.stdin:
        solution(io.StringIO(line), sys.stdout)
        print("$ ", end="")
