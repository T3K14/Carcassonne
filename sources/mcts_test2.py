import unittest
from mcts2 import MCTS, Node

import random

from mcts2 import MCTS, Node
from Spiel_class import Spiel
from card_class import Card, karteninfoliste, create_kartenliste, determinized_karteninfoliste, determinized_short_karteninfoliste

from Ort import Ort
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese
from Player_Class import Player


from plot_cards import display_spielbrett_dict, draw_card


class MCTSTEST(unittest.TestCase):

    def test_1(self):

        player1 = Player(1)
        player2 = Player(2, 'ai')
        d = {player1: player2, player2: player1}

        kartenliste = create_kartenliste(['SOWS', 'WWSS', 'SOSSG', 'OSSW', 'OOSOOT', 'OSSW', 'WWSWK', 'OSSW'], False)
        spiel = Spiel(kartenliste, player1, player2)

        mcts = MCTS([player1, player2])
        mcts.root = Node(True, None, player1.nummer)

        current_player = player1
        #display_spielbrett_dict(spiel.cards_set)

        # spiel geht los
        k1 = spiel.cards_left.pop(0)
        spiel.make_action(current_player, k1, 1, 0, 2, k1.orte[0])

        # tree updaten
        mcts.root = Node(True, (1, 0, 2, 'o', 1), player2.nummer, mcts.root)

        current_player = d[current_player]
        #display_spielbrett_dict(spiel.cards_set)


        # AI Zug 1
        proposed_node = mcts.find_next_move(spiel)
        spiel.make_action(current_player, spiel.cards_left[0], 0, 1, 0, spiel.cards_left[0].strassen[0])

        for node in mcts.root.children:
            if node.action == (0, 1, 0, 's', 1):
                mcts.root = node
                break
            #print('\n', node.action)
            #print(node.wins,'/', node.visits)

        del spiel.cards_left[0]
        current_player = d[current_player]
        #display_spielbrett_dict(spiel.cards_set)

        self.assertEqual(7, player1.meeples)
        self.assertEqual(6, player2.meeples)

        # neuer human Zug
        k3 = spiel.cards_left.pop(0)

        wiese = None
        nr = None
        for w in k3.wiesen:
            if w.ecken == [5, 6]:
                wiese = w
                nr = w.name

        spiel.make_action(current_player, k3, 2, 0, 3, wiese)

        # tree updaten
        for node in mcts.root.children:
            if node.action == (2, 0, 3, 'w', nr):
                mcts.root = node

        current_player = d[current_player]
        #display_spielbrett_dict(spiel.cards_set)


        # AI Zug 2
        proposed_node = mcts.find_next_move(spiel)

        wiese = None
        for w in spiel.cards_left[0].wiesen:
            if w.ecken == [4, 5, 7]:
                wiese = w
        spiel.make_action(current_player, spiel.cards_left[0], -1, 1, 0, wiese)

        for node in mcts.root.children:
            if node.action == (-1, 1, 0, 'w', 1):
                mcts.root = node
            #print('\n', node.action)
            #print(node.wins,'/', node.visits)

        del spiel.cards_left[0]
        current_player = d[current_player]
        #display_spielbrett_dict(spiel.cards_set)

        self.assertEqual(5, player2.meeples)
        self.assertEqual(6, player1.meeples)

        # neuer human Zug
        k5 = spiel.cards_left.pop(0)

        spiel.make_action(current_player, k5, 2, 1, 1, k5.orte[0])

        # tree updaten
        for node in mcts.root.children:
            if node.action == (2, 1, 1, 'o', 1):
                mcts.root = node

        current_player = d[current_player]
        #display_spielbrett_dict(spiel.cards_set)

        # AI Zug 3
        proposed_node = mcts.find_next_move(spiel)
        spiel.make_action(current_player, spiel.cards_left[0], -1, 2, 2, spiel.cards_left[0].orte[0])

        for node in mcts.root.children:
            if node.action == (-1, 2, 2, 'o', 1):
                mcts.root = node
            # print('\n', node.action)
            # print(node.wins,'/', node.visits)

        del spiel.cards_left[0]
        current_player = d[current_player]
        #display_spielbrett_dict(spiel.cards_set)

        # neuer human Zug
        k7 = spiel.cards_left.pop(0)

        spiel.make_action(current_player, k7, 1, 1, 3, 'k')

        # tree updaten
        for node in mcts.root.children:
            #print(node.action)
            if node.action == (1, 1, 3, 'k', 1):
                mcts.root = node

        current_player = d[current_player]
        display_spielbrett_dict(spiel.cards_set)

        self.assertEqual(4, player1.punkte)
        self.assertEqual(4, player2.punkte)

        self.assertEqual(4, player1.meeples)
        self.assertEqual(5, player2.meeples)

        # AI Zug 4
        for c in spiel.cards_left:
            print(c.matrix)
        proposed_node = mcts.find_next_move(spiel)




if __name__ == '__main__':
    unittest.main()