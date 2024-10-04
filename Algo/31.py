"""
Пусть после статического анализа про каждую функцию в
программе известно, вызовы каких других функций присутствуют
в ее коде. Формат входных данных:
foo: bar, baz, qux
bar: baz, foo, bar
qux: qux
Вам необходимо найти наибольшую рекурсивную компоненту:
множество функций, при исполнении которых можно попасть в
любую другую функцию из этого множества.
Кроме того, для каждой функции определить, есть ли в ней
рекурсивные (в т.ч. непрямые) вызовы.
"""

from collections import defaultdict, deque
from functools import reduce


def solution(graph):
    graph = defaultdict(set, graph)
    regraph = defaultdict(set)
    for e, g in sorted(graph.items()):
        for h in g:
            regraph[h].add(e)
    first_dfs = []  # в этой реализации наоборот, в порядка возрастания
    visited = set()

    def dfs(now):
        if now in visited:
            return
        visited.add(now)
        for next in regraph[now]:
            dfs(next)
        first_dfs.append(now)

    for start in frozenset(regraph.keys()):
        if start in visited:
            continue
        dfs(start)

    cmps = []
    visited = set()
    for start in reversed(first_dfs):
        cmps.append([start])
        visited.add(start)
        que = deque(graph[start])
        while que:
            now = que.pop()
            if now == start:
                break
            if now in visited:
                continue
            cmps[-1].append(now)
            visited.add(now)
            que.extend(graph[now])
        else:
            del cmps[-1]

    return max(cmps, key=len) if cmps else [], list(
        reduce(lambda a, b: [a.update(b), a][1], cmps, set())
    )


if __name__ == "__main__":
    tests = [
        {"foo": ["bar", "baz", "qux"], "bar": ["baz", "foo", "baz"], "qux": ["qux"]},
        {"foo": ["bar", "baz"], "bar": ["baz", "foo", "qux"], "qux": ["qux", "foo"]},
        {"foo": [], "bar": [], "baz": [], "qux": []},
    ]
    for test in tests:
        print(solution(test))
