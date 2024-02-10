def divide(a, b): # a - n разрядное b - m разрядное, a - делимое b - делитель
    ln = 0
    while a >= b: # не больше n раз
        b <<= 1
        ln += 1
    b >>= 1
    out = 0
    for i in range(ln): #ln не превышает n
        t = 0
        cnt = 0
        while t <= a: # не больше m раз
            t += b
            cnt += 1
        cnt -= 1 if cnt != 0 and a != t else 0

        k = cnt
        while True: # также не больше m раз
            out <<= 1
            k >>= 1
            if not k:
                break

        out += cnt
        a -= t - b
        b >>= 1
    return (out, a) # значение и остаток от деления

#2n*2m = O(n*m)

if __name__ == "__main__":
    divide(2, 1)
    for a in range(0, 100):
        for b in range(1, 100):
            if divide(a, b) != (a // b, a % b):
                print(f"{a}/{b}!={divide(a,b)}")
