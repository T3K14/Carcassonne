from Player_Class import Player
from Spiel_class import Spiel
from card_class import karteninfoliste, create_kartenliste
from mcts2 import Node
from UCB import Node as UCB_Node


from Wiese import WieseAufKarte
from Strasse import StasseAufKarte
from Ort import Ort_auf_Karte

import random
from copy import deepcopy

# Hilfsdictionaries
dic1 = {1: 2, 2: 1}     # zum player tauschen


def testing(func1, func2, nr_of_games=100):
    """function for simulating, evaluating and logging AI Battles based one determinized card lists"""

    player1 = Player(1)
    player2 = Player(2)
    d = {player1: player2, player2: player1}
    d2 = {player1: func1, player2: func2}
    d3 = {random_select: 'Random', mc_select: 'UCB1-MC', mcts_select: 'MCTS'}

    allg_log_werte = 0
    allg_log = open('../simulations/auswertung', 'w+')
    allg_log.write('Player1 spielt nach der {}-Taktik und Player2 nach der {}-Taktik\n\n'.format(d3[func1], d3[func2]))

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
        cardlist = create_kartenliste(karteninfoliste, True)

        spiel = Spiel(cardlist, player1, player2)

        mcts_tree = None

        # starting player
        turn = player1 if i < 10 else player2

        game_log.write('Player1 spielt nach der {}-Taktik und Player2 nach der {}-Taktik\n\n'.format(d3[func1], d3[func2]))
        game_log.write('Player{} beginnt das Spiel.\n\n'.format(turn.nummer))


        while len(spiel.cards_left) > 0:

            next_card = spiel.cards_left.pop(0)                 # ?????????????????????????

            game_log.write('Neuer Zug:\n\n')
            game_log.write('Aktuell hat Player1 {} Punkte und Player2 {} Punkte.\n\n'.format(player1.punkte, player2.punkte))
            game_log.write('Player{0} zieht die Karte [{1}, {2}, {3}, {4}, {5}, {6}]'.format(turn.nummer, next_card.info[0], next_card.info[1],
                                                                                            next_card.info[2], next_card.info[3],
                                                                                            next_card.mitte, next_card.schild))
            game_log.write('\nSie enthält folgende moegliche Meeplepositionen:')
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
                action = d2[turn](spiel, next_card, turn, pos, d, mcts_tree)
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
                turn = d[turn]

            else:
                game_log.write('\nEs gibt fuer diese Kerte keine Anlegestellt.\n\n')
                print(i, 'Es gibt in diesem Spiel mal keine Anlegemoeglichkeit')
                continue

        game_log.write('Das Spiel ist vorbei. Player1 hat {} und Player2 {} Punkte.'.format(player1.punkte, player2.punkte))
        game_log.write('Die Punkte von Player1 verteilen sich dabei wie folgt:\n\nKloester:\t{}\n\nOrte:\t\t{}\n\nStrassen:\t{}\n\nWiesen:\t\t{}'.format(player1.kloster_points,
                                                                                                                                             player1.ort_points,
                                                                                                                                             player1.strassen_points,
                                                                                                                                             player1.wiesen_points))
        game_log.write(
            '\n\nDie Punkte von Player2 verteilen sich dabei wie folgt:\n\nKloester:\t{}\n\nOrte:\t\t{}\n\nStrassen:\t{}\n\nWiesen:\t\t{}'.format(
                player2.kloster_points,
                player2.ort_points,
                player2.strassen_points,
                player2.wiesen_points))
        game_log.close()

        # allg log werte anpassen
        allg_log_werte = 0

        i += 1

    allg_log.write('allg_log_werte')
    allg_log.close()


def random_select(spiel, next_card, player, pos, d, mcts=None):
    return random.choice(pos)


def mc_select(spiel, current_card, player, pos, d, mcts=None):

    child_nodes = [UCB_Node(action) for action in pos]

    t = 0
    t_end = 5

    # player stats in real game
    # current_player_stats = (player.meeples, player.punkte)
    # other_player_stats = (d[player].meeples, d[player].punkte)

    # loop as long as time is left:
    while t < t_end:

        spiel_copy = deepcopy(spiel)
        current_card_copy = deepcopy(current_card)

        current_node = max(child_nodes, key=lambda nod: nod.calculate_UCB1_value(t))

        meeple_pos = 'k'

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
        spiel_copy.make_action(player_copy, current_card_copy, current_node.action[0], current_node.action[1],
                               current_node.action[2], meeple_pos)

        # play random

        # the enemy player
        op_copy = spiel_copy.player_to_playernumber[dic1[player_copy.nummer]]

        winner = spiel_copy.play_random1v1(op_copy, player_copy, False)     # False for no random card raw

        current_node.visits += 1

        # neue evaluierung
        current_node.wins += player_copy.punkte - op_copy.punkte

        # spieler nach random-spiel wieder auf ihre ausgangswerte setzen
        # player.meeples = current_player_stats[0]
        # player.punkte = current_player_stats[1]

        # d[player].meeples = other_player_stats[0]
        # d[player].punkte = other_player_stats[1]

        # erste Karte nach dem Spiel wieder resetten
        # current_card.ecken, current_card.kanten, current_card.orte, current_card.orte_kanten,\
        # current_card.strassen, current_card.strassen_kanten, current_card.wiesen, current_card.wiesen_kanten = card_stats[0], card_stats[1], card_stats[2], card_stats[3], card_stats[4], card_stats[5], card_stats[6], card_stats[7]

        t += 1

    return max(child_nodes, key=lambda nod: nod.wins).action


def mcts_select(spiel, next_card, player, pos, d, mcts_root):
    pass


testing(mc_select, random_select, 20)
