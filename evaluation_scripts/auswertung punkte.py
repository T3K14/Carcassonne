import numpy as np

werte1 = [88, 113, 93, 104, 81, 97]

werte2 = [35, 45, 37, 50, 45, 67]

abw1 = []
abw2 = []

while True:
    try:
        a, b = input('Gib hier die Werte ein:\n').split()

        werte1.append(float(a))
        werte2.append(float(b))

    except ValueError:
        break

# Ergebnisse wiedergeben

mittelwert1 = 0
for wert in werte1:
    mittelwert1 += wert
if mittelwert1 != 0:
    mittelwert1 = mittelwert1 / len(werte1)

mittelwert2 = 0
for wert in werte2:
    mittelwert2 += wert
if mittelwert2 != 0:
    mittelwert2 = mittelwert2 / len(werte2)

for wert in werte1:
    abw1.append((wert-mittelwert1)**2)

for wert in werte2:
    abw2.append((wert-mittelwert2)**2)

summe1 = 0
for wert in abw1:
    summe1 += wert

standardabweichung1 = np.sqrt(summe1 / (len(werte1) - 1))

summe2 = 0
for wert in abw2:
    summe2 += wert

standardabweichung2 = np.sqrt(summe2 / (len(werte2) - 1))

print(werte1)
print(werte2)
print('Mittelwerte: ', mittelwert1, mittelwert2)
print('Standardabweichung: ', standardabweichung1, standardabweichung2)
