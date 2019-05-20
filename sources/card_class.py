import numpy as np
from Ort import Ort_auf_Karte
from Strasse import StasseAufKarte
from Wiese import WieseAufKarte
#from strasse, etc
from rotate2 import rotate_info_right, rotate_list_right, rotate_matrix_right, rotate_kanten_dict_right

class Card:

    def __init__(self, o, r, u, l, m=None, schild=False):

        self.info = [o, r, u, l]
        self.mitte = m
        self.schild = schild

        self.matrix = np.zeros((7, 7))

        self.orte_kanten = []
        self.strassen_kanten = []
        self.wiesen_kanten = []

        self.kloster = False
        self.orte = []
        self.strassen = []
        self.wiesen = []

        self.kanten = {0: None, 1: None, 2: None, 3: None}

        for position, status in enumerate(self.info):
            if status == "S":
                self.strassen_kanten.append(position)
            elif status == "O":
                self.orte_kanten.append(position)
            else:
                self.wiesen_kanten.append(position)

        self.create_matrix()
        self.create_orte()
        self.create_strassen()
        self.create_wiesen()
        self.initialize_kanten()


    def create_matrix(self):
        """einfach von frueher reinkopiert, kann gegebenenfalls optimiert werden"""
        info_old = self.info[:]

        s = True
        while s:

            if len(self.strassen_kanten) == 2:
                if self.strassen_kanten[0] == 0:
                    if self.strassen_kanten[1] == 1:
                        self.matrix[:, 3][0:3], self.matrix[3][3:] = 2, 2
                    if self.strassen_kanten[1] == 2:
                        self.matrix[:, 3] = 2
                    if self.strassen_kanten[1] == 3:
                        self.matrix[:, 3][0:3], self.matrix[3][0:4] = 2, 2
                else:
                    self.info = rotate_info_right(self.info)
                    self.strassen_kanten = rotate_list_right(self.strassen_kanten)
                    self.orte_kanten = rotate_list_right(self.orte_kanten)
                    self.wiesen_kanten = rotate_list_right(self.wiesen_kanten)
                    continue

            if len(self.strassen_kanten) == 3:
                if self.strassen_kanten[0] == 0:
                    if self.strassen_kanten[1] == 1:
                        if self.strassen_kanten[2] == 2:
                            self.matrix[:, 3], self.matrix[3][3:] = 2, 2
                        else:
                            self.matrix[:, 3][0:3], self.matrix[3] = 2, 2
                    if self.strassen_kanten[1] == 2:
                        self.matrix[:, 3], self.matrix[3][0:3] = 2, 2
                else:
                    self.info = rotate_info_right(self.info)
                    self.strassen_kanten = rotate_list_right(self.strassen_kanten)
                    self.orte_kanten = rotate_list_right(self.orte_kanten)
                    continue

            if len(self.strassen_kanten) == 4:
                self.matrix[:, 3], self.matrix[3] = 2, 2

            s = False

        # liste und matrix auf anfang zurückdrehen? ne, da self.info gedreht wurde, stimmen die ortsplätze
        # noch in bezug auf die strassenplätze
        o = True
        while o:

            self.orte_kanten = sorted(self.orte_kanten)

            # for position, status in enumerate(self.info[:-1]):
            #    if status == "O":
            #        self.orte_kanten.append(position)
            if len(self.orte_kanten) == 1:
                if self.orte_kanten[0] == 0:
                    self.matrix[0] = 1
                else:
                    self.info = rotate_info_right(self.info)
                    self.matrix = rotate_matrix_right(self.matrix)
                    self.strassen_kanten = rotate_list_right(self.strassen_kanten)
                    self.orte_kanten = rotate_list_right(self.orte_kanten)
                    continue
            if len(self.orte_kanten) == 2:
                if self.mitte == "O":
                    if abs(self.orte_kanten[0] - self.orte_kanten[1]) == 2:  # O,W,O,W,O
                        if self.orte_kanten[0] == 0:
                            self.matrix = np.ones(self.matrix.shape)
                            self.matrix[:, 0][1:-1], self.matrix[:, 6][1:-1] = 0, 0
                            self.matrix[:, 1][1:-1], self.matrix[:, 5][1:-1] = 0, 0
                            global ww
                            ww = True

                        else:
                            self.info = rotate_info_right(self.info)
                            self.matrix = rotate_matrix_right(self.matrix)
                            self.strassen_kanten = rotate_list_right(self.strassen_kanten)
                            self.orte_kanten = rotate_list_right(self.orte_kanten)
                            continue
                    elif self.orte_kanten[0] == 0:  # O,O,W,W,O
                        if self.orte_kanten[1] == 1:
                            self.matrix[0], self.matrix[:, 6], self.matrix[1][2:], self.matrix[:, 5][:-2] = 1, 1, 1, 1
                        else:
                            self.info = rotate_info_right(self.info)
                            self.matrix = rotate_matrix_right(self.matrix)
                            self.strassen_kanten = rotate_list_right(self.strassen_kanten)
                            self.orte_kanten = rotate_list_right(self.orte_kanten)
                            continue
                    else:
                        self.info = rotate_info_right(self.info)
                        self.matrix = rotate_matrix_right(self.matrix)
                        self.strassen_kanten = rotate_list_right(self.strassen_kanten)
                        self.orte_kanten = rotate_list_right(self.orte_kanten)
                        continue
                else:
                    if abs(self.orte_kanten[0] - self.orte_kanten[1]) == 2:  # O,W,O,W,!=O
                        if self.orte_kanten[0] == 0:
                            self.matrix[0], self.matrix[6] = 1, 1
                        else:
                            self.info = rotate_info_right(self.info)
                            self.matrix = rotate_matrix_right(self.matrix)
                            self.strassen_kanten = rotate_list_right(self.strassen_kanten)
                            self.orte_kanten = rotate_list_right(self.orte_kanten)
                            continue
                    elif self.orte_kanten[0] == 0:
                        if self.orte_kanten[1] == 1:
                            self.matrix[0], self.matrix[:, 6] = 1, 1
                        else:
                            self.info = rotate_info_right(self.info)
                            self.matrix = rotate_matrix_right(self.matrix)
                            self.strassen_kanten = rotate_list_right(self.strassen_kanten)
                            self.orte_kanten = rotate_list_right(self.orte_kanten)
                            continue
                    else:
                        self.info = rotate_info_right(self.info)
                        self.matrix = rotate_matrix_right(self.matrix)
                        self.strassen_kanten = rotate_list_right(self.strassen_kanten)
                        self.orte_kanten = rotate_list_right(self.orte_kanten)
                        continue
            if len(self.orte_kanten) == 3:
                # if "S" not in self.info[:-1]:
                for i in [0, 1, 2, 3]:
                    if self.info[0] == "O":
                        self.info = rotate_info_right(self.info)
                        self.matrix = rotate_matrix_right(self.matrix)
                        self.strassen_kanten = rotate_list_right(self.strassen_kanten)
                        self.orte_kanten = rotate_list_right(self.orte_kanten)
                        continue
                    elif self.info[0] != "O":
                        self.matrix = np.ones((7, 7))
                        self.matrix[1][1:-1], self.matrix[0][1:-1] = 0, 0
                        if "S" in self.info:
                            self.matrix[:, 3][:2] = 2
                        break
            if len(self.orte_kanten) == 4:
                self.matrix = np.ones((7, 7))
                # self.strassen_kanten = rotate_list_right(self.strassen_kanten)
                # self.orte_kanten = rotate_list_right(self.orte_kanten)
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
                        self.info = rotate_info_right(self.info)
                        self.matrix = rotate_matrix_right(self.matrix)
                        self.strassen_kanten = rotate_list_right(self.strassen_kanten)
                        self.orte_kanten = rotate_list_right(self.orte_kanten)
                        continue

        if self.mitte == "G":
            self.matrix[3][3] = 4

        # dient dazu nach erstellen der karte, info und matrix auf ausgangsposition zu drehen

        while True:
            if self.info == info_old:
                break
            else:
                self.info = rotate_info_right(self.info)
                self.matrix = rotate_matrix_right(self.matrix)
                self.orte_kanten = rotate_list_right(self.orte_kanten)
                self.strassen_kanten = rotate_list_right(self.strassen_kanten)

        #self.wiesen = []
        #for position, status in enumerate(self.info[:-1]):
        #    if status == "W":
        #        self.wiesen.append(position)

    def rotate_right(self):
        self.info = rotate_info_right(self.info)
        self.strassen_kanten = rotate_list_right(self.strassen_kanten)
        self.orte_kanten = rotate_list_right(self.orte_kanten)
        self.wiesen_kanten = rotate_list_right(self.wiesen_kanten)
        self.matrix = rotate_matrix_right(self.matrix)
        self.kanten = rotate_kanten_dict_right(self.kanten)

        # auch noch fuer orte, strassen, wiesen auf karte die kanten rotieren
        for o in self.orte:
            o.kanten = rotate_list_right(o.kanten)
        for s in self.strassen:
            s.kanten = rotate_list_right(s.kanten)

    def create_orte(self):
        """um alle Orte auf der Karte zu erstellen"""
        if self.mitte == 'O':
            if self.schild:
                self.orte.append(Ort_auf_Karte(self.orte_kanten[:], 4))
            else:
                self.orte.append(Ort_auf_Karte(self.orte_kanten[:], 2))

        else:
            for k in self.orte_kanten:
                self.orte.append(Ort_auf_Karte([k]))

    def create_strassen(self):
        """um alle Strassen auf der Karte zu erstellen"""

        if 0 < len(self.strassen_kanten) < 3:
            self.strassen.append(StasseAufKarte(self.strassen_kanten[:]))
        else:
            for k in self.strassen_kanten:
                self.strassen.append(StasseAufKarte([k]))

    def create_wiesen(self):

        # fuer strassen
        d = {(0, 2): [[5, 6], [4, 7]], (1, 2): [[4, 5, 7], [6]], (0, 3): [[5, 6, 7], [4]], (2, 3): [[4, 5, 6], [7]],
             (1, 3): [[4, 5], [6, 7]], (0, 1): [[4, 6, 7], [5]]}
        # fuer oooso
        d2 = {0: [[4], [5]], 1: [[5], [6]], 2: [[6], [7]], 3: [[4], [7]]}
        # fuer wiesenkanten
        d3 = {0: [4, 5], 1: [5, 6], 2: [6, 7], 3: [4, 7]}
        #fuer oowwo
        d4 = {(0, 1): [4, 5, 6], (1, 2): [5, 6, 7], (2, 3): [4, 6, 7], (0, 3): [4, 5, 7]}
        # fuer drei strassenkarten
        d5 = {(0, 1, 2): [[5], [6], [4, 7]], (1, 2, 3): [[4, 5], [6], [7]], (0, 2, 3): [[4], [5, 6], [7]],
              (0, 1, 3): [[4], [5], [6, 7]]}
        if len(self.orte_kanten) != 4:

            if self.mitte == 'O':
                # wenn auf Karte Strassen sind
                if len(self.strassen_kanten) == 2:
                    for l in d[tuple(sorted(self.strassen_kanten))]:
                        self.wiesen.append(l)
                elif len(self.strassen_kanten) == 1:
                    for l in d2[self.strassen_kanten[0]]:
                        self.wiesen.append(l)

                # 2 ortskanten
                elif len(self.orte_kanten) == 2:
                    if self.orte_kanten in [[0, 2], [1, 3]]:
                        for w in self.wiesen_kanten:
                            self.wiesen.append(WieseAufKarte(d3[w]))
                    else:
                        self.wiesen.append(WieseAufKarte(d4[tuple(sorted(self.wiesen_kanten))]))
                # sonst
                else:
                    self.wiesen.append(WieseAufKarte(self.wiesen_kanten))
            elif len(self.strassen_kanten) >= 2:
                if len(self.strassen_kanten) == 2:
                    for i in d[tuple(sorted(self.strassen_kanten))]:
                        self.wiesen.append(WieseAufKarte(i))
                elif len(self.strassen_kanten) == 3:
                    for i in d5[tuple(sorted(self.strassen_kanten))]:
                        self.wiesen.append(i)
                else:
                    for i in range(4, 8):
                        self.wiesen.append(WieseAufKarte([i]))
            else:
                self.wiesen.append(WieseAufKarte([4, 5, 6, 7]))

    def update_kanten(self, landschaft, globale_landschaft):
        for l in self.kanten:
            if self.kanten[l] is not None and landschaft == self.kanten[l]:
                self.kanten[l] = globale_landschaft

    def initialize_kanten(self):
        for ort in self.orte:
            for k in ort.kanten:
                self.kanten[k] = ort
        for strasse in self.strassen:
            for k in strasse.kanten:
                self.kanten[k] = strasse


Karteninfos = ["4WWWWK", "2WWSWK", "OOOOOT", "3SOSW", "5OWWW", "2WOWOOT",
               "OWOWO", "3WOWO", "2WOOW", "3OSSW", "3SOWS","3SOSSG",
               "2OWWOOT", "3OWWOO", "2OSSOOT", "3OSSOO", "OOWOOT", "3OOWOO",
               "2OOSOOT", "OOSOO", "8SWSW", "9WWSS", "4WSSSG", "SSSSG"]

Karteninfos_neu = []

for card in Karteninfos:
    i = list(card)
    try:
        if int(i[0]) in range(10):
            for z in range(int(i[0])):
                Karteninfos_neu.append(card[1:])
    except ValueError:
        Karteninfos_neu.append(card)


def create_kartenliste(karteninfos):

    l = []

    for info in karteninfos:
        i = list(info)

        if len(i) == 4:
            a, b, c, d, m, schild = i[0], i[1], i[2], i[3], None, False
        elif len(i) == 5:
            a, b, c, d, m, schild = i[0], i[1], i[2], i[3], i[4], False
        else:
            a, b, c, d, m, schild = i[0], i[1], i[2], i[3], i[4], True

        k = Card(a, b, c, d, m, schild)
        l.append(k)

    return l

Kartenliste = create_kartenliste(Karteninfos_neu)

if __name__ == "__main__":
    ka = Card("O", "S", "S", "W")
    print(ka.matrix)
    ka.rotate_right()
    print("\n", ka.matrix)
    ka.rotate_right()
    print("\n", ka.matrix)
    ka.rotate_right()
    print("\n", ka.matrix)

