import Spiel_class
import card_class
import Player_Class
import unittest
from Strasse import Strasse
import plot_cards
from Ort import Ort

class MakeActionTest(unittest.TestCase):

    def test_1(self):
        spiel = Spiel_class.Spiel(card_class.Kartenliste)

        # alle_orte nach Zug
        goal = [spiel.alle_orte[0]]
        # alle strassen nach Zug
        goal2 = [spiel.alle_strassen[0], Strasse((1, 0), [1, 2])]

        k = card_class.Card("O", "S", 'S', 'O', 'O')
        spiel.make_action(k, (1, 0), 0, Player_Class.Player(1), None)

        self.assertEqual(len(spiel.alle_orte), len(goal))
        self.assertEqual(len(goal2), len(spiel.alle_strassen))
        self.assertEqual(sorted(k.kanten), sorted({0: spiel.cards_set[(0, 0)].kanten[1], 1: k.kanten[1], 2: k.kanten[2], 3: spiel.cards_set[(0, 0)].kanten[1]}))

        for o in spiel.alle_orte:
            a = True
            for ort in goal:
                a = a or o == ort
            self.assertTrue(a)
        for s in spiel.alle_strassen:
            a = True
            for strasse in goal2:
                a = a or s == strasse
            self.assertTrue(a)

    def test_2(self):
        spiel = Spiel_class.Spiel(card_class.Kartenliste)
        player1 = Player_Class.Player(1)
        player2 = Player_Class.Player(2)

        k1 = card_class.Card('O', 'W', 'S', 'S')
        spiel.make_action(k1, (0, 1), 0, player1, k1.strassen[0])

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(player1.meeples, 6)

        k2 = card_class.Card('O', 'W', 'W', 'O', 'O')
        spiel.make_action(k2, (1, 1), 2, player2, k2.orte[0])

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 3)
        self.assertEqual(player2.meeples, 6)

        k3 = card_class.Card('W', 'S', 'S', 'S', 'G')
        spiel.make_action(k3, (0, -1), 3, player1, None)

        self.assertEqual(len(spiel.alle_strassen), 3)
        self.assertEqual(len(spiel.alle_orte), 3)

        k4 = card_class.Card('O', 'S', 'S', 'O', 'O', True)
        spiel.make_action(k4, (1, -1), 1, player2, None)

        self.assertEqual(len(spiel.alle_strassen), 3)
        self.assertEqual(len(spiel.alle_orte), 4)

        k5 = card_class.Card('O', 'O', 'O', 'O', 'O', True)
        spiel.make_action(k5, (1, 0), 1, player1, None)

        self.assertEqual(len(spiel.alle_strassen), 3)
        self.assertEqual(len(spiel.alle_orte), 2)

    def test_3(self):
        spiel = Spiel_class.Spiel(card_class.Kartenliste)
        player1 = Player_Class.Player(1)
        player2 = Player_Class.Player(2)

        k1 = card_class.Card('O', 'W', 'W', 'W')
        spiel.make_action(k1, (1, 0), 3, player1, k1.orte[0])

        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player1.meeples, 7)

    def test_4(self):
        spiel = Spiel_class.Spiel(card_class.Kartenliste)
        player1 = Player_Class.Player(1)
        player2 = Player_Class.Player(2)

        k1 = card_class.Card('O', 'W', 'W', 'O', 'O', True)
        #plot_cards.draw_card(k1)
        spiel.make_action(k1, (1, 0), 0, player1, k1.orte[0])

        self.assertEqual(spiel.alle_orte[0].besitzer, player1)
        self.assertEqual(len(spiel.alle_orte[0].meeples), 1)

        k2 = card_class.Card('O', 'O', 'W', 'O', 'O')
        #plot_cards.draw_card(k2)
        spiel.make_action(k2, (2, 0), 1, player2, k2.orte[0])

        self.assertEqual(spiel.alle_orte[-1].besitzer, player2)
        self.assertEqual(len(spiel.alle_orte[-1].meeples), 1)


        k3 = card_class.Card('O', 'W', 'W', 'O', 'O')
        spiel.make_action(k3, (1, 1), 2, player1)

        k4 = card_class.Card('O', 'W', 'W', 'O', 'O')
        spiel.make_action(k4, (2, 1), 3, player2)

        print('end')

if __name__ == '__main__':
    unittest.main()