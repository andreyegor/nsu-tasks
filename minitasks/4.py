from collections import defaultdict


def reversed_dict(d):
    out = defaultdict(lambda: [])
    # out[hashable] сразу вернёт TypeError, по этому доп. кода не нужно
    for key in d:
        out[d[key]].append(key)
    for key in out:
        if len(out[key]) == 1:
            out[key] = out[key][0]
        else:
            out[key] = tuple(out[key])
    return dict(out)


print(reversed_dict({"Ivanov": 97832, "Petrov": 55521, "Kuznecov": 97832}))
print(reversed_dict({"Ivanov": (97832, 2), "Petrov": 55521, "Kuznecov": (97832, 2)}))
print(
    reversed_dict(
        {("Ivanov", 1): (97832, 2), "Petrov": 55521, ("Kuznecov", 1): (97832, 2)}
    )
)
