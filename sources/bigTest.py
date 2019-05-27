import unittest
import Spiel_class
from card_class import Card
import Player_Class
from plot_cards import display_spielbrett_dict, draw_card

Kartenliste = []

class BigTest(unittest.TestCase):



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

        #display_spielbrett_dict(spiel.cards_set)

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

    def test3(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player_Class.Player(1)
        player2 = Player_Class.Player(2)

        k1 = Card('O', 'W', 'W', 'W')
        spiel.make_action(k1, (1, 0), 3, player1, k1.orte[0])

        self.assertEqual(len(spiel.cards_set), 2)
        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 1)
        self.assertEqual(len(spiel.alle_wiesen), 3)
        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 7)
        self.assertEqual(player2.meeples, 7)
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 0)

        k2 = Card('W', 'W', 'S', 'S')
        spiel.make_action(k2, (0, 1), 0, player2, k2.strassen[0])

        self.assertEqual(len(spiel.cards_set), 3)

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 1)
        self.assertEqual(len(spiel.alle_wiesen), 3)
        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 7)
        self.assertEqual(player2.meeples, 6)
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 0)

        k3 = Card('O', 'S', 'S', 'O', 'O', True)
        spiel.make_action(k3, (0, -1), 3, player1, k3.orte[0])

        self.assertEqual(len(spiel.cards_set), 4)

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 2)
        self.assertEqual(len(spiel.alle_wiesen), 3)
        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 6)
        self.assertEqual(player2.meeples, 6)
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 0)

        k4 = Card('O', 'O', 'S', 'O', 'O', True)
        spiel.make_action(k4, (-1, 1), 3, player2, k4.orte[0])

        self.assertEqual(len(spiel.cards_set), 5)

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 3)
        self.assertEqual(len(spiel.alle_wiesen), 3)
        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 6)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 0)

        k5 = Card('W', 'O', 'O', 'W')
        ort1 = None
        for o in k5.orte:
            if o.kanten == [1]:
                ort1 = o
        spiel.make_action(k5, (-1, -1), 0, player1, ort1)

        self.assertEqual(len(spiel.cards_set), 6)

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 4)
        self.assertEqual(len(spiel.alle_wiesen), 4)
        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 5)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 0)

        k6 = Card('S', 'W', 'S', 'W')
        spiel.make_action(k6, (1, -1), 3, player2)

        self.assertEqual(len(spiel.cards_set), 7)

        self.assertEqual(len(spiel.alle_strassen), 1)
        self.assertEqual(len(spiel.alle_orte), 4)
        self.assertEqual(len(spiel.alle_wiesen), 3)
        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 5)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 0)

        #display_spielbrett_dict(spiel.cards_set)

        k7 = Card('W', 'S', 'S', 'S', 'G')
        strasse1 = None
        for s in k7.strassen:
            if s.kanten == [3]:
                strasse1 = s
        spiel.make_action(k7, (2, 0), 3, player1, strasse1)

        self.assertEqual(len(spiel.cards_set), 8)

        self.assertEqual(len(spiel.alle_strassen), 4)
        self.assertEqual(len(spiel.alle_orte), 4)
        self.assertEqual(len(spiel.alle_wiesen), 5)
        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 4)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 0)

        k8 = Card('O', 'S', 'S', 'W')
        spiel.make_action(k8, (-1, 2), 2, player2)

        self.assertEqual(len(spiel.cards_set), 9)

        self.assertEqual(len(spiel.alle_strassen), 5)
        self.assertEqual(len(spiel.alle_orte), 4)
        self.assertEqual(len(spiel.alle_wiesen), 7)
        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 4)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 0)

        k9 = Card('W', 'S', 'S', 'S', 'G')
        strasse2 = None
        for s in k9.strassen:
            if s.kanten == [1]:
                strasse2 = s
        spiel.make_action(k9, (-2, 2), 0, player1, strasse2)

        self.assertEqual(len(spiel.cards_set), 10)

        self.assertEqual(len(spiel.alle_strassen), 7)
        self.assertEqual(len(spiel.alle_orte), 4)
        self.assertEqual(len(spiel.alle_wiesen), 8)
        self.assertEqual(len(spiel.alle_kloester), 0)

        self.assertEqual(player1.meeples, 3)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 0)

        k10 = Card('W', 'W', 'W', 'W', 'K')
        spiel.make_action(k10, (1, 1), 2, player2, 'K')

        self.assertEqual(len(spiel.cards_set), 11)

        self.assertEqual(len(spiel.alle_strassen), 7)
        self.assertEqual(len(spiel.alle_orte), 4)
        self.assertEqual(len(spiel.alle_wiesen), 8)
        self.assertEqual(len(spiel.alle_kloester), 1)

        self.assertEqual(player1.meeples, 3)
        self.assertEqual(player2.meeples, 4)
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 0)

        k11 = Card('W', 'O', 'W', 'O', 'O', True)
        spiel.make_action(k11, (-2, 3), 0, player1)

        self.assertEqual(len(spiel.cards_set), 12)

        self.assertEqual(len(spiel.alle_strassen), 7)
        self.assertEqual(len(spiel.alle_orte), 5)
        self.assertEqual(len(spiel.alle_wiesen), 9)
        self.assertEqual(len(spiel.alle_kloester), 1)

        self.assertEqual(player1.meeples, 3)
        self.assertEqual(player2.meeples, 4)
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 0)

        k12 = Card('O', 'W', 'W', 'O', 'O')
        spiel.make_action(k12, (-1, 0), 0, player2)

        self.assertEqual(len(spiel.cards_set), 13)

        self.assertEqual(len(spiel.alle_strassen), 7)
        self.assertEqual(len(spiel.alle_orte), 5)
        self.assertEqual(len(spiel.alle_wiesen), 8)
        self.assertEqual(len(spiel.alle_kloester), 1)

        self.assertEqual(player1.meeples, 3)
        self.assertEqual(player2.meeples, 4)
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 0)

        k13 = Card('W', 'W', 'S', 'S')
        spiel.make_action(k13, (2, -1), 1, player1)

        #display_spielbrett_dict(spiel.cards_set)

        self.assertEqual(len(spiel.cards_set), 14)

        self.assertEqual(len(spiel.alle_strassen), 6)
        self.assertEqual(len(spiel.alle_orte), 5)
        self.assertEqual(len(spiel.alle_wiesen), 7)
        self.assertEqual(len(spiel.alle_kloester), 1)

        self.assertEqual(player1.meeples, 4)
        self.assertEqual(player2.meeples, 5)
        self.assertEqual(player1.punkte, 11)
        self.assertEqual(player2.punkte, 7)

        k14 = Card('S', 'W', 'S', 'W')
        spiel.make_action(k14, (3, 0), 1, player2, k14.strassen[0])

        self.assertEqual(len(spiel.cards_set), 15)

        self.assertEqual(len(spiel.alle_strassen), 6)
        self.assertEqual(len(spiel.alle_orte), 5)
        self.assertEqual(len(spiel.alle_wiesen), 7)
        self.assertEqual(len(spiel.alle_kloester), 1)

        self.assertEqual(player1.meeples, 4)
        self.assertEqual(player2.meeples, 4)
        self.assertEqual(player1.punkte, 11)
        self.assertEqual(player2.punkte, 7)

    def test4(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player_Class.Player(1)
        player2 = Player_Class.Player(2)

        k1 = Card('O', 'O', 'W', 'O', 'O')
        spiel.make_action(k1, (1, 0), 2, player1)

        k2 = Card('O', 'S', 'S', 'O', 'O')
        spiel.make_action(k2, (1, -1), 1, player2)

        k3 = Card('O', 'W', 'W', 'O', 'O')
        spiel.make_action(k3, (2, -1), 0, player1)

        k4 = Card('O', 'O', 'O', 'O', 'O')
        spiel.make_action(k4, (2, 0), 0, player2)


if __name__ == '__main__':
    unittest.main()