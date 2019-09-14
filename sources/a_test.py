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
from card_class import karteninfoliste
import random

#print(karteninfoliste)
#print(random.shuffle(karteninfoliste))

class player:

    def __init__(self):
        self.punkt = 0


def f(p):
    p.punkt += 1

P1 = player()
f(P1)

print(P1.punkt)

import time

start = time.time()
time.sleep(5)
print(time.time()-start)