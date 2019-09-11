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


def testing(func1, func2, nr_of_games=100):
    """function for simulating, evaluating and logging AI Battles based one determinized card lists"""

    player1 = Player(1)
    player2 = Player(2)
    d = {player1: player2, player2: player1}
    d2 = {player1: func1, player2: func2}
    d3 = {random_select: 'Random', mc_select: 'UCB1-MC', mcts_select: 'MCTS'}

    allg_log_werte = 0
    allg_log = open('../simulations/auswertung', 'w+')
    allg_log.write('Player1 spielt nach der {}-Taktik und Player2 nach der {}-Taktik'.format(d3[func1], d3[func2]))

    i = 0
    while i < nr_of_games:
        game_log = open('../simulations/game{}'.format(i), 'w+')

        # reset for new game
        player1.meeples = 7
        player2.meeples = 7
        player1.punkte = 0
        player2.punkte = 0

        # erstellt gemischte Kartenliste
        cardlist = create_kartenliste(karteninfoliste, True)

        spiel = Spiel(cardlist, player1, player2)

        mcts_tree = None

        # starting player
        turn = player1 if i < 50 else player2

        game_log.write('Player{} beginnt das Spiel.'.format(turn.nummer))

        while len(spiel.cards_left) > 0:

            next_card = spiel.cards_left.pop(0)                 # ?????????????????????????

            game_log.write('Neuer Zug:\n')
            game_log.write('Player{0} zieht die Karte [{1}, {2}, {3}, {4}, {5}, {6}]'.format(turn.nummer, next_card.info[0], next_card.info[1],
                                                                                            next_card.info[2], next_card.info[3],
                                                                                            next_card.mitte, next_card.schild))


            # calculate next move according to the selection function (random/MC/MCTS)
            action = d2[turn](spiel, next_card, turn, d, mcts_tree)
            spiel.make_action(turn, next_card, action[0], action[1], action[2], action[3])  # ####

            if action[3] == None:
                game_log.write('Player{} setzt keinen Meeple.')
            game_log.write('Player{} rotiert die Karte {} mal und setzt sie auf ({}, {})')

            turn = d[turn]

        game_log.write('Fertig gespielt')
        game_log.close()

        # allg log werte anpassen
        allg_log_werte = 0

        i += 1

    allg_log.write('allg_log_werte')
    allg_log.close()


def random_select(spiel, next_card, player, d, mcts=None):
    return random.choice(spiel.calculate_possible_actions(next_card, player))


def mc_select(spiel, current_card, player, d, mcts=None):

    child_nodes = [UCB_Node(action) for action in spiel.calculate_possible_actions(current_card, player)]

    t = 0
    t_end = 3
    # player stats in real game
    current_player_stats = (player.meeples, player.punkte)
    other_player_stats = (d[player].meeples, d[player].punkte)

    # loop as long as time is left:
    while t < t_end:

        spiel_copy = deepcopy(spiel)
        current_card_copy = deepcopy(current_card)

        # player zurueckaendern:
        """die spieler, die beim kopieren vom Spiel veraendert wurden werden hier wieder zurueckgesetzt"""
        l = [spiel_copy.alle_orte, spiel_copy.alle_wiesen, spiel_copy.alle_strassen]
        for landart in l:
            for instance in landart:
                if instance.meeples:

                    new_d = {player: 0, d[player]: 0}
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

        # current_card_copy = deepcopy(current_card)

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

        spiel_copy.make_action(player, current_card_copy, current_node.action[0], current_node.action[1],
                               current_node.action[2], meeple_pos)

        # play random
        winner = spiel_copy.play_random1v1(d[player], player)

        current_node.visits += 1
        # if winner == player:
        #    current_node.wins += 1
        # elif winner == 0:
        #    current_node.wins += 0.5

        # neue evaluierung
        current_node.wins += player.punkte - d[player].punkte

        # spieler nach random-spiel wieder auf ihre ausgangswerte setzen
        player.meeples = current_player_stats[0]
        player.punkte = current_player_stats[1]

        d[player].meeples = other_player_stats[0]
        d[player].punkte = other_player_stats[1]

        # erste Karte nach dem Spiel wieder resetten
        # current_card.ecken, current_card.kanten, current_card.orte, current_card.orte_kanten,\
        # current_card.strassen, current_card.strassen_kanten, current_card.wiesen, current_card.wiesen_kanten = card_stats[0], card_stats[1], card_stats[2], card_stats[3], card_stats[4], card_stats[5], card_stats[6], card_stats[7]

        t += 1

    return max(child_nodes, key=lambda nod: nod.wins).action

def mcts_select(spiel, next_card, player, d, mcts_root):
    pass


testing(mc_select, random_select)