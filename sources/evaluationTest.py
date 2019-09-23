import unittest

from Ort import Ort
from Strasse import Strasse
from Wiese import Wiese
import card_class
import Spiel_class
from Player_Class import Player
from card_class import Card, speed_test_karteninfoliste
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

        #display_spielbrett_dict(spiel.cards_set)

        k6 = Card('W', 'W', 'S', 'S')
        spiel.make_action(player1, k6, 3, 1, 3, k6.strassen[0])

        x, y = player1.punkte, player2.punkte

        spiel.final_evaluate()

        self.assertEqual(player1.punkte, 9)
        self.assertEqual(player2.punkte, 9)

        player1.punkte, player2.punkte = x, y

    def test2(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        k1 = Card('W', 'S', 'S', 'W')
        spiel.make_action(player1, k1, 0, 1, 1, k1.strassen[0])

        k2 = Card("S", 'W', 'S', 'W')
        spiel.make_action(player2, k2, -1, 0, 0, k2.strassen[0])


        k3 = Card('W', 'S', 'S', 'W')
        spiel.make_action(player1, k3, -1, 1, 0, None)

        # display_spielbrett_dict(spiel.cards_set)

        spiel.final_evaluate()

        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player2.punkte, 4)

    def test3(self):
        spiel = Spiel_class.Spiel(card_class.create_kartenliste(['SOWS', 'SWSW', 'WWSS', 'WWSWK', 'OOSOOT', 'OSSW', 'SOSSG', 'OSSW', 'WWSS', 'OSSW'], False))
        player1 = Player(1)
        player2 = Player(2)

        k1 = spiel.cards_left.pop(0)
        spiel.make_action(player2, k1, 1, 0, 2, k1.orte[0])

        k2 = spiel.cards_left.pop(0)
        spiel.make_action(player1, k2, 2, 0, 1, k2.strassen[0])

        k3 = spiel.cards_left.pop(0)
        spiel.make_action(player2, k3, 0, 1, 3, k3.strassen[0])

        k4 = spiel.cards_left.pop(0)
        spiel.make_action(player1, k4, 1, -1, 2, 'k')

        k5 = spiel.cards_left.pop(0)
        spiel.make_action(player2, k5, 3, 0, 1, k5.orte[0])

        k6 = spiel.cards_left.pop(0)
        spiel.make_action(player1, k6, 1, -2, 1, k6.strassen[0])

        k7 = spiel.cards_left.pop(0)

        strasse = None
        for s in k7.strassen:
            if s.kanten == [0]:
                strasse = s

        spiel.make_action(player2, k7, 3, 1, 1, strasse)

        k8 = spiel.cards_left.pop(0)
        spiel.make_action(player1, k8, 2, -2, 3, k8.orte[0])

        k9 = spiel.cards_left.pop(0)

        w = [wi for wi in k9.wiesen if wi.ecken == [7]][0]
        spiel.make_action(player2, k9,  1, -3, 2, w)

        #display_spielbrett_dict(spiel.cards_set)

        k10 = spiel.cards_left.pop(0)
        spiel.make_action(player1, k10, 0, -2, 0, k10.orte[0])

        spiel.final_evaluate()

        self.assertEqual(player1.punkte, 19)
        self.assertEqual(player2.punkte, 16)

    def test4(self):
        spiel = Spiel_class.Spiel(card_class.create_kartenliste(['OSSW', 'SWSW', 'SOSSG', 'WWSWK', 'WWSS', 'WWSS', 'OOSOOT', 'OSSW', 'SOWS', 'OSSW'], False))
        player1 = Player(1)
        player2 = Player(2)

        k1 = Card('O', 'S', 'S', 'W')
        spiel.make_action(player1, k1, 1, 0, 3)

        k2 = Card('W', 'W', 'S', 'W', 'K')
        spiel.make_action(player2, k2, 1, -1, 1, 'k')

        k3 = Card('S', 'O', 'W', 'S')
        spiel.make_action(player1, k3, 0, 1, 3)

        k4 = Card('O', 'S', 'S', 'W')
        spiel.make_action(player2, k4, 0, -1, 3)

        k5 = Card('W', 'W', 'S', 'S')
        spiel.make_action(player1, k5, 1, 1, 3)

        self.assertEqual(len(spiel.alle_wiesen), 2)

    def test5(self):
        spiel = Spiel_class.Spiel(card_class.create_kartenliste(
            ['OSSW', 'SWSW', 'SOSSG', 'WWSWK', 'WWSS', 'WWSS', 'OOSOOT', 'OSSW', 'SOWS', 'OSSW'], False))
        player1 = Player(1)
        player2 = Player(2)

        k1 = Card('O', 'S', 'S', 'W')
        spiel.make_action(player1, k1, 1, 0, 3)

        k2 = Card('W', 'W', 'S', 'W', 'K')
        spiel.make_action(player2, k2, 1, -1, 1, 'k')

        k3 = Card('W', 'W', 'S', 'W', 'K')
        spiel.make_action(player1, k3, 0, 1, 1, 'k')

        k4 = Card('W', 'W', 'S', 'S')
        spiel.make_action(player2, k4, 0, -1, 2)

        a = sorted([list(v) for v in [w.alle_teile.items() for w in spiel.alle_wiesen]])
        b = [[((1, 0), [5])], [((1, 0), [7, 4, 6]), ((1, -1), [5, 6, 7, 4]), ((0, -1), [6, 7, 4, 5]), ((0, 0), [5, 6, 4, 7]), ((0, 1), [5, 6, 7, 4])]]

        self.assertEqual(a, b)

        w = [w for w in spiel.alle_wiesen if len(w.alle_teile) != 1][0]

        for c in spiel.cards_set:
            if c != (1, 0):
                for ecke in spiel.cards_set[c].ecken:

                    self.assertEqual(spiel.cards_set[c].ecken[ecke], w)

    def test6(self):
        spiel = Spiel_class.Spiel(card_class.create_kartenliste(
            ['OSSW', 'SWSW', 'SOSSG', 'WWSWK', 'WWSS', 'WWSS', 'OOSOOT', 'OSSW', 'SOWS', 'OSSW'], False))
        player1 = Player(1)
        player2 = Player(2)

        k0 = Card('S', 'W', 'W', 'S')
        spiel.make_action(player1, k0, 0, 1, 2)

        k1 = Card('W', 'W', 'S', 'S')
        spiel.make_action(player2, k1, 0, 2, 1)

        k2 = Card('W', 'W', 'S', 'W', 'K')
        spiel.make_action(player1, k2, 1, 2, 0)

        k3 = Card('O', 'S', 'S', 'W')
        spiel.make_action(player2, k3, 1, 1, 2)

        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()