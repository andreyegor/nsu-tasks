def flatten(arr):
    out = []
    for e in arr:
        if isinstance(e, list):
            out+=flatten(e)
        else:
            out.append(e)
    return out

print(flatten([1, 2, [4, 5], [6, [7]], 8]))