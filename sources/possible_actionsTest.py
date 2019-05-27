import unittest

from Ort import Ort
from Strasse import Strasse
from Wiese import Wiese
import card_class
import Spiel_class
from Player_Class import Player

Kartenliste = []

class PossibleActionsTest(unittest.TestCase):

    def test_1(self):
        spiel = Spiel_class.Spiel(Kartenliste)

        # startvorgaben
        card1 = card_class.Card("W", "O", "O", "W", "O")
        spiel.cards_set.update({(1, 1): card1})

        ort1 = Ort((1, 1), [1, 2])
        wiese2 = Wiese((1, 1), [4, 5, 7])
        spiel.alle_orte.append(ort1)
        spiel.alle_wiesen.append(wiese2)

        spiel.cards_set[(1, 1)].ecken = {4: wiese2, 5: wiese2, 6: None, 7: wiese2}
        spiel.cards_set[(1, 1)].kanten = {0: None, 1: ort1, 2: ort1, 3: None}

        spiel.possible_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 2), (2, 1)]

        k = card_class.Card("S", "O", "O", "S", "O")

        goal = [(0, -1, 0, k.strassen[0]), (0, -1, 0, k.orte[0]), (0, -1, 1, k.strassen[0]),
                (0, -1, 1, k.orte[0]), (2, 1, 1, k.strassen[0]), (2, 1, 1, k.orte[0]),
                (2, 1, 2, k.strassen[0]), (2, 1, 2, k.orte[0]), (1, 0, 2, k.orte[0]),
                (1, 0, 2, k.strassen[0]), (0, -1, 0, None), (0, -1, 1, None), (1, 0, 2, None), (2, 1, 1, None), (2, 1, 2, None),
                ]

        player1 = Player(1)
        pos_act = spiel.calculate_possible_actions(k, player1)
        self.assertEqual(25, len(pos_act))

        for tup in spiel.calculate_possible_actions(k, Player(1)):
            print(tup)
            self.assertTrue(tup in goal)

    def test_2(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        card0 = card_class.Card("S", "O", "S", "W")
        card1 = card_class.Card("S", "S", "W", "W")
        card2 = card_class.Card("O", "O", "O", "O", "O", True)
        card3 = card_class.Card("W", "O", "O", "W")
        card4 = card_class.Card("W", "O", "W", "O")

        k = card_class.Card("O", "S", "S", "O", "O", True)

        strasse0 = Strasse((0, 0), [0, 2])
        strasse0.koordinaten_plus_oeffnungen.update({(0, -1): [1]})
        strasse0.koordinaten_plus_oeffnungen[(0, 0)].remove(2)

        ort0 = Ort((0, 0), [1])
        ort1 = Ort((1, 1), [1])
        ort2 = Ort((2, 0), [1])
        ort0.koordinaten_plus_oeffnungen.update({(1, 0): 2, (1, 1): [], (2, 0): []})
        ort0.koordinaten_plus_oeffnungen[(0, 0)].remove(1)

        # meeple in ort2
        ort2.besitzer = Player(2)

        spiel.cards_set = {(0, 0): card0, (0, -1): card1, (1, 0): card2, (1, 1): card3, (2, 0): card4}
        spiel.possible_coordinates = [(0, 1), (-1, 0), (-1, -1), (0, -2), (1, -1), (2, -1), (3, 0), (2, 1), (1, 2)]

        goal = [(1, -1, 1, k.strassen[0]), (1, -1, 1, k.orte[0], (1, -1, 1, None)), (3, 0, 0, None),
                (3, 0, 0, k.strassen[0]), (3, 0, 3, None), (3, 0, 3, k.strassen[0])]

if __name__ == "__main__":
    unittest.main()
