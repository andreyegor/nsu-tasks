#include <math.h>
#include <stdio.h>

void scanArr(int* arr, size_t len) {
    for (size_t i = 0; i < len; i++) {
        scanf("%d", &arr[i]);
    }
}

void printArr(int* arr, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void revertArr(int* arr, size_t len) {
    int tmp;
    for (size_t i = 0; i < len / 2; i++) {
        tmp = arr[i];
        arr[i] = arr[len - i - 1];
        arr[len - i - 1] = tmp;
    }
}

int maxlnArr(int* arr, size_t len) {
    int mx = 0;
    for (size_t i = 0; i < len; i++) {
        if (arr[i] > mx) mx = arr[i];
    }
    return mx;
}

size_t findlnArr(int* arr, size_t len, int x) {
    for (size_t i = 0; i < len; i++) {
        if (arr[i] == x) return i;
    }
    return -1;
}

void extractDigits(int* arr, size_t len, int x) {
    int x_len = -1, x_tmp = x;
    while (x_tmp) {
        x_len += 1;
        x_tmp /= 10;
    }
    if (x_len == -1) x_len = 0;
    for (int i = x_len; i >= 0; i--) {
        arr[i] = x % 10;
        x /= 10;
    }
}

int compareArrays(int* arr1, size_t len1, int* arr2, size_t len2) {
    size_t len = (len1 < len2) ? len1 : len2;
    for (size_t i = 0; i < len; i++) {
        if (arr1[i] < arr2[i]) return -1;
        if (arr1[i] > arr2[i]) return 1;
    }
    if (len1 == len2) return 0;
    return (len1 > len2) ? 1 : -1;
}

int main() {
    char del40[] = "--------------------------------------\n";

    // scanArr
    printf("%s>scanArr\n", del40);

    int len;
    printf("enter your array length: ");
    scanf("%d", &len);
    int arr[len];
    printf("enter your array: ");
    scanArr(arr, len);
    printf("your array: ");
    printArr(arr, len);

    // revertArr
    printf("%s>revertArr\n", del40);

    revertArr(arr, len);
    printf("your reverse array: ");
    printArr(arr, len);
    revertArr(arr, len);

    // maxlnArr
    printf("%s>maxlnArr\n", del40);
    printf("maximum from the array: %d\n", maxlnArr(arr, len));

    // findlnArr
    printf("%s>findlnArr\n", del40);

    int el, out;
    printf("enter element to find: ");
    scanf("%d", &el);
    out = findlnArr(arr, len, el);
    if (out == -1)
        printf("element not found\n");
    else
        printf("%d is on %d position in array\n", el, out);

    // extractDigits
    printf("%s>extractDigits\n", del40);

    if (len < 0)
        printf("array is too small for extractDigits function\n");
    else {
        int digits;
        int arr_copy[len];
        for (size_t i = 0; i < len; i++) arr_copy[i] = arr[i];
        printf("enter your digits: ");
        scanf("%d", &digits);
        extractDigits(arr_copy, len, digits);
        printf("Array with %d extracted:", digits);
        printArr(arr_copy, len);
    }

    // compareArrays
    printf("%s>compareArrays\n", del40);
    int len_;
    printf("enter array to compare length: ");
    scanf("%d", &len_);
    int arr_[len_];
    printf("enter array to compare: ");
    scanArr(arr_, len_);
    printf("your first array: ");
    printArr(arr, len);
    printf("your array to compare: ");
    printArr(arr_, len_);

    out = compareArrays(arr, len, arr_, len_);

    if (out == 1)
        printf("first array is greater");
    else if (out == -1)
        printf("second array is greater");
    else
        printf("arrays are equal");

    return 0;
}