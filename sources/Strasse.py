class StasseAufKarte:
    def __init__(self, kanten):
        self.kanten = kanten
        self.wert = 1

class Strasse():
    def __init__(self, koordinaten, kanten, meeple = False):
        self.koordinaten_plus_oeffnungen = {koordinaten: kanten}
        self.wert = 1
        self.besitzer = None
        self.fertig = False
        self.name = None  # zum debuggen

    def update_kanten(self, koordinaten_kanten):
        """ nimmt liste mit koordinaten und kanten an, die an den koordinaten geloescht werden sollen"""

        for kante in koordinaten_kanten[1]:
            self.koordinaten_plus_oeffnungen[koordinaten_kanten[0]].remove(kante)

    def add_part(self, koordinaten, strasse):
        """ nimmt ortsteil, koordinaten des neuen teils und wo dieses teil den aktuellen ort beruehrt"""

        self.koordinaten_plus_oeffnungen.update({(koordinaten[0], koordinaten[1]): strasse.kanten})
        self.wert += strasse.wert

    def add_global(self, global_strasse, alle_strassen):
        """ fuegt sich selbst die orte in dictionary bei und loescht diese aus alle orte"""

        self.koordinaten_plus_oeffnungen.update(global_strasse.koordinaten_plus_oeffnungen)
        self.wert += global_strasse.wert

        if self.besitzer is None:
            self.besitzer = global_strasse.besitzer

        self.fertig = self.check_if_fertig()
        if self.fertig:
            self.besitzer.punkt += self.wert
            self.besitzer.meeples += 1
        alle_strassen.remove(global_strasse)

    def check_if_fertig(self):
        t = True
        for koordinaten in self.koordinaten_plus_oeffnungen:
            # wenn es an den koords noch offene kanten gibt
            if self.koordinaten_plus_oeffnungen[koordinaten]:
                t = False
        return t

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(repr(self))


