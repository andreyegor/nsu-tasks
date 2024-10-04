"""
Необходимо принять решение о месте магистрального
нефтепровода с запада на восток через нефтеносное
поле. На этом поле расположены N нефтяных скважин (их
координаты заданы). От магистрали до скважин отходят
перпендикулярные трубопроводы.

Необходимо выбрать место магистрального нефтепровода
так, чтобы суммарная длина трубопроводов была
минимальной.

Решить задачу нужно за линейное.
"""

from math import ceil
from random import randint


def naive(arr: list[list[int, int]]) -> int:
    out = [(None, float("inf"))]
    for i in range(min(arr, key=lambda x: x[1])[1], max(arr, key=lambda x: x[1])[1]):
        this = (i, sum(abs(e[1] - i) for e in arr))
        if this[1] == out[0][1]:
            out.append(this)
        if this[1] < out[0][1]:
            out = [this]
    return [e[0] for e in out]


def rand_test(xmin=0, xmax=100, ymin=0, ymax=100, mincount=100, maxcount=100):
    out = []
    for i in range(randint(mincount, maxcount)):
        out.append([randint(xmin, xmax), randint(ymin, ymax)])
    return out


def kth_hoar(arr, k, left=None, right=None):
    left = left if left != None else 0
    right = right if right != None else len(arr)

    if right - left <= 1:
        return arr[left]

    i, j = left, right - 1

    pivot = arr[randint(left, right - 1)]
    while True:
        while i <= j and arr[i] < pivot:
            i += 1
        while i <= j and arr[j] > pivot:
            j -= 1
        if i >= j:
            break
        arr[i], arr[j] = arr[j], arr[i]
        i += 1
        j -= 1

    if (arr[j] == pivot and j == k) or (arr[i] == pivot and i == k) :
        return pivot
    if i > k:
        return kth_hoar(arr, k, left, i)
    return kth_hoar(arr, k, j + 1, right)


def solution(arr):
    return kth_hoar([e[1] for e in arr], ceil(len(arr) / 2) - 1)


for i in range(100):
    case = rand_test()
    if solution(case) not in naive(case):
        print(naive(case), solution(case))
        print(case)
        break

