class WieseAufKarte:
    def __init__(self, ecken):
        self.ecken = ecken


class Wiese:
    def __init__(self, koordinates, ecken):
        self.wert = 0
        self.alle_teile = {koordinates: ecken}
        self.besitzer = None

    def add_part(self, koords, wiese_auf_karte):
        self.alle_teile.update({(koords[0], koords[1]): wiese_auf_karte.ecken})

    def add_global(self, global_wiese, alle_wiesen):
        self.alle_teile.update(global_wiese.alle_teile)

        if self.besitzer is None:
            self.besitzer = global_wiese.besitzer
        alle_wiesen.remove(global_wiese)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        a = hash(repr(self))
        return hash(repr(self))

