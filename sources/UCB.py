from Player_Class import Player
from Spiel_class import Spiel
from card_class import create_kartenliste, karteninfoliste, Card
from copy import deepcopy

import sys
import numpy as np

class Node:

    def __init__(self, action):
        self.action = action
        self.visits = 0
        self.wins = 0

    def calculate_UCB1_value(self, nr_simulations, c=1.4142):

        if self.visits == 0:
            return sys.maxsize
        else:
            result = self.wins / self.visits + c * np.sqrt(np.log(nr_simulations / self.visits))
            return result

def get_best_child_via_ucb1():

        # start time replacement
        t = 0
        t_end = 3000

        # loop as long as time is left:
        while t < t_end:
            pass


        return 1

def player_vs_ucb():

    player1 = Player(1)
    player2 = Player(2, 'ai')

    d = {player1: player2, player2: player1}

    #spiel = Spiel(create_kartenliste(karteninfoliste))
    spiel = Spiel([Card('S', 'O', 'W', 'S')])

    #select startspieler
    current_player = player2

    game_is_running = True
    while game_is_running:

        # display spielbrett
        current_card = spiel.draw_card()
        pos = spiel.calculate_possible_actions(current_card, current_player)

        if pos:

            if current_player.art == 'human':
                 #gib move ein
                    inp = input('Bitte gib deine Aktion an:')
                    inp_split = inp.split(' ')
                    if inp_split[3][0] == 'o':
                        o = [a for a in current_card.orte if a.name == int(inp_split[3][1])]
                        action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), o[0])
                    elif inp_split[3][0] == 's':
                        s = [a for a in current_card.strassen if a.name == int(inp_split[3][1])]
                        action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), s[0])
                    elif inp_split[3][0] == 'w':
                        w = [a for a in current_card.wiesen if a.name == int(inp_split[3][1])]
                        action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), w[0])
                    else:
                        action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), None)

                    #falls move unguelig:
                    while action not in pos:
                        print("illegaler Move")
                        inp = input('Bitte gib deine Aktion an:')
                        inp_split = inp.split(' ')
                        if inp_split[3][0] == 'o':
                            o = [a for a in current_card.orte if a.name == int(inp_split[3][1])]
                            action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), o[0])
                        elif inp_split[3][0] == 's':
                            s = [a for a in current_card.strassen if a.name == int(inp_split[3][1])]
                            action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), s[0])
                        elif inp_split[3][0] == 'w':
                            w = [a for a in current_card.wiesen if a.name == int(inp_split[3][1])]
                            action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), w[0])
                        else:
                            action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), None)

                    spiel.make_action(current_card, (action[0], action[1]), action[2], current_player, action[3])

                    #spieler wechseln
                    current_player = d[current_player]

                    if not spiel.cards_left:
                        game_is_running = False

            else:
                # ai
                child_nodes = [Node(action) for action in pos]

                t = 0
                t_end = 5

                # loop as long as time is left:
                while t < t_end:
                    spiel_copy = deepcopy(spiel)

                    current_node = max(child_nodes, key=lambda nod: nod.calculate_UCB1_value(t))
                    spiel_copy.make_action(current_card, (current_node.action[0], current_node.action[1]), current_node.action[2], current_player, current_node.action[3])

                    # play random
                    winner = spiel_copy.play_random1v1(d[current_player], current_player)

                    current_node.visits += 1
                    if winner == current_player:
                        current_node.wins += 1
                    elif winner == 0:
                        current_node.wins += 0.5

                    t += 1

                #spiel.make_action(max(child_nodes, key=lambda nod: nod.wins).action)
                action = max(child_nodes, key=lambda nod: nod.wins).action
                spiel.make_action(current_card, (action[0], action[1]), action[2], current_player, action[3])

                # switch players
                current_player = d[current_player]

                if not spiel.cards_left:
                    game_is_running = False

        else:
            continue

    print("Spielende: Player1 hat {} Punkte, Player2 hat {} Punkte.".format(player1.punkte, player2.punkte))

if __name__ == '__main__':
    player_vs_ucb()
