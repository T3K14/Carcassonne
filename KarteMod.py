import numpy as np

from Rotate import Rotate
from Ort import Ort_auf_Karte

anzahl_orte = -1
anzahl_strassen = 0
anzahl_kloester = 0
anzahlWiesen = 1
ww = False

class Karte():
    """erstellt zu jeder eingabe von Infoliste passende Matrix der Karte"""  #####


    def __init__(self, a, b, c, d, m = None, Schild = False):
        self.mitte = m
        self.info = [a, b, c, d, m]
        self.info_alt = [a, b, c, d, m]
        self.matrix = np.zeros((7, 7))
        self.schild = Schild

        self.strassen = []
        self.orte = []
        #self.wiesen = []

        for position, status in enumerate(self.info[:-1]):
            if status == "S":
                self.strassen.append(position)
            elif status == "O":
                self.orte.append(position)
            #else:
            #    self.wiesen.append(position)

        s = True
        while s:

            if len(self.strassen) == 2:
                if self.strassen[0] == 0:
                    if self.strassen[1] == 1:
                        self.matrix[:, 3][0:3], self.matrix[3][3:] = 2, 2
                    if self.strassen[1] == 2:
                        self.matrix[:, 3] = 2
                    if self.strassen[1] == 3:
                        self.matrix[:, 3][0:3], self.matrix[3][0:4] = 2, 2
                else:
                    self.info = Rotate.rotate_card_right(self.info)
                    self.strassen = Rotate.rotate_list_right(self.strassen)
                    self.orte = Rotate.rotate_list_right(self.orte)
                    continue

            if len(self.strassen) == 3:
                if self.strassen[0] == 0:
                    if self.strassen[1] == 1:
                        if self.strassen[2] == 2:
                            self.matrix[:, 3], self.matrix[3][3:] = 2, 2
                        else:
                            self.matrix[:, 3][0:3], self.matrix[3] = 2, 2
                    if self.strassen[1] == 2:
                        self.matrix[:, 3], self.matrix[3][0:3] = 2, 2
                else:
                    self.info = Rotate.rotate_card_right(self.info)
                    self.strassen = Rotate.rotate_list_right(self.strassen)
                    self.orte = Rotate.rotate_list_right(self.orte)
                    continue

            if len(self.strassen) == 4:
                self.matrix[:, 3], self.matrix[3] = 2, 2

            s = False

        # liste und matrix auf anfang zurückdrehen? ne, da self.info gedreht wurde, stimmen die ortsplätze
        # noch in bezug auf die strassenplätze
        o = True
        while o:

            self.orte = sorted(self.orte)

            # for position, status in enumerate(self.info[:-1]):
            #    if status == "O":
            #        self.orte.append(position)
            if len(self.orte) == 1:
                if self.orte[0] == 0:
                    self.matrix[0] = 1
                else:
                    self.info = Rotate.rotate_card_right(self.info)
                    self.matrix = Rotate.rotate_matrix_right(self.matrix)
                    self.strassen = Rotate.rotate_list_right(self.strassen)
                    self.orte = Rotate.rotate_list_right(self.orte)
                    continue
            if len(self.orte) == 2:
                if self.mitte == "O":
                    if abs(self.orte[0] - self.orte[1]) == 2:  # O,W,O,W,O
                        if self.orte[0] == 0:
                            self.matrix = np.ones(self.matrix.shape)
                            self.matrix[:, 0][1:-1], self.matrix[:, 6][1:-1] = 0, 0
                            self.matrix[:, 1][1:-1], self.matrix[:, 5][1:-1] = 0, 0
                            global ww
                            ww = True

                        else:
                            self.info = Rotate.rotate_card_right(self.info)
                            self.matrix = Rotate.rotate_matrix_right(self.matrix)
                            self.strassen = Rotate.rotate_list_right(self.strassen)
                            self.orte = Rotate.rotate_list_right(self.orte)
                            continue
                    elif self.orte[0] == 0:  # O,O,W,W,O
                        if self.orte[1] == 1:
                            self.matrix[0], self.matrix[:, 6], self.matrix[1][2:], self.matrix[:, 5][:-2] = 1, 1, 1, 1
                        else:
                            self.info = Rotate.rotate_card_right(self.info)
                            self.matrix = Rotate.rotate_matrix_right(self.matrix)
                            self.strassen = Rotate.rotate_list_right(self.strassen)
                            self.orte = Rotate.rotate_list_right(self.orte)
                            continue
                    else:
                        self.info = Rotate.rotate_card_right(self.info)
                        self.matrix = Rotate.rotate_matrix_right(self.matrix)
                        self.strassen = Rotate.rotate_list_right(self.strassen)
                        self.orte = Rotate.rotate_list_right(self.orte)
                        continue
                else:
                    if abs(self.orte[0] - self.orte[1]) == 2:  # O,W,O,W,!=O
                        if self.orte[0] == 0:
                            self.matrix[0], self.matrix[6] = 1, 1
                        else:
                            self.info = Rotate.rotate_card_right(self.info)
                            self.matrix = Rotate.rotate_matrix_right(self.matrix)
                            self.strassen = Rotate.rotate_list_right(self.strassen)
                            self.orte = Rotate.rotate_list_right(self.orte)
                            continue
                    elif self.orte[0] == 0:
                        if self.orte[1] == 1:
                            self.matrix[0], self.matrix[:, 6] = 1, 1
                        else:
                            self.info = Rotate.rotate_card_right(self.info)
                            self.matrix = Rotate.rotate_matrix_right(self.matrix)
                            self.strassen = Rotate.rotate_list_right(self.strassen)
                            self.orte = Rotate.rotate_list_right(self.orte)
                            continue
                    else:
                        self.info = Rotate.rotate_card_right(self.info)
                        self.matrix = Rotate.rotate_matrix_right(self.matrix)
                        self.strassen = Rotate.rotate_list_right(self.strassen)
                        self.orte = Rotate.rotate_list_right(self.orte)
                        continue
            if len(self.orte) == 3:
                # if "S" not in self.info[:-1]:
                for i in [0, 1, 2, 3]:
                    if self.info[0] == "O":
                        self.info = Rotate.rotate_card_right(self.info)
                        self.matrix = Rotate.rotate_matrix_right(self.matrix)
                        self.strassen = Rotate.rotate_list_right(self.strassen)
                        self.orte = Rotate.rotate_list_right(self.orte)
                        continue
                    elif self.info[0] != "O":
                        self.matrix = np.ones((7, 7))
                        self.matrix[1][1:-1], self.matrix[0][1:-1] = 0, 0
                        if "S" in self.info:
                            self.matrix[:, 3][:2] = 2
                        break
            if len(self.orte) == 4:
                self.matrix = np.ones((7, 7))
                # self.strassen = Rotate.rotate_list_right(self.strassen)
                # self.orte = Rotate.rotate_list_right(self.orte)
            o = False
        if self.mitte == "K":
            self.matrix[3][3] = 3

            if "S" in self.info:
                k = True
                while k:
                    if self.info[2] == "S":
                        self.matrix[:, 3][4:] = 2
                        k = False
                    else:
                        self.info = Rotate.rotate_card_right(self.info)
                        self.matrix = Rotate.rotate_matrix_right(self.matrix)
                        self.strassen = Rotate.rotate_list_right(self.strassen)
                        self.orte = Rotate.rotate_list_right(self.orte)
                        continue


        if self.mitte == "G":
            self.matrix[3][3] = 4

        # dient dazu nach erstellen der karte, info und matrix auf ausgangsposition zu drehen

        while True:
            if self.info == self.info_alt:
                break
            else:
                self.info = Rotate.rotate_card_right(self.info)
                self.matrix = Rotate.rotate_matrix_right(self.matrix)
                self.orte = Rotate.rotate_list_right(self.orte)
                self.strassen = Rotate.rotate_list_right(self.strassen)


        self.wiesen = []
        for position, status in enumerate(self.info[:-1]):
            if status == "W":
                self.wiesen.append(position)


        self.orte_karte = []
        self.strassen_karte = []
        self.kloster_karte = []
        self.wiesenKarte = []

        global anzahl_orte
        global anzahl_strassen
        global anzahl_kloester
        global anzahlWiesen

        self.lo = int(self.matrix[1][1])
        self.ro = int(self.matrix[1][-2])
        self.lu = int(self.matrix[5][1])
        self.ru = int(self.matrix[5][-2])

        dic = {0: [4, 5], 1: [5, 6], 2: [6, 7], 3: [7, 4]}
        dic2 = {(4, 5): 0, (5, 6): 1, (6, 7): 2, (7, 4): 3}

        ortswert = 2
        if self.mitte == "O":
            anzahl_orte += 1
            if self.schild:
                ortswert += 2
            ortsname = "Ort_{}".format(anzahl_orte)

            self.orte_karte.append(Ort_auf_Karte(ortsname, self.orte, ortswert))
            #self.orte_karte.append((ort, self.orte, ortswert))

            #erstellt zwei Wiesen

            if ww:
                #print("ja moin", self.matrix)
                for w in self.wiesen:
                    anzahlWiesen += 1
                    wiese = "Wiese_{}".format(anzahlWiesen)
                    #print(dic[w])
                    self.wiesenKarte.append((wiese, dic[w]))

        else:
            for pos, i in enumerate(self.orte):
                #print("moin")
                anzahl_orte += 1
                ortsname = "Ort_{}".format(anzahl_orte)

                self.orte_karte.append(Ort_auf_Karte(ortsname, [self.orte[pos]], ortswert))
                #self.orte_karte.append((ort, [self.orte[pos]], ortswert))

        for pos, i in enumerate(self.strassen):

            anzahl_strassen += 1
            strasse = "Strasse_{}".format(anzahl_strassen)

            if len(self.strassen) < 3:
                self.strassen_karte.append((strasse, self.strassen))
                break
            else:
                self.strassen_karte.append((strasse, [self.strassen[pos]]))

        if self.mitte == "K":
            anzahl_kloester += 1
            kloster = "Kloster_{}".format(anzahl_kloester)
            self.kloster_karte.append(kloster)

            anzahlWiesen += 1
            wiese = "Wiese_{}".format(anzahlWiesen)
            self.wiesenKarte.append((wiese, [4, 5, 6, 7]))

        if self.mitte != "K" and not ww:
            #print("jetzt weiter", self.wiesenKarte)

            wListe = []
            liste_paare = []
            liste_einzeln = []
            ecken = {4: self.lo, 5: self.ro, 6: self.lu, 7: self.ru}
            dic2 = {(4, 5): 0, (5, 6): 1, (6, 7): 2, (7, 4): 3}
            #extraDic = {(4, 6): "PLATZHALTER", (5, 7): "PLATZHALTER"}

            dic2Kopie = dic2.copy()

            for ecke in ecken:
                if ecken[ecke] != 0:
                    for d in dic2Kopie:
                        if ecke in d:
                            #print(self.matrix, d)
                            if d in dic2:
                                del dic2[d]

            #print("DIC", dic2)
                #None

            for (a, b) in dic2:

                if self.info[dic2[(a, b)]] != "S":

                    liste_paare.append([a, b])

                else:
                    if a not in liste_einzeln:
                        liste_einzeln.append(a)
                    if b not in liste_einzeln:
                        liste_einzeln.append(b)

            for i in liste_einzeln[:]:
                for j in liste_paare:
                    if i in j:
                        liste_einzeln.remove(i)

            if len(liste_paare) > 0:
                a, b = liste_paare[0]
                del liste_paare[0]
                set = {a, b}

                kopie = liste_paare[:]

                for element in kopie:
                    if element[0] in set or element[1] in set:
                        set.update(element)
                        liste_paare.remove(element)

                y = [i for i in set]
                wListe = [j for j in liste_paare]
                wListe.append(y)
                for i in liste_einzeln:
                    wListe.append([i])
            else:
                if self.mitte == "O" and len(self.strassen) == 2:
                    #print(self.matrix)
                    dic3 = {4: 6, 5: 7, 6: 4, 7: 5}
                    for i in liste_einzeln:
                        if dic3[i] in liste_einzeln:
                            liste_einzeln.remove(i)
                            liste_einzeln.remove(dic3[i])
                            wListe = [[i, dic3[i]], liste_einzeln]
                else:
                    hliste = []
                    if len(liste_einzeln) > 0:
                        hliste = []
                        for i in liste_einzeln:
                            hliste.append(i)
                        for j in hliste:
                            wListe.append([j])
                    else:
                        wListe = []

            for w in wListe:
                anzahlWiesen += 1
                wiese = "Wiese_{}".format(anzahlWiesen)

                self.wiesenKarte.append((wiese, w))

        ww = False


Karteninfos = ["4WWWWK", "2WWSWK", "OOOOOT", "3SOSW", "5OWWW", "2WOWOOT", "OWOWO", "3WOWO", "2WOOW", "3OSSW", "3SOWS",
               "3SOSSG", "2OWWOOT", "3OWWOO", "2OSSOOT", "3OSSOO", "OOWOOT", "3OOWOO", "2OOSOOT", "OOSOO", "8SWSW",
               "9WWSS", "4WSSSG", "SSSSG"]

Karteninfos_neu = []
Kartenliste = []

for card in Karteninfos:
    i = list(card)
    try:
        if int(i[0]) in range(10):
            for z in range(int(i[0])):
                Karteninfos_neu.append(card[1:])
    except ValueError:
        Karteninfos_neu.append(card)

#print(Karteninfos_neu)

for card in Karteninfos_neu:
    i = list(card)

    if len(i) == 4:
        a, b, c, d, m, schild = i[0], i[1], i[2], i[3], None, False
    elif len(i) == 5:
        a, b, c, d, m, schild = i[0], i[1], i[2], i[3], i[4], False
    else:
        a, b, c, d, m, schild = i[0], i[1], i[2], i[3], i[4], True

    card_to_add = Karte(a,b,c,d,m,schild)
    Kartenliste.append(card_to_add)

#for k in Kartenliste:
    #print("\n", k.matrix, k.wiesenKarte)
