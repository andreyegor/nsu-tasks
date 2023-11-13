class Counter:
    def __init__(self, initial_count=0,step=1):
        self.count = initial_count
        self.step = step
    def increment(self):
        self.count += self.step


class Singleton():
    __created__ = None
    def __new__(cls, *args, **kwargs):
        if cls.__created__ == None:
            cls.__created__ = super().__new__(cls, *args, **kwargs)
        return cls.__created__
    
class GlobalCounter(Singleton, Counter):
    pass

gc1 = GlobalCounter()
gc2 = GlobalCounter()
assert id(gc1) == id(gc2) # True