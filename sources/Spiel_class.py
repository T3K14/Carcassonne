from KarteMod import Karte

from Ort import Ort
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese

from copy import deepcopy
from rotate2 import rotate_info_right


class Spiel:
    def __init__(self, card_list):
        self.cards_left = card_list

        # dict of cards beeing laid and their coordinates
        self.cards_set = {(0, 0): Karte("S", "O", "S", "W")}

        # list of coordinates already blocked
        self.unavailable_coordinates = [(0, 0)]

        # possible next coordinates
        self.possible_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        self.alle_orte = {"Ort_0": Ort((0, 0), [1])}
        self.alle_strassen = {"Strasse_0": Strasse((0, 0), [0, 2])}
        self.alle_kloester = {}
        self.alle_wiesen = {"Wiese_0": Wiese((0, 0), [4, 7]), "Wiese_1": Wiese((0, 0), [5, 6])}

    def draw_card(self):
        """from drawing the next card randomly"""
        pass

    def calculate_possible_actions(self, card, player):
        """checkt, ob und wie karte an jede freie stelle gelegt werden kann,
            returned liste mit tupel bestehend aus moeglicher anlegestelle und anzahl von rotationen die dafür noetig sind
            nimmt eine Karte an, sowie liste möglicher anlegestellen und dictionary von gelegten Karten
            """

        possible_actions = []

        # ich will hier nicht wirklich was an der Karte rotieren, nur um zu schauen, wo was passt
        info = card.info[:]

        d = {0: 2, 1: 3, 2: 0, 3: 1}

        for x, y in self.possible_coordinates:

            # zuerst alle nachbarkarten finden und speichern wo sie relatativ zu eigener Karte liegen
            # das sollte woanders gemacht werden, da man sonst fuer jede neu gezogene Karte immer wieder die umgebung
            # untersucht, obwohl man das schon x mal davor gemacht hat
            nachbar_koordinaten = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
            nachbar_karten = []

            for relative_pos, nkoo in enumerate(nachbar_koordinaten):
                for koord_von_karte in self.cards_set:
                    if koord_von_karte == nkoo:
                        nachbar_karten.append((relative_pos, self.cards_set[koord_von_karte].info[d[relative_pos]]))

                        # nicht 100 pro sicher, aber da dann schon karte an nkoo gefunden wurde, kann da ja keine weitere mehr sein
                        continue

            for i in range(4):

                # wenn pro Rotation nach allen Ueberpruefungen immer noch True, dann hinzufuegen
                b = True
                for n in nachbar_karten:
                    if b:
                        b = b and info[n[0]] == n[1]
                    else:
                        break

                if b:
                    possible_actions.append((x, y, i))

                # eins weiter rotieren
                info = rotate_info_right(info)

        # jetzt Meeples
        if player.meeples > 0:
            pass

        return possible_actions


    def make_action(self, card, koordinates, rotations, meeple_position=None):
        """for setting a card and placing a meeple"""

        # if action_is_valid() muss im Spielprogramm dann davor!!!!!!
        # fuer human spieler: if "action" in possible actions

        # entprechend der Rotationen Karte drehen
        for i in range(rotations):
            card.rotate_right()

        # cards_st updaten
        self.cards_set.update({(koordinates[0], koordinates[1]): Karte})

        # wenn auf Karte Orte, Strassen oder Wiesen sind, muessen globale Aequivalente geupdatet werden
        if len(card.orte) > 0:
            self.update_all_orte(card, koordinates[0], koordinates[1], meeple_position)
        if len(card.strassen) > 0:
            self.update_all_strassen(card, koordinates[0], koordinates[1], meeple_position)
        if len(card.wiesenKarte) > 0:
            self.update_all_wiesen(card, koordinates[0], koordinates[1], meeple_position)

        # kloester muessen moeglicherweise immer geupdatet werden, da sie von der Anzahl an Umgebungskarten abhaengen
        self.update_all_kloester(card, koordinates[0], koordinates[1], meeple_position)

        # possible_coordinates und unavailable coordinates updaten
        self.unavailable_coordinates.append((koordinates[0], koordinates[1]))

        for i, (v, w) in enumerate(self.possible_coordinates):
            if (koordinates[0], koordinates[1]) == (v, w):
                del self.possible_coordinates[i]

                # neue possible coordinates hinzufuegen
                for (a, b) in [(koordinates[0], koordinates[1] - 1), (koordinates[0], koordinates[1] + 1), (koordinates[0] - 1, koordinates[1]), (koordinates[0] + 1, koordinates[1])]:
                    if (a, b) not in self.possible_coordinates and (a, b) not in self.unavailable_coordinates:
                        self.possible_coordinates.append((a, b))

    def update_all_orte(self, card, x, y, meeple_position):

        ### finde für jeden Ort auf Karte alle globale Orte, die mit diesem Ort wechselwirken und wie sie wechselwirken

        ### update alle Orte, inklusive Meeples

        pass

    def update_all_strassen(self, card, x, y, meeple_position):
        pass

    def update_all_wiesen(self, card, x, y, meeple_position):
        pass

    def update_all_kloester(self, card, x, y, meeple_position):
        pass

    def final_evaluate(self):
        """for counting if the game is finished to declare the winning player"""
        pass


if __name__ == "__main__":
    c = Karte("O", "W", "S", "S")
    print(c.orte)
    print(isinstance(c, Karte))
    pass
