from KarteMod import Karte

from Ort import Ort, Ort_auf_Karte
from Strasse import Strasse
from Kloster import Kloster
from Wiese import Wiese

from copy import deepcopy
from rotate2 import rotate_info_right


class Spiel:
    def __init__(self, card_list):
        self.cards_left = card_list

        # dict of cards beeing laid and their coordinates
        self.cards_set = {(0, 0): Karte("S", "O", "S", "W")}

        # list of coordinates already blocked
        self.unavailable_coordinates = [(0, 0)]

        # possible next coordinates
        self.possible_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        self.alle_orte = {"Ort_0": Ort((0, 0), [1])}
        self.alle_strassen = {"Strasse_0": Strasse((0, 0), [0, 2])}
        self.alle_kloester = {}
        self.alle_wiesen = {"Wiese_0": Wiese((0, 0), [4, 7]), "Wiese_1": Wiese((0, 0), [5, 6])}

        # hilfsdictionaries
        self.d = {0: 2, 1: 3, 2: 0, 3: 1}



    def draw_card(self):
        """from drawing the next card randomly"""
        pass

    def meeple_check(self, x, y, z, landschaftsart_liste, nachbar_karten, buchstabe, actions):
        """checkt"""

        d2 = {0: (x, y +1 ), 1: (x + 1, y), 2: (x, y - 1), 3: (x - 1, y)}
        # d3 = {'O': Ort_auf_Karte}#: Strasse_auf_Karte, 'W': Wiese_auf_Karte}

        # durchsuche alle landschaften in liste nach dem Typ der dort liegt und checke, ob er angrenzt, ob der schon besetzt ist, falls nicht
        # append mit dieser moeglichkeit

        # fuer alle nachbar_karten suche ich die landschaft die angrenzt
        for rel_pos in nachbar_karten:
            if nachbar_karten[rel_pos][0] == buchstabe:
                for landschaft in landschaftsart_liste:
                    # wenn die landschaft angrenzt und (and) Kante uebereinstimmt
                    if d2[rel_pos] in landschaft.koordinaten_plus_oeffnungen and self.d[rel_pos] in landschaft.koordinaten_plus_oeffnungen[d2[rel_pos]]:
                        if landschaft.besitzer is not None:
                            continue
                        else:
                            actions.append(x, y, z, nachbar_karten[rel_pos][1])

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

                        # art der Landschaft, die oberhalb der Kante relative_pos liegt
                        buchstabe = self.cards_set[koord_von_karte].info[self.d[relative_pos]]

                        name = None
                        # name von landschaft finden, welche in dem fall auf der Karte betroffen waere
                        if buchstabe == 'O':
                            for o in card.orte:
                                if relative_pos in o.kanten:
                                    name = o.name

                        elif buchstabe == 'S':
                            for s in card.strassen:
                                if relative_pos in s.kanten:
                                    name = s.name
                        else:
                            #wiese
                            pass

                        nachbar_karten.update({relative_pos: (buchstabe, name)})

                        # nicht 100 pro sicher, aber da dann schon karte an nkoo gefunden wurde, kann da ja keine weitere mehr sein
                        continue

            for i in range(4):

                # wenn pro Rotation nach allen Ueberpruefungen immer noch True, dann hinzufuegen
                b = True
                for n in nachbar_karten:
                    if b:
                        b = b and info[n] == nachbar_karten[n][0]
                    else:
                        break

                if b:

                    # jetzt Meeples
                    m = None

                    if player.meeples > 0:

                        # falls beliebig viele ort angrenzen
                        if 'O' in nachbar_karten.values():

                            # durchsuche alle orte nach dem der dort liegt und checke, ob der schon besetzt ist, falls nicht
                            # append mit dieser moeglichkeit
                            self.meeple_check(x, y, i, self.alle_orte, nachbar_karten, 'O', possible_actions)
                        else:
                            # fuer alle Orte auf der Karte appende actions mit diesem als meepleauswahl
                            for o in card.orte:
                                possible_actions.append((x, y, i, o.name))

                        # falls bel viele strassen angrenzen
                        if 'S' in nachbar_karten.values():

                            # durchsuche alle strassen nach der die dort ist unf schau, ob die schon besetzt ist, wenn nicht
                            # appende mit dieser moeglichkeit
                            self.meeple_check(x, y, i, self.alle_strassen, nachbar_karten, 'S', possible_actions)
                        else:
                            # fuer alle strassen auf der Karte das wie oben
                            for s in card.strassen:
                                possible_actions.append((x, y, i, s.name))

                        # falls beliebig viele strassen angrenzen
                        if 'W' in nachbar_karten.values():

                            # durchsuche alle wiesen nach der die dort ist unf schau, ob die schon besetzt ist, wenn nicht
                            # appende mit dieser moeglichkeit
                            pass
                        else:
                            # fuer alle wiesen auf Karte das wie oben
                            pass
                    else:

                        possible_actions.append((x, y, i, m))

                # eins weiter rotieren
                info = rotate_info_right(info)



        return possible_actions


    def make_action(self, card, koordinates, rotations, meeple_position=None):
        """for setting a card and placing a meeple"""

        # if action_is_valid() muss im Spielprogramm dann davor!!!!!!
        # fuer human spieler: if "action" in possible actions

        # entprechend der Rotationen Karte drehen
        for i in range(rotations):
            card.rotate_right()

        # cards_st updaten
        self.cards_set.update({(koordinates[0], koordinates[1]): Karte})

        # wenn auf Karte Orte, Strassen oder Wiesen sind, muessen globale Aequivalente geupdatet werden
        if len(card.orte) > 0:
            self.update_all_orte(card, koordinates[0], koordinates[1], meeple_position)
        if len(card.strassen) > 0:
            self.update_all_strassen(card, koordinates[0], koordinates[1], meeple_position)
        if len(card.wiesenKarte) > 0:
            self.update_all_wiesen(card, koordinates[0], koordinates[1], meeple_position)

        # kloester muessen moeglicherweise immer geupdatet werden, da sie von der Anzahl an Umgebungskarten abhaengen
        self.update_all_kloester(card, koordinates[0], koordinates[1], meeple_position)

        # possible_coordinates und unavailable coordinates updaten
        self.unavailable_coordinates.append((koordinates[0], koordinates[1]))

        for i, (v, w) in enumerate(self.possible_coordinates):
            if (koordinates[0], koordinates[1]) == (v, w):
                del self.possible_coordinates[i]

                # neue possible coordinates hinzufuegen
                for (a, b) in [(koordinates[0], koordinates[1] - 1), (koordinates[0], koordinates[1] + 1), (koordinates[0] - 1, koordinates[1]), (koordinates[0] + 1, koordinates[1])]:
                    if (a, b) not in self.possible_coordinates and (a, b) not in self.unavailable_coordinates:
                        self.possible_coordinates.append((a, b))

    def update_all_orte(self, card, x, y, meeple_position):

        ### finde für jeden Ort auf Karte alle globale Orte, die mit diesem Ort wechselwirken und wie sie wechselwirken

        ### update alle Orte, inklusive Meeples

        pass

    def update_all_strassen(self, card, x, y, meeple_position):
        pass

    def update_all_wiesen(self, card, x, y, meeple_position):
        pass

    def update_all_kloester(self, card, x, y, meeple_position):
        pass

    def final_evaluate(self):
        """for counting if the game is finished to declare the winning player"""
        pass


if __name__ == "__main__":
    c = Karte("O", "W", "S", "S")
    print(c.orte)
    print(isinstance(c, Karte))
    pass
