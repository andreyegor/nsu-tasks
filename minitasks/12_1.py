def cycle(itr):
    while True:
        yield from itr
    
ccl = cycle(range(5))
for i in range(10):
    print(next(ccl))