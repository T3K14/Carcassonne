class Ort_auf_Karte:
    def __init__(self, kanten, name, wert=2):
        self.kanten = kanten
        self.wert = wert
        self.name = name


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
        self.fertig = self.check_if_fertig()
        if self.fertig:
            self.besitzer.punkte += self.wert
            self.besitzer.meeples += 1

    def add_global(self, global_ort, alle_orte):
        """ fuegt sich selbst die orte in dictionary bei und loescht diese aus alle orte"""

        self.koordinaten_plus_oeffnungen.update(global_ort.koordinaten_plus_oeffnungen)
        self.wert += global_ort.wert
        if self.besitzer is None:
            self.besitzer = global_ort.besitzer
        self.fertig = self.check_if_fertig()
        if self.fertig:
            self.besitzer.punkte += self.wert
            self.besitzer.meeples += 1
        alle_orte.remove(global_ort)

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
        a = hash(repr(self))
        return hash(repr(self))

