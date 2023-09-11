#include <stdio.h>

int main() {
    unsigned long long n;
    scanf("%lld", &n);
    if (n < 2) {
        printf("Число должно быть больше 1");
        return 0;
    }
    n++;
    unsigned long long m[n];
    for (unsigned long long i = 0; i < n; i++) m[i] = 1;
    m[0] = 0;
    m[1] = 0;

    for (unsigned long long i = 0; i < n; i++) {
        if (m[i] == 0) continue;
        printf("%lld ", i);
        for (unsigned long long j = i * 2; j < n; j += i) {
            m[j] = 0;
        }
    }
    return 0;
}