def flatten(arr, deph = float('inf')):
    out = []
    for e in arr:
        if isinstance(e, list) and deph!=0:
            out+=flatten(e, deph=deph-1)
        else:
            out.append(e)
    return out

print(flatten([1, 2, [4, 5], [6, [7]], 8],deph=1))
print(flatten([1, 2, [4, 5], [6, [7]], 8]))