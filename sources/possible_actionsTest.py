import unittest

import card_class
import Spiel_class
from Player_Class import Player

spiel = Spiel_class.Spiel(card_class.Kartenliste)

class possible_actionsTest(unittest.TestCase):

    def test_1(self):
        spiel.cards_set = {(0, 0): card_class.Card("S", "O", "S", "W"), (1, 1): card_class.Card("W", "O", "O", "W","O")}
        spiel.possible_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 2), (2, 1)]

        k = card_class.Card("S", "O", "O", "S", "O")

        goal = [(0, -1, 0), (0, -1, 1), (2, 1, 1), (2, 1, 2), (1, 0, 2)]
        # self.assertEqual(calculate_possible_actions(Karte("S", "O", "O", "S", "O"), possible_coordinates, cards_set), [(0, -1, 0), (0, -1, 1), (2, 1, 1), (2, 1, 2), (1, 0, 2)])
        self.assertEqual(len(goal), len(spiel.calculate_possible_actions(k, Player(0))))

        self.assertEqual(sorted(goal), sorted(spiel.calculate_possible_actions(card_class.Card("S", "O", "O", "S", "O"), Player(0))))


if __name__ == "__main__":
    unittest.main()
