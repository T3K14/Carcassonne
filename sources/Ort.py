class Ort_auf_Karte:
    def __init__(self, kanten, wert=2):
        self.kanten = kanten
        self.wert = wert


class Ort:
    def __init__(self, koordinaten, kanten, meeple = False, wert=2):
        self.koordinaten_plus_oeffnungen = {koordinaten: kanten}
        self.wert = wert
        self.besitzer = None
        self.fertig = False
        self.name = None # zum debuggen

    def update_kanten(self, koordinaten_kanten):
        """ nimmt liste mit koordinaten und kanten an, die an den koordinaten geloescht werden sollen"""

        for kante in koordinaten_kanten[1]:
            self.koordinaten_plus_oeffnungen[koordinaten_kanten[0]].remove(kante)

    def add_part(self, koordinaten, ort):
        """ nimmt ortsteil, koordinaten des neuen teils und wo dieses teil den aktuellen ort beruehrt"""

        self.koordinaten_plus_oeffnungen.update({(koordinaten[0], koordinaten[1]): ort.kanten})
        self.wert += ort.wert

    def add_orte(self, dictionary, alle_orte):
        """ fuegt sich selbst die orte in dictionary bei und loescht diese aus alle orte"""

        for ort in dictionary:
            self.koordinaten_plus_oeffnungen.update(alle_orte[ort].koordinaten_plus_oeffnungen)
            del alle_orte[ort]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(repr(self))

