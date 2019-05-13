import numpy as np
from Ort import Ort_auf_Karte
#from strasse, etc
from rotate2 import rotate_info_right, rotate_list_right, rotate_matrix_right

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

        for position, status in enumerate(self.info):
            if status == "S":
                self.strassen_kanten.append(position)
            elif status == "O":
                self.orte_kanten.append(position)
            else:
                self.wiesen_kanten.append(position)

        self.create_matrix()

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

        self.wiesen = []
        for position, status in enumerate(self.info[:-1]):
            if status == "W":
                self.wiesen.append(position)

    def rotate_right(self):
        self.info = rotate_info_right(self.info)
        self.strassen_kanten = rotate_list_right(self.strassen_kanten)
        self.orte_kanten = rotate_list_right(self.orte_kanten)
        self.wiesen_kanten = rotate_list_right(self.wiesen_kanten)
        self.matrix = rotate_matrix_right(self.matrix)

        # auch noch fuer orte, strassen, wiesen auf karte die kanten rotieren


    def create_orte(self, name):
        pass

    def delete_ort(self):
        pass

def create_kartenliste():
    anzahl_orte = -1
    anzahl_strassen = 0
    anzahl_kloester = 0
    anzahlWiesen = 1
    ww = False

    ortswert = 2

    pass

if __name__ == "__main__":
    k = Card("O", "S", "S", "W")
    print(k.matrix)
    k.rotate_right()
    print("\n", k.matrix)
    k.rotate_right()
    print("\n", k.matrix)
    k.rotate_right()
    print("\n", k.matrix)

