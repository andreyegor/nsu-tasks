from math import ceil, log
from random import choice, randint, sample


def is_prime(a):
    for i in range(2, a):
        if a % i == 0:
            return False
    return True


class Bloom:
    __PRIME = 909091

    def __init__(self, quan, prob):
        self.__hshs = ceil(log(prob, 1/2))  # ???
        self.__bitset = [False] * ceil(self.__hshs*quan/log(2))

        self.__abhshs = [
            [randint(0, len(self.__bitset) - 1), randint(0, len(self.__bitset) - 1)]
            for i in range(self.__hshs)
        ]

    def lookup(self, val):
        for i in range(self.__hshs):
            if self.__bitset[self.__hash(val, i)] == False:
                return False
        return True

    def insert(self, val):
        for i in range(self.__hshs):
            self.__bitset[self.__hash(val, i)] = True

    def __hash(self, val, i):
        a, b = self.__abhshs[i]
        return ((a * val + b) % self.__PRIME) % len(self.__bitset)


if __name__ == "__main__":
    TEST_RANGE = 5000
    PROB = 0.99
    test = sample(range(1,  0xffffffff), TEST_RANGE*2)
    includes, not_includes = test[0:TEST_RANGE], test[TEST_RANGE:]

    blm = Bloom(TEST_RANGE*10, PROB)
    for e in includes:
        blm.insert(e)

    for e in includes:
        assert blm.lookup(e)

    cntr = 0
    for e in not_includes:
        if blm.lookup(e):
            cntr += 1
    if not cntr / TEST_RANGE <= PROB * 1.5:
        print (cntr/TEST_RANGE)
