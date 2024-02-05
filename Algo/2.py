def plus(n1, n2):
    return str(int(n1) + int(n2))  # TODO


def minus(n1, n2):
    return str(int(n1) - int(n2))  # TODO


def multiply(n1, n2):
    out = 0
    n2 = int(n2)
    for i in range(int(n1)):
        out += n2
    return str(out)  # TODO


def karatsuba(n1: str, n2: str) -> str:
    n1, n2 = sorted([n1, n2], key=len)
    if len(n2) == 1:
        return multiply(n1, n2)
    if len(n2) % 2 != 0:
        n2 = "0" + n2
    n1 = n1.rjust(len(n2), "0")

    a, b = n1[: len(n1) // 2], n1[len(n1) // 2 :]
    c, d = n2[: len(n2) // 2], n2[len(n2) // 2 :]

    k1 = karatsuba(a, c)
    k2 = karatsuba(b, d)
    k3 = karatsuba(plus(a, b), plus(c, d))
    k4 = minus(minus(k3, k2), k1)
    out = plus(k1 + "0" * len(n1), plus(k4 + "0" * (len(n1) // 2), k2))

    assert out == multiply(n1, n2)

    return out


if __name__ == "__main__":
    tests = [
        [["1234", "5678"], "7006652"],
        [["1234", "0"], "0"],
        [["1234", "1"], "1234"],
        [["1234", "2"], "2468"],
    ]
    for inp, outp in tests:
        if (res := karatsuba(*inp)) != outp:
            print(f"{inp[0]} * {inp[1]} = {res}, but {outp} expected")
    # assert all(multiply(*a) == b for a, b in tests)
