#include <assert.h>
#include <malloc.h>
#include <setjmp.h>
#include <stdio.h>
#include <string.h>

#include <cmath>

void of_check(void* ptr) {
    if (ptr == NULL) {
        printf("out of memory");
        exit(0);
    }
}

void exeption(jmp_buf buf, const char* message) {
    if (buf != NULL) {
        longjmp(buf, 1);
    } else {
        printf("%s", message);
        exit(0);
    }
}

unsigned int my_pow(unsigned int a, unsigned int b,unsigned int limit, jmp_buf buf){
    unsigned int out = 1;
    for(int i=0; i<b; i++){
        if (out*a>limit){
            exeption(buf, "overflow");
        }
        out*=a;
    }
    return out;
}
signed int s2i(const char* line, int base, jmp_buf buf) {
    const char alphabet[17] = "0123456789ABCDEF";

    int len = strlen(line);
    signed int sign = 1;
    if (line[0] == '-') {
        sign = -1;
        len--;
    }
    unsigned int limit = sign > 0 ? 0 : 1;
    for (int i = 0; i < (sizeof(int) * 8) - 1; i++) limit += (1 << i);

    unsigned int n = 0;
    for (int i = sign > 0 ? 0 : 1; i < len; i++) {
        for (int j = 0; j <= base; j++) {
            if (line[i] == alphabet[j]) {
                unsigned int k = my_pow(base, len - i - 1, limit, buf) * j;  // нужна своя реализация pow
                n += k;
                if (n > limit) {
                    exeption(buf, "overflow");
                }
                break;
            }
            if (j == base) {
                exeption(buf, "wrong alphabet");
            }
        }
    }
    signed int out = n * sign;
    return out;
}

int main() {
    char line[128];
    int base;
    scanf("%s", line);
    scanf("%d", &base);
    printf("%d", s2i(line, base, NULL));
    return 0;
}
