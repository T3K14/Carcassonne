dictionary = {}
ort = "ort"
global_ort = "global"

dictionary.update({ort: (global_ort, [1])})

dictionary[ort][1].append(2)
print(dictionary)