class Ort_auf_Karte:
    def __init__(self, name, kanten, wert):
        self.name = name
        self.kanten = kanten
        self.wert = wert


class Ort:
    def __init__(self, koordinaten, kanten, meeple = False):
        self.koordinaten_plus_oeffnungen = {koordinaten: kanten}
        self.wert = 2

    def add_part(self, ort_auf_karte, coordinates, kanten):
        """ nimmt ortsteil, koordinaten des neuen teils und wo dieses teil den aktuellen ort beruehrt"""

        # muss checken, ob dadurch noch ein anderer ort eingegliedert wird

        self.koordinaten_plus_oeffnungen.update({coordinates: kanten})

    def update_kanten(self, coordinates, kanten):
        #koordinates muessen die sein,
        self.koordinaten_plus_oeffnungen[coordinates].remove(kanten)
    #braucht folgende methoden: update: das bedeutet, dass der Ort mit seiner umgebung interagieren muss, ist ja kein problem, ich kann der method ja die nötigen listen übergeben
    #                             checken, wer sich in ihm befindet und ob er fertig ist, wer punkte bekommt