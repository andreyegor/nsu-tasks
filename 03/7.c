#include <stdio.h>

int main() {
    unsigned int n;
    unsigned int  ypos = 0, xpos = 0;
    unsigned long cnt = 0;
    unsigned char in;

    scanf("%d", &n);
    if (n < 2) {
        printf("ерор: слишком маленькое значение");
        return 0;
    }

    // условие находится внутри блока
    while (1) {
        for (int i = 0; i < n + 1; i++) printf("--");
        printf("\n");
        for (int i = 0; i < n; i++) {
            printf("|");
            for (int j = 0; j < n; j++) {
                if (i == ypos && j == xpos)
                    printf("🙂");
                else
                    printf("  ");
            }
            printf("|\n");
        }
        for (int i = 0; i < n + 1; i++) printf("--");
        printf("\n");

        if (ypos == n - 1 && xpos == n - 1) break;

        printf("Счёт:%ld Команда:", cnt);
        scanf(" %c", &in);
        if (in == '8' && ypos != 0)
            ypos--;
        else if (in == '4' && xpos != 0)
            xpos--;
        else if (in == '5' && ypos != n-1)
            ypos++;
        else if (in == '6' && xpos != n-1)
            xpos++;
        else{
            printf("Недопустимое значение!\n");
            continue;
        }
        cnt++;
    }
    printf("Победа со счётом %ld!", cnt);
    return 0;
}