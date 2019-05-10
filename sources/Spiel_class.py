from KarteMod import Karte

from Ort import Ort
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese


class Spiel:
    def __init__(self, card_list):
        self.cards_left = card_list

        # list of coordinates already blocked
        self.unavailable_coordinates = [(0, 0)]

        # dict of cards beeing laid and their coordinates
        self.cards_set = {(0, 0): Karte("S", "O", "S", "W")}

        # possible next coordinates
        self.possible_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        self.alle_orte = {"Ort_0": Ort((0, 0), [1])}
        self.alle_strassen = {"Strasse_0": Strasse((0, 0), [0, 2])}
        self.alle_kloester = {}
        self.alle_wiesen = {"Wiese_0": Wiese((0, 0), [4, 7]), "Wiese_1": Wiese((0, 0), [5, 6])}

    def draw_card(self):
        """from drawing the next card randomly"""
        pass

    def make_action(self):
        """for setting a card and placing a meeple"""

        possible_actions = []
        pass

    def update_board(self):
        """for updating all lists after making an action

        VIELLEICHT IN MAKE_ACTION EINBAUEN"""
        pass

    def final_evaluate(self):
        """for counting if the game is finished to declare the winning player"""
        pass


if __name__ == "__main__":
    c = Karte("O", "W", "S", "S")
    print(c.orte)
    print(isinstance(c, Karte))
    pass
