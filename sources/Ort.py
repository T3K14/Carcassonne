class Ort_auf_Karte:
    def __init__(self, name, kanten, wert):
        self.name = name
        self.kanten = kanten
        self.wert = wert


class Ort:
    def __init__(self, koordinaten, kanten, meeple = False):
        self.koordinaten_plus_oeffnungen = {koordinaten: kanten}
        self.wert = 2

    def add_part(self,ort, x, y):
        """ nimmt ortsteil, koordinaten des neuen teils und wo dieses teil den aktuellen ort beruehrt"""

        # muss checken, ob dadurch noch ein anderer ort eingegliedert wird

        self.koordinaten_plus_oeffnungen.update({(x, y): ort.kanten})
        self.wert += ort.wert

    def update_kanten(self, liste):
        """ nimmt liste mit koordinaten und kanten an, die an den koordinaten geloescht werden sollen"""

        for coordinates, kante in liste:

            self.koordinaten_plus_oeffnungen[coordinates].remove(kante)

    def add_orte(self, dictionary, alle_orte):
        """ fuegt sich selbst die orte in dictionary bei und loescht diese aus alle orte"""

        for ort in dictionary:
            self.koordinaten_plus_oeffnungen.update(alle_orte[ort].koordinaten_plus_oeffnungen)
            del alle_orte[ort]