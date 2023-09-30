#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>

int of_check(void* ptr){
    if (ptr==NULL){
        printf("out of memory");
        exit(0);
    }
}

int* findSubArr(int* arr1, size_t len1, int* arr2, size_t len2) {
    for (int i = 0; i < len1; i++) {
        for (int j = 0; j < len2; j++){
            if (arr1[i+j] != arr2[j]) break;
            if (j==len2-1) return &arr1[i];
        }
    }
    return NULL;
}

int removeSubArr(int* arr1, size_t len1, int* arr2, size_t len2){
    int* subarr;
    while ((subarr = findSubArr(arr1, len1, arr2, len2))!=NULL){
        len1-=len2;
        for (size_t i =0; i<len1; i++){
            subarr[i] = subarr[i+len2];
        }
    }
    arr1 = (int*) realloc(arr1, len1*sizeof(int));
    of_check(arr1);
    return len1;
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

    len1 = removeSubArr(arr1, len1, arr2, len2);
    for (size_t i = 0; i <len1; i++) printf("%d ", arr1[i]);
    free(arr1);
    free(arr2);
    
    return 0;
}