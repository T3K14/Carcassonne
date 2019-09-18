
def f(x, y=2):
    #print(x + y)
    return x, y

f(1)

def g(y):
    def decorator(func):
        def func_wrapper(x):
            return func(x, y)
        return func_wrapper
    return decorator


f = g(3)(f)

a, b = f(1)
print(a, b)