from Player_Class import Player
from Spiel_class import Spiel
from card_class import karteninfoliste


import random

def testing(func1, func2='human', nr_of_games=100):
    """function for simulating, evaluating and logging AI Battles or games of an AI-agent against a human player based
    one determinized card lists"""

    player1 = Player(1)
    player2 = Player(2)
    d = {player1: player2, player2: player1}
    d2 = {player1: func1, player2: func2}

    allg_log_werte = 0
    allg_log = open('../simulations/auswertung', 'w+')

    i = 0
    while i < nr_of_games:
        game_log = open('../simulations/game{}'.format(i), 'w+')

        # reset for new game
        player1.meeples = 7
        player2.meeples = 7
        player1.punkte = 0
        player2.punkte = 0

        cardlist = random.shuffle(karteninfoliste)
        spiel = Spiel(cardlist, player1, player2)

        mcts_tree = None

        #starting player
        turn = player1 if i < 50 else player2

        while len(spiel.cards_left > 0):

            next_card = spiel.cards_left.pop(0)                 #?????????????????????????

            #if turn == player1:

            #calculate next move according to the selection function (random/MC/MCTS)
            action = d2[turn]('alles, was die funktionen brauchen')
            spiel.make_action(turn, next_card, [0], action[0], action[1], 'und so weiter')

            game_log.write('string')

            turn = d[turn]

        game_log.write('Fertig gespielt')
        game_log.close()

        #allg log werte anpassen
        allg_log_werte = 0

        i += 1

    allg_log.write('allg_log_werte')
    allg_log.close()


def random_select(spiel, next_card):
    pass


def mc_select():
    pass

def mcts_select():
    pass