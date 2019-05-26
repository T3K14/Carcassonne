d = {'a': {'a1': 3, 'a2': 4}, 'b': {'b1': 5, 'b2': 6}}

print([k for lak in d for k in d[lak]])