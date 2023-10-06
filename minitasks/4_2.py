def reversed_dict(d):
    keys = set()
    is_tupple = set()
    out = dict()
    for key, val in d.items():
        if val not in keys:
            out[val] = key
            keys.add(key)
        elif val not in is_tupple:
            out[val] = (out[val], key)
            is_tupple.add(val)
        else:
            out[val] += key
    return out


print(reversed_dict({"Ivanov": 97832, "Petrov": 55521, "Kuznecov": 97832}))
print(reversed_dict({"Ivanov": (97832, 2), "Petrov": 55521, "Kuznecov": (97832, 2)}))
print(reversed_dict({("Ivanov", 1): (97832, 2), "Petrov": 55521, ("Kuznecov", 1): (97832, 2)}))
