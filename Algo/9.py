from time import sleep, time
from random import randint


class Matrix:
    def __init__(self, in_matrix: list):
        if type(in_matrix) == Matrix:
            self.data = in_matrix.data
        else:
            self.data = list(in_matrix)

    def __eq__(self, other):
        # print(self.data == other.data, self.data, other.data)
        return self.data == other.data

    def __str__(self) -> str:
        return str(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        if type(key) == tuple:
            return Matrix([e[key[1]] for e in self.data[key[0]]])
        else:
            return self.data[key]

    def __setitem__(self, key, value):
        if type(key) == tuple:
            k = 0
            start1 = key[0].start
            stop1 = min(
                key[0].stop if key[0].stop != None else start1 + 1, len(self.data)
            )
            step1 = key[0].step if key[0].step != None else 1

            start2 = key[1].start
            stop2 = min(
                key[1].stop if key[1].stop != None else start2 + 1, len(value[0])
            )
            step2 = key[1].step if key[1].step != None else 1
            for i in range(start1, stop1, step1):
                self.data[i][start2:stop2:step2] = value[k]
                k += 1
        else:
            self.data.__setitem__(key, value)

    def __add__(self, other):
        return Matrix(
            [
                [self.data[i][j] + other[i][j] for j, _ in enumerate(self.data[0])]
                for i, _ in enumerate(self.data)
            ]
        )

    def __sub__(self, other):
        return Matrix(
            [
                [self.data[i][j] - other[i][j] for j, _ in enumerate(self.data[0])]
                for i, _ in enumerate(self.data)
            ]
        )

    def __mul__(self, other):
        out = Matrix([[0] * len(other[0]) for i in range(len(self.data))])
        for i in range(len(self.data)):
            for j in range(len(other[0])):
                for k in range(len(other)):
                    out[i][j] += self.data[i][k] * other[k][j]
        return out

    def __matmul__(self, other):
        LIMIT = 1
        ln = max(len(self.data), len(self.data[0]), len(other[0]))
        if ln & (ln - 1) != 0:
            i = 0
            while ln:
                ln >>= 1
                i += 1
            ln = 1 << (i)

        if not (
            len(self.data) == ln and len(self.data[0]) == ln and len(other[0]) == ln
        ):
            m1, m2 = Matrix([[0] * ln for i in range(ln)]), Matrix(
                [[0] * ln for i in range(ln)]
            )
            for i, _ in enumerate(self.data):
                for j, _ in enumerate(self.data[i]):
                    m1[i][j] = self.data[i][j]
            for i, _ in enumerate(other):
                for j, _ in enumerate(other[i]):
                    m2[i][j] = other[i][j]
        else:
            m1, m2, ln = Matrix(self.data), Matrix(other), len(other)

        half_ln = ln // 2
        if ln <= LIMIT:
            return m1 * m2
        a, b, c, d = (
            m1[0:half_ln, 0:half_ln],
            m1[0:half_ln, half_ln:ln],
            m1[half_ln:ln, 0:half_ln],
            m1[half_ln:ln, half_ln:ln],
        )

        e, f, g, h = (
            m2[0:half_ln, 0:half_ln],
            m2[0:half_ln, half_ln:ln],
            m2[half_ln:ln, 0:half_ln],
            m2[half_ln:ln, half_ln:ln],
        )

        p1 = a @ (f - h)
        p2 = (a + b) @ h
        p3 = (c + d) @ e
        p4 = d @ (g - e)
        p5 = (a + d) @ (e + h)
        p6 = (b - d) @ (g + h)
        p7 = (a - c) @ (e + f)

        q1 = p5 + p4 - p2 + p6
        q2 = p1 + p2
        q3 = p3 + p4
        q4 = p1 + p5 - p3 - p7

        out = Matrix([[0] * ln for i in range(ln)])
        out[0:half_ln, 0:half_ln] = q1
        out[0:half_ln, half_ln:ln] = q2
        out[half_ln:ln, 0:half_ln] = q3
        out[half_ln:ln, half_ln:ln] = q4

        out = out[: len(self.data), : len(other[0])]
        if out != self * other:
            print(self)
            print(other)
            print(out, self * other)
            print("---")
        return out[: len(self.data), : len(self.data[0])]


class Bench:
    def __init__(self):
        self.tests = []
        self.funcs = []
        self.results = []

    def run(self, func, inp):
        # print([str(e) for e in inp])
        start = time()
        out = func(*inp)
        return (out, time() - start)

    def do(self):
        for test in self.tests:
            self.results.append([])
            for foo in self.funcs:
                self.results[-1].append(self.run(foo, test)[1])

    def print_formatted(self):
        benchmarks = [f"test {i}" for i, _ in enumerate(be.tests)]
        algos = [foo.__name__ for foo in be.funcs]
        results = [list(map(str, e)) for e in self.results]

        heading = ["Benchmark", *algos]
        lines = [[benchmarks[i], *results[i]] for i in range(len(benchmarks))]
        columns_width = [
            max(len(str(heading[i])), *[len(str(line[i])) for line in lines])
            for i in range(len(heading))
        ]

        normalized_heading = [
            heading[i].ljust(columns_width[i]) for i in range(len(heading))
        ]
        print("|" + "|".join(normalized_heading) + "|")
        print("|" + "-" * len("|".join(normalized_heading)) + "|")
        for line in lines:
            line = [line[i].ljust(columns_width[i]) for i in range(len(line))]
            print("|" + "|".join(line) + "|")


be = Bench()

tests_count = 15
for _ in range(15):
    i, j, k = randint(1, 10), randint(1, 10), randint(1, 10)
    a = Matrix([[randint(0, 100) for _ in range(j)] for _ in range(i)])
    b = Matrix([[randint(0, 100) for _ in range(k)] for _ in range(j)])
    be.tests.append(
        [
            Matrix([[randint(0, 10) for _ in range(j)] for _ in range(i)]),
            Matrix([[randint(0, 10) for _ in range(k)] for _ in range(j)]),
        ]
    )
    assert len(a[0]) == len(b)
    a @ b

# строки это столбцы, КАК ОБЫЧНО А НЕТ НЕ ПЕРЕПУТАНЫ
print(Matrix([[50], [69], [66]]) * Matrix([[9]]))
print(Matrix([[50], [69], [66]]) @ Matrix([[9]]))


def triv(a, b):
    return a * b


def shtra(a, b):
    return a @ b


be.funcs = [triv, shtra]
be.do()
be.print_formatted()
