import random
import copy
import numpy as np
import matplotlib.pyplot as plt

import KarteMod                 #for cardlist
from plot_cards import display_spielbrett_dict          #for plotting playing field
import rotate2                  #for rotating cards and their matricies

from KarteMod import Karte

from Ort import Ort
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese

from SetCard import check_card_to_possible_coordinates, set_card  #dont import update_orte etc, because they are used
#in the other modul by the imported function and work allone because they take the lists of orte and strassen etc as argument
#complete cardlist with #of streets per card, etc
card_list = KarteMod.Kartenliste

#startparameter

#list of coordinates already blocked
unavailable_coordinates = [(0, 0)]

#dict of cards beeing laid and their coordinates
cards_set = {(0, 0): Karte("S", "O", "S", "W")}
#possible next coordinates
possible_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0)]

alle_orte = {"Ort_0": Ort((0, 0), [1])}
alle_strassen = {"Strasse_0": Strasse((0, 0), [0, 2])}
alle_kloester = {}
alle_wiesen = {"Wiese_0": Wiese((0, 0), [4, 7]), "Wiese_1": Wiese((0, 0), [5, 6])}


def play_random(Kartenliste):
    """zieht zufällig karten und setzt diese random""" #mit präferenz auf positionen, die von 3 oder 4 karten umgeben sind """

    Kartenliste_in = copy.deepcopy(Kartenliste)

    #print("dis", Kartenliste_in)

    global cards_set
    global possible_coordinates
    global unavailable_coordinates
    global alle_orte, alle_strassen, alle_kloester, alle_wiesen

    random.shuffle(Kartenliste_in)

    running = True
    while running:
        if len(Kartenliste_in) < 1:  # 59
            break
        card = Kartenliste_in[0]

        moegliche_anlegestellen = check_card_to_possible_coordinates(card, possible_coordinates, cards_set)

        #print(moegliche_anlegestellen)
        #break
        try:
            choice = random.choice(moegliche_anlegestellen)

            cards_set, possible_coordinates, unavailable_coordinates, alle_orte, alle_strassen, alle_kloester,\
                alle_wiesen = set_card(choice, card, possible_coordinates, unavailable_coordinates, cards_set,\
                                      alle_orte, alle_strassen, alle_kloester, alle_wiesen)
            del Kartenliste_in[0]
        except IndexError:
            print(card.matrix)
            del Kartenliste_in[0]
            #random.shuffle(Kartenliste_in)
            continue

#play_random(card_list)

cards_set = {(0, 0): Karte("S", "O", "S", "W"),(1, 1): Karte("W", "O", "O", "W","O")}
alle_orte = {"Ort_0": Ort((0, 0), [1]), "Ort_a": Ort((1, 1), [1,2])}


#display_spielbrett_dict(cards_set)
Karte_1 = Karte("O","W","W","O","W")
#print("in spiel.py", Karte_1.orte_karte)
choice_1 = ((1, 0), 0)
cs, ak, uk, ao, ast, akl, aw = set_card(choice_1, Karte_1, possible_coordinates, unavailable_coordinates, cards_set, alle_orte, alle_strassen, alle_kloester, alle_wiesen)
#

#print(cards_set)
print([(ort, alle_orte[ort].koordinaten_plus_oeffnungen) for ort in alle_orte])
print(len(alle_orte))

#display_spielbrett_dict(cards_set)

#print(cards_set)
