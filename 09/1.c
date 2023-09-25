#include <stdio.h>

void concat(int* arr1, size_t len1, int* arr2, size_t len2, int* out_arr, size_t* out_len) {
    *out_len = len1 + len2;
    for (int i = 0; i < len1; i++) out_arr[i] = arr1[i];
    for (int i = 0; i < len2; i++) out_arr[len1 + i] = arr2[i];
}

int main() {
    size_t len1, len2;
    scanf("%lld", &len1);
    int arr1[len1];
    for (size_t i = 0; i < len1; i++) scanf("%d", &arr1[i]);

    scanf("%lld", &len2);
    int arr2[len2];
    for (size_t i = 0; i < len2; i++) scanf("%d", &arr2[i]);

    size_t out_len;
    int out_arr[len1 + len2];
    concat(arr1, len1, arr2, len2, out_arr, &out_len);
    printf("%d\n", out_len);
    for (size_t i = 0; i < out_len; i++) printf("%d ", out_arr[i]);
    return 0;
}