#include <stdio.h>

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
    for (size_t i = 0; i<len/2; i++){
        tmp = arr[i];
        arr[i] = arr[len-i-1];
        arr[len-i-1] = tmp;
    } 
}

void maxlnArr(int* arr, size_t len){
    int mx = 0;
    for (size_t i = 0; i<len; i++){
        if arr[i]>mx mx = arr[i];
        
    }
}