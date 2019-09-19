import time

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
#print(a, b)



def time_helper(bool, t):
    """
    for calculating the current iteration, or the current time to determine if the algorithm is allowed to calculate
    another iteration
    :param bool: True: return t, False: return current time
    :param t: the current number of iterations
    :return: the relative already used time

    if bool == True: the algorithm works with iterations and the current iteration is returned
    else: The algorithm works with a time limit and the current time is returned

    """
    if bool:
        return t
    else:
        return time.time()

print(time.time(), time.time() + 3)

boole = True
step = time.time() if boole else 0

ende = time.time() +3

while time_helper(False, 3) < ende:
    print("noch ok")


