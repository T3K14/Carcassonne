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

        spiel.make_action(card1, (-1, 0), 1, player1, 'K')

        self.assertEqual(player1.meeples, 6)
        self.assertEqual(len(spiel.alle_kloester), 1)

    def test_2(self):
        spiel = Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        card1 = Card('W', 'W', 'S', 'S')
        spiel.make_action(card1, (0, -1), 1, player1)

        card2 = Card('O', 'S', 'S', 'O', 'O')
        spiel.make_action(card2, (0, 1), 1, player2)

        card3 = Card('O', 'S', 'S', 'W')
        spiel.make_action(card3, (-1, 1), 3, player1)

        card4 = Card('S', 'W', 'S', 'W')
        spiel.make_action(card4, (-1, -1), 1, player2)

        card5 = Card('S', 'O', 'W', 'S')
        spiel.make_action(card5, (-2, -1), 1, player1)

        card6 = Card('O', 'W', 'W', 'W')
        spiel.make_action(card6, (-2, 1), 1, player2)

        card7 = Card('W', 'W', 'S', 'W', 'K')
        spiel.make_action(card7, (-2, 0), 0, player1, 'K')

        self.assertEqual(len(spiel.alle_kloester), 1)
        self.assertEqual(player1.meeples, 6)

        card8 = Card('W', 'W', 'W', 'W', 'K')
        spiel.make_action(card8, (-1, 0), 0, player2, 'K')

        self.assertEqual(len(spiel.alle_kloester), 1)
        self.assertEqual(player2.meeples, 7)

        plot_cards.display_spielbrett_dict(spiel.cards_set)

if __name__ == '__main__':
    unittest.main()