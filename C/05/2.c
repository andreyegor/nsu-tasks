#include <stdio.h>

void evil_scanf(int* p0, int* p1, int* p2) {
    int n0, n1, n2;
    scanf("%d %d %d", &n0, &n1, &n2);
    if (n0 > 0) {
        *p1 = n1;
        *p2 = n2;
    } else {
        *p2 = n0 * n1 * n2 * (*p1) * (*p2);
        *p1 = *p0;
    }
    *p0 = n0;
}

int main() {
    int p0=1, p1=1, p2=1;
    evil_scanf(&p0, &p1, &p2);
    printf("%d %d %d", p0, p1,p2);
    return 0;
}