def sum(a, b):
    return a + b

def specialize(f, *spec_args, **spec_kwargs):
    """В этой реализации можно переопределять аргументы как угодно, а ещё менять переопределённые значения итоговой функции"""

    spec_kwargs.update(**dict(zip(f.__code__.co_varnames, spec_args)))
    
    # альтернативная версия альтернативной реализации, и я без понятия как будет лучше - при работе с f(a,b) 
    # код ниже разберёт specialize(f,1,a=2) как а=2 b=1, тогда как код выше разберёт те же данные как a=1
    # spec_kwargs.update(**dict(zip(
    # filter(lambda x: x not in spec_kwargs,f.__code__.co_varnames), spec_args)))

    def spec_f(*args, **kwargs):
        default_kwargs = spec_kwargs.copy()
        default_kwargs.update(kwargs)
        if len(args)+len(default_kwargs) != len(f.__code__.co_varnames):
            raise TypeError(f"Количество запрошенных и полученных аргументов не совпадает")
        
        default_kwargs.update(**dict(zip(
        filter(lambda x: x not in default_kwargs,f.__code__.co_varnames), args)))
        return f(**default_kwargs)

    return spec_f

# в первой реализации нельзя сделать во так
plus_one = specialize(sum, a=1)
print(plus_one(10))
# и вот так
print(plus_one(10, a=5))

just_two = specialize(sum, 1, 1)
print(just_two())
