from copy import deepcopy
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

from rotate2 import rotate_info_right, rotate_kanten_dict_right

def uct_vs_uct(counter):

    logfile = open('../log/logfile{}'.format(counter), 'w+')
    logfile.write('NEUES SPIEL')

    player1 = Player(1)
    player2 = Player(2, 'ai')

    # player1.punkte = 3

    d = {player1: player2, player2: player1}

    # zum probieren
    # von einer random-Kartenliste die ersten 10 Karten
    spiel = Spiel(create_kartenliste(karteninfoliste)[:10], player1, player2)

    #spiel = Spiel(create_kartenliste(determinized_karteninfoliste, False), player1, player2)

    # select startspieler
    current_player = random.choice([player1, player2])

    mcts = MCTS((player1, player2))
    mcts.root = Node(True, None, current_player.nummer)

    game_is_running = True
    while game_is_running:

        logfile.write("\n\n\nNEUER ZUG: Player{} ist am Zug\n".format(current_player.nummer))
        logfile.write('Aktuell hat player1 {} Punkte und player2 {} Punkte.\n'.format(player1.punkte,
                                                                                             player2.punkte))
        #display_spielbrett_dict(spiel.cards_set)
        current_card = spiel.cards_left[0]

        print('\nDie nachste Karte ist [{0}, {1}, {2}, {3}, {4}, {5}]'.format(current_card.info[0], current_card.info[1],
                                                                            current_card.info[2], current_card.info[3],
                                                                            current_card.mitte, current_card.schild))
        logfile.write('\nDie nachste Karte ist [{0}, {1}, {2}, {3}, {4}, {5}]'.format(current_card.info[0], current_card.info[1],
                                                                            current_card.info[2], current_card.info[3],
                                                                            current_card.mitte, current_card.schild))
        #draw_card(current_card)
        logfile.write('\nSie enthält folgende moegliche Meeplepositionen:')
        logfile.write('\nOrte: ')
        for o in current_card.orte:
            logfile.write("{}: {}  ".format(o.name, o.kanten))
        logfile.write('\nStrassen: ')
        for s in current_card.strassen:
            logfile.write("{}: {}  ".format(s.name, s.kanten))
        logfile.write('\nWiesen: ')
        for w in current_card.wiesen:
            logfile.write("{}: {}  ".format(w.name, w.ecken))

        pos = spiel.calculate_possible_actions(current_card, current_player)

        # wenn es moegliche anlegestellenn (fuer den aktuellen Spieler) gibt, (es gibt fuer einen spieler auf jeden Fall
        # eine Anlegemoeglichkeit, wenn es fuer den anderen auch eine gibt)
        if pos:
            if current_player.nummer == 1:
                #logfile.write('\nPlayer1 ist am Zug')

                mcts.root = mcts.find_next_move(spiel)

                # l_a_K auf die gespielt werden soll
                if mcts.root.action[2] is None:
                    landschaft = None
                elif mcts.root.action[2] == 'k':
                    landschaft = 'K'
                else:
                    l_dict = {'o': current_card.orte, 's': current_card.strassen, 'w': current_card.wiesen}
                    landschaft = [l for l in l_dict[mcts.root.action[2]] if l.name == mcts.root.action[3]][0]

                spiel.make_action(current_card, mcts.root.action[0], mcts.root.action[1], current_player,
                                  landschaft)  #######################################

                if mcts.root.action[2] is not None:
                    # action_ausgabe = 'K' if mcts.root.action[2] == 'k' else mcts.root.action[2]
                    logfile.write("\n\nDie AI setzt einen Meeple auf {}{}.".format(mcts.root.action[2], mcts.root.action[3]))
                elif mcts.root.action[2] == 'k':
                    logfile.write("\nDie AI setzt einem Meeple auf das Kloster.")
                else:
                    logfile.write("\nDie AI setzt keinen Meeple.")

                logfile.write("\nDie AI setzt die Karte an {} und rotiert sie {} mal".format(mcts.root.action[0],
                                                                                   mcts.root.action[1]))

                # gesetzte Karte loeschen
                del spiel.cards_left[0]

                if len(spiel.cards_left) == 0:
                    game_is_running = False

                # spieler wechseln
                current_player = d[current_player]

            else:
                # player2
                #logfile.write('Player2 ist am Zug')

                mcts.root = mcts.find_next_move(spiel)

                # l_a_K auf die gespielt werden soll
                if mcts.root.action[2] is None:
                    landschaft = None
                elif mcts.root.action[2] == 'k':
                    landschaft = 'K'
                else:
                    l_dict = {'o': current_card.orte, 's': current_card.strassen, 'w': current_card.wiesen}
                    landschaft = [l for l in l_dict[mcts.root.action[2]] if l.name == mcts.root.action[3]][0]

                spiel.make_action(current_card, mcts.root.action[0], mcts.root.action[1], current_player,
                                  landschaft)  #######################################

                if mcts.root.action[2] is not None:
                    # action_ausgabe = 'K' if mcts.root.action[2] == 'k' else mcts.root.action[2]
                    logfile.write("\n\nDie AI setzt einen Meeple auf {}{}.".format(mcts.root.action[2], mcts.root.action[3]))
                elif mcts.root.action[2] == 'k':
                    logfile.write("\nDie AI setzt einem Meeple auf das Kloster.")
                else:
                    logfile.write("\nDie AI setzt keinen Meeple.")

                logfile.write("Die AI setzt die Karte an {} und rotiert sie {} mal".format(mcts.root.action[0],
                                                                                   mcts.root.action[1]))

                # gesetzte Karte loeschen
                del spiel.cards_left[0]

                if len(spiel.cards_left) == 0:
                    game_is_running = False

                # spieler wechseln
                current_player = d[current_player]

        else:
            continue

    spiel.final_evaluate()
    logfile.write("\nSpielende: Player1 hat {} Punkte, Player2 hat {} Punkte.".format(player1.punkte, player2.punkte))
    logfile.close()

def player_vs_uct():

    player1 = Player(1)
    player2 = Player(2, 'ai')

    #player1.punkte = 3

    d = {player1: player2, player2: player1}

    #zum probieren
    #spiel = Spiel(create_kartenliste(determinized_short_karteninfoliste, False), player1, player2)

    spiel = Spiel(create_kartenliste(determinized_karteninfoliste, False), player1, player2)

    #select startspieler
    current_player = player1

    mcts = MCTS((player1, player2), spiel.play_random1v1, spiel.calculate_possible_actions)
    mcts.root = Node(True, None, current_player.nummer)

    game_is_running = True
    while game_is_running:

        print('\n\nNEUER ZUG: Aktuell hat player1 {} Punkte und player2 {} Punkte.\n'.format(player1.punkte, player2.punkte))

        display_spielbrett_dict(spiel.cards_set)
        current_card = spiel.cards_left[0]

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

                    # falls move unguelig:
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

                    # root anpassen
                    if mcts.root.children:
                        for child in mcts.root.children:
                            # wenn die action von der child-node der gespielten entspricht

                            # wenn nicht none
                            if action[3]:
                                landschafts_name = 1 if inp_split[3][0] == 'k' else action[3].name
                                landschafts_id = inp_split[3][0]
                            else:
                                landschafts_name = None
                                landschafts_id = None
                            if child.action == ((action[0], action[1]), action[2], landschafts_id, landschafts_name):  ###
                                mcts.root = child
                                break
                    else:
                        #another player made the first move of the game
                        if action[3]:
                            landschafts_name = 1 if inp_split[3][0] == 'k' else action[3].name
                            landschafts_id = inp_split[3][0]
                        else:
                            landschafts_name = None
                            landschafts_id = None
                        p_num = 1 if current_player.nummer == 2 else 2
                        mcts.root = Node(True, ((action[0], action[1]), action[2], landschafts_id, landschafts_name), p_num, mcts.root)

                    #gesetzte Karte loeschen
                    del spiel.cards_left[0]

                    if len(spiel.cards_left) == 0:
                        game_is_running = False
                    #spieler wechseln
                    current_player = d[current_player]

            else:
                # AI-PLayer
                mcts.root = mcts.find_next_move(spiel)

                # l_a_K auf die gespielt werden soll
                if mcts.root.action[2] is None:
                    landschaft = None
                elif mcts.root.action[2] == 'k':
                    landschaft = 'K'
                else:
                    l_dict = {'o': current_card.orte, 's': current_card.strassen, 'w': current_card.wiesen}
                    landschaft = [l for l in l_dict[mcts.root.action[2]] if l.name == mcts.root.action[3]][0]

                spiel.make_action(current_card, mcts.root.action[0], mcts.root.action[1], current_player, landschaft)   #######################################

                if mcts.root.action[2] is not None:
                    #action_ausgabe = 'K' if mcts.root.action[2] == 'k' else mcts.root.action[2]
                    print("\nDie AI setzt einen Meeple auf {}{}.".format(mcts.root.action[2], mcts.root.action[3]))
                elif mcts.root.action[2] == 'k':
                    print("\nDie AI setzt einem Meeple auf das Kloster.")
                else:
                    print("\nDie AI setzt keinen Meeple.")

                print("Die AI setzt die Karte an {} und rotiert sie {} mal".format(mcts.root.action[0], mcts.root.action[1]))


                # gesetzte Karte loeschen
                del spiel.cards_left[0]

                if len(spiel.cards_left) == 0:
                    game_is_running = False

                # spieler wechseln
                current_player = d[current_player]

        else:
            continue

    spiel.final_evaluate()
    print("\nSpielende: Player1 hat {} Punkte, Player2 hat {} Punkte.".format(player1.punkte, player2.punkte))

if __name__ == '__main__':
    #player_vs_uct()
    c = 0
    while True:

        print("\n\n\nNEUES SPIEL")
        uct_vs_uct(c)
        c += 1