from Player_Class import Player
from Spiel_class import Spiel
from card_class import create_kartenliste, karteninfoliste, Card
from copy import deepcopy
from plot_cards import draw_card, display_spielbrett_dict

from Wiese import WieseAufKarte
from Strasse import StasseAufKarte
from Ort import Ort_auf_Karte

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

def player_vs_ucb(kartenliste=None):

    player1 = Player(1)
    player2 = Player(2, 'ai')

    #player1.meeples = 3
    #player2.meeples = 3

    #player1.punkte = 3

    d = {player1: player2, player2: player1}

    if kartenliste is None:
        spiel = Spiel(create_kartenliste(karteninfoliste))
    else:
        spiel = Spiel(kartenliste)

    #select startspieler
    current_player = player2



    #####
    #k1 = Card('O', 'W', 'W', 'O', 'O')
    #spiel.make_action(k1, (1, 0), 0, player1, k1.orte[0])

    #k2 = Card('O', 'W', 'W', 'O', 'O')
    #spiel.make_action(k2, (1, 0), 0, player1)
    #####


    game_is_running = True
    while game_is_running:

        print('player1 hat {} Punkte, player2 hat {} Punkte.'.format(player1.punkte, player2.punkte))

        # display spielbrett
        display_spielbrett_dict(spiel.cards_set)

        current_card = spiel.draw_card()
        #print('Alle moeglichen actions:')
        #print(spiel.calculate_possible_actions(current_card, current_player))

        print('\nDie nachste Karte ist [{0}, {1}, {2}, {3}, {4}, {5}]'.format(current_card.info[0], current_card.info[1], current_card.info[2], current_card.info[3], current_card.mitte, current_card.schild))

        draw_card(current_card)
        print('Sie enthält folgende moegliche Meeplepositionen:')
        print('Orte:')
        for o in current_card.orte:
            print(o.name, o.kanten)
        print('Strassen:')
        for s in current_card.strassen:
            print(s.name, s.kanten)
        print('Wiesen:')
        for w in current_card.wiesen:
            print(w.name, w.ecken)

        pos = spiel.calculate_possible_actions(current_card, current_player)

        if pos:

            if current_player.art == 'human':
                 #gib move ein
                    inp = input('Bitte gib deine Aktion an:')

                    inp_split = inp.split(' ')
                    ungueltig = True
                    action = None
                    try:
                        if inp_split[3][0] == 'o':
                            o = [a for a in current_card.orte if a.name == int(inp_split[3][1])]
                            action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), o[0])
                        elif inp_split[3][0] == 's':
                            s = [a for a in current_card.strassen if a.name == int(inp_split[3][1])]
                            action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), s[0])
                        elif inp_split[3][0] == 'w':
                            w = [a for a in current_card.wiesen if a.name == int(inp_split[3][1])]
                            action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), w[0])
                        elif inp_split[3][0] == 'k':
                            action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), 'K')
                        else:
                            action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), None)
                    except IndexError or ValueError:
                        pass

                    #falls move unguelig:
                    if action in pos:
                        ungueltig = False
                    while ungueltig:
                        print("illegaler Move")
                        inp = input('Bitte gib deine Aktion an:')
                        inp_split = inp.split(' ')
                        try:
                            if inp_split[3][0] == 'o':
                                o = [a for a in current_card.orte if a.name == int(inp_split[3][1])]
                                action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), o[0])
                            elif inp_split[3][0] == 's':
                                s = [a for a in current_card.strassen if a.name == int(inp_split[3][1])]
                                action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), s[0])
                            elif inp_split[3][0] == 'w':
                                w = [a for a in current_card.wiesen if a.name == int(inp_split[3][1])]
                                action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), w[0])
                            elif inp_split[3][0] == 'k':
                                action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), 'K')
                            else:
                                action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), None)
                        except IndexError or ValueError:
                            pass
                        if action in pos:
                            ungueltig = False


                    spiel.make_action(current_card, (action[0], action[1]), action[2], current_player, action[3])

                    #spieler wechseln
                    current_player = d[current_player]

                    if not spiel.cards_left:
                        game_is_running = False

            else:

                # ai
                child_nodes = [Node(action) for action in pos]

                t = 0
                t_end = 500

                # player stats in real game
                current_player_stats = (current_player.meeples, current_player.punkte)
                other_player_stats = (d[current_player].meeples, d[current_player].punkte)

                # loop as long as time is left:
                while t < t_end:

                    spiel_copy = deepcopy(spiel)
                    current_card_copy = deepcopy(current_card)

                    #player zurueckaendern:
                    """die spieler, die beim kopieren vom Spiel veraendert wurden werden hier wieder zurueckgesetzt"""
                    l = [spiel_copy.alle_orte, spiel_copy.alle_wiesen, spiel_copy.alle_strassen]
                    for landart in l:
                        for instance in landart:
                            if instance.meeples:

                                new_d = {current_player: 0, d[current_player]: 0}
                                for player in instance.meeples:
                                    for global_player in new_d:
                                        if global_player.nummer == player.nummer:
                                            new_d[global_player] = instance.meeples[player]
                                instance.meeples = new_d
                                instance.update_besitzer()

                    # spieler von kloestern zuruecksetzen
                    for global_kloster in spiel.alle_kloester:
                        for kloster in spiel_copy.alle_kloester:
                            if kloster.umgebungs_koordinaten == global_kloster.umgebungs_koordinaten:
                                kloster.besitzer = global_kloster.besitzer

                    #current_card_copy = deepcopy(current_card)

                    current_node = max(child_nodes, key=lambda nod: nod.calculate_UCB1_value(t))

                    meeple_pos = 'K'

                    if isinstance(current_node.action[3], Ort_auf_Karte):
                        for ort in current_card_copy.orte:
                            if ort.name == current_node.action[3].name:
                                meeple_pos = ort
                                break
                    elif isinstance(current_node.action[3], StasseAufKarte):
                        for strasse in current_card_copy.strassen:
                            if strasse.name == current_node.action[3].name:
                                meeple_pos = strasse
                                break
                    elif isinstance(current_node.action[3], WieseAufKarte):
                        for wiese in current_card_copy.wiesen:
                            if wiese.name == current_node.action[3].name:
                                meeple_pos = wiese
                                break

                    spiel_copy.make_action(current_card_copy, (current_node.action[0], current_node.action[1]), current_node.action[2], current_player, meeple_pos)

                    # play random
                    winner = spiel_copy.play_random1v1(d[current_player], current_player)

                    current_node.visits += 1
                    if winner == current_player:
                        current_node.wins += 1
                    elif winner == 0:
                        current_node.wins += 0.5

                    # spieler nach random-spiel wieder auf ihre ausgangswerte setzen
                    current_player.meeples = current_player_stats[0]
                    current_player.punkte = current_player_stats[1]

                    d[current_player].meeples = other_player_stats[0]
                    d[current_player].punkte = other_player_stats[1]

                    # erste Karte nach dem Spiel wieder resetten
                    #current_card.ecken, current_card.kanten, current_card.orte, current_card.orte_kanten,\
                    #current_card.strassen, current_card.strassen_kanten, current_card.wiesen, current_card.wiesen_kanten = card_stats[0], card_stats[1], card_stats[2], card_stats[3], card_stats[4], card_stats[5], card_stats[6], card_stats[7]

                    t += 1


                #spiel.make_action(max(child_nodes, key=lambda nod: nod.wins).action)
                action = max(child_nodes, key=lambda nod: nod.wins).action
                spiel.make_action(current_card, (action[0], action[1]), action[2], current_player, action[3])

                if action[3] is not None:
                    action_ausgabe = 'K' if action[3] == 'K' else action[3].name
                    print("\nEin Meeple wird auf {} mit Namen {} gesetzt".format(action[3], action_ausgabe))
                else:
                    print("\nEs wird kein Meeple gesetzt")

                print("\nDie AI setzt die Karte an ({}, {}) und rotiert sie {} mal".format(action[0], action[1], action[2]))


                # switch players
                current_player = d[current_player]

                if not spiel.cards_left:
                    game_is_running = False

        else:
            continue

    spiel.final_evaluate()
    print("Spielende: Player1 hat {} Punkte, Player2 hat {} Punkte.".format(player1.punkte, player2.punkte))

if __name__ == '__main__':
    #player_vs_ucb([Card('O', 'W', 'W', 'O', 'O'), Card('O', 'W', 'W', 'W'), Card('W', 'W', 'W', 'W', 'K'),
    #               Card('S', 'O', 'S', 'W'), Card('W', 'W', 'S', 'S'), Card('O', 'W', 'O', 'W', 'O'),
    #               Card('W', 'O', 'W', 'O'), Card('O', 'O', 'S', 'O', 'O', True), Card('O', 'W', 'W', 'O', 'O'),
    #               Card('S', 'O', 'S', 'S', 'G')])
    #player_vs_ucb([Card('W', 'O', 'W', 'O'), Card('')])
    #player_vs_ucb([Card('W', 'W','W','W','K')])

    #player_vs_ucb([Card('O', 'W', 'W', 'W'), Card('O', 'W', 'W', 'O', 'O')])
    #player_vs_ucb([Card('W', 'O', 'W', 'O')])

    player_vs_ucb(create_kartenliste(karteninfoliste))