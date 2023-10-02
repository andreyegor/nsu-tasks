def matrix(data):
    out = []
    for line in data.split("|"):
        out.append([])
        for e in line.split():
            out[-1].append(float(e))
    return out


print(matrix("1 2| 3 4"))
