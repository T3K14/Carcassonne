"""d = {'a': {'a1': 3, 'a2': 4}, 'b': {'b1': 5, 'b2': 6}}

print([k for lak in d for k in d[lak]])

class P:
    def __init__(self, pkt):
        self.punkte = pkt


p1 = P(4)
p2 = P(5)

d2 = {p1: p2, p2: p1}

winner = max(list(d2), key=lambda x: x.punkte)
print(winner.punkte)


#spiel = Spiel(card_list, start=True)

import numpy

a = numpy.array([1, 2, 3])
print(a)

b = [1, 2, 3]
print(b.__len__())

c = {None: 1, None: 4}
print(c[None])

from Wiese import WieseAufKarte

a = WieseAufKarte([1], 2)
b = type(a)
print(b)
print(type(a))

liste = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

a = filter(lambda x: x/2 in (1,2,3,4,5,6), liste)
print(list(a))


d = {}

if d:
    print("not d")

k = []
print(k[:-1]
"""
from rotate2 import rotate_info_right

infos = [1, 2, 3, 4]
rotations = 2


print(liste)