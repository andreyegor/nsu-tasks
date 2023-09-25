#include <stdio.h>

int main(){
    int m[4][4];
    for (size_t i=0; i<4; i++){
        for (size_t j=0; j<4; j++){
            scanf("%d", &m[i][j]);

        }
    }

    for (size_t i=0; i<4; i++){
        for (size_t j=i; j<4; j++){
            int tmp = m[j][i];
            m[j][i] = m[i][j];
            m[i][j] = tmp;

        }
    }

    for (int i=0; i<4; i++){
        for (int j=0; j<4; j++){
            printf("%d ", m[i][j]);
        }
        printf("\n");
    }
}