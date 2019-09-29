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

    def add_global2(self, global_wiese, cards_set, card):

        # flag wird True, falls ein neues Teil dazu kommt, oder neue Kanten zu bestehenden Teilen
        flag = False

        for teil in list(global_wiese.alle_teile):
            if teil not in self.alle_teile:
                self.alle_teile.update({teil: global_wiese.alle_teile[teil]})
                flag = True

            else:
                for ecke in global_wiese.alle_teile[teil]:
                    if ecke not in self.alle_teile[teil]:
                        self.alle_teile[teil].append(ecke)
                        flag = True

            # die neue Karte kann in der globalen Wiese bereits enthalten sein, aber das Teil dazu ist noch nicht in cards_set vorhanden
            if teil in cards_set:
                cards_set[teil].update_ecken(global_wiese, self)
            else:
                # die Ecken der neuen Karte muessen auch geupdated werden
                for ecke in global_wiese.alle_teile[teil]:
                    if card.ecken[ecke] == global_wiese:
                        card.ecken[ecke] = self

        # nur, falls was neues dazu gekommen ist, werden meeples geupdated, sonst werden vllt Wiesen zweimal hinzugefuegt und meeple-counts falsch
        if flag:

            for pl in global_wiese.meeples:
                if pl in self.meeples:
                    self.meeples[pl] += global_wiese.meeples[pl]
                else:
                    self.meeples.update({pl: global_wiese.meeples[pl]})

            if len(global_wiese.meeples) > 0:
                self.update_besitzer()

    def hat_ueberschneidung_mit(self, hauptwiese):
        """
        nimmt eine andere Hauptwiese an und returend True, wenn beide Wiesen sich ueberschneiden, sonst false

        :param hauptwiese: andere Hauptwiese
        :return: True if Ueberschneidung sonst False
        """
        for koords in self.alle_teile:
            if koords in hauptwiese.alle_teile:
                if set(self.alle_teile[koords]).issubset(set(hauptwiese.alle_teile[koords])) or set(hauptwiese.alle_teile[koords]).issubset(set(self.alle_teile[koords])):
                    return True

        return False

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

