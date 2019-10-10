import unittest

from Ort import Ort
from Strasse import Strasse
from Wiese import Wiese
import card_class
import Spiel_class
from Player_Class import Player
from card_class import Card
from plot_cards import display_spielbrett_dict, draw_card

class possible_actionsTest(unittest.TestCase):

    def test1(self):
        player1 = Player(1)
        player2 = Player(2)

        spiel = Spiel_class.Spiel([])

        k1 = Card('S', 'W', 'S', 'W')
        pos = spiel.calculate_possible_actions(k1, player1)

        self.assertEqual(12, len(pos))


if __name__ == '__main__':
    unittest.main()