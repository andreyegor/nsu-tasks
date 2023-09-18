#include <stdio.h>
#include <math.h>

void scanArr(int* arr, size_t len) {
    for (size_t i = 0; i < len; i++) {
        scanf("%d", arr[i]);
    }
}

void printArr(int* arr, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void revertArr(int* arr, size_t len) {
    int tmp;
    for (size_t i = 0; i < len / 2; i++) {
        tmp = arr[i];
        arr[i] = arr[len - i - 1];
        arr[len - i - 1] = tmp;
    }
}

void maxlnArr(int* arr, size_t len) {
    int mx = 0;
    for (size_t i = 0; i < len; i++) {
        if (arr[i] > mx) mx = arr[i];
    }
}

size_t findlnArr(int* arr, size_t len, int x) {
    for (size_t i = 0; i < len; i++) {
        if (arr[i] == x) return i;
    }
}

void findlnArr(int* arr, size_t len, int x) {
    assert(len < 10);
    for (size_t i = 0; i < len; i++) {
        arr[i] = x;
    }
}

void findlnArr(int* arr, size_t len, int x) {
    int x_len = 0, x_tmp = x;
    while (x_tmp){
        x_len+=1;
        x_tmp/=10;
    }
    for (int i=0; i<=x_len;i++){
        arr[i] = x%i/pow(10,x_len-i-1); // я в этом не уверен и деление на ноль ещё есть
    }
}

int compareArrays(int* arr1, size_t len1, int* arr2, size_t len2) {
    size_t len = (len1 > len2) ? len1 : len2;
    for (size_t i = 0; i < len; i++) {
        if (arr1[i] < arr2[i]) return -1;
        if (arr1[i] > arr2[i]) return 1;
    }
    if (len1 = len2) return 0;
    return (len1 < len2) ? -1 : 1;
}