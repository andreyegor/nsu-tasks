#include <stdio.h>
#include <string.h>

int palindrom(const char* line) {
    size_t right = strlen(line);

    for (size_t left = 0; left <= right / 2; left++) {
        right--;
        if (line[left] == ' ')
            right++;
        else if (line[right] == ' ')
            left--;
        else if (line[left] != line[right])
            return 0;
    }
    return 1;
}

int main() {
    char line[128];

    scanf("%[^\n]", line);
    printf("%s", palindrom(line) ? "Yes" : "No");
    return 0;
}
