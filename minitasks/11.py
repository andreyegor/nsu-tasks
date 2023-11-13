class Counter:
    def __init__(self, initial_count=0, step=1):
        self.count = initial_count
        self.step = step

    def increment(self):
        self.count += self.step


class Singleton:
    __created__ = None

    def __new__(cls, *args, **kwargs):
        if cls.__created__ == None:
            cls.__created__ = super().__new__(cls, *args, **kwargs)
        return cls.__created__


class GlobalCounter(Singleton, Counter):
    pass


gc1 = GlobalCounter()
gc2 = GlobalCounter()
assert id(gc1) == id(gc2)  # True


def singleton(cls):
    cls.__created__ = None
    cls.__default_new__ = cls.__new__

    def new(cls, *args, **kwargs):
        if cls.__created__ == None:
            cls.__created__ = cls.__default_new__(cls, *args, **kwargs)
        return cls.__created__

    cls.__new__ = new

    return cls


@singleton
class OtherGlobalCounter(Counter):
    pass


gc1 = OtherGlobalCounter()
gc2 = OtherGlobalCounter()
assert id(gc1) == id(gc2)  # True
