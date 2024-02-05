#include <stdio.h>

int main() {
    unsigned int n;
    scanf("%d", &n);
    for (unsigned int i = 0; i <= n; i++) {
        if (i % 3 != 0 && i % 5 != 0) {
            printf("%d ", i);
            continue;
        }
        if (i % 3 == 0) printf("fizz ");
        if (i % 5 == 0) printf("buzz ");
    }
    return 0;
}