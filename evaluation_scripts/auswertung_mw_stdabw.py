import numpy as np

# meeples
Orte1 = [2, 2, 2, 2, 2, 1, 1, 1, 1, 1]
Strassen1 = [2, 2, 2, 2, 2, 1, 1, 1, 1, 1]
Wiesen1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
Kloester1 = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]

Orte2 = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
Strassen2 = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
Wiesen2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
Kloester2 = [2, 2, 2, 2, 2, 0, 0, 0, 0, 0]


# gebietspunkte
Orte1_punkte = [5, 5, 5, 5, 5, 4, 4, 4, 4, 4]
Strassen1_punkte = [6, 6, 6, 6, 6, 2, 2, 2, 2, 2]
Wiesen1_punkte = [3, 3, 3, 3, 3, 3, 3, 3, 6, 3]
Kloester1_punkte = [0, 0, 0, 0, 0, 10, 10, 11, 11, 11]

Orte2_punkte = [4, 4, 4, 4, 4, 8, 8, 8, 8, 8]
Strassen2_punkte = [3, 4, 3, 3, 4, 5, 5, 6, 6, 6]
Wiesen2_punkte = [3, 3, 3, 3, 3, 6, 6, 6, 6, 6]
Kloester2_punkte = [9, 10, 9, 9, 10, 0, 0, 0, 0, 0]

# gesamtpunkte
Player1_ergebnisse = [14, 14, 14, 14, 14, 19, 19, 20, 23, 20]
Player2_ergebnisse = [19, 21, 19, 19, 21, 19, 19, 20, 20, 20]

gesamtmeeples1 = Orte1[:]
gesamtmeeples2 = Orte2[:]

for i in range(len(Orte1)):
    gesamtmeeples1[i] += Strassen1[i]
    gesamtmeeples1[i] += Wiesen1[i]
    gesamtmeeples1[i] += Kloester1[i]

for i in range(len(Orte2)):
    gesamtmeeples2[i] += Strassen2[i]
    gesamtmeeples2[i] += Wiesen2[i]
    gesamtmeeples2[i] += Kloester2[i]

print(gesamtmeeples2)


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

print('\nPlayer1 hat durchschnittlich folgende Punktezahlen gemacht:')
print(f'Erste Hälfte: {calculate_mittelwert(Player1_ergebnisse[:int(len(Player1_ergebnisse)/2)])} +- {calculate_standardabweichung(Player1_ergebnisse[:int(len(Player1_ergebnisse)/2)], calculate_mittelwert(Player1_ergebnisse[:int(len(Player1_ergebnisse)/2)]))},'
      f'\nzweite Hälfte: {calculate_mittelwert(Player1_ergebnisse[int(len(Player1_ergebnisse)/2):])} +- {calculate_standardabweichung(Player1_ergebnisse[int(len(Player1_ergebnisse)/2):], calculate_mittelwert(Player1_ergebnisse[int(len(Player1_ergebnisse)/2):]))},'
      f'\ngesamt: {calculate_mittelwert(Player1_ergebnisse)} +- {calculate_standardabweichung(Player1_ergebnisse, calculate_mittelwert(Player1_ergebnisse))}')

print('\nPlayer2 hat durchschnittlich folgende Punktezahlen gemacht:')
print(f'Erste Hälfte: {calculate_mittelwert(Player2_ergebnisse[:int(len(Player2_ergebnisse)/2)])} +- {calculate_standardabweichung(Player2_ergebnisse[:int(len(Player2_ergebnisse)/2)], calculate_mittelwert(Player2_ergebnisse[:int(len(Player2_ergebnisse)/2)]))},'
      f'\nzweite Hälfte: {calculate_mittelwert(Player2_ergebnisse[int(len(Player2_ergebnisse)/2):])} +- {calculate_standardabweichung(Player2_ergebnisse[int(len(Player2_ergebnisse)/2):], calculate_mittelwert(Player2_ergebnisse[int(len(Player2_ergebnisse)/2):]))},'
      f'\ngesamt: {calculate_mittelwert(Player2_ergebnisse)} +- {calculate_standardabweichung(Player2_ergebnisse, calculate_mittelwert(Player2_ergebnisse))}')



print('\ndurchschnittlich auf Gebiete gesetzt Meeples:')
print('Player1:')
print('Orte: erste Hälfte: ', calculate_mittelwert(Orte1[:int(len(Orte1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Orte1[int(len(Orte1)/2):]), ', gesamt:', calculate_mittelwert(Orte1), '+-', calculate_standardabweichung(Orte1, calculate_mittelwert(Orte1)))
print('Strassen: erste Hälfte: ', calculate_mittelwert(Strassen1[:int(len(Strassen1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Strassen1[int(len(Strassen1)/2):]), ', gesamt:', calculate_mittelwert(Strassen1), '+-', calculate_standardabweichung(Strassen1, calculate_mittelwert(Strassen1)))
print('Wiesen: erste Hälfte: ', calculate_mittelwert(Wiesen1[:int(len(Wiesen1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Wiesen1[int(len(Wiesen1)/2):]), ', gesamt:', calculate_mittelwert(Wiesen1), '+-', calculate_standardabweichung(Wiesen1, calculate_mittelwert(Wiesen1)))
print('Kloester: erste Hälfte: ', calculate_mittelwert(Kloester1[:int(len(Kloester1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Kloester1[int(len(Kloester1)/2):]), ', gesamt:', calculate_mittelwert(Kloester1), '+-', calculate_standardabweichung(Kloester1, calculate_mittelwert(Kloester1)))
print('gesamt: ', calculate_mittelwert(gesamtmeeples1), '+- ', calculate_standardabweichung(gesamtmeeples1, calculate_mittelwert(gesamtmeeples1)))

print('\n\nPlayer2:')
print('Orte: erste Hälfte: ', calculate_mittelwert(Orte2[:int(len(Orte2)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Orte2[int(len(Orte2)/2):]), ', gesamt:', calculate_mittelwert(Orte2), '+-', calculate_standardabweichung(Orte2, calculate_mittelwert(Orte2)))
print('Strassen: erste Hälfte: ', calculate_mittelwert(Strassen2[:int(len(Strassen2)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Strassen2[int(len(Strassen2)/2):]), ', gesamt:', calculate_mittelwert(Strassen2), '+-', calculate_standardabweichung(Strassen2, calculate_mittelwert(Strassen2)))
print('Wiesen: erste Hälfte: ', calculate_mittelwert(Wiesen2[:int(len(Wiesen2)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Wiesen2[int(len(Wiesen2)/2):]), ', gesamt:', calculate_mittelwert(Wiesen2), '+-', calculate_standardabweichung(Wiesen2, calculate_mittelwert(Wiesen2)))
print('Kloester: erste Hälfte: ', calculate_mittelwert(Kloester2[:int(len(Kloester2)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Kloester2[int(len(Kloester2)/2):]), ', gesamt:', calculate_mittelwert(Kloester2), '+-', calculate_standardabweichung(Kloester2, calculate_mittelwert(Kloester2)))
print('gesamt: ', calculate_mittelwert(gesamtmeeples2), '+- ', calculate_standardabweichung(gesamtmeeples2, calculate_mittelwert(gesamtmeeples2)))



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

