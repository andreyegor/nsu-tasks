def format_table(benchmarks, algos, results):
    benchmarks = list(map(str, benchmarks))
    algos = list(map(str, algos))
    results = [list(map(str, e)) for e in results]

    heading = ["Benchmark", *algos]
    lines = [[benchmarks[i], *results[i]] for i in range(len(benchmarks))]
    columns_width = [
        len(max(heading[i], *[line[i] for line in lines])) for i in range(len(heading))
    ]

    normalized_heading = [
        heading[i].ljust(columns_width[i]) for i in range(len(heading))
    ]
    print("|" + "|".join(normalized_heading) + "|")
    print("|" + "-" * len("|".join(normalized_heading)) + "|")
    for line in lines:
        line = [line[i].ljust(columns_width[i]) for i in range(len(line))]
        print("|" + "|".join(line) + "|")


format_table(
    ["best case", "worst case"],
    ["quick sort", "merge sort", "bubble sort"],
    [[1.23, 1.56, 2.0], [3.3, 2.9, 3.9]],
)
format_table(
    ["best case", "the worst case"],
    ["quick sort", "merge sort", "bubble sort"],
    [[1.23, 1.56, 2.0], [3.3, 2.9, 3.9]],
)
