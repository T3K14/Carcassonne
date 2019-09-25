import gc

class WieseAufKarte:
    def __init__(self, ecken, name):
        self.ecken = ecken
        self.name = name

        # fuer mcts-spielkopie ww
        self.id = 'w'


class Wiese:
    def __init__(self, koordinates, ecken):
        self.wert = 0
        self.alle_teile = {koordinates: ecken}
        self.besitzer = None
        self.meeples = {}

    def add_part(self, koords, wiese_auf_karte):

        if (koords[0], koords[1]) not in self.alle_teile:
            self.alle_teile.update({(koords[0], koords[1]): wiese_auf_karte.ecken})
        else:
            for ecke in wiese_auf_karte.ecken:
                self.alle_teile[(koords[0], koords[1])].append(ecke)

    def add_global(self, global_wiese, alle_wiesen, cards_set, card):

        for teil in list(global_wiese.alle_teile):
            if teil not in self.alle_teile:
                self.alle_teile.update({teil: global_wiese.alle_teile[teil]})

            else:
                for ecke in global_wiese.alle_teile[teil]:
                    self.alle_teile[teil].append(ecke)

            # die neue Karte kann in der globalen Wiese bereits enthalten sein, aber das Teil dazu ist noch nicht in cards_set vorhanden
            if teil in cards_set:
                cards_set[teil].update_ecken(global_wiese, self)
            else:
                # die Ecken der neuen Karte muessen auch geupdated werden
                for ecke in global_wiese.alle_teile[teil]:
                    if card.ecken[ecke] == global_wiese:
                        card.ecken[ecke] = self


        for pl in global_wiese.meeples:
            if pl in self.meeples:
                self.meeples[pl] += global_wiese.meeples[pl]
            else:
                self.meeples.update({pl: global_wiese.meeples[pl]})

        if len(global_wiese.meeples) > 0:
            self.update_besitzer()

        # gilt nur nicht, wenn das Kloster mit strasse involviert ist ??? Quatsch
        if global_wiese in alle_wiesen:
            alle_wiesen.remove(global_wiese)


        """
        if global_wiese in alle_wiesen:
            for teil in list(global_wiese.alle_teile):
                if teil not in self.alle_teile:
                    self.alle_teile.update({teil: global_wiese.alle_teile[teil]})

                else:
                    for ecke in global_wiese.alle_teile[teil]:
                        self.alle_teile[teil].append(ecke)

                cards_set[teil].update_ecken(global_wiese, self)

            for pl in global_wiese.meeples:
                if pl in self.meeples:
                    self.meeples[pl] += global_wiese.meeples[pl]
                else:
                    self.meeples.update({pl: global_wiese.meeples[pl]})

            if len(global_wiese.meeples) > 0:
                self.update_besitzer()

            # gilt nur nicht, wenn das Kloster mit strasse involviert ist ??? Quatsch
            if global_wiese in alle_wiesen:
                alle_wiesen.remove(global_wiese)

        else:
            # die globale Wiese wurde gerade schon zu einer anderen hinzugefuegt

            # finde die globale Wiese
            to_delete = None
            for glob in alle_wiesen:

                # falls es eine globale Wiese gibt, welche die ersten Koord der 'global_wiese' beinhaltet und auch die Kanten
                if list(global_wiese.alle_teile)[0] in glob.alle_teile and set(global_wiese.alle_teile[list(global_wiese.alle_teile)[0]]).issubset(set(glob.alle_teile[list(global_wiese.alle_teile)[0]])):

                    for teil in list(glob.alle_teile):
                        if teil not in self.alle_teile:
                            self.alle_teile.update({teil: glob.alle_teile[teil]})
                        else:
                            for ecke in glob.alle_teile[teil]:
                                self.alle_teile[teil].append(ecke)

                        cards_set[teil].update_ecken(glob, self)

                    for pl in glob.meeples:
                        if pl in self.meeples:
                            self.meeples[pl] += glob.meeples[pl]
                        else:
                            self.meeples.update({pl: glob.meeples[pl]})

                    if len(glob.meeples) > 0:
                        self.update_besitzer()

                    to_delete = glob
                    break
            alle_wiesen.remove(to_delete)
        """

    def update_meeples(self, player):
        """ nimmt player an, welcher ein meeple auf diese landschaft setzt"""
        if player in self.meeples:
            self.meeples[player] += 1
        else:
            self.meeples.update({player: 1})

    def update_besitzer(self):

        max_meeple_count = max(self.meeples.values())
        players_with_max_count = [pl for pl in self.meeples if self.meeples[pl] == max_meeple_count]

        if len(players_with_max_count) != 1:
            self.besitzer = None
        else:
            self.besitzer = players_with_max_count[0]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        a = hash(repr(self))
        return hash(repr(self))

