from card_class import Card as Karte
from random import choice
from Ort import Ort
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese
from Player_Class import Player
from plot_cards import display_spielbrett_dict, draw_card

from rotate2 import rotate_info_right, rotate_kanten_dict_right, rotate_ecken_dict_right
import random
from copy import deepcopy

class Spiel:

    #def __init__(self, card_list, cards_set=None, unavailable_coords=None, possible_coords=None, alle_orte=None,
    #             alle_strassen=None, alle_wiesen=None, alle_kloester=None, start=False):

    #    if cards_set==None:
    #        self.cards_set = []

    def __init__(self, card_list, player1=None, player2=None):
        self.cards_left = card_list

       # self.next_player = {player1: player2, player2: player1}
        self.player_to_playernumber = {1: player1, 2: player2}

        # dict of cards beeing laid and their coordinates
        self.cards_set = {(0, 0): Karte("S", "O", "S", "W")}
        # cards_seT initializen
        strasse0 = Strasse((0, 0), [0, 2])
        ort0 = Ort((0, 0), [1])
        wiese0 = Wiese((0, 0), [5, 6])
        wiese1 = Wiese((0, 0), [4, 7])

        # NONE steht hier noch fuer Wiese
        self.cards_set[(0, 0)].kanten = {0: strasse0, 1: ort0, 2: strasse0, 3: None}
        self.cards_set[(0, 0)].ecken = {4: wiese1, 5: wiese0, 6: wiese0, 7: wiese1}

        # list of coordinates already blocked
        self.unavailable_coordinates = [(0, 0)]

        # possible next coordinates
        self.possible_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        self.alle_orte = [ort0]
        self.alle_strassen = [strasse0]
        self.alle_kloester = []
        self.alle_wiesen = [wiese0, wiese1]

        # hilfsdictionaries
        self.d = {0: 2, 1: 3, 2: 0, 3: 1}
        # kanten fuer ecken bei wiesen
        self.d2 = {4: [0, 3], 5: [0, 1], 6: [1, 2], 7: [2, 3]}
        # ecken von nachbarkarten nach ecke und kante auf aktueller karte
        self.d3 = {(4, 0): 7, (4, 3): 5, (5, 0): 6, (5, 1): 4, (6, 1): 7, (6, 2): 5, (7, 2): 4, (7, 3): 6}

    def draw_card(self):
        auswahl = choice(self.cards_left)
        self.cards_left.remove(auswahl)
        return auswahl

    #def draw_first_card_from_stack(self):
    #    """returned den ersten Eintrag der Kartenliste und entfernt die Karte aus der Liste"""
    #    return self.cards_left.pop(0)

    #obsolet
    def meeple_check(self, x, y, nachbar_kanten, kanten_dict):
        """berechnet zu bel. rotierter Karte an geg Koordinaten zu gegebenem Landschaftstyp (buchstabe, zB. 'O')
         wo ich auf der Karte ein meeple setzen kann (Strassen und Orte)

        :param x: die koordinaten an denen gecheckt werden soll
        :param y:

        :param nachbar_kanten: ein dict der Form {2: 'O'} das angibt welcher Landschaftstyp an welche Kante
                                der aktuellen Karte angrenzt. Hier: An die Kante 2 der Karte grenzt ein Ort an
                                Dabei ist zu sagen, dass das unabhaengig von der Karte passiert. Das dict gibt an,
                                welche Landschaftstypen an den Kanten der leeren Stelle an den Koordinaten x, y
                                angrenzen

        :param kanten_dict: ein dict der Form {0: <Ort.Ort_auf_Karte object at 0x7fd3ef25e0b8>,
                                                1: None, 2: <Ort.Ort_auf_Karte object at 0x7fd3ef25e080>, 3: None}
        Es ist das kanten dict der Karte zur aktuellen Rotation:
        An Kante 0 der Karte liegt der OaK 0x7fd... etc

        :return: gibt Liste mit Landschaften auf der Karte zurueck, auf die in Abhaengigkeit mit anderen Landschaften
        des selben Typs noch Meeples gesetzt werden koennen
        """
        output = []
        d2 = {0: (x, y + 1), 1: (x + 1, y), 2: (x, y - 1), 3: (x - 1, y)}

        for kante in nachbar_kanten:
            if nachbar_kanten[kante] is not 'W' and d2[kante] in self.cards_set and self.cards_set[d2[kante]].kanten[self.d[kante]].besitzer is None:

                # appende die entprechende Landschaft auf der Karte
                if kanten_dict[kante] not in output:
                    output.append(kanten_dict[kante])

        return output

    def meeple_check2(self, x, y, nachbar_kanten, kanten_dict):
        """berechnet zu bel. rotierter Karte an geg Koordinaten zu gegebenem Landschaftstyp (buchstabe, zB. 'O')
         wo ich auf der Karte ein meeple setzen kann (Strassen und Orte)

        :param x: die koordinaten an denen gecheckt werden soll
        :param y:

        :param nachbar_kanten: ein dict der Form {2: 'O'} das angibt welcher Landschaftstyp an welche Kante
                                der aktuellen Karte angrenzt. Hier: An die Kante 2 der Karte grenzt ein Ort an
                                Dabei ist zu sagen, dass das unabhaengig von der Karte passiert. Das dict gibt an,
                                welche Landschaftstypen an den Kanten der leeren Stelle an den Koordinaten x, y
                                angrenzen

        :param kanten_dict: ein dict der Form {0: <Ort.Ort_auf_Karte object at 0x7fd3ef25e0b8>,
                                                1: None, 2: <Ort.Ort_auf_Karte object at 0x7fd3ef25e080>, 3: None}
        Es ist das kanten dict der Karte zur aktuellen Rotation:
        An Kante 0 der Karte liegt der OaK 0x7fd... etc

        :return: gibt Liste mit Landschaften auf der Karte zurueck, auf die in Abhaengigkeit mit anderen Landschaften
        des selben Typs keine Meeples gesetzt werden koennen"""

        forbidden_landschaften = []
        d2 = {0: (x, y + 1), 1: (x + 1, y), 2: (x, y - 1), 3: (x - 1, y)}

        for kante in nachbar_kanten:
            if nachbar_kanten[kante] is not 'W' and d2[kante] in self.cards_set and self.cards_set[d2[kante]].kanten[self.d[kante]].besitzer is not None:

                # appende die entprechende Landschaft auf der Karte
                if kanten_dict[kante] not in forbidden_landschaften:
                    forbidden_landschaften.append(kanten_dict[kante])

        return forbidden_landschaften

    # obsolet
    def find_angrenzende_wiesen(self, x, y, info, wiese_auf_karte):
        """finde zu einer Wiese_auf_karte alle angrenzenden globalen wiesen und returne liste von diesen"""
        o = []
        d = {(4, 0): (x, y + 1), (5, 1): (x + 1, y), (6, 2): (x, y - 1), (7, 3): (x - 1, y),
              (5, 0): (x, y + 1), (6, 1): (x + 1, y), (7, 2): (x, y - 1), (4, 3): (x - 1, y)}
        for ecke in wiese_auf_karte.ecken:
            for kante in self.d2[ecke]:
                if info[kante] in ('W', 'S'):
                    if d[(ecke, kante)] in self.cards_set:
                        o.append(self.cards_set[d[(ecke, kante)]].ecken[self.d3[(ecke, kante)]])
        return o

    def meeple_check_wiesen(self, x, y, rotations, info, card):
        """

        :param x:
        :param y:
        :param rotations:
        :param card:
        :return: soll fuer die Karte bei der Anzahl von i rechts-Rotationen ausgeben, welche Wiesen nicht besetzt werden duerfen
        """
        d = {(4, 0): (x, y + 1), (5, 1): (x + 1, y), (6, 2): (x, y - 1), (7, 3): (x - 1, y),
             (5, 0): (x, y + 1), (6, 1): (x + 1, y), (7, 2): (x, y - 1), (4, 3): (x - 1, y)}

        forbidden = []

        ecken = card.ecken.copy()
        for i in range(rotations):
            ecken = rotate_ecken_dict_right(ecken)

        for ecke in ecken:
            # wenn die wak zu der die Ecke gehoert noch nicht als verboten gesetzt wurde
            if ecken[ecke] not in forbidden:
                #schau mir beide Kanten zu der Ecke an
                for kante in self.d2[ecke]:
                    if info[kante] in ('W', 'S'):
                        if d[(ecke, kante)] in self.cards_set:
                            if self.cards_set[d[(ecke, kante)]].ecken[self.d3[(ecke, kante)]].besitzer is not None:
                                forbidden.append(ecken[ecke])

        return forbidden


    def calculate_possible_actions(self, card, player):
        """
        :param card:
        :param player:
        :return:

        checkt, ob und wie karte an jede freie stelle gelegt werden kann,
        returned liste mit tupel bestehend aus moeglicher anlegestelle und anzahl von rotationen die dafür noetig sind

        fuer jede theoretisch freien koordinaten werden aktuell noch die Nachbarkanten ermittelt, um zu schauen, ob dort angelegt werden kann

        nun wird fuer jede rotation ermittelt, ob die gezogene Karte zu diesen Kanten passt

        dann werden alle angrenzenden landschaften nach besitzern gecheckt


        """

        possible_actions = []

        # ich will hier nicht wirklich was an der Karte rotieren, nur um zu schauen, wo was passt
        info = card.info[:]

        for x, y in self.possible_coordinates:

            # zuerst alle nachbarkarten finden und speichern wo sie relatativ zu eigener Karte liegen
            # das sollte woanders gemacht werden, da man sonst fuer jede neu gezogene Karte immer wieder die umgebung
            # untersucht, obwohl man das schon x mal davor gemacht hat
            nachbar_koordinaten = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
            nachbar_karten = {}

            for relative_pos, nkoo in enumerate(nachbar_koordinaten):
                for koord_von_karte in self.cards_set:
                    if koord_von_karte == nkoo:

                        # art der Landschaft, die neben der Kante relative_pos liegt
                        # buchstabe = self.cards_set[koord_von_karte].info[self.d[relative_pos]]
                        # das selbe nur direkt schon als argument eingegeben
                        nachbar_karten.update({relative_pos: self.cards_set[koord_von_karte].info[self.d[relative_pos]]})

                        # nicht 100 pro sicher, aber da dann schon karte an nkoo gefunden wurde, kann da ja keine weitere mehr sein
                        continue

            # ecken_dict = card.ecken.copy()
            kanten_dict = card.kanten.copy()
            for i in range(4):

                # wenn pro Rotation nach allen Ueberpruefungen immer noch True, dann hinzufuegen
                b = True
                for n in nachbar_karten:
                    if b:
                        b = b and info[n] == nachbar_karten[n]
                    else:
                        break
                # hinzufuegen?
                if b:
                    # jetzt Meeples
                    if player.meeples > 0:
                        # falls beliebig viele ort angrenzen
                        if 'O' in nachbar_karten.values():

                            # durchsuche alle orte nach dem der dort liegt und checke, ob der schon besetzt ist, falls nicht
                            # append mit dieser moeglichkeit
                            for o in card.orte:
                                if o not in self.meeple_check2(x, y, nachbar_karten, kanten_dict):
                                    possible_actions.append((x, y, i, o))

                            # fuer alle orte, die nicht wechselwirken, aber noch auf der Karte sind:



                        else:
                            # fuer alle Orte auf der Karte appende actions mit diesem als meepleauswahl
                            for o in card.orte:
                                possible_actions.append((x, y, i, o))

                        if 'S' in nachbar_karten.values():

                            # durchsuche alle orte nach dem der dort liegt und checke, ob der schon besetzt ist, falls nicht
                            # append mit dieser moeglichkeit
                            for s in card.strassen:
                                forbidden = self.meeple_check2(x, y, nachbar_karten, kanten_dict)
                                if s not in forbidden:
                                    possible_actions.append((x, y, i, s))
                        else:
                            # fuer alle Orte auf der Karte appende actions mit diesem als meepleauswahl
                            for s in card.strassen:
                                possible_actions.append((x, y, i, s))

                        # TESTEN
                        #for wiese_auf_karte in card.wiesen:
                        #    besitzer = [0 for x in self.find_angrenzende_wiesen(x, y, info, wiese_auf_karte) if x.besitzer is not None]
                        #    if not besitzer:
                        #        possible_actions.append((x, y, i, wiese_auf_karte))

                        forbidden_wiesen = self.meeple_check_wiesen(x, y, i, info, card)
                        for wiese in card.wiesen:
                            if wiese not in forbidden_wiesen:
                                possible_actions.append((x, y, i, wiese))

                        if card.mitte == 'K':
                            possible_actions.append((x, y, i, 'K'))

                    possible_actions.append((x, y, i, None))

                # eins weiter rotieren
                info = rotate_info_right(info)
                kanten_dict = rotate_kanten_dict_right(kanten_dict)



        return possible_actions

    def make_action(self, card, koordinates, rotations, player, meeple_position=None):
        """

        :param card: Karte, die gespielt werden soll
        :param koordinates: tuple (x, y)
        :param rotations: anzahl an rechtsrotationen zum Karte legen
        :param player: Spieler, der diese Aktion spielt
        :param meeple_position: Landschaft auf der ein Meeple pletziert werden soll, standard=None, also keine Meeple-Platzierung
        :return:
        for setting a card and placing a meeple, geht davon aus, dass die action auch legitim ist (sollte ja
        vorher gechekt werden)"""

        # if action_is_valid() muss im Spielprogramm dann davor!!!!!!

        if meeple_position is not None:
            player.meeples -= 1

        # entprechend der Rotationen Karte drehen
        for i in range(rotations):
            card.rotate_right()

        # wenn auf Karte Orte, Strassen oder Wiesen sind, muessen globale Aequivalente geupdatet werden
        if len(card.orte) > 0:
            self.update_all_landschaften(card, koordinates[0], koordinates[1], meeple_position, 'O', player)
        if len(card.strassen) > 0:
            self.update_all_landschaften(card, koordinates[0], koordinates[1], meeple_position, 'S', player)
        if len(card.wiesen) > 0:            # nur bei ooooo nicht
            self.update_all_wiesen(card, koordinates[0], koordinates[1], meeple_position, player)

        # kloester muessen moeglicherweise immer geupdatet werden, da sie von der Anzahl an Umgebungskarten abhaengen
        self.update_all_kloester(card, koordinates[0], koordinates[1], meeple_position, player)

        # cards_set updaten
        self.cards_set.update({(koordinates[0], koordinates[1]): card})

        # possible_coordinates und unavailable coordinates updaten
        self.unavailable_coordinates.append((koordinates[0], koordinates[1]))

        for i, (v, w) in enumerate(self.possible_coordinates):
            if (koordinates[0], koordinates[1]) == (v, w):
                del self.possible_coordinates[i]

                # neue possible coordinates hinzufuegen
                for (a, b) in [(koordinates[0], koordinates[1] - 1), (koordinates[0], koordinates[1] + 1), (koordinates[0] - 1, koordinates[1]), (koordinates[0] + 1, koordinates[1])]:
                    if (a, b) not in self.possible_coordinates and (a, b) not in self.unavailable_coordinates:
                        self.possible_coordinates.append((a, b))

    def update_all_landschaften(self, card, x, y, meeple_position, buchstabe, player):

        d2 = {0: (x, y + 1), 1: (x + 1, y), 2: (x, y - 1), 3: (x - 1, y)}
        d3 = {'O': card.orte, 'S': card.strassen}
        d4 = {'O': self.alle_orte, 'S': self.alle_strassen}

        ww = {}

        ### update alle Landschaften, inklusive Meeples

        for landschaft in d3[buchstabe][:]:
            for kante in landschaft.kanten[:]:

                # nach richtiger ausrichtung muss ich ja nicht mehr ueberpruefen, da das calculate_possible_actions schon gemacht hat
                if d2[kante] in self.cards_set:
                    if landschaft not in ww:
                        ww.update({landschaft: {self.cards_set[d2[kante]].kanten[self.d[kante]]: [(d2[kante], self.d[kante])]}})
                    else:
                        # wenn die globale_landschaft schon als ww-ls zu ls eingetragen wurde
                        if self.cards_set[d2[kante]].kanten[self.d[kante]] in ww[landschaft]:
                            ww[landschaft][self.cards_set[d2[kante]].kanten[self.d[kante]]].append((d2[kante], self.d[kante]))
                        else:
                            ww[landschaft].update({self.cards_set[d2[kante]].kanten[self.d[kante]]: [(d2[kante], self.d[kante])]})

                    # eingehen darauf, dass die hier betrachteten kanten des ortes auf der neu gelegten Karte jetzt
                    # keine offenen mehr sein können
                    landschaft.kanten.remove(kante)
                    if landschaft in d3[buchstabe]:
                        d3[buchstabe].remove(landschaft)

        # print("ww fertig")
        # fuer alle landschaften auf der karte, die wechselwirken berechne WW mit globalen Landschaften
        for landschaft in ww:
            hauptlandschaft = list(ww[landschaft])[0]
            for global_landschaft in ww[landschaft]:

                # wenn die landschaft nur mit einer globalen wechselwirkt
                if len(ww[landschaft]) == 1:

                        if landschaft == meeple_position:
                            global_landschaft.update_meeples(player)
                            global_landschaft.update_besitzer()
                            #global_landschaft.besitzer = player

                        global_landschaft.update_kanten(ww[landschaft][global_landschaft])
                        global_landschaft.add_part((x, y), landschaft)


                # sonst arbeite mit der hauptlandschaft
                else:
                    # passt kanten von der landschaft an
                    global_landschaft.update_kanten(ww[landschaft][global_landschaft])

                    if global_landschaft != hauptlandschaft:

                        # HIER AUCH FUER ALLE Beteiligten karten die kanten updaten, nicht nur fuer die neue

                        for koos in global_landschaft.koordinaten_plus_oeffnungen:
                            self.cards_set[koos].update_kanten(global_landschaft, hauptlandschaft)

                            #self.cards_set[ww[landschaft][global_landschaft][0]].update_kanten(global_landschaft, hauptlandschaft)

                        if buchstabe == 'O':
                            hauptlandschaft.add_global(global_landschaft, self.alle_orte)
                        else:
                            hauptlandschaft.add_global(global_landschaft, self.alle_strassen)
                    else:
                        hauptlandschaft.add_part((x, y), landschaft)

                        if landschaft == meeple_position:
                            hauptlandschaft.update_meeples(player)
                            hauptlandschaft.update_besitzer()

            card.update_kanten(landschaft, hauptlandschaft)

        # fuer alle globalen landschaften checke, ob die fertig sind und wenn ja werte korrekt aus
        glob_lands = [gl for lak in ww for gl in ww[lak] if gl in d4[buchstabe]]
        for global_land in glob_lands:
            global_land.check_if_fertig()
            global_land.evaluate()

        # kreiere neue landschaften fuer die auf der karte, die nicht wechselwirken
        for landschaft in d3[buchstabe]:
            # create neue landschaft:
            if buchstabe == 'O':
                new_landschaft = Ort((x, y), landschaft.kanten, landschaft.wert)

                if meeple_position == landschaft:
                    new_landschaft.update_meeples(player)
                    new_landschaft.update_besitzer()
                self.alle_orte.append(new_landschaft)
            else:
                new_landschaft = Strasse((x, y), landschaft.kanten)
                if meeple_position == landschaft:
                    new_landschaft.update_meeples(player)
                    new_landschaft.update_besitzer()
                self.alle_strassen.append(new_landschaft)

            card.update_kanten(landschaft, new_landschaft)

           # if meeple_position == landschaft:
           #     new_landschaft.besitzer = player

    def update_all_wiesen(self, card, x, y, meeple_position, player):

        d2 = {(4, 0): (x, y + 1), (5, 1): (x + 1, y), (6, 2): (x, y - 1), (7, 3): (x - 1, y),
              (5, 0): (x, y + 1), (6, 1): (x + 1, y), (7, 2): (x, y - 1), (4, 3): (x - 1, y)}
        ww = {}

        # fuer jede wiese auf der karte
        for wiese in card.wiesen:
            for ecke in wiese.ecken:
                for kante in self.d2[ecke]:
                    # wenn an der Kante Wiese oder Strasse ist
                    if card.info[kante] in ('W', 'S'):
                        if d2[(ecke, kante)] in self.cards_set:
                            if wiese not in ww:
                                #ww.update({wiese: [self.cards_set[d2[(ecke, kante)]].ecken[self.d3[(ecke, kante)]]]})
                                ww.update({wiese: [(self.cards_set[d2[(ecke, kante)]].ecken[self.d3[(ecke, kante)]], d2[(ecke, kante)])]})

                            else:
                                # wenn die globale wiese schon als ww eingetregen ist
                                #if self.cards_set[d2[(ecke, kante)]].ecken[self.d3[(ecke, kante)]]:
                                if self.cards_set[d2[(ecke, kante)]].ecken[self.d3[(ecke, kante)]] in [w[0] for w in ww[wiese]]:
                                    continue
                                else:
                                    #ww[wiese].append(self.cards_set[d2[(ecke, kante)]].ecken[self.d3[(ecke, kante)]])
                                    ww[wiese].append((self.cards_set[d2[(ecke, kante)]].ecken[self.d3[(ecke, kante)]], d2[(ecke, kante)]))


        # rechne die ww so aus, dass danach alles global upgedatet ist
        for wiese_auf_karte in ww:
            hauptwiese = list(ww[wiese_auf_karte])[0][0]
            for global_wiese, koo in ww[wiese_auf_karte]:

                # wenn die wiese nur mit einer globalen wiese wechselwirkt
                if len(ww[wiese_auf_karte]) == 1:
                    # wenn euf das Teil das gesetzt wird ein meeple auf die wiese gesetzt wird
                    if wiese_auf_karte == meeple_position:
                        global_wiese.update_meeples(player)
                        global_wiese.update_besitzer()

                    global_wiese.add_part((x, y), wiese_auf_karte)

                else:
                    # hauptwiese kommt zum einsatz
                    if global_wiese != hauptwiese:



                        hauptwiese.add_global(global_wiese, self.alle_wiesen)
                        for koos in global_wiese.alle_teile:
                            if koos in self.cards_set:
                                self.cards_set[koos].update_ecken(global_wiese, hauptwiese)
                    else:



                        hauptwiese.add_part((x, y), wiese_auf_karte)

                #if meeple_position == wiese_auf_karte:
                #    hauptwiese.besizter = player

            card.update_ecken(wiese_auf_karte, hauptwiese)


        # erstelle neue Wiesen fuer solche die nicht wechselwirken
        for w in card.wiesen:
            if w not in ww:
                neue_wiese = Wiese((x, y), w.ecken)
                if meeple_position == w:
                    neue_wiese.update_meeples(player)
                    neue_wiese.update_besitzer()
                self.alle_wiesen.append(neue_wiese)
                card.update_ecken(w, neue_wiese)

    def update_all_kloester(self, card, x, y, meeple_position, player):
        if card.mitte == 'K' and meeple_position == 'K':
            new_kloster = Kloster((x, y), player)
            for k in new_kloster.umgebungs_koordinaten:
                if k in self.cards_set:
                    new_kloster.counter += 1
            # wenn das kloster nach Erstellung noch nicht fertig ist
            new_kloster.check_if_fertig()
            if not new_kloster.fertig:
                self.alle_kloester.append(new_kloster)

        #else:
        for kloster in self.alle_kloester[:]:
            if (x, y) in kloster.umgebungs_koordinaten:
                kloster.counter += 1
                kloster.check_if_fertig()
                if kloster.fertig:
                    self.alle_kloester.remove(kloster)

    def final_evaluate(self):
        """for counting if the game is finished to declare the winning player"""

        for k in self.alle_kloester:
            k.besitzer.punkte += k.counter
        for s in self.alle_strassen:
            if s.besitzer and not s.fertig:
                s.besitzer.punkte += s.wert
        for o in self.alle_orte:
            if o.besitzer and not o.fertig:
                o.besitzer.punkte += int(o.wert / 2)
        for w in self.alle_wiesen:
            if len(w.meeples) > 0:
                # damit spaeter nicht jeder ort mehrmals ueberprueft wird
                o = []

                # alle ww orte appenden
                for koords in w.alle_teile:
                    for ecke in w.alle_teile[koords]:
                        for kante in self.d2[ecke]:
                            # wenn an der kante auf der Karte ein Ortsteil ist und dieser Ort noch nicht beruecksichtigt wurde
                            if isinstance(self.cards_set[koords].kanten[kante], Ort) and self.cards_set[koords].kanten[kante] not in o:
                                o.append(self.cards_set[koords].kanten[kante])
                # fuer jeden fertigen ort 3 punkte
                for ort in o:
                    if ort.fertig:
                        if w.besitzer is not None:
                            w.besitzer.punkte += 3
                        else:
                            for pl in w.meeples:
                                pl.punkte += 3


    def player_vs_player(self):
        player1 = Player(1)
        player2 = Player(2)

        turn = player1
        d = {player1: player2, player2: player1}

        while len(self.cards_left) > 0:
            print("\nplayer1:", player1.punkte, " punkte\nplayer2:", player2.punkte, "punkte")
            display_spielbrett_dict(self.cards_set)
            auswahl = self.draw_card()
            print('Deine Karte ist [{0}, {1}, {2}, {3}, {4}, {5}]'.format(auswahl.info[0], auswahl.info[1], auswahl.info[2], auswahl.info[3], auswahl.mitte, auswahl.schild))
            draw_card(auswahl)
            print('Sie enthält folgende moegliche Meeplepositionen:')
            print('Orte:')
            for o in auswahl.orte:
                print(o.name, o.kanten)
            print('Strassen:')
            for s in auswahl.strassen:
                print(s.name, s.kanten)
            print('Wiesen:')
            for w in auswahl.wiesen:
                print(w.name, w.ecken)

            pos_anl = self.calculate_possible_actions(auswahl, turn)

            # wenn es anlegestellen gibt
            if pos_anl:

                inp = input('Bitte gib deine Aktion an:')
                inp_split = inp.split(' ')
                if inp_split[3][0] == 'o':
                    o = [a for a in auswahl.orte if a.name == int(inp_split[3][1])]
                    action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), o[0])
                elif inp_split[3][0] == 's':
                    s = [a for a in auswahl.strassen if a.name == int(inp_split[3][1])]
                    action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), s[0])
                elif inp_split[3][0] == 'w':
                    w = [a for a in auswahl.wiesen if a.name == int(inp_split[3][1])]
                    action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), w[0])
                else:
                    action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), None)

                while action not in pos_anl:
                    print("illegaler Move")
                    inp = input('Bitte gib deine Aktion an:')
                    inp_split = inp.split(' ')
                    if inp_split[3][0] == 'o':
                        o = [a for a in auswahl.orte if a.name == int(inp_split[3][1])]
                        action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), o[0])
                    elif inp_split[3][0] == 's':
                        s = [a for a in auswahl.strassen if a.name == int(inp_split[3][1])]
                        action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), s[0])
                    elif inp_split[3][0] == 'w':
                        w = [a for a in auswahl.wiesen if a.name == int(inp_split[3][1])]
                        action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), w[0])
                    else:
                        action = (int(inp_split[0]), int(inp_split[1]), int(inp_split[2]), None)

                self.make_action(auswahl, (action[0], action[1]), action[2], turn, action[3])

            else:
                turn = d[turn]
                continue

            turn = d[turn]


    def play_random1v1(self, player1, player2):
        """

        :param player1: spieler der zuerst seinen Zug macht
        :param player2:
        :return: Spieler, der am Ende gewonnen hat
        """
        d = {player1: player2, player2: player1}
        turn_player = player1

        while len(self.cards_left) > 0:
            card = self.draw_card()
            #draw_card(card)
            pos = self.calculate_possible_actions(card, turn_player)
            if len(pos) > 0:
                action = random.choice(pos)

            # keine moegliche anlegestelle
            else:
                continue


            self.make_action(card, (action[0], action[1]), action[2], turn_player, action[3])
            #display_spielbrett_dict(self.cards_set)

            turn_player = d[turn_player]

        self.final_evaluate()
        #display_spielbrett_dict(self.cards_set)

        #unentschieden:
        if player1.punkte == player2.punkte:
            return 0
        else:
            # ansonsten returne den gewinner
            return max(list(d), key=lambda x: x.punkte)



if __name__ == "__main__":

    from card_class import create_kartenliste

    karteninfoliste = ['WWWWK', 'WWWWK', 'WWWWK', 'WWWWK', 'WWSWK', 'WWSWK', 'OOOOOT', 'SOSW', 'SOSW', 'SOSW', 'OWWW',
                       'OWWW', 'OWWW', 'OWWW', 'OWWW', 'WOWOOT', 'WOWOOT', 'OWOWO', 'WOWO', 'WOWO', 'WOWO', 'WOOW',
                       'WOOW', 'OSSW', 'OSSW', 'OSSW', 'SOWS', 'SOWS', 'SOWS', 'SOSSG', 'SOSSG', 'SOSSG', 'OWWOOT',
                       'OWWOOT', 'OWWOO', 'OWWOO', 'OWWOO', 'OSSOOT', 'OSSOOT', 'OSSOO', 'OSSOO', 'OSSOO', 'OOWOOT',
                       'OOWOO', 'OOWOO', 'OOWOO', 'OOSOOT', 'OOSOOT', 'OOSOO', 'SWSW', 'SWSW', 'SWSW', 'SWSW', 'SWSW',
                       'SWSW', 'SWSW', 'SWSW', 'WWSS', 'WWSS', 'WWSS', 'WWSS', 'WWSS', 'WWSS', 'WWSS', 'WWSS', 'WWSS',
                       'WSSSG', 'WSSSG', 'WSSSG', 'WSSSG', 'SSSSG']

    kartenliste = create_kartenliste(karteninfoliste)

    c1 = 0
    c2 = 0
    c3 = 0

    c = 1
    while True:
        print("Spiel{}".format(c))
        privateliste = deepcopy(kartenliste)
        print(privateliste)

        spiel = Spiel(privateliste)
        #spiel2 = deepcopy(spiel)
    #spiel.player_vs_player()
    #draw_card(spiel.draw_card())

        pl1 = Player(1)
        pl2 = Player(2)

        spiel.play_random1v1(pl1, pl2)

        if pl1.punkte != pl2.punkte:
            winner = max((pl1, pl2), key=lambda x: x.punkte)
        else:
            winner = 0

        if winner == pl1:
            c1 += 1
        elif winner == pl2:
            c2 += 1
        else:
            c3 += 1

        c += 1

        print("Gewinne 1: {}, Gewinne 2: {}, Unentschieden: {}".format(c1, c2, c3))
