#include <assert.h>
#include <math.h>
#include <stdio.h>

int is_prime(unsigned long long n) {
    assert(n > 1);
    unsigned long r = ceil(sqrt(n));
    for (unsigned long int i = 2; i < r; i++) {
        if (n % i == 0) {
            return 0;
        }
    }
    return 1;
}

int main() {
    unsigned long long n;
    scanf("%lld", &n);
    if (n < 2) {
        printf("n should be > 1");
        return 0;
    }
    for (long long int i = 0; i < n; i++) {
        if (is_prime(i)) {
            printf("%lld", i);
        }
    }

    return 0;
}