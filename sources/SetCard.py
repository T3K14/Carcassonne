#modul das funktionen zum anlegen einer Karte an das bestehende spielfeld beinhaltet


import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import time

from rotate2 import rotate_card_left, rotate_card_right, rotate_matrix_left, rotate_matrix_right, rotate_list_right, rotateWiesenRight
from Rotate import Rotate
from KarteMod import Karte
from KarteMod import Kartenliste

from Ort import Ort
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese

#start_time = time.clock()

def check_card_to_possible_coordinates(Karte, possible_coordinates, cards_set):
    """checkt, ob und wie karte an jede freie stelle gelegt werden kann,
        returned liste mit tupel bestehend aus moeglicher anlegestelle und anzahl von rotationen die dafür noetig sind
        nimmt eine Karte an, sowie liste möglicher anlegestellen und dictionary von gelegten Karten
        """

    possible_anlegemoeglichkeiten = []

    card = Karte

    ij = [(0, 2), (1, 3), (2, 0), (3, 1)]
    for x, y in possible_coordinates:
        nkoos = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
        nks = []

        for relative_pos, nkoo in enumerate(nkoos):
            for gelegte_karte in cards_set:
                if gelegte_karte == nkoo:
                    nks.append(((gelegte_karte, cards_set[gelegte_karte]), relative_pos))

        if len(nks) == 1:
            i, j = ij[nks[0][1]]
            for z in range(4):
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
    return possible_anlegemoeglichkeiten


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

def set_card(coordinates, Karte, possible_coordinates, unavailable_coordinates, cards_set, alle_orte, strassen, kloester, wiesen):
    """setzt karte an koordinaten (x,y) (coordinates) und updated cards_set, possible_coordiantes
     und unavailable_coordinates

     ausserdem werden Orte, Strassen, Wiesen und Kloester geupdated
     """
    (x, y) = coordinates[0]  # koordinaten
    z = coordinates[1]  # anzahl an rechtsrotationen und entsprechende rotation
    for i in range(z):
        Karte.info = rotate_card_right(Karte.info)
        Karte.matrix = rotate_matrix_right(Karte.matrix)
        rotate_list_right(Karte.orte)

        # kanten einzeln drehen, da die orte.kanten nicht mehr auf das selbe objekt wie self.orte zeigen
        for ort in Karte.orte_karte:
            ort.kanten = rotate_list_right(ort.kanten)

        Karte.strassen = rotate_list_right(Karte.strassen)
        Karte.wiesenKarte = rotateWiesenRight(Karte.wiesenKarte)

    #add card to cards_set
    cards_set.update({(x, y): Karte})  # ((x,y),Karte)

    if len(Karte.orte) > 0:
        update_orte(alle_orte, Karte, x, y)
    if len(Karte.strassen) > 0:
        update_strasse(strassen, (x, y), Karte)
    if len(Karte.wiesenKarte) > 0:
        updateWiesen(wiesen, (x, y), Karte, cards_set)

    # updateKloester

    if len(Karte.kloster_karte) > 0:
        # print(Karte.kloster_karte)
        liste = [(x - 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y), (x + 1, y), (x - 1, y - 1), (x, y - 1),
                 (x + 1, y - 1)]
        kloester.update({Karte.kloster_karte[0]: Kloster((x, y))})
        # print("huihui", kloester)
        for i in liste:
            if i in cards_set and i not in kloester[Karte.kloster_karte[0]].umgebung:
                # print(Karte.kloster_karte[0])
                kloester[Karte.kloster_karte[0]].umgebung.append(i)

        # kloster_dict = {0: ()}

    for k in kloester:
        (v, w) = kloester[k].koordinaten
        liste_ = [(v - 1, w + 1), (v, w + 1), (v - 1, w + 1), (v - 1, w), (v + 1, w), (v - 1, w - 1), (v, w - 1),
                  (v + 1, w - 1)]
        if (x, y) in liste_ and (x, y) not in kloester[k].umgebung:
            kloester[k].umgebung.append((x, y))

    # unavailable_- und possible_coordinates updaten

    for i, (v, w) in enumerate(possible_coordinates):
        if (x, y) == (v, w):
            unavailable_coordinates.append((v, w))
            del possible_coordinates[i]
            for (a, b) in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
                if (a, b) not in possible_coordinates and (a, b) not in unavailable_coordinates:
                    possible_coordinates.append((a, b))
    #print("ahoi",cards_set)
    return cards_set, possible_coordinates, unavailable_coordinates, alle_orte, strassen, kloester, wiesen


def update_orte(alle_orte, Karte, x, y):

    # dictionary gibt koordinaten von nachbarkarte an, welche zu bestimmter kante ueberprueft werden muessen
    koord_to_kante = {0: (x, y - 1), 1: (x - 1, y), 2: (x, y + 1), 3: (x + 1, y)}

    # dictionary enthält orte auf karte und zu jedem ein weiters dict mit bereits existierenden Orten, mit denen eine
    # WW stattfindet und wo
    dictionary = {}

    for ort in Karte.orte_karte[:]: #kopie daher, da orte aus der liste geloescht und die verbliebenen neue werden

        for kante in ort.kanten[:]: # kopie, da die kanten an die was angrenzt geloescht werden und die uebrigen dann
                                    # noch zum ort hinzugefuegt werden sollen

            if kante < 2:
                nachbarkante = kante + 2
            else:
                nachbarkante = kante - 2

            # ueberpruefe ob es orte o in alle_orte gibt, welche teile an den koordinaten zu dict haben und ob dafuer
            # auch noch die kanten passen
            for global_ort in alle_orte:

                # wenn nachbarkoordinaten mit Karte mit existierendem ort besetzt sind UND dieser Ort eine offene Kante
                # hat, die an eine Kante des Ortes der neuen Karte grenzt
                if koord_to_kante[nachbarkante] in alle_orte[global_ort].koordinaten_plus_oeffnungen and \
                nachbarkante in alle_orte[global_ort].koordinaten_plus_oeffnungen[koord_to_kante[nachbarkante]]:

                    # falls der Ort auf der Karte noch nicht eingetragen ist
                    if ort not in dictionary:

                        dictionary.update({ort: {global_ort: [(koord_to_kante[nachbarkante], nachbarkante)]}})
                        #dictionary.update({ort: {global_ort: {koord_to_kante[nachbarkante]: nachbarkante}}})

                    else:

                        # wenn der globale Ort schon als Ort eingetragen wurde, welcher mit dem auf der Karte ww, sollen
                        # hier nur neue wechselwirkungskoordinaten hinzugefuegt werden
                        if global_ort in list(dictionary[ort]):
                            dictionary[ort][global_ort].append((koord_to_kante[nachbarkante], nachbarkante))
                            #dictionary[ort][global_ort].update({koord_to_kante[nachbarkante]: nachbarkante})

                        else:
                            dictionary[ort].update({global_ort: [(koord_to_kante[nachbarkante], nachbarkante)]})
                            #dictionary[ort].update({global_ort: {koord_to_kante[nachbarkante]: nachbarkante}})

                    # eingehen darauf, dass die hier betrachteten kanten des ortes auf der neu gelegten Karte jetzt
                    # keine offenen mehr sein können
                    ort.kanten.remove(kante)
                    if ort in Karte.orte_karte:
                        Karte.orte_karte.remove(ort)

    ## kanten updaten, neue Ortsteile hinzufuegen und orte verbinden, falls notwendig

    for ort in dictionary:

        if len(dictionary[ort]) == 1:

            # #### ghet vllt eleganter ohne nochmal ein for loop bemuehen zu muessen
            for global_ort in dictionary[ort]:
                # fkt, um die jetzt nicht mehr offenen kanten zu löschen
                alle_orte[global_ort].update_kanten(dictionary[ort][global_ort])  # funktioniert

                # fkt, um die noch offenen kanten dem ort hinzuzufuegen, mit dem interagiert wurde, falls nur ein glob. Ort beteiligt ist
                alle_orte[global_ort].add_part(ort, x, y) #funktioniert

        else:
            hauptort = list(dictionary[ort])[0]
            #print("aloa", alle_orte[hauptort].koordinaten_plus_oeffnungen)

            # update aller Kanten
            for global_ort in dictionary[ort]:
                alle_orte[global_ort].update_kanten(dictionary[ort][global_ort])

            # update hauptort normal
            #alle_orte[hauptort].update_kanten(dictionary[ort][hauptort])
            alle_orte[hauptort].add_part(ort, x, y)

            # delete hauptort from dictionary[ort]
            del dictionary[ort][hauptort]

            alle_orte[hauptort].add_orte(dictionary[ort], alle_orte)

    # erstelle neue Orte, die mit keinem globalen interagiert haben
    for ort in Karte.orte_karte:
        #print(ort.kanten)
        alle_orte.update({ort.name: Ort((x, y), ort.kanten)})




    #for i in alle_orte:
        #print(alle_orte[i].koordinaten_plus_oeffnungen)
    #print("Ende alternativ --------------------------------------")

    # liste aller kanten der karte an denen sich ortsausgaenge befinden
    #liste_kanten = [i for ort in Karte.orte_karte for i in ort.kanten]
#
    #zu_loeschende_orte = []
    #beteiligte_orte = []
    #counter = []
#
    ## orte updaten
    ## betrachte jeden ort auf Karte
    #for ort in Karte.orte_karte:
#
    #    # ueberpruefe die kanten der Karte zu diesem Ort
    #    for oeffnung in ort.kanten:
#
    #        if oeffnung < 2:
    #            oe_to_check = oeffnung + 2
    #        else:
    #            oe_to_check = oeffnung - 2
    #        print("oe_to_check:", oe_to_check)
    #        # dictionary gibt koordinaten an, welche zu bestimmter kante ueberprueft werden muessen
    #        dict = {0: (x, y - 1), 1: (x - 1, y), 2: (x, y + 1), 3: (x + 1, y)}
#
    #        # ueberpruefe ob es orte o in alle_orte gibt, welche teile an den koordinaten zu dict haben und ob dafuer
    #        # auch noch die kanten passen
    #        for o in alle_orte:
    #            # wenn nachbarkoordinaten mit Karte mit existierendem ort besetzt sind UND deren ortskanten zu neuer
    #            # karte mit denen dieser neuen Karte uebereinstimmen
    #            if dict[oe_to_check] in alle_orte[o].koordinaten_plus_oeffnungen and \
    #                    oe_to_check in alle_orte[o].koordinaten_plus_oeffnungen[dict[oe_to_check]]:
#
    #                # liste den beteiligten ort, der koordinate des ortsteil an dessen kante der an das neue teil anschliesst
    #                beteiligte_orte.append((o, dict[oe_to_check], oe_to_check))
#
    #                # falls der existierende ort an mehreren kanten beruehrt wird, soll er trotzdem nur einmal beim
    #                # updaten beruecksichtigt werden
    #                if o not in counter:
    #                    counter.append(o)
#
    #                # die betrachtete kannt wird aus der liste aller kanten geloescht, dass sie spater nicht als offene
    #                # kante des geupdateten ortes eingetragen wird
    #                liste_kanten.remove(oeffnung)
#
    #                # ort wird geloescht, dass spater kein neuer ort damit erzeugt wird
    #                if ort not in zu_loeschende_orte:
    #                    zu_loeschende_orte.append(ort)
#
    #for integrierter_ort in zu_loeschende_orte:
    #    Karte.orte_karte.remove(integrierter_ort)
#
    ## Ortskanten auf Karte werden auf uebrig gebliebene offene kanten reduziert
    #for kartenort in Karte.orte_karte:
    #    for kante in kartenort.kanten:
    #        if kante in liste_kanten:
    #            liste_kanten.remove(kante)
#
    #for beteiligter_ort in beteiligte_orte:
    #    print("beteiligter_ort", beteiligter_ort)
#
    #    # beteiligter_ort[1] ist die koordinaten vom beteiligten ort an dessen kante(n) (beteiligter_ort[2])
    #    # der neue ort anschliesst
    #    alle_orte[beteiligter_ort[0]].update_kanten(beteiligter_ort[1], beteiligter_ort[2])
#
    #    #### alt
    #    # alle_orte[beteiligter_ort[0]].koordinaten_plus_oeffnungen[beteiligter_ort[1]].remove(beteiligter_ort[2])
#
    #### neue Orte erstellen
#
    #for ort in Karte.orte_karte:
    #    alle_orte.update({ort[0]: Ort(koordinaten, ort[1])})
#
    #### alte Orte updaten
#
    ## print("C", counter_)
#
    #if len(counter) == 1:
    #    alle_orte[counter[0]].koordinaten_plus_oeffnungen.update({koordinaten: liste_kanten})
    #    alle_orte[counter[0]].wert += wert
#
    #else:
    #    if len(counter_) > 0:
    #        if Karte_.mitte == "O":
    #            hauptort = counter_[0]
    #            counter_.remove(hauptort)
    #            alle_orte[hauptort].koordinaten_plus_oeffnungen.update({koordinaten_: liste_kanten_})
    #            alle_orte[hauptort].wert += wert_
#
    #            for ort in counter_:
    #                alle_orte[hauptort].koordinaten_plus_oeffnungen.update(alle_orte[ort].koordinaten_plus_oeffnungen)
    #                alle_orte[hauptort].wert += alle_orte[ort].wert
    #                del alle_orte[ort]
#
    #        else:
    #            for ort in counter_:
    #                alle_orte[ort].koordinaten_plus_oeffnungen.update({koordinaten_: []})
    #                alle_orte[ort].wert += wert_
    return alle_orte
def update_strasse(liste_strassen, koordinaten_, Karte_):

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

            for s in liste_strassen:
                if dict[oe_to_check] in liste_strassen[s].koordinaten_plus_oeffnungen and \
                        oe_to_check in liste_strassen[s].koordinaten_plus_oeffnungen[dict[oe_to_check]]:
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
        liste_strassen[j[0]].koordinaten_plus_oeffnungen[j[1]].remove(j[2])
        # print(liste_strassen[j[0]].koordinaten_plus_oeffnungen)

    # neue Strassen erstellen

    for strasse in Karte_.strassen_karte:
        # print("huih", strasse)
        liste_strassen.update({strasse[0]: Strasse(koordinaten_, strasse[1])})

    #print("liste_strassen\n")
    #for i in liste_strassen:
    #    print(liste_strassen[i].koordinaten_plus_oeffnungen)

    # alte Strassen updaten

    liste = []

    #print(beteiligte_strassen)

    for i in beteiligte_strassen:
        if i not in liste:
            liste.append(i)

   # print("L", liste)

    if len(liste) == 1:
        # print(liste_strassen[liste[0][0]].koordinaten_plus_oeffnungen)
        liste_strassen[liste[0][0]].koordinaten_plus_oeffnungen.update({(x, y): liste_kanten})
        liste_strassen[liste[0][0]].wert += 1

    else:
        if len(liste) > 0:
            #print("\nneu", liste)

            if Karte_.mitte == "G":
                for strasse in liste:
                    liste_strassen[strasse[0]].koordinaten_plus_oeffnungen.update({koordinaten_: liste_kanten})
                    liste_strassen[strasse[0]].wert += 1

            else:

                hauptstrasse = liste[0]
                liste.remove(hauptstrasse)
                liste_strassen[hauptstrasse[0]].koordinaten_plus_oeffnungen.update({koordinaten_: liste_kanten})
                liste_strassen[hauptstrasse[0]].wert += 1

                for s in liste:
                    liste_strassen[hauptstrasse[0]].koordinaten_plus_oeffnungen.update(
                        liste_strassen[s[0]].koordinaten_plus_oeffnungen)
                    liste_strassen[hauptstrasse[0]].wert += liste_strassen[s[0]].wert
                    del liste_strassen[s[0]]

    return liste_strassen

def updateWiesen(liste_wiesen, koordinates_, Karte_,cards_set):

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
            for w in liste_wiesen:
                #print("alo", cards_set)
                #bw = []
                #print("hier", dic[ecke][0][0])
                #print("hui",liste_wiesen[w].teile)
                #if dic[ecke][0][0] in liste_wiesen[w].teile and dicOU[ecke] in liste_wiesen[w].teile[dic[ecke][0][0]]:
                #    print("alo", cards_set)


                if dic[ecke][0][0] in liste_wiesen[w].teile and dicOU[ecke] in liste_wiesen[w].teile[dic[ecke][0][0]]\
                and cards_set[dic[ecke][0][0]].info[dic[ecke][0][1]] != "O":
                    if w not in bw:
                    #if (liste_wiesen[w], wiese[1], liste_wiesen[w].teile[dic[ecke][0][0]]) not in angrenzendeWiesen:

                        #angrenzendeWiesen.append((w, liste_wiesen[w], wiese[1], wiese[0]))
                        bw.append(w)


                        if wiese in Karte_.wiesenKarte:
                            Karte_.wiesenKarte.remove(wiese)
                    #continue

                if dic[ecke][1][0] in liste_wiesen[w].teile and dicRL[ecke] in liste_wiesen[w].teile[dic[ecke][1][0]]\
                and cards_set[dic[ecke][1][0]].info[dic[ecke][1][1]] != "O":
                    #if (liste_wiesen[w], wiese[1], liste_wiesen[w].teile[dic[ecke][1][0]]) not in angrenzendeWiesen:
                    if w not in bw:
                        #angrenzendeWiesen.append((w, liste_wiesen[w], wiese[1], wiese[0]))
                        bw.append(w)
                        if wiese in Karte_.wiesenKarte:
                            Karte_.wiesenKarte.remove(wiese)
            angrenzendeWiesen.update({wiese[0]: (wiese[1], bw)})


    for neueWiese in Karte_.wiesenKarte:
        liste_wiesen.update({neueWiese[0]: Wiese(koordinates_, neueWiese[1])})

    dicKarte = angrenzendeWiesen
    dicKarteKopie = dicKarte.copy()
    #print(Karte_.matrix)
    #print("D_start", koordinates_, dicKarte)

    #for angrenzendeWiese in angrenzendeWiesen:
        #print("A",angrenzendeWiesen[angrenzendeWiese])
    #    if angrenzendeWiese not in dicKarte:
    #        dicKarte.update({angrenzendeWiese: angrenzendeWiesen[angrenzendeWiese]})

    if len(dicKarte) > 0:
        #print("WIESEN:")
        for infos in dicKarte.values():
            #for w in infos[1]:
                #print(w, liste_wiesen[w].teile)
            if len(infos[1]) > 0:
                if len(infos[1]) == 1:
                    #print(Karte_.matrix)
                    #for w in liste_wiesen:
                        #print(w, liste_wiesen[w].teile)
                        #display_spielbrett(cards_set)
                        #print("hier",infos, koordinates_)
                    try:
                        if koordinates_ not in liste_wiesen[infos[1][0]].teile:
                            liste_wiesen[infos[1][0]].teile.update({koordinates_: infos[0]})
                            continue
                    except KeyError:
                        #print(KeyError)
                        print("ERROR")
                        #print(infos, koordinates_)
                        #print(Karte_.matrix)
                        #for w in liste_wiesen:
                        #    print(w, liste_wiesen[w].teile)
                        display_spielbrett(cards_set)


                    else:
                        #print(infos)
                        #print("hier", liste_wiesen[infos[1][0]].teile)
                        for t in infos[0]:
                            liste_wiesen[infos[1][0]].teile[koordinates_].append(t)
                else:
                    #print("hoioio")
                    hauptwiese = infos[1][0]
                    #print("vorher")
                    #print(infos)
                    del infos[1][0]
                    #print("nachher")
                    #print(infos)
                    try:
                        if koordinates_ not in liste_wiesen[hauptwiese].teile:
                            liste_wiesen[hauptwiese].teile.update({koordinates_: infos[0]})
                        else:
                            #print("einmalig")
                            #print(infos[0])
                            for t in infos[0]:
                                liste_wiesen[hauptwiese].teile[koordinates_].append(t)

                    except KeyError:
                        print("ERROR_3")
                        #print(koordinates_)
                        #print(Karte_.matrix)
                        #for w in liste_wiesen:
                        #    print(w, liste_wiesen[w].teile)
                        display_spielbrett(cards_set)


                    for restwiese in infos[1]:
                        for teil in liste_wiesen[restwiese].teile:                                #hier gibts noch nen error, nicht mehr
                            if teil not in liste_wiesen[hauptwiese].teile:
                                liste_wiesen[hauptwiese].teile.update({teil: liste_wiesen[restwiese].teile[teil]})
                            else:
                                c = 0
                                for t in liste_wiesen[restwiese].teile[teil]:
                                    #print(liste_wiesen[restwiese].teile)
                                    liste_wiesen[hauptwiese].teile[teil].append(t)            ##bleibt haengen
                                    c += 1
                                    if c > 15:
                                        print("start")
                                        print("D", dicKarte)
                                        print("Haupt", hauptwiese)
                                        print(infos)
                                        print("Teil", teil)
                                        print(liste_wiesen[hauptwiese].teile)
                                        for w in liste_wiesen:
                                            print(w, liste_wiesen[w].teile)
                                        print("RestwieseTeile", liste_wiesen[restwiese].teile)
                                        display_spielbrett(cards_set)
                        #print("restwiese zu del:", restwiese)
                        del liste_wiesen[restwiese]
                        for x in dicKarte.values():
                            for pos, i in enumerate(x[1]):
                                if i == restwiese:
                                    if hauptwiese not in x[1]:
                                        x[1][pos] = hauptwiese
                                    else:
                                        del x[1][pos]
    return liste_wiesen


if __name__ == "__main__":

    alle_orte = {"Ort_0": Ort((0, 0), [1])}
    alle_strassen = {"Strasse_0": Strasse((0, 0), [0, 2])}
    alle_kloester = {}
    alleWiesen = {"Wiese_0": Wiese((0, 0), [4, 7]), "Wiese_1": Wiese((0, 0), [5, 6])}

    cards_set = {(0, 0): Karte("S", "O", "S", "W")}

    possible_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    unavailable_coordinates = [(0, 0)]

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
            print(moegliche_anlegestellen)
            #break

            try:
                choice = random.choice(moegliche_anlegestellen)

                cards_set, possible_coordinates, unavailable_coordinates, alle_orte, alle_strassen, alle_kloester,\
                    alleWiesen = set_card(choice, card, possible_coordinates, unavailable_coordinates, cards_set,\
                                          alle_orte, alle_strassen, alle_kloester, alleWiesen)


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

    print("HIHIHI")

    counter = 0
    k = True
    while k:
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
