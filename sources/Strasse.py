class StasseAufKarte:
    def __init__(self, kanten):
        self.kanten = kanten
        self.wert = 1

class Strasse():
    def __init__(self, koordinaten, kanten, meeple = False):
        self.koordinaten_plus_oeffnungen = {koordinaten: kanten}
        self.wert = 1

