#include <stdio.h>
signed int a,b;
int main(){
    scanf("%d %d", &a, &b);
    printf("+ %d \n ", a+b);
    printf("- %d \n", a-b);
    printf("* %d \n", a*b);
    if (b!=0){
        printf("/ %d \n", a/b);
        printf("%% %d \n", a%b);
    } else{
        printf("я не умею делить на 0 :(\n");
    }
    printf("> %d \n", a>b);
    printf("< %d \n", a<b);
    printf("== %d \n", a==b);
    printf("!= %d \n", a==b);
    printf("- %d \n", a-b);
    printf("&& %d \n", a&&b);
    printf("|| %d \n", a||b);
    printf("!a %d \n", a);
    printf("& %d \n", a&b);
    printf("| %d \n", a|b);
    printf("^ %d \n", a^b);
    printf("!a %d \n", a);
    a = (1<<31)-1;
    printf(" переполнение %d %d", a, a+1);
    printf("a/0 %d \n", a/0); //Arithmetic exception  
    return 0;
}