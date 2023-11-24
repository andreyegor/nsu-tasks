from ast import literal_eval
from collections.abc import Iterable
from itertools import tee
from typing import Callable


#TODO проверить аннотации типов во всей проге
def str_to_list_constructor(line: str) -> list:
    line = f"[{line[1:-1]}]"

    def inner():
        return iter(literal_eval(line))

    return inner

def dot_func_constructor(left, right):
            is_dot = is_constructor(right, "set")

            def inner():
                for e in left():
                    if is_dot(e):
                        try:
                            yield from getattr(e, right)
                        except ValueError:
                            yield getattr(e, right)

            return inner

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
        #TODO заглушка, в итоге райт должен быть только коллабл
        itr = right()
        try:
            return getattr(obj, left) in itr
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


# TODO мне не нравится, переделать
def dot_constructor(left, right):

    def inner():
        for e in left:
            try:
                yield from getattr(e, right)()
            except ValueError:
                yield getattr(e, right)()

    return inner


def str_to_iter_constructor(line: str) -> list:
    line = f"[{line[1:-1]}]"

    def inner():
        return literal_eval(line)

    return inner
