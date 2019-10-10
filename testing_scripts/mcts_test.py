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
import unittest

from rotate2 import rotate_info_right, rotate_kanten_dict_right


class MCTSTest(unittest.TestCase):

    def test_1(self):

        player1 = Player(1)
        player2 = Player(2, 'ai')
        d = {player1: player2, player2: player1}

        #zum probieren
        #spiel = Spiel(create_kartenliste(determinized_short_karteninfoliste, False), player1, player2)

        spiel = Spiel(create_kartenliste(determinized_karteninfoliste, False), player1, player2)

        #select startspieler
        current_player = player1

        k1 = spiel.cards_left.pop(0)
        spiel.make_action(current_player, k1, 1, 0, 2, k1.orte[0])

        self.assertEqual(70, len(spiel.cards_left))
        self.assertEqual(player1.punkte, 4)
        self.assertEqual(player1.meeples, 7)

        k1 = spiel.cards_left.pop(0)
        wiese = None
        for w in k1.wiesen:
            if w.ecken == [4, 5, 6]:
                wiese = w
                break
        spiel.make_action(d[current_player], k1, 0, 1, 0, wiese)

        self.assertEqual(69, len(spiel.cards_left))
        self.assertEqual(4, player1.punkte)
        self.assertEqual(7, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(6, player2.meeples)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(current_player, k1, 0, -1, 1, k1.orte[0])

        self.assertEqual(68, len(spiel.cards_left))
        self.assertEqual(4, player1.punkte)
        self.assertEqual(6, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(6, player2.meeples)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(d[current_player], k1, -1, 0, 2)

        self.assertEqual(67, len(spiel.cards_left))
        self.assertEqual(4, player1.punkte)
        self.assertEqual(6, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(6, player2.meeples)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(current_player, k1, -1, -1, 3, k1.orte[0])

        self.assertEqual(66, len(spiel.cards_left))
        self.assertEqual(4, player1.punkte)
        self.assertEqual(5, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(6, player2.meeples)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(d[current_player], k1, 1, 1, 3, 'k')

        self.assertEqual(65, len(spiel.cards_left))
        self.assertEqual(4, player1.punkte)
        self.assertEqual(5, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(5, player2.meeples)

        k1 = spiel.cards_left.pop(0)

        #display_spielbrett_dict(spiel.cards_set)
        spiel.make_action(current_player, k1, -1, 1, 0, k1.strassen[0])

        self.assertEqual(64, len(spiel.cards_left))
        self.assertEqual(4, player1.punkte)
        self.assertEqual(4, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(5, player2.meeples)

        k1 = spiel.cards_left.pop(0)

        wiese = None
        for w in k1.wiesen:
            if w.ecken == [7]:
                wiese = w
                break
        spiel.make_action(d[current_player], k1, -2, 0, 3, wiese)

        self.assertEqual(63, len(spiel.cards_left))
        self.assertEqual(4, player1.punkte)
        self.assertEqual(4, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(4, player2.meeples)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(current_player, k1, 0, 2, 1, None)

        self.assertEqual(62, len(spiel.cards_left))
        self.assertEqual(4, player1.punkte)
        self.assertEqual(4, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(4, player2.meeples)


        k1 = spiel.cards_left.pop(0)

        spiel.make_action(d[current_player], k1, 0, 3, 0, k1.orte[0])

        self.assertEqual(61, len(spiel.cards_left))
        self.assertEqual(4, player1.punkte)
        self.assertEqual(4, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(3, player2.meeples)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(current_player, k1, -2, -1, 0, None)

        self.assertEqual(60, len(spiel.cards_left))
        self.assertEqual(11, player1.punkte)
        self.assertEqual(5, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(3, player2.meeples)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(d[current_player], k1, -1, 3, 0, None)

        self.assertEqual(59, len(spiel.cards_left))
        self.assertEqual(11, player1.punkte)
        self.assertEqual(5, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(3, player2.meeples)

        self.assertEqual(len(spiel.alle_kloester), 1)
        self.assertEqual(len(spiel.alle_strassen), 8)
        self.assertEqual(len(spiel.alle_orte), 5)
        self.assertEqual(len(spiel.alle_wiesen), 8)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(current_player, k1, -1, -2, 3 , k1.wiesen[0])

        self.assertEqual(58, len(spiel.cards_left))
        self.assertEqual(21, player1.punkte)
        self.assertEqual(5, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(3, player2.meeples)

        self.assertEqual(len(spiel.alle_kloester), 1)
        self.assertEqual(len(spiel.alle_strassen), 8)
        self.assertEqual(len(spiel.alle_orte), 6)
        self.assertEqual(len(spiel.alle_wiesen), 9)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(d[current_player], k1, 2, 1, 1, None)

        self.assertEqual(57, len(spiel.cards_left))
        self.assertEqual(21, player1.punkte)
        self.assertEqual(5, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(3, player2.meeples)

        self.assertEqual(len(spiel.alle_kloester), 1)
        self.assertEqual(len(spiel.alle_strassen), 8)
        self.assertEqual(len(spiel.alle_orte), 6)
        self.assertEqual(len(spiel.alle_wiesen), 9)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(current_player, k1, -1, -3, 0, k1.orte[0])

        self.assertEqual(56, len(spiel.cards_left))
        self.assertEqual(21, player1.punkte)
        self.assertEqual(4, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(3, player2.meeples)

        self.assertEqual(len(spiel.alle_kloester), 1)
        self.assertEqual(len(spiel.alle_strassen), 8)
        self.assertEqual(len(spiel.alle_orte), 7)
        self.assertEqual(len(spiel.alle_wiesen), 10)


        k1 = spiel.cards_left.pop(0)

        ort = None
        for o in k1.orte:
            if o.kanten == [3]:
                ort = o
                break
        spiel.make_action( d[current_player], k1, -3, 0, 1, ort)

        self.assertEqual(55, len(spiel.cards_left))
        self.assertEqual(21, player1.punkte)
        self.assertEqual(4, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(2, player2.meeples)

        self.assertEqual(len(spiel.alle_kloester), 1)
        self.assertEqual(len(spiel.alle_strassen), 8)
        self.assertEqual(len(spiel.alle_orte), 9)
        self.assertEqual(len(spiel.alle_wiesen), 10)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(current_player, k1, 0, -2, 0, None)

        self.assertEqual(54, len(spiel.cards_left))
        self.assertEqual(27, player1.punkte)
        self.assertEqual(5, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(2, player2.meeples)

        self.assertEqual(len(spiel.alle_kloester), 1)
        self.assertEqual(len(spiel.alle_strassen), 8)
        self.assertEqual(len(spiel.alle_orte), 8)
        self.assertEqual(len(spiel.alle_wiesen), 11)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(d[current_player], k1, 3, 1, 1 , None)

        self.assertEqual(53, len(spiel.cards_left))
        self.assertEqual(27, player1.punkte)
        self.assertEqual(5, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(2, player2.meeples)

        self.assertEqual(len(spiel.alle_kloester), 1)
        self.assertEqual(len(spiel.alle_strassen), 8)
        self.assertEqual(len(spiel.alle_orte), 8)
        self.assertEqual(len(spiel.alle_wiesen), 11)

        k1 = spiel.cards_left.pop(0)

        spiel.make_action(current_player, k1, -2, 1, 0, 'k')

        self.assertEqual(52, len(spiel.cards_left))
        self.assertEqual(27, player1.punkte)
        self.assertEqual(4, player1.meeples)

        self.assertEqual(0, player2.punkte)
        self.assertEqual(2, player2.meeples)

        self.assertEqual(len(spiel.alle_kloester), 2)
        self.assertEqual(len(spiel.alle_strassen), 8)
        self.assertEqual(len(spiel.alle_orte), 8)
        self.assertEqual(len(spiel.alle_wiesen), 11)

        mcts = MCTS((player1, player2), spiel.play_random1v1, spiel.calculate_possible_actions)
        mcts.root = Node(True, None, d[current_player].nummer)

        player1.art = 'human'
        player2.art = 'ai'

        current_player = d[current_player]

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
    unittest.main()