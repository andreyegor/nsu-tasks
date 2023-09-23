#include "stdio.h"
#include <malloc.h>
size_t cnt = 2027;
int not_main(){
    void *a = alloca(1);
    for (;a!=NULL;cnt++){
        void *a = alloca(cnt);
        printf("%d\n", cnt);
    }
    return 0;
}


int main(){
    int cnt;
    for(ptrdiff_t a=1; a; a<<=1) cnt++;
    printf("%d", cnt);
    return 0;
}