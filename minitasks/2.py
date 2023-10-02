def my_zip(a, b):
    return ((a[i], b[i]) for i in range(min(len(a), len(b)))) #сразу ленивая функция, возвращаю генератор

print(list(my_zip([1,2,3], ['1','2','3'])))