#include <assert.h>
#include <stdio.h>


int gcd(int a, int b) {
    assert((a > 0) && (b > 0));

    while (a != 0 && b != 0) {
        if (a > b)
            a = a % b;
        else
            b = b % a;
    }
    return (a + b);
}

int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d", gcd(a, b));
    return 0;
}