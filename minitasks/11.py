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
            cls.__init__(cls.__created__, *args, **kwargs)
            cls.__init__ = lambda self, *args, **kwargs: None
        return cls.__created__


class GlobalCounter(Singleton, Counter):
    pass


gc1 = GlobalCounter()
gc1.increment()
print(gc1.count)
gc2 = GlobalCounter()
print(gc2.count)
assert id(gc1) == id(gc2)  # True
