import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import time

from Rotate import Rotate
from KarteMod import Karte
from KarteMod import Kartenliste

from Ort import Ort
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese

start_time = time.clock()

def check_card_to_possible_coordinates(Karte, possible_coordinates, cards_set):
    """checkt, ob und wie karte an jede freie stelle gelegt werden kann,
        returned liste mit tupel bestehend aus moeglicher anlegestelle und anzahl von rotationen die dafür noetig sind """

    possible_anlegemoeglichkeiten = []

    card = Karte

    ij = [(0, 2), (1, 3), (2, 0), (3, 1)]
    for x, y in possible_coordinates:
        nkoos = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
        nks = []

        for relative_pos, nkoo in enumerate(nkoos):
            for gelegte_karte in cards_set:
                #print("G",gelegte_karte)
                if gelegte_karte == nkoo:
                    nks.append(((gelegte_karte, cards_set[gelegte_karte]), relative_pos))

        #print(nks)

        if len(nks) == 1:
            i, j = ij[nks[0][1]]
            for z in range(4):
                # print(card.info)
                if card.info[i] == nks[0][0][1].info[j]:
                    possible_anlegemoeglichkeiten.append(((x, y), z))
                card.info = Rotate.rotate_card_right(card.info)

        if len(nks) == 2:
            ij_neu = [ij[nks[länge][1]] for länge in range(len(nks))]
            for z in range(4):
                i, j = ij_neu[0]
                if card.info[i] == nks[0][0][1].info[j]:
                    i, j = ij_neu[1]
                    if card.info[i] == nks[1][0][1].info[j]:
                        possible_anlegemoeglichkeiten.append(((x, y), z))
                card.info = Rotate.rotate_card_right(card.info)

        if len(nks) == 3:
            ij_neu = [ij[nks[länge][1]] for länge in range(len(nks))]
            for z in range(4):
                i, j = ij_neu[0]
                if card.info[i] == nks[0][0][1].info[j]:
                    i, j = ij_neu[1]
                    if card.info[i] == nks[1][0][1].info[j]:
                        i, j = ij_neu[2]
                        if card.info[i] == nks[2][0][1].info[j]:
                            possible_anlegemoeglichkeiten.append(((x, y), z))

                card.info = Rotate.rotate_card_right(card.info)

        if len(nks) == 4:
            ij_neu = [ij[nks[länge][1]] for länge in range(len(nks))]
            for z in range(4):
                i, j = ij_neu[0]
                if card.info[i] == nks[0][0][1].info[j]:
                    i, j = ij_neu[1]
                    if card.info[i] == nks[1][0][1].info[j]:
                        i, j = ij_neu[2]
                        if card.info[i] == nks[2][0][1].info[j]:
                            i, j = ij_neu[3]
                            if card.info[i] == nks[3][0][1].info[j]:
                                possible_anlegemoeglichkeiten.append(((x, y), z))

                card.info = Rotate.rotate_card_right(card.info)
    return (possible_anlegemoeglichkeiten)


#kommt spaeter raus

def display_spielbrett(cards_set):
    bild = plt.figure()
    x_coord_list = []
    y_coord_list = []

    for (a, b) in cards_set:
        x_coord_list.append(a)
        y_coord_list.append(b)

    x_max = max(x_coord_list)
    x_min = min(x_coord_list)

    y_max = max(y_coord_list)
    y_min = min(y_coord_list)

    x_sub = x_max - x_min + 1
    y_sub = y_max - y_min + 1

    from matplotlib.colors import ListedColormap
    custom_cmap = ListedColormap(['green', 'brown', 'white', 'blue', 'k'])

    for nr, info in enumerate(cards_set):
        (x, y) = info
        card = cards_set[info]
        i = (abs(y - y_max)) * x_sub + abs(x - x_min) + 1
        ax = bild.add_subplot(y_sub, x_sub, i)
        ax.title.set_text(str((x,y)))
        ax.matshow(card.matrix, cmap=custom_cmap, vmin=0, vmax=4)

        plt.subplots_adjust(wspace=0.25, hspace=0.25)                 # 0, 0
        plt.xticks(np.array([]))
        plt.yticks(np.array([]))
    plt.show()

def set_card(tuple, Karte, possible_coordinates, unavailable_coordinates, cards_set):
    """setzt karte an koordinaten (x,y) und updated cards_set, possible_coordiantes und unavailable_coordinates"""

    #print(Karte.wiesenKarte)


    (x, y) = tuple[0]  # koordinaten
    z = tuple[1]  # anzahl an rechtsrotationen
    for i in range(z):
        Karte.info = Rotate.rotate_card_right(Karte.info)
        Karte.matrix = Rotate.rotate_matrix_right(Karte.matrix)
        Karte.orte = Rotate.rotate_list_right(Karte.orte)
        Karte.strassen = Rotate.rotate_list_right(Karte.strassen)
        Karte.wiesenKarte = Rotate.rotateWiesenRight(Karte.wiesenKarte)


    cards_set.update({(x, y): Karte})  # ((x,y),Karte)

    liste_kanten = [i for ort in Karte.orte_karte for i in ort[1]]
    zu_loeschende_orte = []
    beteiligte_orte = []
    counter = []

    for ort in Karte.orte_karte:

        wert_ort = ort[2]

        for oeffnung in ort[1]:
            if oeffnung < 2:
                oe_to_check = oeffnung + 2
            else:
                oe_to_check = oeffnung - 2
            dict = {0: (x, y - 1), 1: (x - 1, y), 2: (x, y + 1), 3: (x + 1, y)}

            for o in alle_orte:
                ### wenn nachbarkoordinaten besetzt sind UND deren ortskanten zu neuer karte mit denen dieser neuen Karte uebereinstimmen
                if dict[oe_to_check] in alle_orte[o].koordinaten_plus_oeffnungen and \
                        oe_to_check in alle_orte[o].koordinaten_plus_oeffnungen[dict[oe_to_check]]:

                    beteiligte_orte.append((o, dict[oe_to_check], oe_to_check))
                    if o not in counter:
                        counter.append(o)

                    liste_kanten.remove(oeffnung)
                    if ort not in zu_loeschende_orte:
                        zu_loeschende_orte.append(ort)

    for ä in zu_loeschende_orte:
        #   print(ä)
        Karte.orte_karte.remove(ä)

    for ü in Karte.orte_karte:
        for oe in ü[1]:
            if oe in liste_kanten:
                liste_kanten.remove(oe)

    if len(Karte.orte) > 0:
        update_ort(liste_kanten, Karte, beteiligte_orte, tuple[0], counter, wert_ort)

    if len(Karte.strassen) > 0:
        update_strasse((x, y), Karte)

    if len(Karte.wiesenKarte) > 0:
        updateWiesen((x, y), Karte)

    # updateKloester

    if len(Karte.kloster_karte) > 0:
        # print(Karte.kloster_karte)
        liste = [(x - 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y), (x + 1, y), (x - 1, y - 1), (x, y - 1),
                 (x + 1, y - 1)]
        alle_kloester.update({Karte.kloster_karte[0]: Kloster((x, y))})
        # print("huihui", alle_kloester)
        for i in liste:
            if i in cards_set and i not in alle_kloester[Karte.kloster_karte[0]].umgebung:
                # print(Karte.kloster_karte[0])
                alle_kloester[Karte.kloster_karte[0]].umgebung.append(i)

        # kloster_dict = {0: ()}

    for k in alle_kloester:
        (v, w) = alle_kloester[k].koordinaten
        liste_ = [(v - 1, w + 1), (v, w + 1), (v - 1, w + 1), (v - 1, w), (v + 1, w), (v - 1, w - 1), (v, w - 1),
                  (v + 1, w - 1)]
        if (x, y) in liste_ and (x, y) not in alle_kloester[k].umgebung:
            alle_kloester[k].umgebung.append((x, y))

    # unavailable_- und possible_coordinates updaten

    for i, (v, w) in enumerate(possible_coordinates):
        if (x, y) == (v, w):
            unavailable_coordinates.append((v, w))
            del possible_coordinates[i]
            for (a, b) in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
                if (a, b) not in possible_coordinates and (a, b) not in unavailable_coordinates:
                    possible_coordinates.append((a, b))
    #print("ahoi",cards_set)
    return cards_set, possible_coordinates, unavailable_coordinates

meeples = 7

def update_ort(liste_kanten_, Karte_, beteiligte_orte_, koordinaten_, counter_, wert_):
    ### alte Kanten loeschen

    for i in beteiligte_orte_:
        # print("i", i)
        alle_orte[i[0]].koordinaten_plus_oeffnungen[i[1]].remove(i[2])

    ### neue Orte erstellen

    for ort in Karte_.orte_karte:
        alle_orte.update({ort[0]: Ort(koordinaten_, ort[1])})

    ### alte Orte updaten

    #print("C", counter_)

    if len(counter_) == 1:
        alle_orte[counter_[0]].koordinaten_plus_oeffnungen.update({koordinaten_: liste_kanten_})
        alle_orte[counter_[0]].wert += wert_

    else:
         if len(counter_) > 0:
            if Karte_.mitte == "O":
                hauptort = counter_[0]
                counter_.remove(hauptort)
                alle_orte[hauptort].koordinaten_plus_oeffnungen.update({koordinaten_: liste_kanten_})
                alle_orte[hauptort].wert += wert_

                for ort in counter_:
                    alle_orte[hauptort].koordinaten_plus_oeffnungen.update(alle_orte[ort].koordinaten_plus_oeffnungen)
                    alle_orte[hauptort].wert += alle_orte[ort].wert
                    del alle_orte[ort]

            else:
                for ort in counter_:
                    alle_orte[ort].koordinaten_plus_oeffnungen.update({koordinaten_: []})
                    alle_orte[ort].wert += wert_

def update_strasse(koordinaten_, Karte_):

    #print(Karte_.info, Karte_.strassen_karte)

    beteiligte_strassen = []

    if Karte_.mitte != "G":
        liste_kanten = Karte_.strassen_karte[0][1][:]

    else:
        liste_kanten = [i for strasse in Karte_.strassen_karte for i in strasse[1]]

    x, y = koordinaten_

    for strasse in Karte_.strassen_karte[:]:
        for oeffnung in strasse[1]:
            if oeffnung < 2:
                oe_to_check = oeffnung + 2

            else:
                oe_to_check = oeffnung - 2

            dict = {0: (x, y - 1), 1: (x - 1, y), 2: (x, y + 1), 3: (x + 1, y)}

            for s in alle_strassen:
                if dict[oe_to_check] in alle_strassen[s].koordinaten_plus_oeffnungen and \
                        oe_to_check in alle_strassen[s].koordinaten_plus_oeffnungen[dict[oe_to_check]]:
                    beteiligte_strassen.append((s, dict[oe_to_check], oe_to_check))
                    liste_kanten.remove(oeffnung)
                    if strasse in Karte_.strassen_karte:
                        Karte_.strassen_karte.remove(strasse)

    #print(Karte_.matrix)
    #print(beteiligte_strassen, liste_kanten)

    for strasse in Karte_.strassen_karte:
        for k in strasse[1]:
            if k in liste_kanten:
                liste_kanten.remove(k)

    # print("hier!", beteiligte_strassen, liste_kanten, Karte_.strassen_karte)

    # alte Kanten loeschen

    for j in beteiligte_strassen:
        # print("j", j)
        alle_strassen[j[0]].koordinaten_plus_oeffnungen[j[1]].remove(j[2])
        # print(alle_strassen[j[0]].koordinaten_plus_oeffnungen)

    # neue Strassen erstellen

    for strasse in Karte_.strassen_karte:
        # print("huih", strasse)
        alle_strassen.update({strasse[0]: Strasse(koordinaten_, strasse[1])})

    #print("alle_strassen\n")
    #for i in alle_strassen:
    #    print(alle_strassen[i].koordinaten_plus_oeffnungen)

    # alte Strassen updaten

    liste = []

    #print(beteiligte_strassen)

    for i in beteiligte_strassen:
        if i not in liste:
            liste.append(i)

   # print("L", liste)

    if len(liste) == 1:
        # print(alle_strassen[liste[0][0]].koordinaten_plus_oeffnungen)
        alle_strassen[liste[0][0]].koordinaten_plus_oeffnungen.update({(x, y): liste_kanten})
        alle_strassen[liste[0][0]].wert += 1

    else:
        if len(liste) > 0:
            #print("\nneu", liste)

            if Karte_.mitte == "G":
                for strasse in liste:
                    alle_strassen[strasse[0]].koordinaten_plus_oeffnungen.update({koordinaten_: liste_kanten})
                    alle_strassen[strasse[0]].wert += 1

            else:

                hauptstrasse = liste[0]
                liste.remove(hauptstrasse)
                alle_strassen[hauptstrasse[0]].koordinaten_plus_oeffnungen.update({koordinaten_: liste_kanten})
                alle_strassen[hauptstrasse[0]].wert += 1

                for s in liste:
                    alle_strassen[hauptstrasse[0]].koordinaten_plus_oeffnungen.update(
                        alle_strassen[s[0]].koordinaten_plus_oeffnungen)
                    alle_strassen[hauptstrasse[0]].wert += alle_strassen[s[0]].wert
                    del alle_strassen[s[0]]

def updateWiesen(koordinates_, Karte_):

    x, y = koordinates_

    bw = []
    angrenzendeWiesen = {}


    dic = {4: [((x, y + 1), 2), ((x - 1, y), 1)], 5: [((x, y + 1), 2), ((x + 1, y), 3)],
           6: [((x, y - 1), 0), ((x + 1, y), 3)], 7: [((x, y - 1), 0), ((x - 1, y), 1)]}

    dicOU = {4: 7, 5: 6, 6: 5, 7: 4}
    dicRL = {4: 5, 5: 4, 6: 7, 7: 6}

    for wiese in Karte_.wiesenKarte[:]:
        bw = []
        #print(Karte_.matrix)
        #print("h",wiese)
        for ecke in wiese[1]:
            #print("ecke", ecke)
            for w in alleWiesen:
                #print("alo", cards_set)
                #bw = []
                #print("hier", dic[ecke][0][0])
                #print("hui",alleWiesen[w].teile)
                #if dic[ecke][0][0] in alleWiesen[w].teile and dicOU[ecke] in alleWiesen[w].teile[dic[ecke][0][0]]:
                #    print("alo", cards_set)


                if dic[ecke][0][0] in alleWiesen[w].teile and dicOU[ecke] in alleWiesen[w].teile[dic[ecke][0][0]]\
                and cards_set[dic[ecke][0][0]].info[dic[ecke][0][1]] != "O":
                    if w not in bw:
                    #if (alleWiesen[w], wiese[1], alleWiesen[w].teile[dic[ecke][0][0]]) not in angrenzendeWiesen:

                        #angrenzendeWiesen.append((w, alleWiesen[w], wiese[1], wiese[0]))
                        bw.append(w)


                        if wiese in Karte_.wiesenKarte:
                            Karte_.wiesenKarte.remove(wiese)
                    #continue

                if dic[ecke][1][0] in alleWiesen[w].teile and dicRL[ecke] in alleWiesen[w].teile[dic[ecke][1][0]]\
                and cards_set[dic[ecke][1][0]].info[dic[ecke][1][1]] != "O":
                    #if (alleWiesen[w], wiese[1], alleWiesen[w].teile[dic[ecke][1][0]]) not in angrenzendeWiesen:
                    if w not in bw:
                        #angrenzendeWiesen.append((w, alleWiesen[w], wiese[1], wiese[0]))
                        bw.append(w)
                        if wiese in Karte_.wiesenKarte:
                            Karte_.wiesenKarte.remove(wiese)
            angrenzendeWiesen.update({wiese[0]: (wiese[1], bw)})


    for neueWiese in Karte_.wiesenKarte:
        alleWiesen.update({neueWiese[0]: Wiese(koordinates_, neueWiese[1])})

    dicKarte = angrenzendeWiesen
    dicKarteKopie = dicKarte.copy()
    print(Karte_.matrix)
    print("D_start", koordinates_, dicKarte)

    #for angrenzendeWiese in angrenzendeWiesen:
        #print("A",angrenzendeWiesen[angrenzendeWiese])
    #    if angrenzendeWiese not in dicKarte:
    #        dicKarte.update({angrenzendeWiese: angrenzendeWiesen[angrenzendeWiese]})

    if len(dicKarte) > 0:
        print("WIESEN:")
        for infos in dicKarte.values():
            for w in infos[1]:
                print(w, alleWiesen[w].teile)
            if len(infos[1]) > 0:
                if len(infos[1]) == 1:
                    #print(Karte_.matrix)
                    #for w in alleWiesen:
                        #print(w, alleWiesen[w].teile)
                        #display_spielbrett(cards_set)
                        #print("hier",infos, koordinates_)
                    try:
                        if koordinates_ not in alleWiesen[infos[1][0]].teile:
                            alleWiesen[infos[1][0]].teile.update({koordinates_: infos[0]})
                            continue
                    except KeyError:
                        #print(KeyError)
                        print("ERROR")
                        #print(infos, koordinates_)
                        #print(Karte_.matrix)
                        #for w in alleWiesen:
                        #    print(w, alleWiesen[w].teile)
                        display_spielbrett(cards_set)


                    else:
                        #print(infos)
                        #print("hier", alleWiesen[infos[1][0]].teile)
                        for t in infos[0]:
                            alleWiesen[infos[1][0]].teile[koordinates_].append(t)
                else:
                    #print("hoioio")
                    hauptwiese = infos[1][0]
                    print("vorher")
                    print(infos)
                    del infos[1][0]
                    print("nachher")
                    print(infos)
                    try:
                        if koordinates_ not in alleWiesen[hauptwiese].teile:
                            alleWiesen[hauptwiese].teile.update({koordinates_: infos[0]})
                        else:
                            #print("einmalig")
                            #print(infos[0])
                            for t in infos[0]:
                                alleWiesen[hauptwiese].teile[koordinates_].append(t)

                    except KeyError:
                        print("ERROR_3")
                        #print(koordinates_)
                        #print(Karte_.matrix)
                        #for w in alleWiesen:
                        #    print(w, alleWiesen[w].teile)
                        display_spielbrett(cards_set)


                    for restwiese in infos[1]:
                        for teil in alleWiesen[restwiese].teile:                                #hier gibts noch nen error, nicht mehr
                            if teil not in alleWiesen[hauptwiese].teile:
                                alleWiesen[hauptwiese].teile.update({teil: alleWiesen[restwiese].teile[teil]})
                            else:
                                c = 0
                                for t in alleWiesen[restwiese].teile[teil]:
                                    #print(alleWiesen[restwiese].teile)
                                    alleWiesen[hauptwiese].teile[teil].append(t)            ##bleibt haengen
                                    c += 1
                                    if c > 15:
                                        print("start")
                                        print("D", dicKarte)
                                        print("Haupt", hauptwiese)
                                        print(infos)
                                        print("Teil", teil)
                                        print(alleWiesen[hauptwiese].teile)
                                        for w in alleWiesen:
                                            print(w, alleWiesen[w].teile)
                                        print("RestwieseTeile", alleWiesen[restwiese].teile)
                                        display_spielbrett(cards_set)
                        #print("restwiese zu del:", restwiese)
                        del alleWiesen[restwiese]
                        for x in dicKarte.values():
                            for pos, i in enumerate(x[1]):
                                if i == restwiese:
                                    if hauptwiese not in x[1]:
                                        x[1][pos] = hauptwiese


alle_orte = {"Ort_0": Ort((0, 0), [1])}
alle_strassen = {"Strasse_0": Strasse((0, 0), [0, 2])}
alle_kloester = {}
alleWiesen = {"Wiese_0": Wiese((0, 0), [4, 7]), "Wiese_1": Wiese((0, 0), [5, 6])}

cards_set = {(0, 0): Karte("S", "O", "S", "W")}

possible_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0)]
unavailable_coordinates = [(0, 0)]


##### Experimentierecke



#Karte_1 = Karte("W","W","S","S")
#choice_1 = ((1, -1), 3)
#cs, ak, uk = set_card(choice_1, Karte_1, possible_coordinates, unavailable_coordinates, cards_set)
#print("ende_1")
#
#Karte_2 = Karte("S", "W", "S", "W")
#choice_2 = ((2, -2), 0)
#cs, ak, uk = set_card(choice_2, Karte_2, possible_coordinates, unavailable_coordinates, cards_set)
#
#print("ende_2")
#
#Karte_3 = Karte("S","W","W","S")
#choice_3 = ((0, -1), 0)
#cs, ak, uk = set_card(choice_3, Karte_3, possible_coordinates, unavailable_coordinates, cards_set)
#print("ende_3")
#
#Karte_2 = Karte("W", "W", "W", "O")
#choice_2 = ((0, -2), 0)
#cs, ak, uk = set_card(choice_2, Karte_2, possible_coordinates, unavailable_coordinates, cards_set)
#
#print("ende_4")
#
#Karte_5 = Karte("W","W","W","W","K")
#choice_5 = ((0, -3), 3)
#cs, ak, uk = set_card(choice_5, Karte_5, possible_coordinates, unavailable_coordinates, cards_set)
#print("ende_5")
#
#Karte_6 = Karte("W", "W", "O", "W")
#choice_6 = ((1, -3), 0)
#cs, ak, uk = set_card(choice_6, Karte_6, possible_coordinates, unavailable_coordinates, cards_set)
#
#print("ende_6")
#
#Karte_7 = Karte("S","W","S","W")
#choice_7 = ((2, -3), 0)
#cs, ak, uk = set_card(choice_7, Karte_7, possible_coordinates, unavailable_coordinates, cards_set)
#print("ende_7")
#
#for w in alleWiesen:
#    print(w, alleWiesen[w].teile)
#display_spielbrett(cards_set)


#Karte_ende = Karte("W", "O", "S", "S")
#choice_ende = ((2, -1), 0)
#cs, ak, uk = set_card(choice_ende, Karte_ende, possible_coordinates, unavailable_coordinates, cards_set)
#
#print("Ende")
#
#
#
#
#Karte_3 = Karte("W", "W", "S", "S")
#choice_3 = ((-1, 0), 0)
#cs, ak, uk = set_card(choice_3, Karte_3, possible_coordinates, unavailable_coordinates, cards_set)






#for c in cs:
#    print(cs[c].info, cs[c].orte)
# print("alle_orte:",alle_orte)

#for ort in alle_orte:
#    print(ort, alle_orte[ort].koordinaten_plus_oeffnungen, "Wert:", alle_orte[ort].wert)
#
#for strasse in alle_strassen:
#    print(strasse, alle_strassen[strasse].koordinaten_plus_oeffnungen, "Wert:", alle_strassen[strasse].wert)
#
#for kloster in alle_kloester:
#    print(kloster, alle_kloester[kloster].umgebung)

##

#for wiese in alleWiesen:
#    print("WIESE", wiese, alleWiesen[wiese].teile)
#print(alleWiesen)
#
#display_spielbrett(cards_set)


# print(time.clock()-start_time, "seconds")

#Wiese.setWiese(cs, alle_orte)
import random
import copy

def play_random(Kartenliste):
    """zieht zufällig karten und setzt diese random""" #mit präferenz auf positionen, die von 3 oder 4 karten umgeben sind """

    Kartenliste_in = copy.deepcopy(Kartenliste)

    global cards_set
    global possible_coordinates
    global unavailable_coordinates

    #c_s_in = copy.deepcopy(cards_set)
    #p_c_in = list(possible_coordinates)
    #u_c_in = list(unavailable_coordinates)

    random.shuffle(Kartenliste_in)
    running = True

    while running:
        if len(Kartenliste_in) < 1:  # 59
            break
        card = Kartenliste_in[0]
        #print(card.matrix)
        moegliche_anlegestellen = check_card_to_possible_coordinates(card, possible_coordinates, cards_set)
        #print(moegliche_anlegestellen)

        try:
            choice = random.choice(moegliche_anlegestellen)

            cards_set, possible_coordinates, unavailable_coordinates = set_card(choice, card, possible_coordinates, unavailable_coordinates, cards_set)


            del Kartenliste_in[0]
         #   print(cards_set, possible_coordinates, unavailable_coordinates)
        except IndexError:
            print(card.matrix)
            del Kartenliste_in[0]
            #random.shuffle(Kartenliste_in)
            continue

    #display_spielbrett(cards_set)
    #for ort in alle_orte:
    #    print(ort, alle_orte[ort].koordinaten_plus_oeffnungen, "Wert:", alle_orte[ort].wert)
#
    #for strasse in alle_strassen:
    #    print(strasse, alle_strassen[strasse].koordinaten_plus_oeffnungen, "Wert:", alle_strassen[strasse].wert)
#
    #for kloster in alle_kloester:
    #    print(kloster, alle_kloester[kloster].umgebung)
#
    #for wiese in alleWiesen:
    #    print(wiese, alleWiesen[wiese].teile)
    #display_spielbrett(cards_set)

counter = 0
x = True
while x:
    counter += 1
    print(counter)
    alle_orte = {"Ort_0": Ort((0, 0), [1])}
    alle_strassen = {"Strasse_0": Strasse((0, 0), [0, 2])}
    alle_kloester = {}
    alleWiesen = {"Wiese_0": Wiese((0, 0), [4, 7]), "Wiese_1": Wiese((0, 0), [5, 6])}

    cards_set = {(0, 0): Karte("S", "O", "S", "W")}

    possible_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    unavailable_coordinates = [(0, 0)]
    #print("neues spiel")
    play_random(Kartenliste)


#display_spielbrett(cards_set)
