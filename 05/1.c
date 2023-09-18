# include <stdio.h>

int main() {
    int a=0;
    for(;a<100;a++);
    int b;
    printf("%lld %lld", &a, &b);
    return 0;
}