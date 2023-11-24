from ast import literal_eval
from typing import Callable


def str_to_list(line: str) -> list:
    line = f"[{line[1:-1]}]"
    return literal_eval(line)


def and_constructor(left: Callable, right: Callable) -> Callable:
    return lambda obj: left(obj) and right(obj)


def or_constructor(left: Callable, right: Callable) -> Callable:
    return lambda obj: left(obj) or right(obj)


def is_constructor(left, right) -> Callable:
    def inner(obj) -> bool:
        try:
            return str(getattr(obj, left)) == right or right == "set"
        except AttributeError:
            return False

    return inner


def in_constructor(left, right) -> Callable:
    def inner(obj) -> bool:
        try:
            return str(getattr(obj, left)) in right
        except AttributeError:
            return False

    return inner


def contains_constructor(left, right) -> Callable:
    def inner(obj) -> bool:
        try:
            return right in str(getattr(obj, left))
        except AttributeError:
            return False

    return inner
