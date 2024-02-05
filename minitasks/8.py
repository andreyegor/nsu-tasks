import functools


def deprecated(f=None, *, since=None, will_be_removed=None):
    if f == None:
        return functools.partial(
            deprecated, since=since, will_be_removed=will_be_removed
        )

    message = f"Warning: function {f.__name__} is deprecated {'' if since == None else f'since version {since}'}. It will be removed in {'future versions' if will_be_removed==None else f'version {will_be_removed}'}."

    @functools.wraps(f)
    def inner(*args, **kwargs):
        print(message)
        return f(*args, **kwargs)

    return inner


@deprecated
def foo():
    print("Hello from foo")


@deprecated(since="4.2.0", will_be_removed="5.0.1")
def bar():
    print("Hello from bar")


foo()
bar()
