from itertools import permutations
from string import ascii_lowercase, ascii_uppercase
from random import randint, choice


# letters = [
#     ascii_uppercase[i // 2] if i % 2 else ascii_lowercase[i // 2]
#     for i in range(len(ascii_lowercase)*2)
# ]

letters = ascii_uppercase+ascii_lowercase

def lsd_radix_sort(arr: list[str]):
    things = {key: [] for key in letters}
    ln = len(arr[0])
    for i in range(ln - 1, -1, -1):
        for e in arr:
            things[e[i]].append(e)

        arr.clear()
        for e in letters:
            for q in things[e]:
                arr.append(q)
            things[e].clear()

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

        if right-left-1:
            mid = (left+right)//2
            merge_sort(arr, left, mid)
            merge_sort(arr, mid, right)
            merge(arr, left, mid, right)
    
    merge_sort(arr)
        

for i in range(100):
    ln = randint(1, 100)
    cnt = randint(1, 100)
    in_arr = ["".join(choice(letters) for i in range(ln)) for i in range(cnt)]
    that_arr = in_arr.copy()
    other_arr = in_arr.copy()
    in_arr.sort()
    lsd_radix_sort(that_arr)
    not_lsd_radix_sort(other_arr)
    assert that_arr == other_arr and that_arr == in_arr