import numpy as np

Orte1 = [6, 3, 4, 5, 6, 7]
Strassen1 = [4, 6, 4, 5, 3, 4]
Wiesen1 = [5, 3, 4, 2, 2, 3]
Kloester1 = [0, 3, 2, 2, 1, 2]

Orte2 = [6, 5, 4, 5, 3, 4]
Strassen2 = [1, 4, 4, 3, 7, 6]
Wiesen2 = [3, 1, 0, 2, 2, 2]
Kloester2 = [0, 1, 0, 1, 1, 1]

Orte1_punkte = [40, 52, 30, 43, 46, 43]
Strassen1_punkte = [18, 22, 18, 23, 9, 17]
Wiesen1_punkte = [30, 18, 30, 21, 18, 21]
Kloester1_punkte = [0, 21, 15, 17, 8, 16]

Orte2_punkte = [30, 21, 26, 30, 9, 28]
Strassen2_punkte = [5, 16, 11, 14, 19, 23]
Wiesen2_punkte = [0, 0, 0, 0, 9, 9]
Kloester2_punkte = [0, 8, 0, 6, 8, 7]


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

print('durchschnittlich auf Gebiete gesetzt Meeples:')
print('Player1:')
print('Orte: erste Hälfte: ', calculate_mittelwert(Orte1[:int(len(Orte1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Orte1[int(len(Orte1)/2):]), ', gesamt:', calculate_mittelwert(Orte1), '+-', calculate_standardabweichung(Orte1, calculate_mittelwert(Orte1)))
print('Strassen: erste Hälfte: ', calculate_mittelwert(Strassen1[:int(len(Strassen1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Strassen1[int(len(Strassen1)/2):]), ', gesamt:', calculate_mittelwert(Strassen1), '+-', calculate_standardabweichung(Strassen1, calculate_mittelwert(Strassen1)))
print('Wiesen: erste Hälfte: ', calculate_mittelwert(Wiesen1[:int(len(Wiesen1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Wiesen1[int(len(Wiesen1)/2):]), ', gesamt:', calculate_mittelwert(Wiesen1), '+-', calculate_standardabweichung(Wiesen1, calculate_mittelwert(Wiesen1)))
print('Kloester: erste Hälfte: ', calculate_mittelwert(Kloester1[:int(len(Kloester1)/2)]), ', zweite Hälfte: ', calculate_mittelwert(Kloester1[int(len(Kloester1)/2):]), ', gesamt:', calculate_mittelwert(Kloester1), '+-', calculate_standardabweichung(Kloester1, calculate_mittelwert(Kloester1)))


print('\nPlayer2:')
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


m_orte_meeples1 = calculate_mittelwert(Orte1)
m_strassen_meeples1 = calculate_mittelwert(Strassen1)
m_wiesen_meeples1 = calculate_mittelwert(Wiesen1)
m_kloester_meeples1 = calculate_mittelwert(Kloester1)

m_orte_meeples2 = calculate_mittelwert(Orte2)
m_strassen_meeples2 = calculate_mittelwert(Strassen2)
m_wiesen_meeples2 = calculate_mittelwert(Wiesen2)
m_kloester_meeples2 = calculate_mittelwert(Kloester2)

m_orte_punkte1 = calculate_mittelwert(Orte1_punkte)
m_strassen_punkte1 = calculate_mittelwert(Strassen1_punkte)
m_wiesen_punkte1 = calculate_mittelwert(Wiesen1_punkte)
m_kloester_punkte1 = calculate_mittelwert(Kloester1_punkte)

m_orte_punkte2 = calculate_mittelwert(Orte2_punkte)
m_strassen_punkte2 = calculate_mittelwert(Strassen2_punkte)
m_wiesen_punkte2 = calculate_mittelwert(Wiesen2_punkte)
m_kloester_punkte2 = calculate_mittelwert(Kloester2_punkte)

s_orte_meeples1 = calculate_standardabweichung(Orte1, m_orte_meeples1)
s_strassen_meeples1 = calculate_standardabweichung(Strassen1, m_strassen_meeples1)
s_wiesen_meeples1 = calculate_standardabweichung(Wiesen1, m_wiesen_meeples1)
s_kloester_meeples1 = calculate_standardabweichung(Kloester1, m_kloester_meeples1)

s_orte_meeples2 = calculate_standardabweichung(Orte2, m_orte_meeples2)
s_strassen_meeples2 = calculate_standardabweichung(Strassen2, m_strassen_meeples2)
s_wiesen_meeples2 = calculate_standardabweichung(Wiesen2, m_wiesen_meeples2)
s_kloester_meeples2 = calculate_standardabweichung(Kloester2, m_kloester_meeples2)

s_orte_punkte1 = calculate_standardabweichung(Orte1_punkte, m_orte_punkte1)
s_strassen_punkte1 = calculate_standardabweichung(Strassen1_punkte, m_strassen_punkte1)
s_wiesen_punkte1 = calculate_standardabweichung(Wiesen1_punkte, m_wiesen_punkte1)
s_kloester_punkte1 = calculate_standardabweichung(Kloester1_punkte, m_kloester_punkte1)

s_orte_punkte2 = calculate_standardabweichung(Orte2_punkte, m_orte_punkte2)
s_strassen_punkte2 = calculate_standardabweichung(Strassen2_punkte, m_strassen_punkte2)
s_wiesen_punkte2 = calculate_standardabweichung(Wiesen2_punkte, m_wiesen_punkte2)
s_kloester_punkte2 = calculate_standardabweichung(Kloester2_punkte, m_kloester_punkte2)


def calculate_quot_error(punkte, s_punkte, meeples, s_meeples):
    return s_punkte / meeples + punkte * s_meeples / (meeples**2)


punkte_pro_ortsmeeple1 = m_orte_punkte1 / m_orte_meeples1
abw_punkte_pro_ortsmeeple1 = calculate_quot_error(m_orte_punkte1, s_orte_punkte1, m_orte_meeples1, s_orte_meeples1)

punkte_pro_strassenmeeple1 = m_strassen_punkte1 / m_strassen_meeples1
abw_punkte_pro_strassenmeeple1 = calculate_quot_error(m_strassen_punkte1, s_strassen_punkte1, m_strassen_meeples1, s_strassen_meeples1)

punkte_pro_wiesenmeeple1 = m_wiesen_punkte1 / m_wiesen_meeples1
abw_punkte_pro_wiesenmeeple1 = calculate_quot_error(m_wiesen_punkte1, s_wiesen_punkte1, m_wiesen_meeples1, s_wiesen_meeples1)

punkte_pro_klostermeeple1 = m_kloester_punkte1 / m_kloester_meeples1
abw_punkte_pro_klostermeeple1 = calculate_quot_error(m_kloester_punkte1, s_kloester_punkte1, m_kloester_meeples1, s_kloester_meeples1)


punkte_pro_ortsmeeple2 = m_orte_punkte2 / m_orte_meeples2
abw_punkte_pro_ortsmeeple2 = calculate_quot_error(m_orte_punkte2, s_orte_punkte2, m_orte_meeples2, s_orte_meeples2)

punkte_pro_strassenmeeple2 = m_strassen_punkte2 / m_strassen_meeples2
abw_punkte_pro_strassenmeeple2 = calculate_quot_error(m_strassen_punkte2, s_strassen_punkte2, m_strassen_meeples2, s_strassen_meeples2)

punkte_pro_wiesenmeeple2 = m_wiesen_punkte2 / m_wiesen_meeples2
abw_punkte_pro_wiesenmeeple2 = calculate_quot_error(m_wiesen_punkte2, s_wiesen_punkte2, m_wiesen_meeples2, s_wiesen_meeples2)

punkte_pro_klostermeeple2 = m_kloester_punkte2 / m_kloester_meeples2
abw_punkte_pro_klostermeeple2 = calculate_quot_error(m_kloester_punkte2, s_kloester_punkte2, m_kloester_meeples2, s_kloester_meeples2)

print('\ndurchschnittliche Punkte pro Meeple:')

print('Player1:')
print('pkt/ortsmeeple:', punkte_pro_ortsmeeple1, ' +- ', abw_punkte_pro_ortsmeeple1)
print('pkt/strassenmeeple:', punkte_pro_strassenmeeple1, '+-', abw_punkte_pro_strassenmeeple1)
print('pkt/wiesenmeeple:', punkte_pro_wiesenmeeple1, '+-', abw_punkte_pro_wiesenmeeple1)
print('pkt/klostermeeple:', punkte_pro_klostermeeple1, '+-', abw_punkte_pro_klostermeeple1)

print('\nPlayer2:')
print('pkt/ortsmeeple:', punkte_pro_ortsmeeple2, ' +- ', abw_punkte_pro_ortsmeeple2)
print('pkt/strassenmeeple:', punkte_pro_strassenmeeple2, '+-', abw_punkte_pro_strassenmeeple2)
print('pkt/wiesenmeeple:', punkte_pro_wiesenmeeple2, '+-', abw_punkte_pro_wiesenmeeple2)
print('pkt/klostermeeple:', punkte_pro_klostermeeple2, '+-', abw_punkte_pro_klostermeeple2)
