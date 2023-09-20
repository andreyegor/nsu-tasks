# include <stdio.h>
void foo(){
    int a;
    printf("%p\n", &a);
}

void bar(){
    foo();
}

int main() {
    // при вызове функции foo в разные моменты времени адрес локальной переменной a разный
    foo();
    bar();
}