#include "stdio.h"
#include <malloc.h>
void foo(ptrdiff_t t){
    if (alloca(t)==NULL){
        printf("aaaaaaaaaa");
    }
}

int main(){
    for (ptrdiff_t t = 1024;1;t+=1024){
        foo(t);
        if (t%1024==0){
            printf("%lld\n", t);
        }
    }
    return 0;
}



// int main(){
//     int cnt;
//     for(ptrdiff_t a=1; a; a<<=1) cnt++;
//     printf("%d", cnt);
//     return 0;
// }