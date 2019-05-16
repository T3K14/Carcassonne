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