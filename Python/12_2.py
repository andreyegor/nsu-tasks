def chain(*itrs):
    for itr in itrs:
        yield from itr
        
print(list(chain([1,2], range(5))))