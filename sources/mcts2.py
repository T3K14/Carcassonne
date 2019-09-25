import random
import sys
import numpy as np

from Spiel_class import Spiel
from copy import deepcopy


class Player:

    def __init__(self, nr, id=None):
        self.id = id
        #self.nr = nr


class Node:

    def __init__(self, status, action, player_number=None, parent=None):
        """

        :param status:
        :param action:          action steht fuer die Aktion, die der Gegner spielen muss, um zu dieser Node zu kommen

                                ist ein Tuple (x, y, rotations, lak.id, lak.name), wobei lak die Landschaft auf der
                                Karte bezeichent, auf die ein Meeple gesetzt werden soll (kann auch None sein)

        :param player_number:   Die Nr. des Spielers, welcher von dieser Node aus den naechsten Zug machen soll
        :param parent:
        """
        # status, ob die Node eine EndNode ist oder nicht
        self.status = status
        self.action = action    # (x, y, rotations, lak.id, lak.name)
        self.player_number = player_number

        self.wins = 0
        self.visits = 0

        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_best_child(self):
        return max(self.children, key=lambda nod: nod.visits)

    def calculate_UCT_value(self, c=1.4142):
        if self.visits == 0:
            return sys.maxsize
        else:
            result = self.wins / self.visits + c * np.sqrt(np.log(self.parent.visits / self.visits))
            return result

    def __del__(self):
        print('Node ', id(self),' gelöscht')

class MCTS:
    """MCTS-class with essential update functions and the core algorithm functions"""

    def __init__(self, player_list, random_play=None, get_possible_next_states=None):

        self.root = None
        self.next_player = {}
        self.player_list = player_list
        self.player_number = len(player_list)

        for i in range(self.player_number):
            if i+1 < self.player_number:
                self.next_player.update({player_list[i]: player_list[i+1]})
            else:
                self.next_player.update({player_list[i]: player_list[0]})

        self.random_play = random_play
        self.get_possible_next_states = get_possible_next_states

        self.next_player_number = {1: 2, 2: 1}

    def update_root(self, new_state):
        """method to update the root, if another player made a move"""
        if self.root.children:
            for child in self.root.children:

                if child.state.board == new_state.board:
                    self.root = child

                    #
                    break

        else:
            # another player made the first move of the game
            self.root = Node(new_state, self.next_player[self.root.player])

    # not used but can be for better understanding
    def get_next_player(self, player):
        return self.next_player[player]

    def find_next_move(self, global_spiel):
        """find the best next move in given settings"""

        # start time replacement
        t = 0
        t_end = 12000
        # loop as long as time is left:
        while t < t_end:

            # create new spiel entsprechend dem aktuellen Großen
            spiel = deepcopy(global_spiel)

            # erste Karte
            card = spiel.cards_left.pop(0)

            # selection
            # in select_next node die action der Node spielen und die Kartenlist updaten

            # startnode (aktuelle root-Node vom globalen Spiel)
            node = self.root

            # as long as there are known children, choose next child-node with uct
            # und spiele den Zug der gewaehlten Node
            while len(node.children) != 0:
                node = max(node.children, key=lambda nod: nod.calculate_UCT_value())

                # wenn kein Meeple platziert wird
                if node.action[3] is None:
                    landschaft = None
                elif node.action[3] == 'k':
                    landschaft = 'k'
                else:
                    l_dict = {'o': card.orte, 's': card.strassen, 'w': card.wiesen}
                    landschaft = [l for l in l_dict[node.action[3]] if l.name == node.action[4]][0]
                spiel.make_action(spiel.player_to_playernumber[node.parent.player_number], card, node.action[0], node.action[1], node.action[2], landschaft) ######################

                # naechste Karte ziehen
                if len(spiel.cards_left) > 0:
                    card = spiel.cards_left.pop(0)

            # expansion if the choosen node does not represent an and-state of the game
            if node.status:
                for pos_act in spiel.calculate_possible_actions(card, spiel.player_to_playernumber[node.player_number]):  ##################################
                    status = True if len(spiel.cards_left) > 0 else False
                    # wenn die Aktion keine Maeepleplatzierung beinhlatet
                    if pos_act[3] is None:
                        node.children.append(Node(status, (pos_act[0], pos_act[1], pos_act[2], None, None), self.next_player_number[node.player_number], node))
                    elif pos_act[3] == 'k':
                        node.children.append(Node(status, (pos_act[0], pos_act[1], pos_act[2], 'k', 1), self.next_player_number[node.player_number], node))
                    else:
                        node.children.append(Node(status, (pos_act[0], pos_act[1], pos_act[2], pos_act[3].id,
                                                       pos_act[3].name), self.next_player_number[node.player_number], node))  ######

            # simulation

            # if there has been an expansion select next node at random, else evaluate instant
            choosen_node = node
            if len(node.children) > 0:
                choosen_node = random.choice(node.children)

                if choosen_node.action[3] is None:
                    landschaft = None
                elif choosen_node.action[3] == 'k':
                    landschaft = 'k'
                else:
                    l_dict = {'o': card.orte, 's': card.strassen, 'w': card.wiesen}
                    landschaft = [l for l in l_dict[choosen_node.action[3]] if l.name == choosen_node.action[4]][0]
                spiel.make_action(spiel.player_to_playernumber[choosen_node.parent.player_number], card, choosen_node.action[0], choosen_node.action[1], choosen_node.action[2], landschaft)

                # naechste Karte ziehen
                #if len(spiel.cards_left) > 0:
                #    card = spiel.cards_left.pop(0)

            winner = spiel.play_random1v1(spiel.player_to_playernumber[choosen_node.player_number], spiel.player_to_playernumber[self.next_player_number[choosen_node.player_number]], random_card_draw=False) ################
            # backprob
            if winner == 0:
                while choosen_node.parent is not None:
                    choosen_node.visits += 1
                    choosen_node.wins += 0.5
                    choosen_node = choosen_node.parent

                # for the root node:
                choosen_node.visits += 1
                choosen_node.wins += 0.5

            else:
                while choosen_node.parent is not None:
                    choosen_node.visits += 1

                    if choosen_node.player_number != winner.nummer:  # if the player for that choosen_node did not win
                        choosen_node.wins += 1
                    choosen_node = choosen_node.parent

                # for the root node:
                choosen_node.visits += 1
                if choosen_node.player_number != winner.nummer:
                    choosen_node.wins += 1

            #current best node zum debuggen
            #print(t, "Aktuell praeferierte Aktion: ", self.root.get_best_child().action, "mit {}/{}".format(self.root.get_best_child().wins, self.root.get_best_child().visits))

            t += 1
        # return the most visited child node with the "best next move"
        return self.root.get_best_child()



    def select_next_node(self):
        """method to choose the next node from the start at root node until one approaches the end of the tree"""

        node = self.root

        # as long as there are known children, choose next child-node with uct
        while len(node.children) != 0:
            node = max(node.children, key=lambda nod: nod.calculate_UCT_value())

        return node

    def expand(self, node):
        """adds new leaf nodes for all possible game states to the node and initializes them correctly"""

        # player of all child nodes is not player of parent node
        player = self.next_player[node.player]

        for state in self.get_possible_next_states(node):

            #der state muss so gespeichert werden, dass die action die zu dieser node gefuehrt hat auch direkt so gespielt werden kann
            node.children.append(Node(state, player, node))

    def backprop(self, node, result):
        """method for updating wins and visits of all included nodes after one simulation

        takes the node from where the simulation started and the result of the simulation (0 for tie or player-instance
        for winning player"""

        # if simulated game ended with a draw
        if result == 0:
            while node.parent != None:
                node.visits += 1
                node.wins += 0.5
                node = node.parent

            # for the root node:
            node.visits += 1
            node.wins += 0.5

        else:
            while node.parent != None:
                node.visits += 1

                if node.player.id != result:           # if the player for that node did not win
                    node.wins += 1
                node = node.parent

            # for the root node:
            node.visits += 1
            if node.player.id != result:
                node.wins += 1


if __name__ == '__main__':
    print("In MCTS.py script")
