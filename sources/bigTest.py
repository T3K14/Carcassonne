import unittest
import Spiel_class
from card_class import Card, Kartenliste
import Player_Class
from plot_cards import display_spielbrett_dict, draw_card


class BigTest(unittest.TestCase):

    # zum simulieren vom zufaellig karten ziehen
    #def test0(self):
    #    spiel = Spiel_class.Spiel(Kartenliste)
    #    a = spiel.draw_card()
    #    draw_card(a)

    def test1(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player_Class.Player(1)
        player2 = Player_Class.Player(2)

        k1 = Card('W', 'W', 'S', 'S')
        spiel.make_action(k1, (0, 1), 0, player1, k1.strassen[0])

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 1)
        self.assertEqual(len(spiel.alle_wiesen), 2)

        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 6)
        self.assertEqual(player2.meeples, 7)
        self.assertEqual(player1.punkte, 0)
        self.assertEqual(player2.punkte, 0)

        k2 = Card('O', 'W', 'W', 'O', 'O', True)
        spiel.make_action(k2, (1, 0), 3, player2, k2.orte[0])

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 1)
        self.assertEqual(len(spiel.alle_wiesen), 3)

        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 6)
        self.assertEqual(player2.meeples, 6)
        self.assertEqual(player1.punkte, 0)
        self.assertEqual(player2.punkte, 0)

        k3 = Card('O', 'W', 'W', 'W')
        spiel.make_action(k3, (2, 0), 1, player1, k3.orte[0])

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(len(spiel.alle_wiesen), 3)

        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 5)
        self.assertEqual(player2.meeples, 6)
        self.assertEqual(player1.punkte, 0)
        self.assertEqual(player2.punkte, 0)

        k4 = Card('W', 'W', 'W', 'W', 'K')
        spiel.make_action(k4, (1, 1), 2, player2, 'K')

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(len(spiel.alle_wiesen), 2)

        self.assertEqual(len(spiel.alle_kloester), 1)

        self.assertEqual(player1.meeples, 5)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 0)
        self.assertEqual(player2.punkte, 0)

        k5 = Card('O', 'W', 'W', 'O', 'O')
        spiel.make_action(k5, (3, 0), 3, player1)

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(len(spiel.alle_wiesen), 3)

        self.assertEqual(len(spiel.alle_kloester), 1)

        self.assertEqual(player1.meeples, 5)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 0)

        k6 = Card('S', 'W', 'S', 'W')
        spiel.make_action(k6, (0, 2), 1, player2)

        self.assertEqual(len(spiel.alle_strassen), 2)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(len(spiel.alle_wiesen), 4)

        self.assertEqual(len(spiel.alle_kloester), 1)

        self.assertEqual(player1.meeples, 5)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 0)

        k7 = Card('W', 'W', 'S', 'S')
        spiel.make_action(k7, (0, -1), 1, player1)

        self.assertEqual(len(spiel.alle_strassen), 2)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(len(spiel.alle_wiesen), 4)

        self.assertEqual(len(spiel.alle_kloester), 1)

        self.assertEqual(player1.meeples, 5)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 0)

        k8 = Card('O', 'W', 'W', 'W')
        spiel.make_action(k8, (1, -1), 0, player2)

        self.assertEqual(len(spiel.alle_strassen), 2)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(len(spiel.alle_wiesen), 4)

        self.assertEqual(len(spiel.alle_kloester), 1)

        self.assertEqual(player1.meeples, 5)
        self.assertEqual(player2.meeples, 6)
        self.assertEqual(player1.punkte, 0)
        self.assertEqual(player2.punkte, 8)

        # display_spielbrett_dict(spiel.cards_set)
        spiel.final_evaluate()

        self.assertEqual(player1.punkte, 5)
        self.assertEqual(player2.punkte, 14)

    def test2(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player_Class.Player(1)
        player2 = Player_Class.Player(2)

        k1 = Card('W', 'W', 'S', 'S')
        spiel.make_action(k1, (0, 1), 3, player1)

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 1)
        self.assertEqual(len(spiel.alle_wiesen), 2)

        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 7)
        self.assertEqual(player2.meeples, 7)
        self.assertEqual(player1.punkte, 0)
        self.assertEqual(player2.punkte, 0)

        k2 = Card('O', 'S', 'S', 'O', 'O', True)
        spiel.make_action(k2, (1, 1), 2, player2, k2.orte[0])

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(len(spiel.alle_wiesen), 2)

        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 7)
        self.assertEqual(player2.meeples, 6)
        self.assertEqual(player1.punkte, 0)
        self.assertEqual(player2.punkte, 0)

        k3 = Card('W', 'W', 'S', 'S')
        spiel.make_action(k3, (0, -1), 2, player1, k3.strassen[0])

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(len(spiel.alle_wiesen), 2)

        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 6)
        self.assertEqual(player2.meeples, 6)
        self.assertEqual(player1.punkte, 0)
        self.assertEqual(player2.punkte, 0)

        k4 = Card('S', 'O', 'W', 'S')
        spiel.make_action(k4, (1, -1), 3, player2, k4. orte[0])

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 3)
        self.assertEqual(len(spiel.alle_wiesen), 2)

        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 6)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 0)
        self.assertEqual(player2.punkte, 0)

        k5 = Card('O', 'O', 'S', 'O', 'O', True)
        wies = None
        for w in k5.wiesen:
            if w.ecken == [6]:
                wies = w
        spiel.make_action(k5, (1, 2), 0, player1, wies)

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 4)
        self.assertEqual(len(spiel.alle_wiesen), 2)

        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 5)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 0)
        self.assertEqual(player2.punkte, 0)

        k6 = Card('O', 'O', 'W', 'O', 'O', True)
        spiel.make_action(k6, (1, 0), 3, player2)

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(len(spiel.alle_wiesen), 3)

        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 5)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 0)
        self.assertEqual(player2.punkte, 0)

        k7 = Card('W', 'S', 'S', 'S')
        spiel.make_action(k7, (1, -2), 1, player1)

        self.assertEqual(len(spiel.alle_strassen), 3)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(len(spiel.alle_wiesen), 4)

        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 6)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 7)
        self.assertEqual(player2.punkte, 0)

        k8 = Card('S', 'O', 'S', 'W')
        spiel.make_action(k8, (2, 1), 2, player2, k8.strassen[0])

        self.assertEqual(len(spiel.alle_strassen), 4)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(len(spiel.alle_wiesen), 6)

        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 6)
        self.assertEqual(player2.meeples, 6)
        self.assertEqual(player1.punkte, 7)
        self.assertEqual(player2.punkte, 14)

        spiel.final_evaluate()
        self.assertEqual(player1.punkte, 10)
        self.assertEqual(player2.punkte, 15)

if __name__ == '__main__':
    unittest.main()