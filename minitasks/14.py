import foreign

m = [[1.0, 2], [3.0, 4.0]]
print([list(map(int, e)) for e in foreign.foreign_matrix_power(m, 3)])
