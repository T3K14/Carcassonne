from Player_Class import Player
from Spiel_class import Spiel
from card_class import karteninfoliste, create_kartenliste, mcts_list, speed_test_karteninfoliste, determinized_karteninfoliste
from mcts2 import Node
from UCB import Node as UCB_Node

from mcts_parallelized import get_best_child
import multiprocessing
from itertools import repeat

from Wiese import WieseAufKarte
from Strasse import StasseAufKarte
from Ort import Ort_auf_Karte

from plot_cards import display_spielbrett_dict, draw_card

import random
import time
from copy import deepcopy

"""Module for testing different AI players for the boardgame Carcassonne.

    For every AI player there is a decorator function and a select function. The select functions include the algorithms
    and the decorator functions are used for taking hyperparameters and then calling the selection functions with the
    given parameters.

    There are four algorithm players:
    
    - random_play():    The random_play() function does not accept any hyperparameters.
    
                        This function implements a player that makes actions at random.
                                          
                        
    - mc():             This function accepts a number of iterations, the standard value is 500.           
        
                        This function implements a simple Monte Carlo AI that divides the number of given iterations by 
                        the number of possible actions and then simulates this number of games after every possible
                        action. After that the action with the highest rewards is selected for beeing played.
                        
                        
    - flat_ucb():       This function accepts either a number of iterations or a time limit (in seconds) and a value
                        for the UCB constant c.
                        The standard settings are: # of iterations=500 and c=sqrt(2).
                        
                        This function implements a Flat-UCB player that selects its nodes with the help of the UCB1 
                        selection formula.
                        
                        
    - uct():            This function accepts either a number of iterations or a timelimit (in seconds), a UCB value for
                        the constant c and an integer for the number of multiprocessing threads that the
                        root-parallelized algorithm may run on. Standard values are: # of iterations: 500, c=sqrt(2) and
                        # of threads=1                    
    
"""

# Hilfsdictionaries
dic1 = {1: 2, 2: 1}     # zum player tauschen


# decorator functions

def mc(t_end=500):
    def mc_decorator(_mc_select, d):
        d.update({'t_end': t_end})

        def wrapper(spiel, current_card, player, pos, d, root_node):
            return _mc_select(spiel, current_card, player, pos, d, root_node, t_end)
        return wrapper
    return mc_decorator


def flat_ucb(t_end=None, rechenzeit=None, c=1.4142):
    if t_end is None and rechenzeit is None:
        t_end = 500

    def flat_ucb_decorator(_flat_ucb_select, d):
        d.update({'t_end': t_end, 'rechenzeit': rechenzeit, 'c': c})

        def wrapper(spiel, current_card, player, pos, d, root_node):
            return _flat_ucb_select(spiel, current_card, player, pos, d, root_node, t_end, rechenzeit, c)
        return wrapper
    return flat_ucb_decorator


def random_play():
    def random_decorator(_random_select, d):
        def wrapper(spiel, current_card, player, pos, d, root_node):
            return _random_select(spiel, current_card, player, pos, d, root_node)
        return wrapper
    return random_decorator


def uct(t_end=None, rechenzeit=None, c=1.4142, threads=1):
    if t_end is None and rechenzeit is None:
        t_end = 500

    def uct_decorator(_uct_select, d):
        d.update({'t_end': t_end, 'rechenzeit': rechenzeit, 'c': c, 'threads': threads})

        def wrapper(spiel, current_card, player, pos, d, root_node):
            return _uct_select(spiel, current_card, player, pos, d, root_node, t_end, rechenzeit, c, threads)
        return wrapper
    return uct_decorator


def time_helper(boole, t):
    """
    for calculating the current iteration, or the current time to determine if the algorithm is allowed to calculate
    another iteration
    :param bool: True: return t, False: return current time
    :param t: the current number of iterations
    :return: the relative already used time

    if bool == True: the algorithm works with iterations and the current iteration is returned
    else: The algorithm works with a time limit and the current time is returned

    """
    if boole:
        return t
    else:
        return time.time()


def random_select(spiel, next_card, player, pos, d, root_node):
    return random.choice(pos), root_node


def flat_ucb_select(spiel, current_card, player, pos, d, root_node, t_end, rechenzeit, c):
    child_nodes = [UCB_Node(action) for action in pos]

    t = 0
    ende = t_end if t_end else time.time() + rechenzeit
    iterationen_bool = True if t_end else False

    # loop as long as time is left:
    # while time.time() - start < rechenzeit_in_s:
    while time_helper(iterationen_bool, t) < ende:

        spiel_copy = deepcopy(spiel)
        current_card_copy = deepcopy(current_card)

        current_node = max(child_nodes, key=lambda nod: nod.calculate_UCB1_value(t, c))

        meeple_pos = 'k' if current_node.action[3] == 'k' else None

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

        # the copy of the player in this copied game
        player_copy = spiel_copy.player_to_playernumber[player.nummer]
        # if (current_node.action[0], current_node.action[1], current_node.action[2],meeple_pos) in spiel_copy.calculate_possible_actions(current_card_copy, player_copy):
        spiel_copy.make_action(player_copy, current_card_copy, current_node.action[0], current_node.action[1],
                                   current_node.action[2], meeple_pos)
        #else:
        #    print("DIE AKTION DARF EIGENTLICH GAR NICHT GESPIELT WERDEN")

        # play random

        # the enemy player
        op_copy = spiel_copy.player_to_playernumber[dic1[player_copy.nummer]]

        winner = spiel_copy.play_random1v1(op_copy, player_copy, False)  # False for no random card raw

        current_node.visits += 1

        # neue evaluierung
        current_node.wins += player_copy.punkte - op_copy.punkte

        t += 1
        #if t % 100 == 0:
        print('flat_ucb:', t)

    # return max(child_nodes, key=lambda nod: nod.wins).action, root_node
    #return max(child_nodes, key=lambda nod: nod.visits).action, root_node
    tmp = max(child_nodes, key=lambda nod: nod.visits).action, root_node
    return tmp


def mc_select(spiel, current_card, player, pos, d, root_node, t_end):
    child_nodes = [UCB_Node(action) for action in pos]

    iterations_per_node = int(t_end / len(pos))

    for node in child_nodes:
        for i in range(iterations_per_node):

            spiel_copy = deepcopy(spiel)
            current_card_copy = deepcopy(current_card)

            meeple_pos = 'k' if node.action[3] == 'k' else None

            if isinstance(node.action[3], Ort_auf_Karte):
                for ort in current_card_copy.orte:
                    if ort.name == node.action[3].name:
                        meeple_pos = ort
                        break
            elif isinstance(node.action[3], StasseAufKarte):
                for strasse in current_card_copy.strassen:
                    if strasse.name == node.action[3].name:
                        meeple_pos = strasse
                        break
            elif isinstance(node.action[3], WieseAufKarte):
                for wiese in current_card_copy.wiesen:
                    if wiese.name == node.action[3].name:
                        meeple_pos = wiese
                        break

            # the copy of the player in this copied game
            player_copy = spiel_copy.player_to_playernumber[player.nummer]

            #if (node.action[0], node.action[1], node.action[2], meeple_pos) in spiel_copy.calculate_possible_actions(current_card_copy, player_copy):
            spiel_copy.make_action(player_copy, current_card_copy, node.action[0], node.action[1], node.action[2], meeple_pos)
            #else:
            #    print("DIE AKTION HAETTE NICHT AUSGEWAEHLT WERDEN DUERFEN!")

            # play random

            # the enemy player
            op_copy = spiel_copy.player_to_playernumber[dic1[player_copy.nummer]]

            winner = spiel_copy.play_random1v1(op_copy, player_copy, False)  # False for no random card raw

            # neue evaluierung
            node.wins += player_copy.punkte - op_copy.punkte

    # return max(child_nodes, key=lambda nod: nod.wins).action, root_node
    return max(child_nodes, key=lambda nod: nod.wins).action, root_node


def uct_select(spiel, next_card, player, pos, d, root_node, t_end, rechenzeit, c, threads):

    if threads > 1:

        root_copies = [deepcopy(root_node) for i in range(threads)]

        # multiprocessing
        pool = multiprocessing.Pool()
        roots = pool.starmap(calculate_tree, zip(root_copies, repeat(spiel, threads), repeat(next_card, threads), repeat(t_end, threads), repeat(rechenzeit, threads), repeat(c, threads)))

        pool.close()
        pool.join()
        # ermittle die neue child-Node

        node = get_best_child(roots)

    else:
        # no multiprocessing
        node = calculate_tree(root_node, spiel, next_card, t_end, rechenzeit, c)

        # memory leak
        #node = get_best_child([node])

        node = max(node.children, key=lambda nod: nod.visits)

    if node.action[3] is None:
        landschaft = None
    elif node.action[3] == 'k':
        landschaft = 'k'
    else:
        l_dict = {'o': next_card.orte, 's': next_card.strassen, 'w': next_card.wiesen}
        landschaft = [l for l in l_dict[node.action[3]] if l.name == node.action[4]][0]

    node.parent = None
    return (node.action[0], node.action[1], node.action[2], landschaft), node


def calculate_tree(root, global_spiel, next_card, t_end, rechenzeit, c):
    """

    :param root:
    :param global_spiel:
    :return:
    """

    t = 0
    ende = t_end if t_end else time.time() + rechenzeit
    iterationen_bool = True if t_end else False

    while time_helper(iterationen_bool, t) < ende:

        # create new spiel entsprechend dem aktuellen Großen
        spiel = deepcopy(global_spiel)

        # nachste Karte
        #card = spiel.cards_left.pop(0)
        card = deepcopy(next_card)

        # selection
        # in select_next node die action der Node spielen und die Kartenlist updaten

        # startnode (aktuelle root-Node vom globalen Spiel)
        node = root

        # as long as there are known children, choose next child-node with uct
        # und spiele den Zug der gewaehlten Node
        while len(node.children) != 0:
            node = max(node.children, key=lambda nod: nod.calculate_UCT_value(c))

            # wenn kein Meeple platziert wird
            if node.action[3] is None:
                landschaft = None
            elif node.action[3] == 'k':
                landschaft = 'k'
            else:
                l_dict = {'o': card.orte, 's': card.strassen, 'w': card.wiesen}
                landschaft = [l for l in l_dict[node.action[3]] if l.name == node.action[4]][0]
            spiel.make_action(spiel.player_to_playernumber[node.parent.player_number], card, node.action[0],
                              node.action[1], node.action[2], landschaft)

            # naechste Karte ziehen
            if len(spiel.cards_left) > 0:
                card = spiel.cards_left.pop(0)

        # expansion if the choosen node does not represent an and-state of the game
        if node.status:
            for pos_act in spiel.calculate_possible_actions(card, spiel.player_to_playernumber[node.player_number]):
                status = True if len(spiel.cards_left) > 0 else False
                # wenn die Aktion keine Maeepleplatzierung beinhlatet
                if pos_act[3] is None:
                    node.children.append(Node(status, (pos_act[0], pos_act[1], pos_act[2], None, None),
                                              dic1[node.player_number], node))
                elif pos_act[3] == 'k':
                    node.children.append(Node(status, (pos_act[0], pos_act[1], pos_act[2], 'k', 1),
                                              dic1[node.player_number], node))
                else:
                    node.children.append(Node(status, (pos_act[0], pos_act[1], pos_act[2], pos_act[3].id,
                                                       pos_act[3].name), dic1[node.player_number], node))

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

        winner = spiel.play_random1v1(spiel.player_to_playernumber[choosen_node.player_number],
                                      spiel.player_to_playernumber[dic1[choosen_node.player_number]],
                                      random_card_draw=False)
        # backprob
        while choosen_node.parent is not None:
            choosen_node.visits += 1
            choosen_node.wins += spiel.player_to_playernumber[choosen_node.parent.player_number].punkte - spiel.player_to_playernumber[choosen_node.player_number].punkte

            choosen_node = choosen_node.parent

        # for root-node
        choosen_node.visits += 1
        #if t % 100 == 0:
        #print(t_end, t)
        t += 1

    return root


select_to_decorator = {'flat_ucb_decorator': flat_ucb_select, 'mc_decorator': mc_select, 'random_decorator': random_select, 'uct_decorator': uct_select}
name_to_method = {'flat_ucb_decorator': 'Flat-UCB', 'random_decorator': 'Random', 'uct_decorator': 'UCT', 'mc_decorator': 'Simple-MC'}


def ai_vs_ai(decorator1, decorator2, nr_of_games=100, karteninfos=karteninfoliste, shuffle=True):
    """function for simulating, evaluating and logging AI Battles based one determinized card lists


    :param decorator1:      the decorator function of the first AI
    :param decorator2:      the decorator function of the first AI
    :param nr_of_games:     the number of games that will be played, should be an even number, since after half the games
                            have been played, the beginning player is changed
    :param karteninfos:     list of card_informations for the game, the cardlist will be created from that list which has
                            the following form: ['WWSWK', 'WWSS', 'OOSSOOT', ...]
    :param shuffle:         boolean which ensures that the cardlist is beeing shuffled if True
    :return:                None
    """

    player1 = Player(1)
    player2 = Player(2)

    # dictionaries, um die Hyperparameter in die log-Dateien schreiben zu koennen
    dic1 = {}
    dic2 = {}

    func1 = decorator1(select_to_decorator[decorator1.__name__], dic1)
    func2 = decorator2(select_to_decorator[decorator2.__name__], dic2)

    next_player_to_player = {player1: player2, player2: player1}

    decorator_to_player = {player1: decorator1, player2: decorator2}
    function_to_player = {player1: func1, player2: func2}

    # allg_log_werte:
    first_half_1 = 0
    first_half_2 = 0
    second_half_1 = 0
    second_half_2 = 0

    first_half_draws = 0
    second_half_draws = 0

    p1_ort_meeples = 0
    p1_strasse_meeples = 0
    p1_wiese_meeple = 0
    p1_kloster_meeples = 0

    p2_ort_meeples = 0
    p2_strasse_meeples = 0
    p2_wiese_meeple = 0
    p2_kloster_meeples = 0

    allg_p1_orts_points = 0
    allg_p1_strassen_points = 0
    allg_p1_wiesen_points = 0
    allg_p1_kloester_points = 0

    allg_p2_orts_points = 0
    allg_p2_strassen_points = 0
    allg_p2_wiesen_points = 0
    allg_p2_kloester_points = 0

    p1_meeples_list_kloester = []
    p1_meeples_list_orte = []
    p1_meeples_list_strassen = []
    p1_meeples_list_wiesen = []
    p1_punkte_list_kloester = []
    p1_punkte_list_orte = []
    p1_punkte_list_strassen = []
    p1_punkte_list_wiesen = []

    p2_meeples_list_kloester = []
    p2_meeples_list_orte = []
    p2_meeples_list_strassen = []
    p2_meeples_list_wiesen = []
    p2_punkte_list_kloester = []
    p2_punkte_list_orte = []
    p2_punkte_list_strassen = []
    p2_punkte_list_wiesen = []

    p1_punkte = []
    p2_punkte = []

    allg_log = open('../simulations/auswertung', 'w+')
    allg_log.write('Player1 spielt nach der {}-Taktik mit den Hyperparametern {} und Player2 nach der {}-Taktik mit den Hyperparametern {}.\n\n'.format(name_to_method[decorator1.__name__], dic1, name_to_method[decorator2.__name__], dic2))

    i = 0
    while i < nr_of_games:


        game_log = open('../simulations/game{}'.format(i), 'w+')

        # reset for new game
        player1.meeples = 7
        player2.meeples = 7
        player1.punkte = 0
        player2.punkte = 0

        player1.meeples_per_kloster = 0
        player1.meeples_per_wiese = 0
        player1.meeples_per_strasse = 0
        player1.meeples_per_ort = 0

        player2.meeples_per_kloster = 0
        player2.meeples_per_wiese = 0
        player2.meeples_per_strasse = 0
        player2.meeples_per_ort = 0

        player1.kloster_points = 0
        player1.wiesen_points = 0
        player1.strassen_points = 0
        player1.ort_points = 0

        player2.kloster_points = 0
        player2.wiesen_points = 0
        player2.strassen_points = 0
        player2.ort_points = 0

        # erstellt gemischte Kartenliste
        cardlist = create_kartenliste(karteninfos, shuffle)
        l  = [c.info for c in cardlist]
        print(l)
        #cardlist = create_kartenliste(mcts_list, False)

        spiel = Spiel(cardlist, player1, player2)

        # starting player
        turn = player1 if i < int(nr_of_games/2) else player2

        # root-nodes
        # falls beide Spieler UCT-Spieler sind, benoetigen beide eine root-node
        root_nodes = {}
        if decorator1.__name__ == 'uct_decorator':
            root_nodes.update({player1: Node(True, None, turn.nummer)})

        if decorator2.__name__ == 'uct_decorator':
            root_nodes.update({player2: Node(True, None, turn.nummer)})

        # falls kein Spieler ein UCT-Spieler ist, wird keine root-Node benoetigt, falls einer ein UCT-Spieler ist, wird
        # dessen root-Node als allgemeine root-node festgelegt
        if len(root_nodes) == 0:
            root_node = None
        elif len(root_nodes) == 1:
            root_node = list(root_nodes.values())[0]

        game_log.write('Player1 spielt nach der {}-Taktik mit den Hyperparametern {} und Player2 nach der {}-Taktik mit den Hyperparametern {}.\n\n'.format(name_to_method[decorator1.__name__], dic1, name_to_method[decorator2.__name__], dic2))
        game_log.write('Player{} beginnt das Spiel.\n\n'.format(turn.nummer))

        while len(spiel.cards_left) > 0:

            next_card = spiel.cards_left.pop(0)

            game_log.write('Neuer Zug:\n\n')
            game_log.write('Aktuell hat Player1 {} Punkte und Player2 {} Punkte.\n\n'.format(player1.punkte, player2.punkte))
            game_log.write('Player{0} zieht die Karte [{1}, {2}, {3}, {4}, {5}, {6}]'.format(turn.nummer, next_card.info[0], next_card.info[1],
                                                                                            next_card.info[2], next_card.info[3],
                                                                                            next_card.mitte, next_card.schild))
            game_log.write('\nSie enthaelt folgende moegliche Meeplepositionen:')
            game_log.write('\nOrte: ')
            for o in next_card.orte:
                game_log.write("{}: {}  ".format(o.name, o.kanten))
            game_log.write('\nStrassen: ')
            for s in next_card.strassen:
                game_log.write("{}: {}  ".format(s.name, s.kanten))
            game_log.write('\nWiesen: ')
            for w in next_card.wiesen:
                game_log.write("{}: {}  ".format(w.name, w.ecken))

            pos = spiel.calculate_possible_actions(next_card, turn)

            if pos:
                # calculate next move according to the selection function (random/MC/MCTS)

                if len(root_nodes) < 2:
                    action, root_node = function_to_player[turn](spiel, next_card, turn, pos, next_player_to_player, root_node)
                else:
                    action, root_nodes[turn] = function_to_player[turn](spiel, next_card, turn, pos, next_player_to_player, root_nodes[turn])

                # root_node updaten
                # falls ueberhaupt ein mcts-spieler mitspielt
                if len(root_nodes) > 0:
                    # falls der turn-spieler kein mcts spieler ist
                    if decorator_to_player[turn].__name__ != 'uct_decorator':
                        # waehle die entprechend naechste Node als neue root_node
                        if root_node.children:
                            for child in root_node.children:

                                # wenn die action von der child-node der gespielten entspricht
                                if action[3] == None:
                                    if child.action == (action[0], action[1], action[2], None, None):  ###
                                        root_node = child
                                        root_node.parent = None
                                        break
                                elif action[3] == 'k':
                                    if child.action == (action[0], action[1], action[2], 'k', 1):  ###
                                        root_node = child
                                        root_node.parent = None
                                        break
                                else:
                                    if child.action == (action[0], action[1], action[2], action[3].id, action[3].name):  ###
                                        root_node = child
                                        root_node.parent = None
                                        break

                    # another player made the first move of the game, or the node has no visits yet
                        else:
                            p_num = 1 if turn.nummer == 2 else 2

                            if action[3] == None:
                                mcts_action = (action[0], action[1], action[2], None, None)
                            elif action[3] == 'k':
                                mcts_action = (action[0], action[1], action[2], 'k', 1)
                            else:
                                mcts_action = (action[0], action[1], action[2], action[3].id, action[3].name)

                            root_node = Node(True, mcts_action, p_num, None)

                    else:
                        # falls es genau zwei uct-Spieler gibt, muss der Gegner updaten. Gibt es nur einen UCT-Spieler,
                        # ansonsten hat der UCT-Spieler die root-Node bereits upgedatet
                        if len(root_nodes) == 2:
                            # der Gegner muss seine Node um die Aktion updaten, die der turn-Spieler gerade gespielt hat
                            if root_nodes[next_player_to_player[turn]].children:
                                for child in root_nodes[next_player_to_player[turn]].children:

                                    # wenn die action von der child-node der gespielten entspricht

                                    if action[3] == None:
                                        mcts_action = (action[0], action[1], action[2], None, None)
                                    elif action[3] == 'k':
                                        mcts_action = (action[0], action[1], action[2], 'k', 1)
                                    else:
                                        mcts_action = (action[0], action[1], action[2], action[3].id, action[3].name)

                                    if child.action == mcts_action:  ###
                                        root_nodes[next_player_to_player[turn]] = child
                                        break

                            # another player made the first move of the game, or the node has no visits yet
                            else:
                                p_num = 1 if turn.nummer == 2 else 2

                                if action[3] == None:
                                    mcts_action = (action[0], action[1], action[2], None, None)
                                elif action[3] == 'k':
                                    mcts_action = (action[0], action[1], action[2], 'k', 1)
                                else:
                                    mcts_action = (action[0], action[1], action[2], action[3].id, action[3].name)

                                root_nodes[next_player_to_player[turn]] = Node(True, mcts_action, p_num, None)

                spiel.make_action(turn, next_card, action[0], action[1], action[2], action[3])

                if action[3] is not None and action[3] != 'k':
                    # action_ausgabe = 'k' if mcts.root.action[2] == 'k' else mcts.root.action[2]
                    game_log.write(
                        "\n\nPlayer{} setzt einen Meeple auf {}{}.".format(turn.nummer, action[3].id, action[3].name))
                elif action[3] == 'k':
                    game_log.write("\nPlayer{} setzt einem Meeple auf das Kloster.".format(turn.nummer))
                else:
                    game_log.write("\nPlayer{} setzt keinen Meeple.".format(turn.nummer))

                game_log.write(
                    "\nPlayer{} setzt die Karte an ({}, {}) und rotiert sie {} mal\n\n".format(turn.nummer, action[0],
                                                                                               action[1], action[2]))
                turn = next_player_to_player[turn]

            else:
                game_log.write('\nEs gibt fuer diese Kerte keine Anlegestellt.\n\n')
                print(i, 'Es gibt in diesem Spiel mal keine Anlegemoeglichkeit')
                continue

        spiel.final_evaluate()

        p1_punkte.append(player1.punkte)
        p2_punkte.append(player2.punkte)

        game_log.write('Das Spiel ist vorbei. Player1 hat {} und Player2 {} Punkte.'.format(player1.punkte, player2.punkte))
        game_log.write(
            '\n\nDie Punkte von Player1 verteilen sich dabei wie folgt:\n\n{} Kloester:\t{}\n\n{} Orte:\t\t{}\n\n{} Strassen:\t{}\n\n{} Wiesen:\t{}'.format(
                player1.meeples_per_kloster,
                player1.kloster_points,
                player1.meeples_per_ort,
                player1.ort_points,
                player1.meeples_per_strasse,
                player1.strassen_points,
                player1.meeples_per_wiese,
                player1.wiesen_points))
        game_log.write(
            '\n\nDie Punkte von Player2 verteilen sich dabei wie folgt:\n\n{} Kloester:\t{}\n\n{} Orte:\t\t{}\n\n{} Strassen:\t{}\n\n{} Wiesen:\t{}'.format(
                player2.meeples_per_kloster,
                player2.kloster_points,
                player2.meeples_per_ort,
                player2.ort_points,
                player2.meeples_per_strasse,
                player2.strassen_points,
                player2.meeples_per_wiese,
                player2.wiesen_points))
        game_log.close()

        # allg log:

        allg_log.write(f'\n\nSpiel {i}: Spieler1 hat {player1.punkte} und Spieler2 hat {player2.punkte} Punkte.')
        allg_log.write(
            '\n\nDie Punkte von Player1 verteilen sich dabei wie folgt:\n\n{} Kloester:\t{}\n\n{} Orte:\t\t{}\n\n{} Strassen:\t{}\n\n{} Wiesen:\t{}'.format(
                player1.meeples_per_kloster,
                player1.kloster_points,
                player1.meeples_per_ort,
                player1.ort_points,
                player1.meeples_per_strasse,
                player1.strassen_points,
                player1.meeples_per_wiese,
                player1.wiesen_points))
        allg_log.write(
            '\n\nDie Punkte von Player2 verteilen sich dabei wie folgt:\n\n{} Kloester:\t{}\n\n{} Orte:\t\t{}\n\n{} Strassen:\t{}\n\n{} Wiesen:\t{}'.format(
                player2.meeples_per_kloster,
                player2.kloster_points,
                player2.meeples_per_ort,
                player2.ort_points,
                player2.meeples_per_strasse,
                player2.strassen_points,
                player2.meeples_per_wiese,
                player2.wiesen_points))


        allg_log_werte = 0
        if i < int(nr_of_games/2):
            if player1.punkte > player2.punkte:
                first_half_1 += 1
            elif player2.punkte > player1.punkte:
                first_half_2 += 1
            else:
                first_half_draws += 1
        else:
            if player1.punkte > player2.punkte:
                second_half_1 += 1
            elif player2.punkte > player1.punkte:
                second_half_2 += 1
            else:
                second_half_draws += 1
        # allg daten

        #meeples
        #player1
        p1_ort_meeples += player1.meeples_per_ort
        p1_meeples_list_orte.append(player1.meeples_per_ort)

        p1_strasse_meeples += player1.meeples_per_strasse
        p1_meeples_list_strassen.append(player1.meeples_per_strasse)

        p1_wiese_meeple += player1.meeples_per_wiese
        p1_meeples_list_wiesen.append(player1.meeples_per_wiese)

        p1_kloster_meeples += player1.meeples_per_kloster
        p1_meeples_list_kloester.append(player1.meeples_per_kloster)

        #player2
        p2_ort_meeples += player2.meeples_per_ort
        p2_meeples_list_orte.append(player2.meeples_per_ort)

        p2_strasse_meeples += player2.meeples_per_strasse
        p2_meeples_list_strassen.append(player2.meeples_per_strasse)

        p2_wiese_meeple += player2.meeples_per_wiese
        p2_meeples_list_wiesen.append(player2.meeples_per_wiese)

        p2_kloster_meeples += player2.meeples_per_kloster
        p2_meeples_list_kloester.append(player2.meeples_per_kloster)

        #punkte
        #player1
        allg_p1_orts_points += player1.ort_points
        p1_punkte_list_orte.append(player1.ort_points)

        allg_p1_strassen_points += player1.strassen_points
        p1_punkte_list_strassen.append(player1.strassen_points)

        allg_p1_wiesen_points += player1.wiesen_points
        p1_punkte_list_wiesen.append(player1.wiesen_points)

        allg_p1_kloester_points += player1.kloster_points
        p1_punkte_list_kloester.append(player1.kloster_points)

        #player2
        allg_p2_orts_points += player2.ort_points
        p2_punkte_list_orte.append(player2.ort_points)

        allg_p2_strassen_points += player2.strassen_points
        p2_punkte_list_strassen.append(player2.strassen_points)

        allg_p2_wiesen_points += player2.wiesen_points
        p2_punkte_list_wiesen.append(player2.wiesen_points)

        allg_p2_kloester_points += player2.kloster_points
        p2_punkte_list_kloester.append(player2.kloster_points)

        i += 1

    allg_log.write('\n\n\nAllgemeine Auswertung:\n\n\n')
    allg_log.write(f'Spieler1 hat in der ersten Haelfte {first_half_1} Spiele gewonnen, Player2 {first_half_2} und {first_half_draws} Spiele endeten Unentschieden.')
    allg_log.write(f'Spieler1 hat in der zweiten Haelfte {second_half_1} Spiele gewonnen, Player2 {second_half_2} und {second_half_draws} Spiele endeten Unentschieden.')

    allg_log.write('\n\nPlayer1 hat durchschnittlich folgende Zahl von Meeples auf die folgenden Gebiete gesetzt:\n\n')
    allg_log.write(f'Orte:\t\t{p1_ort_meeples/nr_of_games}\n')
    allg_log.write(f'Strassen:\t{p1_strasse_meeples/nr_of_games}\n')
    allg_log.write(f'Kloester:\t{p1_kloster_meeples/nr_of_games}\n')
    allg_log.write(f'Wiesen:\t\t{p1_wiese_meeple/nr_of_games}\n\n')

    allg_log.write('Player2 hat durchschnittlich folgende Zahl von Meeples auf die folgenden Gebiete gesetzt:\n\n')
    allg_log.write(f'Orte:\t\t{p2_ort_meeples/nr_of_games}\n')
    allg_log.write(f'Strassen:\t{p2_strasse_meeples/nr_of_games}\n')
    allg_log.write(f'Kloester:\t{p2_kloster_meeples/nr_of_games}\n')
    allg_log.write(f'Wiesen:\t\t{p2_wiese_meeple/nr_of_games}\n\n')

    allg_log.write('Player1 hat in den Spielen durchschnittlich folgende Punktzahlen mit den folgenden Gebieten gemacht:\n\n')
    allg_log.write(f'Orte:\t\t{allg_p1_orts_points/nr_of_games}\n')
    allg_log.write(f'Strassen:\t{allg_p1_strassen_points/nr_of_games}\n')
    allg_log.write(f'Kloester:\t{allg_p1_kloester_points/nr_of_games}\n')
    allg_log.write(f'Wiesen:\t\t{allg_p1_wiesen_points/nr_of_games}\n\n')

    allg_log.write('Player2 hat in den Spielen durchschnittlich folgende Punktzahlen mit den folgenden Gebieten gemacht:\n\n')
    allg_log.write(f'Orte:\t\t{allg_p2_orts_points/nr_of_games}\n')
    allg_log.write(f'Strassen:\t{allg_p2_strassen_points/nr_of_games}\n')
    allg_log.write(f'Kloester:\t{allg_p2_kloester_points/nr_of_games}\n')
    allg_log.write(f'Wiesen:\t\t{allg_p2_wiesen_points/nr_of_games}\n')


    try:
        allg_log.write('\nDas entspricht den folgenden Durchschnittswerten fuer Punkte pro feature-meeple:\n')
        allg_log.write('\nPlayer1:\n\n')
        allg_log.write(f'{allg_p1_orts_points/p1_ort_meeples} Punkte pro Orts-Meeple\n')
        allg_log.write(f'{allg_p1_strassen_points/p1_strasse_meeples} Punkte pro Strassen-Meeple\n')
        allg_log.write(f'{allg_p1_wiesen_points/p1_wiese_meeple} Punkte pro Wiesen-Meeple\n')
        allg_log.write(f'{allg_p1_kloester_points/p1_kloster_meeples} Punkte pro Kloster-Meeple\n\n')

        allg_log.write('Player2:\n\n')
        allg_log.write(f'{allg_p2_orts_points/p2_ort_meeples} Punkte pro Orts-Meeple\n')
        allg_log.write(f'{allg_p2_strassen_points/p2_strasse_meeples} Punkte pro Strassen-Meeple\n')
        allg_log.write(f'{allg_p2_wiesen_points/p2_wiese_meeple} Punkte pro Wiesen-Meeple\n')
        allg_log.write(f'{allg_p2_kloester_points/p2_kloster_meeples} Punkte pro Kloster-Meeple\n')

    except ZeroDivisionError:
        print("Error: Division durch 0")

    allg_log.write('\nDie einzelnen Spielwerte noch mal in Listen:\n')
    allg_log.write('Die von Player1 gesetzen Meeples auf die jeweiligen Gebiete:\n\n')
    allg_log.write(f'Orte1 = {p1_meeples_list_orte}\n')
    allg_log.write(f'Strassen1 = {p1_meeples_list_strassen}\n')
    allg_log.write(f'Wiesen1 = {p1_meeples_list_wiesen}\n')
    allg_log.write(f'Kloester1 = {p1_meeples_list_kloester}\n\n')
    allg_log.write('Die von Player2 gesetzen Meeples auf die jeweiligen Gebiete:\n\n')
    allg_log.write(f'Orte2 = {p2_meeples_list_orte}\n')
    allg_log.write(f'Strassen2 = {p2_meeples_list_strassen}\n')
    allg_log.write(f'Wiesen2 = {p2_meeples_list_wiesen}\n')
    allg_log.write(f'Kloester2 = {p2_meeples_list_kloester}\n\n')

    allg_log.write('Die von Player1 bekommenen Punkte mit den Gebieten:\n\n')
    allg_log.write(f'Orte1_punkte = {p1_punkte_list_orte}\n')
    allg_log.write(f'Strassen1_punkte = {p1_punkte_list_strassen}\n')
    allg_log.write(f'Wiesen1_punkte = {p1_punkte_list_wiesen}\n')
    allg_log.write(f'Kloester1_punkte = {p1_punkte_list_kloester}\n\n')

    allg_log.write('Die von Player2 bekommenen Punkte mit den Gebieten:\n\n')
    allg_log.write(f'Orte2_punkte = {p2_punkte_list_orte}\n')
    allg_log.write(f'Strassen2_punkte = {p2_punkte_list_strassen}\n')
    allg_log.write(f'Wiesen2_punkte = {p2_punkte_list_wiesen}\n')
    allg_log.write(f'Kloester2_punkte = {p2_punkte_list_kloester}\n\n')

    allg_log.write(f'Player1_ergebnisse = {p1_punkte}')
    allg_log.write(f'\nPlayer2_ergebnisse = {p2_punkte}')


    allg_log.close()


def human_vs_ai(decorator, karteninfos=karteninfoliste, shuffle=True, startspieler='human'):
    """

    function for playing a game against any implemented AI as a human player, based on a determinized cardlist

    :param decorator:       the decorator function of the AI player
    :param karteninfos:     list of card_informations for the game, the cardlist will be created from that list which has
                            the following form: ['WWSWK', 'WWSS', 'OOSSOOT', ...]
    :param shuffle:         boolean which ensures that the cardlist is beeing shuffled if True
    :param startspieler:    either 'human', or 'ai' for selecting the starting player
    :return:                None

    The human player enters his commands via the python console:

    For every card that is drawn by the human player there are information printed to the console.
    One example might be:

        Die naechste Karte ist [S, O, S, S, G, False]
        Sie enthaelt folgende moegliche Meeplepositionen:
        Orte:
        1 [1]
        Strassen:
        1 [0]
        2 [2]
        3 [3]
        Wiesen:
        1 [4]
        2 [5, 6]
        3 [7]
        Bitte gib deine Aktion an:

    To enter the command, one has to use the following format:
    x y (# of right-rotations) (letter for territory+# of territory)

    For example:
    0 1 3 o1

    This stands for the following action:
        - placing a meeple on the ort 1, which is located on the right side of the card
        - rotating the card three times to the right
        - placing the tile on the filed (0,1)

    """


    player1 = Player(1)
    player2 = Player(2, 'ai')
    d = {player1: player2, player2: player1}

    spiel = Spiel(create_kartenliste(karteninfos, shuffle), player1, player2)

    # select startspieler
    current_player = player1 if startspieler == 'human' else player2
    print('Der Startspieler ist {} und hat die Nummer {}'.format(current_player.art, current_player.nummer))

    # the function that the AI uses for selecting it's next move
    dic1 = {}
    ai_select = decorator(select_to_decorator[decorator.__name__], dic1)

    # playing against an UCT-Player?
    uct_bool = True if select_to_decorator[decorator.__name__] == uct_select else False

    root = Node(True, None, current_player.nummer)

    while len(spiel.cards_left) > 0:

        print(f'\n\nNEUER ZUG: Aktuell hat player1 {player1.punkte} Punkte und {player1.meeples} Meeples und player2 {player2.punkte} Punkte und {player2.meeples} Meeples.\n')

        display_spielbrett_dict(spiel.cards_set)
        current_card = spiel.cards_left.pop(0)

        print('Die nachste Karte ist [{0}, {1}, {2}, {3}, {4}, {5}]'.format(current_card.info[0], current_card.info[1],
                                                                            current_card.info[2], current_card.info[3],
                                                                            current_card.mitte, current_card.schild))

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

        draw_card(current_card)

        pos = spiel.calculate_possible_actions(current_card, current_player)

        # wenn es moegliche anlegestellenn (fuer den aktuellen Spieler) gibt, (es gibt fuer einen spieler auf jeden Fall
        # eine Anlegemoeglichkeit, wenn es fuer den anderen auch eine gibt)
        if pos:
            if current_player.art == 'human':

                # gib move ein
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

                if uct_bool:

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
                    if root.children:
                        for child in root.children:

                            # wenn die action von der child-node der gespielten entspricht
                            if child.action == node_action:
                                root = child
                                break

                    # another player made the first move of the game, or the node has no visits yet
                    else:
                        root = Node(True, node_action, 2, None)

            # AI-PLayer
            else:

                action, root = ai_select(spiel, current_card, current_player, pos, d, root)
                spiel.make_action(current_player, current_card, action[0], action[1], action[2], action[3])

                # falls die AI-Aktion einen Meeple auf eine Landschaft (ausser Kloster) setzt
                if action[3] == 'k':
                    print("\nDie AI setzt einem Meeple auf das Kloster.")
                elif action[3] is not None:
                    print("\nDie AI setzt einen Meeple auf {}{}.".format(action[3].id, action[3].name))
                else:
                    print("\nDie AI setzt keinen Meeple.")

                print("Die AI rotiert die Karte {} mal und setzt sie an ({}, {}) ".format(action[2], action[0], action[1]))

            # spieler wechseln
            current_player = d[current_player]

        # wenn es fuer die gezogene Karte keine Anlegestelle gibt
        else:
            print("ES GIBT FUER DIESE KARTE KEINE ANLEGESTELLE")
            continue

    print(f'\nVor der finalen Auswertung hat Player1 {player1.punkte} und {player1.meeples} Meeples und Player2 {player2.punkte} Punkte und {player2.meeples} Meeples.')

    spiel.final_evaluate()
    print("\nSpielende: Player1 hat {} Punkte, Player2 hat {} Punkte.".format(player1.punkte, player2.punkte))


if __name__ == '__main__':
    #ai_vs_ai(uct(None, 600, 4), flat_ucb(None, 600, 4),  10, karteninfoliste, True)
    human_vs_ai(uct(None, 150, 4), karteninfoliste, True)
