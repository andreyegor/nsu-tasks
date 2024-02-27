from itertools import permutations
from string import ascii_lowercase, ascii_uppercase
from random import randint, choice


# letters = [
#     ascii_uppercase[i // 2] if i % 2 else ascii_lowercase[i // 2]
#     for i in range(len(ascii_lowercase)*2)
# ]

letters = ascii_uppercase + ascii_lowercase


def count_sort(arr, k):
    things = [0] * (ord(ascii_lowercase[-1]) - 63)
    out = [None] * len(arr)
    for e in arr:
        things[ord(e[k]) - 64] += 1

    places = [0] * (ord(ascii_lowercase[-1]) - 63)
    place = 0
    for i in range(len(things)):
        places[i] = place
        place += things[i]

    for e in arr:
        out[places[ord(e[k]) - 64]] = e
        places[ord(e[k]) - 64] += 1
    return out


def lsd_radix_sort(arr: list[str]):
    for i in range(len(arr[0]) - 1, -1, -1):
        arr = count_sort(arr, i)
    return arr


def not_lsd_radix_sort(arr):
    def merge(arr, left, mid, right):
        left_arr = arr[left:mid]
        right_arr = arr[mid:right]
        l, r, i = 0, 0, left

        while l != len(left_arr) and r != len(right_arr):
            if left_arr[l] <= right_arr[r]:
                arr[i] = left_arr[l]
                l += 1
            else:
                arr[i] = right_arr[r]
                r += 1
            i += 1

        while l != len(left_arr):
            arr[i] = left_arr[l]
            l += 1
            i += 1

        while r != len(right_arr):
            arr[i] = right_arr[r]
            r += 1
            i += 1

    def merge_sort(arr, left=None, right=None):
        if left == None and right == None:
            left = 0
            right = len(arr)

        if right - left - 1:
            mid = (left + right) // 2
            merge_sort(arr, left, mid)
            merge_sort(arr, mid, right)
            merge(arr, left, mid, right)

    merge_sort(arr)


for i in range(100):
    ln = randint(1, 100)
    cnt = randint(1, 100)
    in_arr = ["".join(choice(letters) for i in range(ln)) for i in range(cnt)]

    radix_arr = lsd_radix_sort(in_arr)
    that_arr = sorted(in_arr)
    other_arr = in_arr.copy()
    not_lsd_radix_sort(other_arr)
    assert radix_arr == other_arr and that_arr == radix_arr
