class matrix:
    def __init__(self, matrix: list):
        self.data = list(matrix)

    def __str__(self) -> str:
        return str(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        if type(key) == tuple:
            return matrix([e[key[1]] for e in self.data[key[0]]])
        else:
            return self.data[key]

    def __setitem__(self, key, value):
        if type(key) == tuple:
            k = 0
            start = key[0].start
            stop = key[0].stop if key[0].stop != None else start + 1
            step = key[0].step if key[0].step != None else 1
            for i in range(start, stop, step):
                self.data[i].__setitem__(key[1], value[k])
                k += 1
        else:
            self.data.__setitem__(key, value)

    def __add__(self, other):
        return matrix(
            [
                [self.data[i][j] + other[i][j] for j, _ in enumerate(self.data)]
                for i, _ in enumerate(self.data)
            ]
        )

    def __sub__(self, other):
        return matrix(
            [
                [self.data[i][j] - other[i][j] for j, _ in enumerate(self.data)]
                for i, _ in enumerate(self.data)
            ]
        )

    def __mul__(self, other):
        out = matrix([[0] * len(other[0]) for i in range(len(self.data))])
        for i in range(len(self.data)):
            for j in range(len(other[0])):
                for k in range(len(other)):
                    out[i][j] += self.data[i][k] * other[k][j]
        return out

    def __matmul__(self, other):
        LIMIT = 1
        ln = max(len(self.data), len(self.data[0]), len(other))
        if ln & (ln - 1) != 0:  # TODO не всегда дополнит
            i = 0
            while ln:
                ln >>= 1
                i += 1
            ln = 1 << (i)

        m1, m2 = matrix([[0] * ln for i in range(ln)]), matrix(
            [[0] * ln for i in range(ln)]
        )
        for i, _ in enumerate(self.data):
            for j, _ in enumerate(self.data[i]):
                m1[i][j] = self.data[i][j]
        for i, _ in enumerate(other):
            for j, _ in enumerate(other[i]):
                m2[i][j] = other[i][j]

        half_ln = ln // 2
        if ln <= LIMIT:
            return m1 * m2
        a, b, c, d = (
            m1[0:half_ln, 0:half_ln],
            m1[half_ln:ln, 0:half_ln],
            m1[0:half_ln, half_ln:ln],
            m1[half_ln:ln, half_ln:ln],
        )

        e, f, g, h = (
            m2[0:half_ln, 0:half_ln],
            m2[half_ln:ln, 0:half_ln],
            m2[0:half_ln, half_ln:ln],
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

        m1[0:half_ln, 0:half_ln] = q1
        m1[half_ln:ln, 0:half_ln] = q2
        m1[0:half_ln, half_ln:ln] = q3
        m1[half_ln:ln, half_ln:ln] = q4
        return m1


m1 = matrix([[1, 2], [3, 4]])
print(len(m1))
print(m1 @ m1, m1 * m1)
