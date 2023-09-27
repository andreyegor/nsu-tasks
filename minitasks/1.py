n = int(input())
cnt = n&1 if n!=-1 else 2

while n not in (0,-1):
    #чудеса
    n>>=1
    cnt+=n&1
    print(bin(n), n&1)

print(cnt)