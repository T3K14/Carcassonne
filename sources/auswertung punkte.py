import numpy as np

werte1 = [99.0, 94.0, 55.0, 74.0, 73.0, 52.0, 89.0, 73.0, 73.0, 77.0, 79.0, 63.0, 69.0, 63.0, 51.0, 49.0, 50.0, 70.0, 75.0, 90.0, 56.0, 58.0, 66.0, 35.0, 65.0]


werte2 = [61.0, 99.0, 104.0, 74.0, 96.0, 88.0, 70.0, 85.0, 97.0, 75.0, 76.0, 73.0, 78.0, 57.0, 83.0, 60.0, 79.0, 89.0, 86.0, 58.0, 82.0, 76.0, 61.0, 90.0, 75.0]


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
