def coroutine(f):
    def inner(*args, **kwargs):
        next(out := f(*args, **kwargs))
        return out
    return inner

@coroutine
def storage():
    values = set()
    was_there = False

    while True:
        val = yield was_there
        was_there = val in values
        if not was_there:
            values.add(val)


st = storage()
# next(st)
print(st.send(42))
print(st.send(42))
