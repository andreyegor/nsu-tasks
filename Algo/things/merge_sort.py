from random import shuffle, randint


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


for i in range(100):
    arr = list(range(randint(500,1000)))
    shuffle(arr)
    merge_sort(arr)
    assert arr==list(range(len(arr)))
