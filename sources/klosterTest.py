import unittest
from Spiel_class import Spiel
from card_class import Card, create_kartenliste, karteninfoliste
from Player_Class import Player
import plot_cards


Kartenliste = create_kartenliste(karteninfoliste)
class KlosterTest(unittest.TestCase):

    def test_1(self):
        spiel = Spiel(Kartenliste)
        card1 = Card('W', 'W', 'W', 'W', 'K')
        player1 = Player(1)

        spiel.make_action(player1, card1, -1, 0, 1, 'k')

        self.assertEqual(player1.meeples, 6)
        self.assertEqual(len(spiel.alle_kloester), 1)

    def test_2(self):
        spiel = Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        card1 = Card('W', 'W', 'S', 'S')
        spiel.make_action(player1, card1, 0, -1, 1)

        card2 = Card('O', 'S', 'S', 'O', 'O')
        spiel.make_action(player2, card2, 0, 1, 1)

        card3 = Card('O', 'S', 'S', 'W')
        spiel.make_action(player1, card3, -1, 1, 3)

        card4 = Card('S', 'W', 'S', 'W')
        spiel.make_action(player2, card4, -1, -1, 1)

        card5 = Card('S', 'O', 'W', 'S')
        spiel.make_action(player1, card5, -2, -1, 1)

        card6 = Card('O', 'W', 'W', 'W')
        spiel.make_action(player2, card6, -2, 1, 1)

        card7 = Card('W', 'W', 'S', 'W', 'K')
        spiel.make_action(player1, card7, -2, 0, 0, 'k')

        self.assertEqual(len(spiel.alle_kloester), 1)
        self.assertEqual(player1.meeples, 6)

        card8 = Card('W', 'W', 'W', 'W', 'K')
        spiel.make_action(player2, card8, -1, 0, 0, 'k')

        self.assertEqual(len(spiel.alle_kloester), 1)
        self.assertEqual(player2.meeples, 7)

        #plot_cards.display_spielbrett_dict(spiel.cards_set)

    def test3(self):
        spiel = Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        k1 = Card('W', 'W', 'W', 'W', 'K')
        spiel.make_action(player1, k1, -1, 0, 0, 'k')

        k2 = Card('W', 'W', 'S', 'W', 'K')
        spiel.make_action(player2, k2, -1, 1, 1, 'k')

        #plot_cards.display_spielbrett_dict(spiel.cards_set)

        spiel.final_evaluate()

        self.assertEqual(player1.punkte, 3)
        self.assertEqual(player2.punkte, 3)

if __name__ == '__main__':
    unittest.main()