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

    int* out = findSubArr(arr1, len1, arr2, len2);
    if (out!=NULL) for (size_t i = 0; i <len2; i++) printf("%d ", out[i]);
    else printf("not found");
    return 0;
}