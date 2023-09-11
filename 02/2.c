#include <stdio.h>

int main(){
    unsigned short year;
    scanf("%hi", &year);
    if (year%4==0) printf("Високосный"); else printf("Невисокосный");
    return 0;
}