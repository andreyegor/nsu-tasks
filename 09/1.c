#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>

int of_check(void* ptr){
    if (ptr==NULL){
        printf("out of memory");
        exit(0);
    }
}

size_t concat(int* arr1, size_t len1, int* arr2, size_t len2, int** out_arr) {
    int* arr = (int*) malloc((len1+len2)*sizeof(int));
    of_check(arr);
    for (int i = 0; i < len1+len2; i++){
        int n = (i<len1) ? n=arr1[i] : arr2[i-len1];
        arr[i] = n;
    }
    *out_arr = arr;
    return len1+len2;
}

int main() {
    size_t len1, len2;
    scanf("%lld", &len1);
    int *arr1 = (int*) malloc(len1*sizeof(int));
    of_check(arr1);
    for (size_t i = 0; i < len1; i++) scanf("%d", &arr1[i]);

    scanf("%lld", &len2);
    int *arr2 = (int*) malloc(len2*sizeof(int));
    of_check(arr2);
    for (size_t i = 0; i < len2; i++) scanf("%d", &arr2[i]);

    int *out_arr;
    size_t out_len = concat(arr1, len1, arr2, len2, &out_arr);
    printf("%d\n", out_len);
    for (size_t i = 0; i < out_len; i++) printf("%d ", out_arr[i]);

    free(arr1);
    free(arr2);
    free(out_arr);
    
    return 0;
}