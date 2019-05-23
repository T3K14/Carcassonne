from Ort import Ort
a = Ort((1, 2), [2])
a.besitzer = 1
l = [a, Ort((3, 4), [1, 2])]

b = [x.besitzer for x in l if x.besitzer is not None]
print(b)