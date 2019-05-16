a = {0: "A", 1: "B", 2: "C", 3: "D"}

b = a.copy()

b[3] = 4

print(a)


def rot(a):
    d = {}
    for i in a:
        if i == 0:
            d.update({i: a[3]})
        else:
            d.update({i: a[i-1]})

    return d

print(rot(a))
for i in a:

    print(i)

from card_class import Card

card0 = Card("S", "O", "S", "W")
card1 = Card("S", "S", "W", "W")
card2 = Card("O", "O", "O", "O", "O", True)
card3 = Card("W", "O", "O", "W")
card4 = Card("W", "O", "W", "O")
card_new = Card("O", "S", "S", "O", "O", True)

print(card4.matrix)
print(card_new.matrix)