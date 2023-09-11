#include <stdio.h>

int main() {
    unsigned long n;
    scanf("%ld", &n);
    for (unsigned long i = 0; i < n * n; i++) {
        printf("%3ld", i);
        if ((i + 1) % n == 0)
            printf("\n");
        else
            printf(" ");
    }
    return 0;
}