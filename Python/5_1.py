def sum(a, b):
    return a + b


def specialize(f, *spec_args, **spec_kwargs):
    """Реализация для тестов как на слайде, не сработает если оставить непереопределенные пременные справа"""

    def g(*args, **kwargs):
        return f(*spec_args, *args, **spec_kwargs, **kwargs)

    return g


plus_one = specialize(sum, b=1)
print(plus_one(10))

just_two = specialize(sum, 1, 1)
print(just_two())
