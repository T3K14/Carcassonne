"""import time

def f(tuple):
    x, y = tuple[0], tuple[1]

    for i in range(10):
        a, b = x, y

def f2(tuple):
    for i in range(10):
        a, b = tuple[0], tuple[1]


uple = (1, 2)
t = time.time()
f(uple)

print(time.time()- t)
t = time.time()
f2(uple)

print(time.time()- t)"
""
a = "kloster_1"

print("kloster" in a)
if "kloster" in None:
    print("j")
"""

tuples = ((1, 2), (2, 3), (1, 4))

a = map(lambda x: x[0]+x[1], tuples)
for i in a:
    print(i)