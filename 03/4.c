#include <stdio.h> 
#include <assert.h>

int main(){
    unsigned long long n;
    scanf("%lld", &n);
    if (n<2){
        printf("Число должно быть больше 1");
        return 0;
    }

    for(unsigned long long int i = 2; i<n; i++){ //заменить на sqrt
        if (n%i==0){
            printf("Непростое");
            return 0;
        }
    }
    printf("Простое");
    return 0;
}