import numpy as np
from Ort import Ort_auf_Karte
from Strasse import StasseAufKarte
from Wiese import WieseAufKarte
#from strasse, etc
from rotate2 import rotate_info_right, rotate_list_right, rotate_matrix_right, rotate_kanten_dict_right, rotate_wiesen_right, rotate_ecken_dict_right

import random

class Card:

    def __init__(self, o, r, u, l, m=None, schild=False):

        self.info = [o, r, u, l]
        self.mitte = m
        self.schild = schild

        self.matrix = np.zeros((7, 7))

        self.orte_kanten = []
        self.strassen_kanten = []
        self.wiesen_kanten = []

        self.orte = []
        self.strassen = []
        self.wiesen = []

        self.kanten = {0: None, 1: None, 2: None, 3: None}
        self.ecken = {4: None, 5: None, 6: None, 7: None}

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
        self.ecken = rotate_ecken_dict_right(self.ecken)

        # auch noch fuer orte, strassen, wiesen auf karte die kanten rotieren
        for o in self.orte:
            o.kanten = rotate_list_right(o.kanten)
        for s in self.strassen:
            s.kanten = rotate_list_right(s.kanten)
        for w in self.wiesen:
            w.ecken = rotate_wiesen_right(w.ecken)


    def create_orte(self):
        """um alle Orte auf der Karte zu erstellen"""
        z = 1
        if self.mitte == 'O':
            if self.schild:
                self.orte.append(Ort_auf_Karte(self.orte_kanten[:], z, 4))
            else:
                self.orte.append(Ort_auf_Karte(self.orte_kanten[:], z, 2))

        else:
            for k in self.orte_kanten:
                self.orte.append(Ort_auf_Karte([k], z))
                z += 1

    def create_strassen(self):
        """um alle Strassen auf der Karte zu erstellen"""
        z = 1
        if 0 < len(self.strassen_kanten) < 3:
            self.strassen.append(StasseAufKarte(self.strassen_kanten[:], z))
        else:
            for k in self.strassen_kanten:
                self.strassen.append(StasseAufKarte([k], z))
                z += 1

    def create_wiesen(self):
        z = 1
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
        # fuer oosso
        d6 = {(1, 2): [[5, 7], [6]], (0, 3): [[5, 7], [4]], (2, 3): [[4, 6], [7]], (0, 1): [[4, 6], [5]]}
        if len(self.orte_kanten) != 4:

            if self.mitte == 'O':
                # wenn auf Karte Strassen sind
                if len(self.strassen_kanten) == 2:
                    for l in d6[tuple(sorted(self.strassen_kanten))]:
                        self.wiesen.append(WieseAufKarte(l, z))
                        z += 1
                elif len(self.strassen_kanten) == 1:
                    for l in d2[self.strassen_kanten[0]]:
                        self.wiesen.append(WieseAufKarte(l, z))
                        z += 1

                # 2 ortskanten
                elif len(self.orte_kanten) == 2:
                    if self.orte_kanten in [[0, 2], [1, 3]]:
                        for w in self.wiesen_kanten:
                            self.wiesen.append(WieseAufKarte(d3[w], z))
                            z += 1
                    else:
                        self.wiesen.append(WieseAufKarte(d4[tuple(sorted(self.wiesen_kanten))], z))
                        z += 1
                # sonst
                else:
                    self.wiesen.append(WieseAufKarte(d3[self.wiesen_kanten[0]], z))
                    z += 1
            elif len(self.strassen_kanten) >= 2:
                if len(self.strassen_kanten) == 2:
                    for i in d[tuple(sorted(self.strassen_kanten))]:
                        self.wiesen.append(WieseAufKarte(i, z))
                        z += 1
                elif len(self.strassen_kanten) == 3:
                    for i in d5[tuple(sorted(self.strassen_kanten))]:
                        self.wiesen.append(WieseAufKarte(i, z))
                        z += 1
                else:
                    for i in range(4, 8):
                        self.wiesen.append(WieseAufKarte([i], z))
                        z += 1
            else:
                self.wiesen.append(WieseAufKarte([4, 5, 6, 7], z))
                z += 1

    def update_kanten(self, landschaft, globale_landschaft):
        for l in self.kanten:
            if self.kanten[l] is not None and landschaft == self.kanten[l]:
                self.kanten[l] = globale_landschaft

    def update_ecken(self, wiese, globale_wiese):
        for e in self.ecken:
            if self.ecken[e] is not None and wiese == self.ecken[e]:
                self.ecken[e] = globale_wiese

    def initialize_kanten(self):
        for ort in self.orte:
            for k in ort.kanten:
                self.kanten[k] = ort
        for strasse in self.strassen:
            for k in strasse.kanten:
                self.kanten[k] = strasse
        for wiese in self.wiesen:
            for e in wiese.ecken:
                self.ecken[e] = wiese

karteninfoliste = ['WWWWK', 'WWWWK', 'WWWWK', 'WWWWK', 'WWSWK', 'WWSWK', 'OOOOOT', 'SOSW', 'SOSW', 'SOSW', 'OWWW',
                       'OWWW', 'OWWW', 'OWWW', 'OWWW', 'WOWOOT', 'WOWOOT', 'OWOWO', 'WOWO', 'WOWO', 'WOWO', 'WOOW',
                       'WOOW', 'OSSW', 'OSSW', 'OSSW', 'SOWS', 'SOWS', 'SOWS', 'SOSSG', 'SOSSG', 'SOSSG', 'OWWOOT',
                       'OWWOOT', 'OWWOO', 'OWWOO', 'OWWOO', 'OSSOOT', 'OSSOOT', 'OSSOO', 'OSSOO', 'OSSOO', 'OOWOOT',
                       'OOWOO', 'OOWOO', 'OOWOO', 'OOSOOT', 'OOSOOT', 'OOSOO', 'SWSW', 'SWSW', 'SWSW', 'SWSW', 'SWSW',
                       'SWSW', 'SWSW', 'SWSW', 'WWSS', 'WWSS', 'WWSS', 'WWSS', 'WWSS', 'WWSS', 'WWSS', 'WWSS', 'WWSS',
                       'WSSSG', 'WSSSG', 'WSSSG', 'WSSSG', 'SSSSG']

determinized_karteninfoliste = ['SOWS', 'WWSS', 'SOSSG', 'OSSW', 'OOSOOT', 'WWSWK', 'OSSW', 'WWSS', 'SWSW', 'WOWOOT',
                                'SOSSG', 'OOWOO', 'WOOW', 'SWSW', 'WOWOOT', 'WOWO', 'OWWOO', 'WWSS', 'WWWWK', 'OOSOO',
                                'OOWOO', 'WWSS', 'SOSW', 'OWWW', 'OOOOOT', 'OWOWO', 'SOWS', 'WOWO', 'OSSOO', 'OOWOO',
                                'OSSOOT', 'OWWW', 'WSSSG', 'OSSOO', 'OWWW', 'SWSW', 'OWWW', 'OWWOOT', 'WWSWK', 'SWSW',
                                'SSSSG', 'OWWOO', 'SWSW', 'OOSOOT', 'WWWWK', 'SOSW', 'SOSW', 'WWSS', 'SOSSG', 'WSSSG',
                                'SWSW', 'WWWWK', 'OSSOOT', 'WOWO', 'WWSS', 'WWSS', 'WOOW', 'OOWOOT', 'SOWS', 'OWWOO',
                                'OSSW', 'WWWWK', 'OWWW', 'OWWOOT', 'WWSS', 'SWSW', 'OSSOO', 'WSSSG', 'WSSSG', 'SWSW',
                                                                                                              'WWSS']
#determinized_short_karteninfoliste = ['SOWS', 'WWSS', 'SOSSG', 'OSSW', 'OOSOOT', 'OSSW', 'WWSWK', 'OSSW', 'WWSS', 'SWSW']
determinized_short_karteninfoliste = ['SWSW', 'OSSW', 'SOSSG', 'WWSWK', 'WWSS', 'WWSS', 'OOSOOT', 'OSSW', 'SOWS', 'OSSW']

speed_test_karteninfoliste =['OSSW', 'SWSW', 'SOSSG', 'WWSWK', 'WWSS', 'WWSS', 'OOSOOT', 'OSSW', 'SOWS', 'OSSW']

test_karteninfolist = ['SOSSG', 'OSSW', 'WWSS', 'SWSW', 'OOSOOT', 'OSSW', 'OSSW', 'SOWS', 'WWSS', 'WWSWK']

#determinized_short_karteninfoliste = ['WWSS','WWSWK']

k1 = Card('S', 'O', 'W', 'S')


def create_kartenliste(karteninfos, shuffle=True):
    """
    Zur Erstellung einer Kartenliste aus einer Liste aus Karteninfos

    :param karteninfos:     list: ['WWSWK', 'OOSOO', ...]
    :param shuffle:         bool: falls True, wird die Kartenliste gemischt, bevor sie zurueckgegeben wird
    :return:                list: Liste mit den Kartenobjekten

    """
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
        if shuffle:
            random.shuffle(l)
    return l

#Kartenliste = create_kartenliste(Karteninfos_neu)

if __name__ == "__main__":
    ka = Card("O", "S", "S", "W")
    print(ka.matrix)
    ka.rotate_right()
    print("\n", ka.matrix)
    ka.rotate_right()
    print("\n", ka.matrix)
    ka.rotate_right()
    print("\n", ka.matrix)

    random.shuffle(karteninfoliste)
    print(karteninfoliste)

    import plot_cards
    for c in determinized_karteninfoliste:
        i = list(c)

        if len(i) == 4:
            a, b, c, d, m, schild = i[0], i[1], i[2], i[3], None, False
        elif len(i) == 5:
            a, b, c, d, m, schild = i[0], i[1], i[2], i[3], i[4], False
        else:
            a, b, c, d, m, schild = i[0], i[1], i[2], i[3], i[4], True

        plot_cards.draw_card(Card(a, b, c, d, m, schild))

