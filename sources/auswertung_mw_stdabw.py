import numpy as np

# meeples
Orte1 = [2, 3, 3, 1, 3, 2, 3, 2, 3, 3, 2, 4]
Strassen1 = [2, 4, 2, 2, 3, 3, 2, 1, 4, 2, 2, 2]
Wiesen1 = [1, 1, 2, 3, 1, 0, 3, 3, 1, 1, 0, 0]
Kloester1 = [2, 0, 1, 1, 0, 2, 0, 1, 0, 2, 2, 2]

Orte2 = [4, 2, 2, 3, 3, 3, 2, 3, 2, 3, 3, 3]
Strassen2 = [3, 1, 3, 3, 1, 1, 2, 2, 2, 3, 2, 3]
Wiesen2 = [1, 3, 1, 1, 2, 3, 2, 2, 2, 2, 3, 2]
Kloester2 = [0, 2, 1, 1, 2, 0, 2, 1, 2, 0, 0, 0]


# gebietspunkte
Orte1_punkte = [6, 6, 17, 5, 9, 6, 13, 12, 12, 8, 5, 10]
Strassen1_punkte = [3, 9, 4, 6, 9, 9, 4, 2, 9, 4, 8, 4]
Wiesen1_punkte = [3, 3, 6, 6, 6, 0, 18, 12, 6, 3, 0, 0]
Kloester1_punkte = [14, 0, 4, 4, 0, 12, 0, 8, 0, 12, 14, 11]

Orte2_punkte = [11, 8, 2, 9, 10, 12, 7, 12, 7, 10, 10, 10]
Strassen2_punkte = [11, 2, 8, 6, 2, 3, 6, 5, 5, 9, 3, 8]
Wiesen2_punkte = [3, 6, 0, 3, 9, 9, 12, 9, 9, 3, 15, 6]
Kloester2_punkte = [0, 12, 8, 7, 11, 0, 10, 7, 10, 0, 0, 0]

# gesamtpunkte
Player1_ergebnisse = [26, 18, 31, 21, 24, 27, 35, 34, 27, 27, 27, 25]
Player2_ergebnisse = [25, 28, 18, 25, 32, 24, 35, 33, 31, 22, 28, 24]


def calculate_mittelwert(liste):
    mittelwert1 = 0
    for wert in liste:
        mittelwert1 += wert

    if mittelwert1 != 0:
        return mittelwert1 / len(liste)
    else:
        return None


def calculate_standardabweichung(liste, mittelwert):
    abw = []
    for wert in liste:
        abw.append((wert-mittelwert)**2)

    summe = 0
    for wert in abw:
        summe += wert

    return np.sqrt(summe / (len(liste) - 1))

print(f'\nPlayer 1 hat durchschnittlich {calculate_mittelwert(Player1_ergebnisse)} +- {calculate_standardabweichung(Player1_ergebnisse, calculate_mittelwert(Player1_ergebnisse))}, Player2 {calculate_mittelwert(Player2_ergebnisse)} +- {calculate_standardabweichung(Player2_ergebnisse, calculate_mittelwert(Player2_ergebnisse))}.\n')


print('durchschnittlich auf Gebiete gesetzt Meeples:')
print('Player1:')
print('Orte: erste Hälfte: ', calculate_mittelwert(Orte1[:int(len(Orte1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Orte1[int(len(Orte1)/2):]), ', gesamt:', calculate_mittelwert(Orte1), '+-', calculate_standardabweichung(Orte1, calculate_mittelwert(Orte1)))
print('Strassen: erste Hälfte: ', calculate_mittelwert(Strassen1[:int(len(Strassen1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Strassen1[int(len(Strassen1)/2):]), ', gesamt:', calculate_mittelwert(Strassen1), '+-', calculate_standardabweichung(Strassen1, calculate_mittelwert(Strassen1)))
print('Wiesen: erste Hälfte: ', calculate_mittelwert(Wiesen1[:int(len(Wiesen1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Wiesen1[int(len(Wiesen1)/2):]), ', gesamt:', calculate_mittelwert(Wiesen1), '+-', calculate_standardabweichung(Wiesen1, calculate_mittelwert(Wiesen1)))
print('Kloester: erste Hälfte: ', calculate_mittelwert(Kloester1[:int(len(Kloester1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Kloester1[int(len(Kloester1)/2):]), ', gesamt:', calculate_mittelwert(Kloester1), '+-', calculate_standardabweichung(Kloester1, calculate_mittelwert(Kloester1)))


print('\n\nPlayer2:')
print('Orte: erste Hälfte: ', calculate_mittelwert(Orte2[:int(len(Orte2)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Orte2[int(len(Orte2)/2):]), ', gesamt:', calculate_mittelwert(Orte2), '+-', calculate_standardabweichung(Orte2, calculate_mittelwert(Orte2)))
print('Strassen: erste Hälfte: ', calculate_mittelwert(Strassen2[:int(len(Strassen2)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Strassen2[int(len(Strassen2)/2):]), ', gesamt:', calculate_mittelwert(Strassen2), '+-', calculate_standardabweichung(Strassen2, calculate_mittelwert(Strassen2)))
print('Wiesen: erste Hälfte: ', calculate_mittelwert(Wiesen2[:int(len(Wiesen2)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Wiesen2[int(len(Wiesen2)/2):]), ', gesamt:', calculate_mittelwert(Wiesen2), '+-', calculate_standardabweichung(Wiesen2, calculate_mittelwert(Wiesen2)))
print('Kloester: erste Hälfte: ', calculate_mittelwert(Kloester2[:int(len(Kloester2)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Kloester2[int(len(Kloester2)/2):]), ', gesamt:', calculate_mittelwert(Kloester2), '+-', calculate_standardabweichung(Kloester2, calculate_mittelwert(Kloester2)))



print('\ndurchschnittlich gemachte Punkte mit den Gebieten:')

print('Player1:')
print('Orte: erste Hälfte: ', calculate_mittelwert(Orte1_punkte[:int(len(Orte1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Orte1_punkte[int(len(Orte1_punkte)/2):]), ', gesamt:', calculate_mittelwert(Orte1_punkte), '+-', calculate_standardabweichung(Orte1_punkte, calculate_mittelwert(Orte1_punkte)))
print('Strassen: erste Hälfte: ', calculate_mittelwert(Strassen1_punkte[:int(len(Strassen1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Strassen1_punkte[int(len(Strassen1_punkte)/2):]), ', gesamt:', calculate_mittelwert(Strassen1_punkte), '+-', calculate_standardabweichung(Strassen1_punkte, calculate_mittelwert(Strassen1_punkte)))
print('Wiesen: erste Hälfte: ', calculate_mittelwert(Wiesen1_punkte[:int(len(Wiesen1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Wiesen1_punkte[int(len(Wiesen1_punkte)/2):]), ', gesamt:', calculate_mittelwert(Wiesen1_punkte), '+-', calculate_standardabweichung(Wiesen1_punkte, calculate_mittelwert(Wiesen1_punkte)))
print('Kloester: erste Hälfte: ', calculate_mittelwert(Kloester1_punkte[:int(len(Kloester1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Kloester1_punkte[int(len(Kloester1_punkte)/2):]), ', gesamt:', calculate_mittelwert(Kloester1_punkte), '+-', calculate_standardabweichung(Kloester1_punkte, calculate_mittelwert(Kloester1_punkte)))


print('Player2:')
print('Orte: erste Hälfte: ', calculate_mittelwert(Orte2_punkte[:int(len(Orte2)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Orte2_punkte[int(len(Orte2_punkte)/2):]), ', gesamt:', calculate_mittelwert(Orte2_punkte), '+-', calculate_standardabweichung(Orte2_punkte, calculate_mittelwert(Orte2_punkte)))
print('Strassen: erste Hälfte: ', calculate_mittelwert(Strassen2_punkte[:int(len(Strassen2)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Strassen2_punkte[int(len(Strassen2_punkte)/2):]), ', gesamt:', calculate_mittelwert(Strassen2_punkte), '+-', calculate_standardabweichung(Strassen2_punkte, calculate_mittelwert(Strassen2_punkte)))
print('Wiesen: erste Hälfte: ', calculate_mittelwert(Wiesen2_punkte[:int(len(Wiesen2)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Wiesen2_punkte[int(len(Wiesen2_punkte)/2):]), ', gesamt:', calculate_mittelwert(Wiesen2_punkte), '+-', calculate_standardabweichung(Wiesen2_punkte, calculate_mittelwert(Wiesen2_punkte)))
print('Kloester: erste Hälfte: ', calculate_mittelwert(Kloester2_punkte[:int(len(Kloester2)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Kloester2_punkte[int(len(Kloester2_punkte)/2):]), ', gesamt:', calculate_mittelwert(Kloester2_punkte), '+-', calculate_standardabweichung(Kloester2_punkte, calculate_mittelwert(Kloester2_punkte)))

