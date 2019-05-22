from card_class import Card as Karte

from Ort import Ort
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese

from copy import deepcopy
from rotate2 import rotate_info_right, rotate_kanten_dict_right


class Spiel:
    def __init__(self, card_list):
        self.cards_left = card_list

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
        """from drawing the next card randomly"""
        pass

    def meeple_check(self, x, y, nachbar_karten, kanten_dict):
        """berechnet zu geg. Rotation an geg Koordinaten zu gegebenem Landschaftstyp (buchstabe, zB. 'O') wo ich auf der Karte ein meeple setzen kann (Strassen und Orte)"""

        output = []
        d2 = {0: (x, y + 1), 1: (x + 1, y), 2: (x, y - 1), 3: (x - 1, y)}

        for kante in nachbar_karten:
            if d2[kante] in self.cards_set and self.cards_set[d2[kante]].kanten[self.d[kante]].besitzer is None:

                # appende die entprechende Landschaft auf der Karte
                if kanten_dict[kante] not in output:
                    output.append(kanten_dict[kante])

        return output

    def find_wiesen(self, x, y, card):
        o = []
        d = {(4, 0): (x, y + 1), (5, 1): (x + 1, y), (6, 2): (x, y - 1), (7, 3): (x - 1, y),
              (5, 0): (x, y + 1), (6, 1): (x + 1, y), (7, 2): (x, y - 1), (4, 3): (x - 1, y)}
        for wiese_auf_karte in card.wiesen:
            for ecke in wiese_auf_karte.ecken:
                for kante in self.d2[ecke]:
                    if card.info[kante] in ('W', 'S'):
                        if d[(ecke, kante)] in self.cards_set:
                            if self.cards_set[d[(ecke, kante)]].ecken[self.d3[(ecke, kante)]].besitzer is not None:
                                o.append(wiese_auf_karte)
        return o

    def calculate_possible_actions(self, card, player):
        """checkt, ob und wie karte an jede freie stelle gelegt werden kann,
            returned liste mit tupel bestehend aus moeglicher anlegestelle und anzahl von rotationen die dafür noetig sind
            nimmt eine Karte an, sowie liste möglicher anlegestellen und dictionary von gelegten Karten
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
                            for o in self.meeple_check(x, y, nachbar_karten, kanten_dict):
                                possible_actions.append((x, y, i, o))
                        else:
                            # fuer alle Orte auf der Karte appende actions mit diesem als meepleauswahl
                            for o in card.orte:
                                possible_actions.append((x, y, i, o))

                        if 'S' in nachbar_karten.values():

                            # durchsuche alle orte nach dem der dort liegt und checke, ob der schon besetzt ist, falls nicht
                            # append mit dieser moeglichkeit
                            for s in self.meeple_check(x, y, nachbar_karten, kanten_dict):
                                possible_actions.append((x, y, i, s))
                        else:
                            # fuer alle Orte auf der Karte appende actions mit diesem als meepleauswahl
                            for s in card.strassen:
                                possible_actions.append((x, y, i, s))

                        # TESTEN
                        if len(card.wiesen) > 0:
                            for wiese_auf_karte in self.find_wiesen(x, y, card):
                                possible_actions.append((x, y, i, wiese_auf_karte))

                        if card.mitte == 'K':
                            possible_actions.append((x, y, i, 'K'))

                    possible_actions.append((x, y, i, None))

                # eins weiter rotieren
                info = rotate_info_right(info)
                kanten_dict = rotate_kanten_dict_right(kanten_dict)



        return possible_actions

    def make_action(self, card, koordinates, rotations, player, meeple_position=None):
        """for setting a card and placing a meeple, geht davon aus, dass die action auch legitim ist (sollte ja
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

        ww = {}

        ### update alle Landschaften, inklusive Meeples

        for landschaft in d3[buchstabe][:]:
            for kante in landschaft.kanten[:]:

                # nach richtiger ausrichtung muss ich ja nicht mehr ueberpruefen, da das calculate_possible_actions schon gemacht hat
                if d2[kante] in self.cards_set:
                    if landschaft not in ww:
                        ww.update({landschaft: {self.cards_set[d2[kante]].kanten[self.d[kante]]: (d2[kante], [self.d[kante]])}})
                    else:
                        # wenn die globale_landschaft schon als ww-ls zu ls eingetragen wurde
                        if self.cards_set[d2[kante]].kanten[self.d[kante]] in ww[landschaft]:
                            ww[landschaft][self.cards_set[d2[kante]].kanten[self.d[kante]]][1].append(self.d[kante])
                        else:
                            ww[landschaft].update({self.cards_set[d2[kante]].kanten[self.d[kante]]: (d2[kante], [self.d[kante]])})

                    # eingehen darauf, dass die hier betrachteten kanten des ortes auf der neu gelegten Karte jetzt
                    # keine offenen mehr sein können
                    landschaft.kanten.remove(kante)
                    if landschaft in d3[buchstabe]:
                        d3[buchstabe].remove(landschaft)

        # fuer alle landschaften auf der karte, die wechselwirken berechne WW mit globalen Landschaften
        for landschaft in ww:
            hauptlandschaft = list(ww[landschaft])[0]
            for global_landschaft in ww[landschaft]:

                # wenn die landschaft nur mit einer globalen wechselwirkt
                if len(ww[landschaft]) == 1:

                        global_landschaft.update_kanten(ww[landschaft][global_landschaft])
                        global_landschaft.add_part((x, y), landschaft)

                        if landschaft == meeple_position:
                            global_landschaft.besitzer = player

                # sonst arbeite mit der hauptlandschaft
                else:
                    # passt kanten von der landschaft an
                    global_landschaft.update_kanten(ww[landschaft][global_landschaft])

                    if global_landschaft != hauptlandschaft:
                        self.cards_set[ww[landschaft][global_landschaft][0]].update_kanten(global_landschaft, hauptlandschaft)

                        if buchstabe == 'O':
                            hauptlandschaft.add_global(global_landschaft, self.alle_orte)
                        else:
                            hauptlandschaft.add_global(global_landschaft, self.alle_strassen)
                    else:
                        hauptlandschaft.add_part((x, y), landschaft)


                    if landschaft == meeple_position:
                        hauptlandschaft.besitzer = player
            card.update_kanten(landschaft, hauptlandschaft)

        # kreiere neue landschaften fuer die auf der karte, die nicht wechselwirken
        for landschaft in d3[buchstabe]:
            # create neue landschaft:
            if buchstabe == 'O':
                new_landschaft = Ort((x, y), landschaft.kanten)
                self.alle_orte.append(new_landschaft)
            else:
                new_landschaft = Strasse((x, y), landschaft.kanten)
                self.alle_strassen.append(new_landschaft)

            card.update_kanten(landschaft, new_landschaft)

            if meeple_position == landschaft:
                new_landschaft.besitzer = player

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
                                if (self.cards_set[d2[(ecke, kante)]].ecken[self.d3[(ecke, kante)]], d2[(ecke, kante)]) in ww[wiese]:
                                    continue
                                else:
                                    #ww[wiese].append(self.cards_set[d2[(ecke, kante)]].ecken[self.d3[(ecke, kante)]])
                                    ww[wiese].append((self.cards_set[d2[(ecke, kante)]].ecken[self.d3[(ecke, kante)]], d2[(ecke, kante)]))


        # rechne die ww so aus, dass danach alles global upgedatet ist
        for wiese_auf_karte in ww:
            hauptwiese = list(ww[wiese_auf_karte])[0]
            for global_wiese, koo in ww[wiese_auf_karte]:

                # wenn die wiese nur mit einer globalen wiese wechselwirkt
                if len(ww[wiese_auf_karte]) == 1:
                    global_wiese.add_part((x, y), wiese_auf_karte)

                else:
                    # hauptwiese kommt zum einsatz
                    if global_wiese != hauptwiese:
                        hauptwiese.add_global(global_wiese, self.alle_wiesen)
                        self.cards_set[koo].update_ecken(global_wiese, hauptwiese)
                    else:
                        hauptwiese.add_part((x, y), wiese_auf_karte)

                if meeple_position == wiese_auf_karte:
                    hauptwiese.besizter = player

                card.update_ecken(wiese_auf_karte, global_wiese)


        # erstelle neue Wiesen fuer solche die nicht wechselwirken
        for w in card.wiesen:
            if w not in ww:
                neue_wiese = Wiese((x, y), w.ecken)
                if meeple_position == w:
                    w.besitzer = player
                self.alle_wiesen.append(neue_wiese)
                card.update_ecken(w, neue_wiese)

    def update_all_kloester(self, card, x, y, meeple_position, player):
        if card.mitte == 'K' and meeple_position == 'K':
            self.alle_kloester.append(Kloster((x, y), player))
        else:
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
            if s.besitzer:
                s.besitzer.punkte += s.wert
        for o in self.alle_orte:
            if o.besitzer:
                o.besitzer.punkte += o.wert / 2
        for w in self.alle_wiesen:
            if w.besitzer:
                # damit spaeter nicht jeder ort mehrmals ueberprueft wird
                o = []

                # alle ww orte appenden
                for koords in w.alle_teile:
                    for ecke in w.alle_teile[koords]:
                        for kante in self.d2[ecke]:
                            if isinstance(self.cards_set[koords].kanten[kante], Ort) and self.cards_set[koords].kanten[kante] not in o:
                                o.append(self.cards_set[koords].kanten[kante])
                # fuer jeden fertigen ort 3 punkte
                for ort in o:
                    if ort.fertig:
                        ort.besitzer.punkte += 3

if __name__ == "__main__":
    pass
