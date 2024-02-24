from time import sleep, time
from random import randint
from functools import reduce


class Matrix:
    def __init__(self, in_matrix):
        if type(in_matrix) == Matrix:
            self.data = in_matrix.data
        else:
            self.data = list(in_matrix)

    def __eq__(self, other):
        return self.data == other.data

    def __str__(self):
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
            for i in range(key[0].start, key[0].stop):
                self.data[i][key[1].start : key[1].stop] = value[k]
                k += 1
        else:
            self.data.__setitem__(key, value)

    def append(self, inp):
        self.data.append(inp)

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
        LIMIT = 16

        len(self)
        if len(self) <= LIMIT:
            return self * other
        half_ln = len(self) // 2

        a, b, c, d = (
            self[0:half_ln, 0:half_ln],
            self[0:half_ln, half_ln : len(self)],
            self[half_ln : len(self), 0:half_ln],
            self[half_ln : len(self), half_ln : len(self)],
        )

        e, f, g, h = (
            other[0:half_ln, 0:half_ln],
            other[0:half_ln, half_ln : len(self)],
            other[half_ln : len(self), 0:half_ln],
            other[half_ln : len(self), half_ln : len(self)],
        )

        p1 = a @ (f - h)
        p2 = (a + b) @ h
        p3 = (c + d) @ e
        p4 = d @ (g - e)
        p5 = (a + d) @ (e + h)
        p6 = (b - d) @ (g + h)
        p7 = (a - c) @ (e + f)

        out = Matrix([[0] * (len(other[0])) for _, _ in enumerate(self.data)])
        out[0:half_ln, 0:half_ln] = p5 + p4 - p2 + p6
        out[0:half_ln, half_ln : len(self)] = p1 + p2
        out[half_ln : len(self), 0:half_ln] = p3 + p4
        out[half_ln : len(self), half_ln : len(self)] = p1 + p5 - p3 - p7
        return out

    def __pow__(self, other):
        LIMIT = 16

        len(self)
        if len(self) <= LIMIT:
            return self * other
        half_ln = len(self) // 2

        a, b, c, d = (
            self[0:half_ln, 0:half_ln],
            self[0:half_ln, half_ln : len(self)],
            self[half_ln : len(self), 0:half_ln],
            self[half_ln : len(self), half_ln : len(self)],
        )

        e, f, g, h = (
            other[0:half_ln, 0:half_ln],
            other[0:half_ln, half_ln : len(self)],
            other[half_ln : len(self), 0:half_ln],
            other[half_ln : len(self), half_ln : len(self)],
        )

        out = Matrix([[0] * (len(other[0])) for _, _ in enumerate(self.data)])
        out[0:half_ln, 0:half_ln] = a**e + b**g
        out[0:half_ln, half_ln : len(self)] = a**f + b**h
        out[half_ln : len(self), 0:half_ln] = c**e + d**g
        out[half_ln : len(self), half_ln : len(self)] = c**f + d**h
        return out


class Bench:
    def __init__(self):
        self.tests = []
        self.funcs = []
        self.results = []
        self.benchmarks = []

    def run(self, func, inp):
        start = time()
        func(*inp)
        return time() - start

    def do(self):
        self.results = [[] for _ in range(len(self.funcs))]
        for i, test in enumerate(self.tests):
            self.benchmarks += [
                f"matrix {len(test[0])}x{len(test[0][0])} and {len(test[1])}x{len(test[1][0])}",
                "-sample mean ",
                "-standard deviation",
                "-geometric mean",
            ]
            for i, foo in enumerate(self.funcs):
                tests = [self.run(foo, test) for _ in range(10)]
                sample_mean = sum(tests) / len(tests)
                standard_deviation = sum((sample_mean - e) ** 2 for e in tests) / len(
                    tests
                )
                geometric_mean = reduce(lambda a, b: a * b, tests) ** (1 / len(tests))
                self.results[i] += [
                    "",
                    str(sample_mean),
                    str(standard_deviation),
                    str(geometric_mean),
                ]
                print(
                    f"{foo.__name__}",
                    str(sample_mean),
                    str(standard_deviation),
                    str(geometric_mean),
                )

    def print_formatted(self):
        benchmarks = self.benchmarks
        algos = [foo.__name__ for foo in self.funcs]
        results = list(zip(*self.results))

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
for q in range(1, 9):
    i, j, k = 2**q, 2**q, 2**q
    a = Matrix([[randint(0, 50) for _ in range(j)] for _ in range(i)])
    b = Matrix([[randint(0, 50) for _ in range(k)] for _ in range(j)])
    be.tests.append(
        [
            Matrix([[randint(0, 10) for _ in range(j)] for _ in range(i)]),
            Matrix([[randint(0, 10) for _ in range(k)] for _ in range(j)]),
        ]
    )
    assert len(a[0]) == len(b)


def expand_2degree(a, b):
    lna, lnb, lnab = len(a), len(b[0]), len(a[0])
    ln = max(lna, lnb, lnab)
    if ln & ln - 1:
        i = 0
        while ln:
            ln >>= 1
            i += 1
        ln = 1 << (i)

    if not (lna == lnb == lnab == ln):
        for e in a:
            e += [0] * (ln - lnab)
        a.data += [[0] * ln for _ in range(ln - lna)]

        for e in b:
            e += [0] * (ln - lnb)
        b.data += [[0] * ln for _ in range(ln - lnab)]

    return lna, lnb


def trivial(a, b):
    return a * b


def recursive_8(a, b):
    lna, lnb = expand_2degree(a, b)
    return (Matrix(a) ** Matrix(b))[0:lna, 0:lnb]


def strassen(a, b):
    lna, lnb = expand_2degree(a, b)
    return (Matrix(a) @ Matrix(b))[0:lna, 0:lnb]

    # m1, m2 = [[0] * ln for i in range(ln)], [[0] * ln for i in range(ln)]
    # for i, _ in enumerate(a):
    #     for j, _ in enumerate(a[i]):
    #         m1[i][j] = a[i][j]
    #     for i, _ in enumerate(a):
    #         for j, _ in enumerate(a[i]):
    #             m2[i][j] = a[i][j]
    # else:
    #     m1, m2 = a, b


be.funcs = [trivial, recursive_8, strassen]
be.do()
be.print_formatted()
"""
На матрицах степени двойки
|Benchmark                 |trivial               |strassen              |
|------------------------------------------------------------------------|
|matrix 2x2 and 2x2        |                      |                      |
|-sample mean              |0.0                   |0.0                   |
|-standard deviation       |0.0                   |0.0                   |
|-geometric mean           |0.0                   |0.0                   |
|matrix 4x4 and 4x4        |                      |                      |
|-sample mean              |3.063678741455078e-05 |0.0                   |
|-standard deviation       |8.447514687759394e-09 |0.0                   |
|-geometric mean           |0.0                   |0.0                   |
|matrix 8x8 and 8x8        |                      |                      |
|-sample mean              |0.00010697841644287109|0.00014431476593017577|
|-standard deviation       |1.029994342616192e-07 |1.874407649893328e-07 |
|-geometric mean           |0.0                   |0.0                   |
|matrix 16x16 and 16x16    |                      |                      |
|-sample mean              |0.0008996009826660156 |0.0009491682052612304 |
|-standard deviation       |2.8794980607926843e-07|1.1040706851872528e-07|
|-geometric mean           |0.0                   |0.0                   |
|matrix 32x32 and 32x32    |                      |                      |
|-sample mean              |0.006925272941589356  |0.007257485389709472  |
|-standard deviation       |1.9428563348355966e-07|2.1251375358133377e-07|
|-geometric mean           |0.006911369963546515  |0.00724301543397998   |
|matrix 64x64 and 64x64    |                      |                      |
|-sample mean              |0.05440037250518799   |0.054233551025390625  |
|-standard deviation       |1.2918244522097668e-07|1.1764184591811499e-06|
|-geometric mean           |0.05439919191848962   |0.05422292985656629   |
|matrix 128x128 and 128x128|                      |                      |
|-sample mean              |0.43776860237121584   |0.39538047313690183   |
|-standard deviation       |4.8806762995354804e-05|6.160003209174646e-06 |
|-geometric mean           |0.4377142195346326    |0.3953727153854916    |
|matrix 256x256 and 256x256|                      |                      |
|-sample mean              |3.4808043003082276    |2.891377091407776     |
|-standard deviation       |0.00029020588155162844|0.0026999749307861976 |
|-geometric mean           |3.480762648189007     |2.890917894719659     |
|matrix 512x512 and 512x512|                      |                      |
|-sample mean              |28.308197927474975    |20.565713691711426    |
|-standard deviation       |0.006990949532880675  |0.23844155411046355   |
|-geometric mean           |28.30807445452816     |20.559961481620622    |
    
Исходная матрица записывается поверх расширенной
|Benchmark                 |trivial               |strassen              |
|------------------------------------------------------------------------|
|matrix 100x100 and 100x100|                      |                      |
|-sample mean              |0.21071949005126953   |0.49933462142944335   |
|-standard deviation       |1.9463239391370732e-06|1.4312449068256686e-05|
|-geometric mean           |0.21071483460159843   |0.4993202905815333    |
|matrix 200x200 and 200x200|                      |                      |
|-sample mean              |1.7775022745132447    |3.754588079452515     |
|-standard deviation       |0.016348170562462773  |0.0042170821824788615 |
|-geometric mean           |1.7731851247284671    |3.7540282813028485    |
|matrix 300x300 and 300x300|                      |                      |
|-sample mean              |5.874099755287171     |22.60898628234863     |
|-standard deviation       |0.008691849779386873  |0.03310805269202547   |
|-geometric mean           |5.873376877832225     |22.608260395978263    |
|matrix 400x400 and 400x400|                      |                      |
|-sample mean              |13.91094241142273     |27.514885663986206    |
|-standard deviation       |0.057888928354568624  |0.27239283405328935   |
|-geometric mean           |13.908871966225007    |27.510081821639872    |
|matrix 500x500 and 500x500|                      |                      |
|-sample mean              |27.24716544151306     |34.804726362228394    |
|-standard deviation       |0.10712507679983219   |0.15079974749205577   |
|-geometric mean           |27.24520850196568     |34.80259389010841     |

Исходная матрица (буквально) расширяется
|Benchmark                 |trivial               |strassen             |
|-----------------------------------------------------------------------|
|matrix 100x100 and 100x100|                      |                     |
|-sample mean              |0.2088937282562256    |0.392126202583313    |
|-standard deviation       |2.0853177238677744e-06|6.745874057401125e-06|
|-geometric mean           |0.20888878721796827   |0.3921176327663869   |
|matrix 200x200 and 200x200|                      |                     |
|-sample mean              |1.6612386226654052    |3.6788541316986083   |
|-standard deviation       |4.066850677645561e-05 |0.0012194826376253332|
|-geometric mean           |1.6612263894902297    |3.678689212338355    |
|matrix 300x300 and 300x300|                      |                     |
|-sample mean              |6.221141791343689     |19.916953802108765   |
|-standard deviation       |0.27313900228357907   |0.010437928596172697 |
|-geometric mean           |6.201957566624515     |19.916692717812047   |
|matrix 400x400 and 400x400|                      |                     |
|-sample mean              |14.121913361549378    |20.478511261940003   |
|-standard deviation       |0.007043649695891076  |0.021924815106229407 |
|-geometric mean           |14.121664786913767    |20.477977816575166   |
|matrix 500x500 and 500x500|                      |                     |
|-sample mean              |27.574809622764587    |20.679905247688293   |
|-standard deviation       |0.05264961679363354   |0.008875918695139831 |
|-geometric mean           |27.57386220710942     |20.679691279909882   |

Итог: Этот алгоритм быстрее тривиального на квадратных матрицах размером в квадрат 
двух больше 64 и на матрицах с максимальной длинной стороны не меньше 500, так как
расширение матрицы в занимает довольно много времени

upd: добавлено сравнение с алгоритмом на 8 рекурсивных вызовов, он ожидаемо медленнее 
двух других, чтобы не состариться в ожидании результата ограничился тестами только на 
матрицах степени двойки, до 256x256
|Benchmark                 |trivial               |recursive_8           |strassen              |
|-----------------------------------------------------------------------------------------------|
|matrix 2x2 and 2x2        |                      |                      |                      |
|-sample mean              |0.0                   |0.0                   |0.0                   |
|-standard deviation       |0.0                   |0.0                   |0.0                   |
|-geometric mean           |0.0                   |0.0                   |0.0                   |
|matrix 4x4 and 4x4        |                      |                      |                      |
|-sample mean              |0.0001108407974243164 |0.0                   |0.0001005411148071289 |
|-standard deviation       |1.1057114136292515e-07|0.0                   |9.097664189994249e-08 |
|-geometric mean           |0.0                   |0.0                   |0.0                   |
|matrix 8x8 and 8x8        |                      |                      |                      |
|-sample mean              |0.00010044574737548828|0.0002004861831665039 |5.042552947998047e-05 |
|-standard deviation       |9.080413349238367e-08 |1.6078272949471286e-07|2.2884606210027414e-08|
|-geometric mean           |0.0                   |0.0                   |0.0                   |
|matrix 16x16 and 16x16    |                      |                      |                      |
|-sample mean              |0.0009380340576171875 |0.0009379148483276367 |0.0010017156600952148 |
|-standard deviation       |1.5225438346533337e-07|1.5750657041735392e-07|5.0379745175632705e-08|
|-geometric mean           |0.0                   |0.0                   |0.0009733678721807987 |
|matrix 32x32 and 32x32    |                      |                      |                      |
|-sample mean              |0.007668805122375488  |0.007733988761901856  |0.007543516159057617  |
|-standard deviation       |3.775262604222007e-07 |2.708980110810444e-07 |1.2686699392361335e-07|
|-geometric mean           |0.00764561631224047   |0.007717142314607832  |0.007534941130421396  |
|matrix 64x64 and 64x64    |                      |                      |                      |
|-sample mean              |0.05711526870727539   |0.06298692226409912   |0.05584373474121094   |
|-standard deviation       |5.076085344626336e-06 |1.0199381000575158e-06|2.9928259118605635e-06|
|-geometric mean           |0.0570725153897097    |0.06297888457432711   |0.05581797665047647   |
|matrix 128x128 and 128x128|                      |                      |                      |
|-sample mean              |0.47293996810913086   |0.4968977212905884    |0.39923045635223386   |
|-standard deviation       |0.00012756413052557037|4.0000831568818284e-05|4.648755855782839e-06 |
|-geometric mean           |0.4728092760247803    |0.4968577266502146    |0.399224643770128     |
|matrix 256x256 and 256x256|                      |                      |                      |
|-sample mean              |3.6855241537094114    |4.128388094902038     |2.912790822982788     |
|-standard deviation       |0.008761427209049658  |0.0025224344417785    |0.0017227230631283422 |
|-geometric mean           |3.6843794957539684    |4.128082016399099     |2.9124992342783       |
"""
