import unittest

from Ort import Ort
from Strasse import Strasse
from Wiese import Wiese
import card_class
import Spiel_class
from Player_Class import Player
from card_class import Card
from plot_cards import display_spielbrett_dict, draw_card

Kartenliste = card_class.create_kartenliste(card_class.karteninfoliste)

class evaluationTest(unittest.TestCase):

    def test1(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        k1 = Card('O', 'W', 'W', 'O', 'O')
        spiel.make_action(player2, k1, 1, 0, 0, k1.orte[0])

        x, y = player1.punkte, player2.punkte

        spiel.final_evaluate()

        self.assertEqual(player1.punkte, 0)
        self.assertEqual(player2.punkte, 2)

        player1.punkte, player2.punkte = x, y

        k2 = Card('O', 'W', 'W', 'W')
        spiel.make_action(player1, k2, 2, 0, 1, k2.orte[0])

        x, y = player1.punkte, player2.punkte

        spiel.final_evaluate()

        self.assertEqual(player1.punkte, 1)
        self.assertEqual(player2.punkte, 2)

        player1.punkte, player2.punkte = x, y

        k3 = Card('O', 'O', 'S', 'O', 'O', True)
        spiel.make_action(player2, k3, 1, 1, 2, k3.strassen[0])

        x, y = player1.punkte, player2.punkte

        spiel.final_evaluate()

        self.assertEqual(player1.punkte, 1)
        self.assertEqual(player2.punkte, 5)

        player1.punkte, player2.punkte = x, y

        k4 = Card('S', 'O', 'S', 'S', 'G')
        wiese = None
        for w in k4.wiesen:
            if w.ecken == [5, 6]:
                wiese = w
                break

        spiel.make_action(player1, k4, 3, 0, 2, wiese)

        x, y = player1.punkte, player2.punkte

        spiel.final_evaluate()

        self.assertEqual(player1.punkte, 7)
        self.assertEqual(player2.punkte, 5)

        player1.punkte, player2.punkte = x, y

        k5 = Card('O', 'W', 'W', 'O', 'O')
        spiel.make_action(player2, k5, 2, 1, 0, k5.wiesen[0])

        x, y = player1.punkte, player2.punkte

        spiel.final_evaluate()

        self.assertEqual(player1.punkte, 7)
        self.assertEqual(player2.punkte, 9)

        player1.punkte, player2.punkte = x, y

        k6 = Card('W', 'W', 'S', 'S')
        spiel.make_action(player1, k6, 3, 1, 3, k6.strassen[0])

        x, y = player1.punkte, player2.punkte

        spiel.final_evaluate()

        self.assertEqual(player1.punkte, 9)
        self.assertEqual(player2.punkte, 9)

        player1.punkte, player2.punkte = x, y


if __name__ == '__main__':
    unittest.main()