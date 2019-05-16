import unittest

from Ort import Ort
from Strasse import Strasse
import card_class
import Spiel_class
from Player_Class import Player


class PossibleActionsTest(unittest.TestCase):

    def test_1(self):
        spiel = Spiel_class.Spiel(card_class.Kartenliste)

        # startvorgaben
        card0 = card_class.Card("S", "O", "S", "W")
        card1 = card_class.Card("W", "O", "O", "W", "O")
        strasse0 = Strasse((0, 0), [0, 2])
        ort0 = Ort((0, 0), [1])
        ort1 = Ort((1, 1), [1, 2])
        card0.kanten = {0: strasse0, 1: ort0, 2: strasse0, 3: None}
        card1.kanten = {0: None, 1: ort1, 2: ort1, 3: None}
        spiel.alle_orte = [ort0, ort1]
        spiel.alle_strassen = [strasse0]

        spiel.cards_set = {(0, 0): card0, (1, 1): card1}
        spiel.possible_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 2), (2, 1)]

        k = card_class.Card("S", "O", "O", "S", "O")

        goal = [(0, -1, 0, k.strassen[0]), (0, -1, 0, k.orte[0]), (0, -1, 1, k.strassen[0]),
                (0, -1, 1, k.orte[0]), (2, 1, 1, k.strassen[0]), (2, 1, 1, k.orte[0]),
                (2, 1, 2, k.strassen[0]), (2, 1, 2, k.orte[0]), (1, 0, 2, k.orte[0]),
                (1, 0, 2, k.strassen[0])]

        self.assertEqual(len(goal), len(spiel.calculate_possible_actions(k, Player(1))))

        for tup in spiel.calculate_possible_actions(k, Player(1)):
            print(tup)
            self.assertTrue(tup in goal)

    def test_2(self):
        spiel = Spiel_class.Spiel(card_class.Kartenliste)
        card0 = card_class.card("S", "O", "S", "W")
        card1 = card_class.card("S", "S", "W", "W")
        card2 = card_class.card("O", "O", "O", "O", "O", True)
        card3 = card_class.card("W", "O", "O", "W")
        card4 = card_class.card("W", "O", "W", "O")

        card_new = card_class.card("O", "S", "S", "O", "O", True)

if __name__ == "__main__":
    unittest.main()
