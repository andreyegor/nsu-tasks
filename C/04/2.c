#include <assert.h>
#include <stdio.h>

int dvs_cnt(unsigned int n) {
    assert(n != 0);
    unsigned int cnt = 1;
    for (int i = 2; i <= n; i++) {
        if (n % i == 0) cnt++;
    }
    return cnt;
}

int main() {
    int n;
    scanf("%d", &n);
    printf("%d", dvs_cnt(n));
    return 0;
}