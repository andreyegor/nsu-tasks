#include <stdio.h> 
#include <math.h>

int main(){
    unsigned long long n, r;
    scanf("%lld", &n);
    if (n<2){
        printf("Число должно быть больше 1");
        return 0;
    }
    r = ceil(sqrt(n));
    for(unsigned long long int i = 2; i<r; i++){ //заменить на sqrt
        if (n%i==0){
            printf("Непростое");
            return 0;
        }
    }
    printf("Простое");
    return 0;
}