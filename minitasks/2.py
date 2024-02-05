def my_zip(a, b):
    # сразу ленивая функция, возвращаю генератор
    return ((a[i], b[i]) for i in range(min(len(a), len(b))))


print(list(my_zip([1, 2, 3], ["a", "b"])))
