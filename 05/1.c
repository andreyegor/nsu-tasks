# include <stdio.h>

int main() {
    // при каждом запуске адрес уникален, а значит они непредсказуемы
    int a;
    printf("%p\n", &a);
    return 0;
}