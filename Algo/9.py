class Matrix:
    def __init__(self, in_matrix: list):
        if type(in_matrix) == Matrix:
            self.data = in_matrix.data
        else:
            self.data = list(in_matrix)

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
            stop1 = key[0].stop if key[0].stop != None else start1 + 1
            step1 = key[0].step if key[0].step != None else 1

            start2 = key[1].start
            stop2 = min(
                key[1].stop if key[1].stop != None else start2 + 1, len(self.data[0])
            )
            step2 = key[1].step if key[1].step != None else 1
            for i in range(start1, stop1, step1):
                self.data[i][start2:stop2:step2] = value[k][: (stop2 - start2) // step2]
                k += 1
        else:
            self.data.__setitem__(key, value)

    def __add__(self, other):
        return Matrix(
            [
                [self.data[i][j] + other[i][j] for j, _ in enumerate(self.data)]
                for i, _ in enumerate(self.data)
            ]
        )

    def __sub__(self, other):
        return Matrix(
            [
                [self.data[i][j] - other[i][j] for j, _ in enumerate(self.data)]
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
        ln = max(len(self.data), len(self.data[0]), len(other))
        if ln & (ln - 1) != 0 or not (
            len(self.data) == len(self.data[0]) == len(other)
        ):
            i = 0
            while ln:
                ln >>= 1
                i += 1
            ln = 1 << (i)

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

        out = Matrix([[0] * len(self.data) for i in range(len(other[0]))])
        out[0:half_ln, 0:half_ln] = q1
        out[0:half_ln, half_ln : len(other[0])] = q2
        out[half_ln : len(self.data), 0:half_ln] = q3
        out[half_ln : len(self.data), half_ln : len(other[0])] = q4
        return out


m1 = Matrix([[1, 2, 3], [4, 5, 6]])
m2 = Matrix([[1, 2], [3, 4], [5, 6]])
print(len(m1))
print(m2 @ m1, m2 * m1)
