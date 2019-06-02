d = {'a': {'a1': 3, 'a2': 4}, 'b': {'b1': 5, 'b2': 6}}

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
