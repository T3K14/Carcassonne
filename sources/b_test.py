d = {'a': 1, 'b': 3, 'c': 2, 'd': 3}

print(d.items())
p = max(d, key=lambda k: d[k])