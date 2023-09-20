# include <stdio.h>
void foo(){
    int a;
    printf("%p\n", &a);
}

void bar(){
    foo();
}

int main() {
    foo();
    bar();
}