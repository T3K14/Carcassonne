from copy import deepcopy
import random
import multiprocessing
from itertools import repeat
import time

from mcts2 import MCTS, Node
from Spiel_class import Spiel
from card_class import Card, karteninfoliste, create_kartenliste, determinized_karteninfoliste, determinized_short_karteninfoliste, test_karteninfolist, speed_test_karteninfoliste

from Ort import Ort
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese
from Player_Class import Player


from plot_cards import display_spielbrett_dict, draw_card

from rotate2 import rotate_info_right, rotate_kanten_dict_right

next_player_number = {1: 2, 2: 1}


def calculate_tree(root, global_spiel):
    """

    :param root:
    :param global_spiel:
    :return:
    """

    # start time replacement
    t = 0
    t_end = 150
    # loop as long as time is left:
    while t < t_end:

        # create new spiel entsprechend dem aktuellen Großen
        spiel = deepcopy(global_spiel)

        # erste Karte
        card = spiel.cards_left.pop(0)

        # selection
        # in select_next node die action der Node spielen und die Kartenlist updaten

        # startnode (aktuelle root-Node vom globalen Spiel)
        node = root

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
            spiel.make_action(spiel.player_to_playernumber[node.parent.player_number], card, node.action[0],
                              node.action[1], node.action[2], landschaft)  ######################

            # naechste Karte ziehen
            if len(spiel.cards_left) > 0:
                card = spiel.cards_left.pop(0)

        # expansion if the choosen node does not represent an and-state of the game
        if node.status:
            for pos_act in spiel.calculate_possible_actions(card, spiel.player_to_playernumber[
                node.player_number]):  ##################################
                status = True if len(spiel.cards_left) > 0 else False
                # wenn die Aktion keine Maeepleplatzierung beinhlatet
                if pos_act[3] is None:
                    node.children.append(Node(status, (pos_act[0], pos_act[1], pos_act[2], None, None),
                                              next_player_number[node.player_number], node))
                elif pos_act[3] == 'k':
                    node.children.append(Node(status, (pos_act[0], pos_act[1], pos_act[2], 'k', 1),
                                              next_player_number[node.player_number], node))
                else:
                    node.children.append(Node(status, (pos_act[0], pos_act[1], pos_act[2], pos_act[3].id,
                                                       pos_act[3].name), next_player_number[node.player_number],
                                              node))  ######

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
            spiel.make_action(spiel.player_to_playernumber[choosen_node.parent.player_number], card,
                              choosen_node.action[0], choosen_node.action[1], choosen_node.action[2], landschaft)

            # naechste Karte ziehen
            # if len(spiel.cards_left) > 0:
            #    card = spiel.cards_left.pop(0)

        winner = spiel.play_random1v1(spiel.player_to_playernumber[choosen_node.player_number],
                                      spiel.player_to_playernumber[next_player_number[choosen_node.player_number]],
                                      random_card_draw=False)  ################
        # backprob
        #if winner == 0:
        #    while choosen_node.parent is not None:
        #        choosen_node.visits += 1
        #        choosen_node.wins += 0.5
        #        choosen_node = choosen_node.parent

            # for the root node:
        #    choosen_node.visits += 1
        #    choosen_node.wins += 0.5

        #else:
        #    while choosen_node.parent is not None:
        #        choosen_node.visits += 1

        #        if choosen_node.player_number != winner.nummer:  # if the player for that choosen_node did not win
        #            choosen_node.wins += 1
        #        choosen_node = choosen_node.parent

        #    # for the root node:
        #    choosen_node.visits += 1
        #    if choosen_node.player_number != winner.nummer:
        #        choosen_node.wins += 1

        while choosen_node.parent is not None:
            choosen_node.visits += 1
            choosen_node.wins += spiel.player_to_playernumber[choosen_node.parent.player_number].punkte - spiel.player_to_playernumber[choosen_node.player_number].punkte

            choosen_node = choosen_node.parent

        # for root-node
        choosen_node.visits += 1

        # current best node zum debuggen
        # print(t, "Aktuell praeferierte Aktion: ", self.root.get_best_child().action, "mit {}/{}".format(self.root.get_best_child().wins, self.root.get_best_child().visits))

        #print(t)
        t += 1

    print('ICH BIN SCHON FERTIG.')
    return root


def get_best_child(root_nodes):
    """
    Funktion zum ermitteln der besten Child-Node aus verschiedenen Trees, welche von der selben root-Node aus starten.
    Die Auswahl findet auf Basis der visits statt.

    :param root_nodes:  list    Liste mit root_nodes, zu welchen ein Tree aufgebaut wurde
    :return:            node    Node mit der besten Aktion von dem Tree, bei welchem diese Node am haeufigsten besucht
                                wurde
    """

    # trage die ersten Werte schon ein
    visits = [node.visits for node in root_nodes[0].children]

    # addiere die uebrigen visit Werte auf die bereits vorhandenen
    for root_node in root_nodes[1:]:
        for i, child in enumerate(root_node.children):
            visits[i] += child.visits

    # ermittle den Index der Child-Node mit den meisten Visits aus allen Trees
    index = visits.index(max(visits))

    # ermittel child_node zu dem Index aus allen Trees, welche am haeufigsten besucht wurde und returne diese
    # die Child Nodes von den Trees zu dem Index = [root.children[index] for root in root_nodes]
    return max([root.children[index] for root in root_nodes], key=lambda nod: nod.visits)


def uct_vs_uct(counter):

    logfile = open('../log/logfile{}'.format(counter), 'w+')
    logfile.write('NEUES SPIEL')

    player1 = Player(1, 'ai')
    player2 = Player(2, 'ai')

    # player1.punkte = 3

    d = {player1: player2, player2: player1}

    # zum probieren
    # von einer random-Kartenliste die ersten 10 Karten
    #spiel = Spiel(create_kartenliste(karteninfoliste)[:10], player1, player2)

    spiel = Spiel(create_kartenliste(determinized_karteninfoliste, False), player1, player2)

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
                if mcts.root.action[3] is None:
                    landschaft = None
                elif mcts.root.action[3] == 'k':
                    landschaft = 'k'
                else:
                    l_dict = {'o': current_card.orte, 's': current_card.strassen, 'w': current_card.wiesen}
                    landschaft = [l for l in l_dict[mcts.root.action[3]] if l.name == mcts.root.action[4]][0]

                spiel.make_action(current_player, current_card, mcts.root.action[0], mcts.root.action[1], mcts.root.action[2],
                                  landschaft)  #######################################

                if mcts.root.action[3] is not None:
                    # action_ausgabe = 'k' if mcts.root.action[2] == 'k' else mcts.root.action[2]
                    logfile.write("\n\nDie AI setzt einen Meeple auf {}{}.".format(mcts.root.action[3], mcts.root.action[4]))
                elif mcts.root.action[3] == 'k':
                    logfile.write("\nDie AI setzt einem Meeple auf das Kloster.")
                else:
                    logfile.write("\nDie AI setzt keinen Meeple.")

                logfile.write("\nDie AI setzt die Karte an ({}, {}) und rotiert sie {} mal".format(mcts.root.action[0], mcts.root.action[1], mcts.root.action[2]))

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
                if mcts.root.action[3] is None:
                    landschaft = None
                elif mcts.root.action[3] == 'k':
                    landschaft = 'k'
                else:
                    l_dict = {'o': current_card.orte, 's': current_card.strassen, 'w': current_card.wiesen}
                    landschaft = [l for l in l_dict[mcts.root.action[3]] if l.name == mcts.root.action[4]][0]

                spiel.make_action(current_player, current_card, mcts.root.action[0], mcts.root.action[1], mcts.root.action[2],
                                  landschaft)  #######################################

                if mcts.root.action[3] is not None:
                    # action_ausgabe = 'k' if mcts.root.action[2] == 'k' else mcts.root.action[2]
                    logfile.write("\n\nDie AI setzt einen Meeple auf {}{}.".format(mcts.root.action[3], mcts.root.action[4]))
                elif mcts.root.action[2] == 'k':
                    logfile.write("\nDie AI setzt einem Meeple auf das Kloster.")
                else:
                    logfile.write("\nDie AI setzt keinen Meeple.")

                logfile.write("\nDie AI setzt die Karte an ({}, {}) und rotiert sie {} mal".format(mcts.root.action[0], mcts.root.action[1], mcts.root.action[2]))

                # gesetzte Karte loeschen
                del spiel.cards_left[0]

                if len(spiel.cards_left) == 0:
                    game_is_running = False

                # spieler wechseln
                current_player = d[current_player]

        else:
            print("ES GIBT FUER DIESE KARTE KEINE ANLEGESTELLE")

            # gesetzte Karte loeschen
            del spiel.cards_left[0]

            if len(spiel.cards_left) == 0:
                game_is_running = False


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

    spiel = Spiel(create_kartenliste(speed_test_karteninfoliste, False), player1, player2)
    #spiel = Spiel(create_kartenliste(test_karteninfolist, False), player1, player2)      #['OSSW', 'WWSS', 'OSSW', 'WWSWK']

    #select startspieler
    current_player = player2#random.choice((player1, player2))
    print('Der Startspieler ist Player{}'.format(current_player.nummer))

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
                            action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), 'k')
                        else:
                            action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), None)
                    except IndexError or ValueError:
                        print('ERROR CATCHED')

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
                                action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), 'k')
                            else:
                                action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), None)
                        except IndexError or ValueError:
                            pass
                        if action in pos:
                            ungueltig = False

                    spiel.make_action(current_player, current_card, action[0], action[1], action[2], action[3])

                    # gespielte action formulieren
                    if action[3]:
                        lak_id = inp_split[3][0]
                        lak_name = 1 if inp_split[3][0] == 'k' else action[3].name
                    else:
                        lak_id = None
                        lak_name = None

                    node_action = (action[0], action[1], action[2], lak_id, lak_name)

                    # root anpassen

                    # falls die aktuelle root_node bereits Kinder hat
                    if mcts.root.children:
                        for child in mcts.root.children:

                            # wenn die action von der child-node der gespielten entspricht
                            if child.action == node_action:  ###
                                mcts.root = child
                                break

                    # another player made the first move of the game, or the node has no visits yet
                    else:
                        p_num = 1 if current_player.nummer == 2 else 2
                        mcts.root = Node(True, node_action, p_num, mcts.root)

            # AI-PLayer
            else:
                #mcts.root = mcts.find_next_move(spiel)

                # erstelle Liste mit den root_nodes_kopien fuer welche die Trees aufgebaut wurden
                t_start = time.time()
                root_copies = [deepcopy(mcts.root) for i in range(4)]

                # multiprocessing
                pool = multiprocessing.Pool()
                roots = pool.starmap(calculate_tree, zip(root_copies, repeat(spiel, 4)))

                pool.close()
                pool.join()
                # ermittle die neue child-Node
                mcts.root = get_best_child(roots)

                t_ende = time.time()

                print(f'Es wurden {t_ende - t_start} Sekunden gebraucht, um die naechste Node auszurechnen.')


                # l_a_K auf die gespielt werden soll
                if mcts.root.action[3] is None:
                    landschaft = None
                elif mcts.root.action[3] == 'k':
                    landschaft = 'k'
                else:
                    l_dict = {'o': current_card.orte, 's': current_card.strassen, 'w': current_card.wiesen}
                    landschaft = [l for l in l_dict[mcts.root.action[3]] if l.name == mcts.root.action[4]][0]

                spiel.make_action(current_player, current_card, mcts.root.action[0], mcts.root.action[1], mcts.root.action[2], landschaft)   #######################################

                # falls die AI-Aktion einen Meeple auf eine Landschaft (ausser Kloster) setzt
                if mcts.root.action[3] is not None:
                    print("\nDie AI setzt einen Meeple auf {}{}.".format(mcts.root.action[3], mcts.root.action[4]))
                elif mcts.root.action[3] == 'k':
                    print("\nDie AI setzt einem Meeple auf das Kloster.")
                else:
                    print("\nDie AI setzt keinen Meeple.")

                print("Die AI setzt die Karte an ({}, {}) und rotiert sie {} mal".format(mcts.root.action[0], mcts.root.action[1], mcts.root.action[2]))

            # Vorbereitung fuer naechsten Zug
            # gesetzte Karte loeschen
            del spiel.cards_left[0]

            if len(spiel.cards_left) == 0:
                    game_is_running = False

            # spieler wechseln
            current_player = d[current_player]

        # wenn es fuer die gezogene Karte keine Anlegestelle gibt
        else:
            print("ES GIBT FUER DIESE KARTE KEINE ANLEGESTELLE")

            # gesetzte Karte loeschen
            del spiel.cards_left[0]

            if len(spiel.cards_left) == 0:
                game_is_running = False

    spiel.final_evaluate()
    print("\nSpielende: Player1 hat {} Punkte, Player2 hat {} Punkte.".format(player1.punkte, player2.punkte))


if __name__ == '__main__':
    uct_vs_uct('test')
    #c = 0
    #while True:

    #    print("\n\n\nNEUES SPIEL{}".format(c))
    #    uct_vs_uct(c)
        #player_vs_uct()
    #    c += 1