def divide(a, b):
    ln = 0
    while a >= b:
        b <<= 1
        ln += 1
    b >>= 1
    out = 0
    for i in range(ln):
        t = 0
        cnt = 0
        while t <= a:
            t += b
            cnt += 1
        cnt -= 1 if cnt != 0 and a != t else 0

        k = cnt
        while True:
            out <<= 1
            k >>= 1
            if not k:
                break

        out += cnt
        a -= t - b
        b >>= 1
    return (out, a)


if __name__ == "__main__":
    divide(2, 1)
    for a in range(0, 10):
        for b in range(1, 10):
            if divide(a, b) != (a // b, a % b):
                print(f"{a}/{b}!={divide(a,b)}")
