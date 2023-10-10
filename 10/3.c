#include <assert.h>
#include <malloc.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    size_t len;
    size_t capacity;
    char** arr;
} DynArr;

void of_check(void* ptr) {
    if (ptr == NULL) {
        printf("out of memory");
        exit(0);
    }
}

DynArr trim(const char* line) {
    DynArr arr;
    arr.capacity = 1;
    arr.len = 0;
    arr.arr = (char**)malloc(sizeof(char*));
    of_check(arr.arr);

    size_t len = strlen(line) - 1;
    for (size_t i = 0; i < len; i++) {
        if (line[i] != ' ') {
            size_t word_len = 0;
            for (; line[i + word_len] != ' ' && i + word_len < len; word_len++) {
            }
            char* word = (char*)malloc((word_len + 1) * sizeof(char));
            of_check(word);
            for (size_t j = 0; j <= word_len; j++) {
                word[j] = line[j + i];
            }
            word[word_len+1] = '\0';
            arr.arr[arr.len] = word;
            arr.len += 1;
            if (arr.len == arr.capacity) {
                arr.capacity *= 2;
                arr.arr = (char**)realloc(arr.arr, arr.capacity * sizeof(char*));
                of_check(arr.arr);
            }
            i += word_len;
        }
    }

    return arr;
}

int main() {
    char line[128];

    scanf("%[^\n]", line);
    DynArr arr = trim(line);
    for (size_t i = 0; i < arr.len; i++) {
        printf("%s\n", arr.arr[i]);
        free(arr.arr[i]);
    }
    free(arr.arr);
    return 0;
}
