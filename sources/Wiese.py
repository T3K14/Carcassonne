class WieseAufKarte:
    def __init__(self, ecken, name):
        self.ecken = ecken
        self.name = name


class Wiese:
    def __init__(self, koordinates, ecken):
        self.wert = 0
        self.alle_teile = {koordinates: ecken}
        self.besitzer = None
        self.meeples = {}

    def add_part(self, koords, wiese_auf_karte):
        self.alle_teile.update({(koords[0], koords[1]): wiese_auf_karte.ecken})

    def add_global(self, global_wiese, alle_wiesen):
        self.alle_teile.update(global_wiese.alle_teile)

        for pl in global_wiese.meeples:
            if pl in self.meeples:
                self.meeples[pl] += global_wiese.meeples[pl]
            else:
                self.meeples.update({pl: global_wiese.meeples[pl]})

        if len(global_wiese.meeples) > 0:
            self.update_besitzer()

        alle_wiesen.remove(global_wiese)

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

