from KarteMod import Karte

from Ort import Ort
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese


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

    def make_action(self, card, koordinates, rotations, meeple_position=None):
        """for setting a card and placing a meeple"""

        # if action_is_valid() muss im Spielprogramm dann davor!!!!!!

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
