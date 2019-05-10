# modul das funktionen zum anlegen einer Karte an das bestehende spielfeld beinhaltet


import numpy as np
# import matplotlib
import matplotlib.pyplot as plt
import time

from Rotate import Rotate
from KarteMod import Karte
from KarteMod import Kartenliste

from Ort import Ort
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese


# start_time = time.clock()

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
    return (possible_anlegemoeglichkeiten)

def set_card(coordinates, Karte, possible_coordinates, unavailable_coordinates, cards_set, alle_orte, strassen, kloester,
             wiesen):
    """setzt karte an koordinaten (x,y) (coordinates) und updated cards_set, possible_coordiantes
     und unavailable_coordinates

     ausserdem werden Orte, Strassen, Wiesen und Kloester geupdated
     """

    (x, y) = coordinates[0]  # koordinaten
    z = coordinates[1]  # anzahl an rechtsrotationen und entsprechende rotation
    for i in range(z):
        Karte.info = Rotate.rotate_card_right(Karte.info)
        Karte.matrix = Rotate.rotate_matrix_right(Karte.matrix)
        Karte.orte = Rotate.rotate_list_right(Karte.orte)
        Karte.strassen = Rotate.rotate_list_right(Karte.strassen)
        Karte.wiesenKarte = Rotate.rotateWiesenRight(Karte.wiesenKarte)

    # add card to cards_set
    cards_set.update({(x, y): Karte})  # ((x,y),Karte)

    update_orte(alle_orte, Karte, x, y)

    # unavailable_- und possible_coordinates updaten

    for i, (v, w) in enumerate(possible_coordinates):
        if (x, y) == (v, w):
            unavailable_coordinates.append((v, w))
            del possible_coordinates[i]
            for (a, b) in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
                if (a, b) not in possible_coordinates and (a, b) not in unavailable_coordinates:
                    possible_coordinates.append((a, b))
    # print("ahoi",cards_set)
    return cards_set, possible_coordinates, unavailable_coordinates, alle_orte, strassen, kloester, wiesen


def update_orte(alle_orte, Karte, x, y):

    # liste aller kanten der karte an denen sich ortsausgaenge befinden
    liste_kanten = [i for ort in Karte.orte_karte for i in ort.kanten]

    zu_loeschende_orte = []
    beteiligte_orte = []
    counter = []

    # orte updaten
    # betrachte jeden ort auf Karte
    for ort in Karte.orte_karte:

        # ueberpruefe, welche kanten der Karte zu diesem Ort gehoeren
        for oeffnung in ort.kanten:

            # print("hi", oeffnung)
            if oeffnung < 2:
                oe_to_check = oeffnung + 2
            else:
                oe_to_check = oeffnung - 2
            print("oe_to_check:", oe_to_check)
            # dictionary gibt koordinaten an, welche zu bestimmter kante ueberprueft werden muessen
            dict = {0: (x, y - 1), 1: (x - 1, y), 2: (x, y + 1), 3: (x + 1, y)}

            # ueberpruefe ob es orte o in alle_orte gibt, welche teile an den koordinaten zu dict haben und ob dafuer
            # auch noch die koordinaten passen
            for o in alle_orte:
                # wenn nachbarkoordinaten mit Karte mit existierendem ort besetzt sind UND deren ortskanten zu neuer
                # karte mit denen dieser neuen Karte uebereinstimmen
                if dict[oe_to_check] in alle_orte[o].koordinaten_plus_oeffnungen and \
                        oe_to_check in alle_orte[o].koordinaten_plus_oeffnungen[dict[oe_to_check]]:

                    # liste den beteiligten ort, der koordinate des ortsteil an dessen kante der an das neue teil anschliesst
                    beteiligte_orte.append((o, dict[oe_to_check], oe_to_check))

                    # falls der existierende ort an mehreren kanten beruehrt wird, soll er trotzdem nur einmal beim
                    # updaten beruecksichtigt werden
                    if o not in counter:
                        counter.append(o)

                    # die betrachtete kannt wird aus der liste aller kanten geloescht, dass sie spater nicht als offene
                    # kante des geupdateten ortes eingetragen wird
                    liste_kanten.remove(oeffnung)

                    # ort wird geloescht, dass spater kein neuer ort damit erzeugt wird
                    if ort not in zu_loeschende_orte:
                        zu_loeschende_orte.append(ort)

    for integrierter_ort in zu_loeschende_orte:
        Karte.orte_karte.remove(integrierter_ort)

    # Ortskanten auf Karte werden auf uebrig gebliebene offene kanten reduziert
    for kartenort in Karte.orte_karte:
        for kante in kartenort.kanten:
            if kante in liste_kanten:
                liste_kanten.remove(kante)

    for beteiligter_ort in beteiligte_orte:
        print("beteiligter_ort", beteiligter_ort)

        # beteiligter_ort[1] ist die koordinaten vom beteiligten ort an dessen kante(n) (beteiligter_ort[2])
        # der neue ort anschliesst
        alle_orte[beteiligter_ort].update_kanten(beteiligter_ort[1], beteiligter_ort[2])

        #### alt
        # alle_orte[beteiligter_ort[0]].koordinaten_plus_oeffnungen[beteiligter_ort[1]].remove(beteiligter_ort[2])

    ### neue Orte erstellen

    for ort in Karte.orte_karte:
        alle_orte.update({ort[0]: Ort(koordinaten, ort[1])})

    ### alte Orte updaten

    # print("C", counter_)

    if len(counter) == 1:
        alle_orte[counter[0]].koordinaten_plus_oeffnungen.update({koordinaten: liste_kanten})
        alle_orte[counter[0]].wert += wert

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
    return alle_orte