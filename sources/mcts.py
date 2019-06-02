from copy import deepcopy
import random

from mcts2 import MCTS, Node, State
from Spiel_class import Spiel
from card_class import Card, karteninfoliste, create_kartenliste

from Ort import Ort
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese
from Player_Class import Player


from plot_cards import display_spielbrett_dict, draw_card

from rotate2 import rotate_info_right, rotate_kanten_dict_right

def player_vs_uct():

    player1 = Player(1)
    player2 = Player(2, 'ai')

    d = {player1: player2, player2: player1}

    spiel = Spiel(create_kartenliste(karteninfoliste))

    #select startspieler
    startspieler = player2
    current_player = startspieler

    mcts = MCTS((player1, player2), spiel.play_random1v1, spiel.calculate_possible_actions)
    mcts.root = Node(State(True, 'startboard'), startspieler)

    # todo wie mache ich hier weiter, was ist ein State?   Entweder einfach ein Spiel objekt zu einem bestimmten
    # Zeitpunkt, oder ne Liste mit allen wichtigen Listen

    

    game_is_running = True
    while game_is_running:

        display_spielbrett_dict(spiel.cards_set)
        current_card = spiel.draw_card()

        print('Die nachste Karte ist [{0}, {1}, {2}, {3}, {4}, {5}]'.format(current_card.info[0], current_card.info[1], current_card.info[2], current_card.info[3], current_card.mitte, current_card.schild))
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

        # wenn es moegliche anlegestellenn (fuer den aktuellen Spieler) gibt, (es gibt fuer einen spieler auf jeden Fall
        # eine Anlegemoeglichkeit, wenn es fuer den anderen auch eine gibt)
        if pos:
            if current_player.art == 'human':

                    #mache deinen move

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

            else:
                # AI-PLayer
                mcts.root = mcts.find_next_move(spiel)
                spiel.make_action()

                # spieler wechseln
                current_player = d[current_player]

        else:
            continue

if __name__ == '__main__':
    player_vs_uct()
