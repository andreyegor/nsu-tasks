def reversed_dict(d):
    out = dict()
    for key in d:
        # d[hashable] сразу вернёт TypeError, по этому доп. кода не нужно
        if d[key] not in out:
            out[d[key]] = key
        elif type(d[key]) != tuple:
            out[d[key]] = (out[d[key]], key)
        else:
            out[d[key]] += (key,)
    return out


print(reversed_dict({"Ivanov": 97832, "Petrov": 55521, "Kuznecov": 97832}))
