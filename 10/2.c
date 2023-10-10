#include <assert.h>
#include <malloc.h>
#include <stdio.h>
#include <string.h>

int of_check(void* ptr) {
    if (ptr == NULL) {
        printf("out of memory");
        exit(0);
    }
}

char* trim(const char* line) {
    size_t left = 0;
    size_t right = strlen(line)-1;
    for (; line[left] == ' '; left++) {
        if (left == right) {
            char* out = (char*)malloc(sizeof(char));
            of_check(out);
            *out = '\0';
            return out;
        }
    }
    for (; line[right] == ' '; right--) {
    }

    char* out = (char*)malloc((right - left+2) * sizeof(char));
    of_check(out);

    for (size_t i = left; i <= right; i++) 
        out[i - left] = line[i];
    out[right-left+1] = '\0';

    return out;
}

int main() {
    char line[128];

    scanf("%[^\n]", line);
    printf("%s", trim(line));
    return 0;
}
