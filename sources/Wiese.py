class WieseAufKarte:
    def __init__(self, ecken):
        self.ecken = ecken


class Wiese:
    def __init__(self, koordinates, ecken, meeples = False):
        self.wert = 0
        self.offene_teile = {koordinates: ecken}
        self.alle_teile = {koordinates: ecken}


