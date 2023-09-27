n = int(input())
cnt = n&1

while n not in (0,-1):
    n>>=1
    cnt+=n&1

print(2 if cnt == 1 and n==-1 else cnt)