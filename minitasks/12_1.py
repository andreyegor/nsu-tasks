def cycle(in_itr):
    itr = in_itr
    while True:
        try:
            yield from itr
        except StopIteration:
            itr = in_itr
    
ccl = cycle(range(5))
for i in range(10):
    print(next(ccl))