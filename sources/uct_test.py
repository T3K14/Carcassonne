import unittest


from Ort import Ort
from Strasse import Strasse
from Wiese import Wiese
import card_class
import Spiel_class
from Player_Class import Player
from card_class import Card, speed_test_karteninfoliste
from plot_cards import display_spielbrett_dict, draw_card

from decoratora import uct_select, calculate_tree
from mcts2 import Node


class evaluationTest(unittest.TestCase):

    def test1(self):

        p1 = Player(1)
        p2 = Player(2)

        spiel = Spiel_class.Spiel([], p1, p2)

        k1 = Card('O', 'O', 'S', 'O', 'O', True)
        spiel.make_action(p1, k1, 1, 0, 0, k1.orte[0])

        k2 = Card('O', 'S', 'S', 'W')
        spiel.make_action(p2, k2, 0, 1, 1, k2.strassen[0])

        k3 = Card('O', 'S', 'S', 'W')
        spiel.make_action(p1, k3, 2, 0, 3, k3.strassen[0])

        k4 = Card('W', 'W', 'S', 'S')
        spiel.make_action(p2, k4, 2, -1, 0, k4.strassen[0])

        k5 = Card('S', 'W', 'S', 'W')
        spiel.make_action(p1, k5, -1, 0, 0, k5.strassen[0])

        k6 = Card('W', 'W', 'S', 'S')
        spiel.make_action(p2, k6, 0, 2, 1, k6.strassen[0])

        k7 = Card('W', 'W', 'S', 'W', 'K')
        spiel.make_action(p1, k7, 2, 1, 0, 'k')

        k8 = Card('S', 'O', 'S', 'S', 'G')

        s = None
        for st in k8.strassen:
            if st.kanten == [3]:
                s = st

        spiel.make_action(p2, k8, 1, -1, 1, s)

        k9 = Card('O', 'S', 'S', 'W')
        spiel.make_action(p1, k9, 1, -2, 0, k9.orte[0])

        k10 = Card('S', 'O', 'W', 'S')

        #pos = spiel.calculate_possible_actions(k10, p2)
        #node = Node(True, None, p2.nummer, None)

        #a, b = uct_select(spiel, k10, p2, pos, d=1, root_node=node, t_end=None, rechenzeit=30, c=1.4142, threads=1)

        #print(a, b)

        w = None
        for wi in k10.wiesen:
            if wi.ecken == [4]:
                w = wi
        spiel.make_action(p2, k10, 2, -2, 0, w)

        spiel.final_evaluate()

        self.assertEqual(p2.punkte, 12)

if __name__ == '__main__':
    unittest.main()