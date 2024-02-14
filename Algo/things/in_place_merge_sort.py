from random import shuffle, randint
from math import ceil


def merge(arr: list, s1: int, f1: int, s2: int, f2: int, out: int) -> None:
    l, r, i = s1, s2, out
    
    while l != f1 and r != f2:
        if arr[l] <= arr[r]:
            arr[i], arr[l] = arr[l], arr[i]
            l += 1
        else:
            arr[i], arr[r] = arr[r], arr[i]
            r += 1
        i += 1

    while l < f1:
        arr[i], arr[l] = arr[l], arr[i]
        l += 1
        i += 1

    while r < f2:
        arr[i], arr[r] = arr[r], arr[i]
        r += 1
        i += 1

    return


def buffer_merge_sort(arr:list, left, right, buffer):
    if right - left - 1:
        mid = (left + right) // 2
        buffer_merge_sort(arr, left, mid, buffer)
        buffer_merge_sort(arr, mid, right, buffer)
        merge(arr, left, mid, mid, right, buffer)
        for i in range(0, right - left):  # merge в таком случае занимает O(2*n+2*m)
            arr[i + left], arr[i + buffer] = arr[i + buffer], arr[i + left]


def no_buffer_merge_sort(arr: list, left, right) -> None:
    if right - left - 1:
        lower_mid = (left + right) // 2 # два mid необходимо для коррктного merge участка нечётной длинны
        upper_mid = ceil((left + right) / 2)
        buffer_merge_sort(arr, left, lower_mid, lower_mid)
        merge(arr, left, lower_mid, right, len(arr), upper_mid)
        no_buffer_merge_sort(arr, left, upper_mid)


def in_place_merge_sort(arr):
    mid = ceil(len(arr)/2)
    buffer_merge_sort(arr, mid, len(arr), 0)
    no_buffer_merge_sort(arr, 0, mid)
    i = 1
    while i <len(arr) and arr[i - 1] > arr[i]: #выполнится один раз без влияния на сложность
        arr[i - 1], arr[i] = arr[i], arr[i- 1]
        i+=1


for i in range(100):
    arr = list(range(randint(500, 1000)))
    shuffle(arr)
    in_place_merge_sort(arr)
    assert arr == list(range(len(arr)))


# arr = [2, 1, 3]
# # arr = [4,2,3,1]
# arr = [2, 6, 5, 0, 8, 3, 4, 7, 1]
# arr = [7, 6, 0, 3, 2, 5, 1]
# arr = [12, 6, 14, 0, 11, 5, 9, 10, 1, 2, 15, 8, 7, 3, 13, 4]
# print(arr, len(arr))
# in_place_merge_sort(arr)
# print(arr, len(arr))
