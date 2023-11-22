import io
import sys
from pathlib import Path
from typing import TextIO

import commands


def write(file: Path, text: str, mode="w"):
    with open(file, mode, encoding="utf-8") as f:
        f.write(text)


def parse(line: str):
    def read_command(token):
        nonlocal command
        try:
            command = getattr(commands, token)
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
                    if err := read_command(token):
                        return err
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
                    if err := read_option(token):
                        return err
                case _:
                    data.append(token)
        correct_files = []
        for file, mode in write_data:
            f = Path(file)
            if not Path(f.parent).is_dir() or (not f.is_file() and (mode == "a")):
                print(f"'{file}': No such file or directory")
                continue
            write(f, out, mode)
            correct_files.append(f)
        try:
            out = command(options, data)
        except Exception:
            out = "Unknown error"

        for f in correct_files:
            write(f, out, "a")
        options, data = [], []
        write_data, write_mode = [], False
        command = None
    return out if not correct_files else ""


def solution(script: TextIO, output: TextIO) -> None:
    for line in script:
        out = parse(line)
        output.write(out + "\n" if out and len(out) > 1 and out[-1:] != "\n" else out)


if __name__ == "__main__":
    print("$ ", end="")
    for line in sys.stdin:
        solution(io.StringIO(line), sys.stdout)
        print("$ ", end="")
