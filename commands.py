import os
import re
from pathlib import Path
from queue import Queue

from shell import command as _command


# ниже записаны сами команды, обязательно в формате def _name( options:list, data:list)->str
@_command
def echo(options, data):
    return " ".join(data) + "\n"


@_command
def pwd(options, data):
    return os.getcwd()


@_command
def cd(options, data):
    try:
        os.chdir(data[0])
        return ""
    except FileNotFoundError:
        return f"'{data[0]}': No such file or directory"


@_command
def mkdir(options, data):
    in_dir = Path(data[0])
    try:
        os.mkdir(in_dir)
        return ""
    except FileNotFoundError:
        return f"‘{in_dir}’: No such file or directory"
    except FileExistsError:
        return f"‘{in_dir}’: File or directory alredy exists"


@_command
def ls(options, data):
    try:
        return " ".join(sorted(os.listdir(data[0]) if data else os.listdir()))
    except FileNotFoundError:
        return f"cannot access '{''.join(data)}': No such file or directory"


@_command
def cat(options, data):
    out = ""
    for file in data:
        path = Path(file)
        if not path.is_file():
            out += f"'{path}': No such file or directory"
            continue
        with open(path, "r", encoding="utf-8") as f:
            out += f.read()
    return out


@_command
def tac(options, data):
    return "\n".join(cat(options, data).splitlines()[::-1])


@_command(options={"-L": 1, "-P": 1})
def tree(options, data):
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
                + "".join(branch if i in branches else space for i in range(deph - 1))
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
def grep(options, data):
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
