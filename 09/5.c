#include <stdio.h> 
#include <malloc.h>
#include <stdlib.h>

int of_check(void* ptr){
    if (ptr==NULL){
        printf("out of memory");
        exit(0);
    }
}

size_t scanArr(int** out_arr, size_t *out_capacity){
    size_t capacity = 1;
    int* arr = (int*) malloc(capacity*sizeof(int)); //malloc
    of_check(arr);
    int inp;
    for(size_t i=0;;i++){
        scanf("%d", &inp);
        if (inp == 0){
            *out_arr = arr;
            *out_capacity = capacity;
            return i;
            }
        if (i==capacity){
            capacity*=2;
            arr = (int*) realloc(arr, capacity*sizeof(int));
            of_check(arr);
        }
        arr[i]=inp;

     }
}

int main(){
    int* arr;
    size_t capacity;
    size_t len = scanArr(&arr, &capacity);
    printf("%d %d\n", len, capacity);
    for (size_t i = 0; i < len; i++) printf("%d ", arr[i]);
    free(arr);
    
    return 0;
}