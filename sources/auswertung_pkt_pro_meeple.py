import numpy as np
import pandas as pd

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


liste_meeples = [1,0,1,1,2,2,2,4,1,2,1,0,2,2,0,0,1,0,2,2,1,1,1,0,2,1,1,0,1,1,2,1,2,3,1,0,1,3,3,1,3,2,2,3,1,2,2,2,1,1]
liste_punkte = [8,0,9,8,15,14,16,32,7,16,8,0,13,15,0,0,6,0,16,17,8,6,7,0,15,7,9,0,8,9,15,8,15,21,8,0,8,25,21,8,22,16,17,23,8,16,16,13,7,9]


def calculate_quotienten(punkte, meeples):
    quotienten = []
    nr_spiele = 0

    for i in range(len(meeples)):
        if meeples[i] == 0:
            continue
        else:
            quotienten.append(punkte[i] / meeples[i])
            nr_spiele += 1

    return nr_spiele, quotienten


#df = pd.read_excel('p2.xlsx') # can also index sheet by name or fetch all sheets
#kloester_punkte = df['kloester'].tolist()
#orte_punkte = df['orte'].tolist()
#strassen_punkte = df['strassen'].tolist()
#wiesen_punkte = df['wiesen'].tolist()

#kloester_meeples = df['k'].tolist()
#orte_meeples = df['o'].tolist()
#strassen_meeples = df['s'].tolist()
#wiesen_meeples = df['w'].tolist()

kloester_meeples = [0, 1, 2, 1, 2, 2, 4, 3, 0, 1, 1, 0, 3, 2, 1, 2, 1, 1, 2, 3]
kloester_punkte = [0, 7, 16, 9, 18, 18, 31, 24, 0, 8, 8, 0, 24, 18, 7, 15, 8, 8, 16, 23]

orte_punkte = [41, 44, 50, 67, 53, 47, 50, 52, 60, 43, 39, 36, 53, 56, 68, 40, 56, 54, 73, 33]
orte_meeples = [4, 6, 9, 8, 8, 7, 7, 6, 8, 6, 2, 5, 7, 9, 7, 6, 7, 6, 10, 3]

strassen_punkte = [29, 23, 7, 11, 20, 25, 28, 18, 20, 23, 37, 20, 21, 16, 22, 8, 33, 21, 29, 17]
strassen_meeples = [7, 4, 1, 3, 6, 6, 6, 4, 5, 3, 9, 4, 6, 4, 7, 1, 5, 2, 7, 4]

wiesen_punkte = [18, 15, 18, 15, 45, 18, 15, 6, 24, 21, 9, 18, 15, 24, 15, 18, 3, 18, 18, 9]
wiesen_meeples = [4, 2, 1, 3, 2, 2, 2, 1, 3, 2, 1, 3, 2, 2, 2, 3, 1, 2, 1, 1]

###
"""
w_punkte = [33, 24, 12, 18, 12, 0]
w_meeples = [3, 3, 2, 2, 1, 1]"""

nr_spiele_kl, kloster_quots = calculate_quotienten(kloester_punkte, kloester_meeples)
m_kloster_quot = calculate_mittelwert(kloster_quots)
s_kloster_quot = calculate_standardabweichung(kloster_quots, m_kloster_quot)

nr_spiele_o, ort_quots = calculate_quotienten(orte_punkte, orte_meeples)
m_ort_quot = calculate_mittelwert(ort_quots)
s_ort_quot = calculate_standardabweichung(ort_quots, m_ort_quot)

nr_spiele_s, strassen_quots = calculate_quotienten(strassen_punkte, strassen_meeples)
m_strassen_quot = calculate_mittelwert(strassen_quots)
s_strassen_quot = calculate_standardabweichung(strassen_quots, m_strassen_quot)

nr_spiele_w, wiesen_quots = calculate_quotienten(wiesen_punkte, wiesen_meeples)
m_wiesen_quot = calculate_mittelwert(wiesen_quots)
s_wiesen_quot = calculate_standardabweichung(wiesen_quots, m_wiesen_quot)

print('Orte:', m_ort_quot, '+-', s_ort_quot, 'bei ', nr_spiele_o, ' Spielen')
print('Strassen:', m_strassen_quot, '+-', s_strassen_quot, 'bei ', nr_spiele_s, ' Spielen')
print('Wiesen:', m_wiesen_quot, '+-', s_wiesen_quot, 'bei ', nr_spiele_w, ' Spielen')
print('Klöster:', m_kloster_quot, '+-', s_kloster_quot, 'bei ', nr_spiele_kl, ' Spielen')


"""n, wq = calculate_quotienten(w_punkte, w_meeples)
mwq = calculate_mittelwert(wq)
swq = calculate_standardabweichung(wq, mwq)

print(wq, mwq, swq)

"""
