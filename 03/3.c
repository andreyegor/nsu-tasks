#include <stdio.h>

int main() {
    unsigned long n, cnt = 2, limit = 0;
    scanf("%ld", &n);
    for (unsigned long i = 0; i <= (n * (n + 1)) / 2 - 1; i++) {
        printf("%3ld ", i);
        if (i == limit) {
            printf("\n");
            limit = i + cnt;
            cnt++;
        }
    }
    return 0;
}