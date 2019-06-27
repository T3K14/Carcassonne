import unittest

from Ort import Ort
from Strasse import Strasse
from Wiese import Wiese
import card_class
import Spiel_class
from Player_Class import Player
from card_class import Card
from plot_cards import display_spielbrett_dict, draw_card

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

        #display_spielbrett_dict(spiel.cards_set)

        k = card_class.Card("S", "O", "O", "S", "O")
        #draw_card(k)

        goal = [(0, -1, 0, k.strassen[0]), (0, -1, 0, k.orte[0]), (0, -1, 1, k.strassen[0]),
                (0, -1, 1, k.orte[0]), (2, 1, 1, k.strassen[0]), (2, 1, 1, k.orte[0]),
                (2, 1, 2, k.strassen[0]), (2, 1, 2, k.orte[0]), (1, 0, 2, k.orte[0]),
                (1, 0, 2, k.strassen[0]), (0, -1, 0, None), (0, -1, 1, None), (1, 0, 2, None), (2, 1, 1, None), (2, 1, 2, None),
                (1, 0, 2, k.wiesen[0]), (1, 0, 2, k.wiesen[1]), (2, 1, 1, k.wiesen[0]), (2, 1, 1, k.wiesen[1]),
                (2, 1, 2, k.wiesen[0]), (2, 1, 2, k.wiesen[1]), (0, -1, 0, k.wiesen[0]), (0, -1, 0, k.wiesen[1]),
                (0, -1, 1, k.wiesen[0]), (0, -1, 1, k.wiesen[1])]

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

    def test3(self):

        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        k1 = Card('O', 'O', 'S', 'O', 'O', True)
        spiel.make_action(player2, k1, 1, 0, 0, k1.orte[0])

        k2 = Card('O', 'W', 'W', 'O', 'O')
        spiel.make_action(player1, k2, 1, 1, 2, k2.wiesen[0])

        k3 = Card('W', 'W', 'W', 'W', 'K')
        pos = spiel.calculate_possible_actions(k3, player2)

        #display_spielbrett_dict(spiel.cards_set)

        goal = [(-1, 0, 0, k3.wiesen[0]), (-1, 0, 0, None), (-1, 0, 0, 'K'), (1, 2, 0, None), (1, 2, 0, 'K')]

        self.assertEqual(len(pos), len(goal))
        for tup in pos:
            self.assertTrue(tup in goal)

    def test4(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        k2 = Card('O', 'W', 'W', 'O', 'O')
        spiel.make_action(player1, k2, 1, 0, 0)

        k3 = Card('W', 'O', 'W', 'O')
        pos = spiel.calculate_possible_actions(k3, player2)

        #display_spielbrett_dict(spiel.cards_set)


        self.assertEqual(len(pos), 16)

    def test5(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        k2 = Card('O', 'W', 'W', 'O', 'O')
        spiel.make_action(player1, k2, 1, 0, 0, k2.orte[0])

        k3 = Card('W', 'O', 'W', 'O')
        pos = spiel.calculate_possible_actions(k3, player2)

        self.assertEqual(len(pos), 15)

    def test6(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        k1 = Card('W', 'W', 'S', 'S')
        spiel.make_action(player1, k1, 0, 1, 3)

        k2 = Card('O', 'S', 'S', 'O', 'O')
        spiel.make_action(player2, k2, 1, 1, 1)

        #display_spielbrett_dict(spiel.cards_set)
        k3 = Card('O', 'O', 'S', 'O', 'O', True)
        pos = spiel.calculate_possible_actions(k3, player1)

        self.assertEqual(len(pos), 40)

    def test7(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        k1 = Card('S', 'W', 'S', 'W')
        pos1 = spiel.calculate_possible_actions(k1, player1)

        self.assertEqual(len(pos1), 12)
        spiel.make_action(player1, k1, 0, 1, 0, k1.strassen[0])

        k2 = Card('O', 'W', 'W', 'O', 'O')
        pos2 = spiel.calculate_possible_actions(k2, player2)

        self.assertEqual(len(pos2), 24)
        spiel.make_action(player2, k2, 1, 0, 0, k2.orte[0])

        #display_spielbrett_dict(spiel.cards_set)

        k3 = Card('W', 'W', 'S', 'S')
        pos3 = spiel.calculate_possible_actions(k3, player1)

        self.assertEqual(len(pos3), 44)
        spiel.make_action(player1, k3, 0, 2, 3)

        k4 = Card('O', 'S', 'S', 'W')
        pos4 = spiel.calculate_possible_actions(k4, player2)

        self.assertEqual(len(pos4), 46)
        spiel.make_action(player2, k4, 1, 2, 2)

        k4 = Card('W', 'O', 'W', 'O')
        pos5 = spiel.calculate_possible_actions(k4, player1)

        #display_spielbrett_dict(spiel.cards_set)

        self.assertEqual(len(pos5), 31)

    def test8(self):
        """fast der gleiche wie test7, nur mit meeple mehr in vorletzem Zug"""
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        k1 = Card('S', 'W', 'S', 'W')
        pos1 = spiel.calculate_possible_actions(k1, player1)

        self.assertEqual(len(pos1), 12)
        spiel.make_action(player1, k1, 0, 1, 0, k1.strassen[0])

        k2 = Card('O', 'W', 'W', 'O', 'O')
        pos2 = spiel.calculate_possible_actions(k2, player2)

        self.assertEqual(len(pos2), 24)
        spiel.make_action(player2, k2, 1, 0, 0, k2.orte[0])

        #display_spielbrett_dict(spiel.cards_set)

        k3 = Card('W', 'W', 'S', 'S')
        pos3 = spiel.calculate_possible_actions(k3, player1)

        self.assertEqual(len(pos3), 44)
        spiel.make_action(player1, k3, 0, 2, 3)

        k4 = Card('O', 'S', 'S', 'W')
        pos4 = spiel.calculate_possible_actions(k4, player2)

        self.assertEqual(len(pos4), 46)
        spiel.make_action(player2, k4, 1, 2, 2, k4.orte[0])

        k5= Card('W', 'O', 'W', 'O')
        pos5 = spiel.calculate_possible_actions(k5, player1)

        self.assertEqual(len(pos5), 30)

    def test9(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        k1 = Card('W', 'W', 'S', 'S')
        pos1 = spiel.calculate_possible_actions(k1, player1)

        self.assertEqual(len(pos1), 24)
        spiel.make_action(player1, k1, 0, 1, 3)

        k2 = Card('S', 'O', 'S', 'W')
        pos2 = spiel.calculate_possible_actions(k2, player2)

        self.assertEqual(len(pos2), 40)
        wiese = [w for w in k2.wiesen if w.ecken == [5, 6]][0]

        spiel.make_action(player1, k2, 1, 1, 1, wiese)

        k3 = Card('O', 'O', 'S', 'O', 'O', True)
        pos3 = spiel.calculate_possible_actions(k3, player1)

        self.assertEqual(len(pos3), 18)

    def test10(self):
        spiel = Spiel_class.Spiel(Kartenliste)
        player1 = Player(1)
        player2 = Player(2)

        k1 = Card('O', 'S', 'S', 'W')
        pos1 = spiel.calculate_possible_actions(k1, player1)

        self.assertEqual(30, len(pos1))
        spiel.make_action(player1, k1, 0, 1, 1, k1.orte[0])

        k2 = Card('O', 'W', 'W', 'O', 'O', True)
        pos2 = spiel.calculate_possible_actions(k2, player2)

        self.assertEqual(22, len(pos2))
        spiel.make_action(player2, k2, 1, 0, 0, k2.orte[0])


        k3 = Card('O', 'O', 'W', 'O', 'O')

        pos3 = spiel.calculate_possible_actions(k3, player1)

        self.assertEqual(16, len(pos3))
        spiel.make_action(player1, k3, 1, 1, 2)

        #display_spielbrett_dict(spiel.cards_set)

        k4 = Card('W', 'O', 'W', 'O')

        pos4 = spiel.calculate_possible_actions(k4, player2)

        self.assertEqual(23, len(pos4))


if __name__ == "__main__":
    unittest.main()
