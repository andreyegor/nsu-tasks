#include <stdio.h>

int main(){
    unsigned int n;
    scanf("%d", &n);
    if (n%3==0) printf("fizz ");
    if (n%5==0) printf("buzz ");
    return 0;
}