def sum(a, b):
    return a + b


print(sum.__code__.co_varnames)


def specialize(f, *spec_args, **spec_kwargs):
    """В этой реализации можно переопределять аргументы как угодно, а ещё менять переопределённые значения итоговой функции"""

    spec_kwargs.update(**dict(zip(f.__code__.co_varnames, spec_args)))

    def spec_f(*args, **kwargs):
        spec_kwargs.update(kwargs)
        spec_kwargs.update(**dict(zip(
        filter(lambda x: x not in spec_kwargs,f.__code__.co_varnames), args)))
        return f(**spec_kwargs)

    return spec_f

# в первой реализации нельзя сделать во так
plus_one = specialize(sum, 1, a=1)
print(plus_one(10))
# и вот так
print(plus_one(10, a=5))

just_two = specialize(sum, 1, 1)
print(just_two())
