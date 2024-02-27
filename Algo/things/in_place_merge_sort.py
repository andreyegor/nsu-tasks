from random import shuffle, randint
from math import ceil


from math import ceil
from random import shuffle, randint


def merge(arr: list, s1: int, f1: int, s2: int, f2: int, out: int) -> None:
    l, r, i = s1, s2, out
    if f2 < r:
        return

    while l != f1 and r != f2:
        if arr[l] <= arr[r]:
            arr[i], arr[l] = arr[l], arr[i]
            l += 1
        else:
            arr[i], arr[r] = arr[r], arr[i]
            r += 1
        i += 1

    while l != f1:
        arr[i], arr[l] = arr[l], arr[i]
        l += 1
        i += 1

    while r != f2:  # TODO оптимизировать для некоторых случаев неравномерного слияния
        arr[i], arr[r] = arr[r], arr[i]
        r += 1
        i += 1

    return


def buffer_merge_sort(arr, left, right, buffer_start):
    lower_mid, upper_mid = (left + right) // 2, ceil((left + right) / 2)
    if right - left == 1:
        arr[left], arr[buffer_start] = arr[buffer_start], arr[left]
        return
    buffer_merge_sort(arr, left, lower_mid, upper_mid)
    merge_sort(arr, left, upper_mid)
    merge(arr, left, upper_mid, upper_mid, right, buffer_start)


def merge_sort(arr: list, left=None, right=None) -> None:
    if left == None and right == None:
        left = 0
        right = len(arr)

    if right - left == 1:
        return
    # два mid необходимо для коррктного merge участка нечётной длинны
    lower_mid, upper_mid = (left + right) // 2, ceil((left + right) / 2)

    buffer_merge_sort(arr, left, lower_mid, upper_mid)
    while upper_mid - left != 1:
        local_right = upper_mid
        lower_mid, upper_mid = (left+upper_mid) // 2, ceil((left+upper_mid) / 2)
        buffer_merge_sort(arr, upper_mid, local_right, left)
        merge(arr, left, lower_mid, local_right, right, upper_mid)

    left += 1
    while left < right and arr[left - 1] > arr[left]:
        arr[left - 1], arr[left] = arr[left], arr[left - 1]
        left += 1


for i in range(100):
    arr = list(range(randint(1, 100)))
    shuffle(arr)
    merge_sort(arr)
    assert arr == sorted(arr)


arr = [12, 6, 14, 0, 11, 5, 9, 10, 1, 2, 15, 8, 7, 3, 13, 4]
arr = [7, 6, 0, 3, 2, 5, 1]
# arr = [4,2,3,1]
arr = [0, 2, 1]
print(arr, len(arr))
merge_sort(arr)
print(arr, len(arr))
