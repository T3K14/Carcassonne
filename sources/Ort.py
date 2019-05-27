class Ort_auf_Karte:
    def __init__(self, kanten, name, wert=2):
        self.kanten = kanten
        self.wert = wert
        self.name = name


class Ort:
    def __init__(self, koordinaten, kanten, wert=2):
        self.koordinaten_plus_oeffnungen = {koordinaten: kanten}
        self.wert = wert
        self.besitzer = None
        self.fertig = False
        self.name = None # zum debuggen
        self.meeples = {}

    def update_kanten(self, koordinaten_kanten):
        """ nimmt liste mit koordinaten und kanten an, die an den koordinaten geloescht werden sollen"""

        #for kante in koordinaten_kanten[1]:
        #    self.koordinaten_plus_oeffnungen[koordinaten_kanten[0]].remove(kante)
        for koordinaten, kante in koordinaten_kanten:
            self.koordinaten_plus_oeffnungen[koordinaten].remove(kante)

    def add_part(self, koordinaten, ort):
        """ nimmt ortsteil, koordinaten des neuen teils und wo dieses teil den aktuellen ort beruehrt"""

        self.koordinaten_plus_oeffnungen.update({(koordinaten[0], koordinaten[1]): ort.kanten})
        self.wert += ort.wert

    def add_global(self, global_ort, alle_orte):
        """ fuegt sich selbst die orte in dictionary bei und loescht diese aus alle orte"""

        self.koordinaten_plus_oeffnungen.update(global_ort.koordinaten_plus_oeffnungen)
        self.wert += global_ort.wert

        # update meeples:
        for pl in global_ort.meeples:
            if pl in self.meeples:
                self.meeples[pl] += global_ort.meeples[pl]
            else:
                self.meeples.update({pl: global_ort.meeples[pl]})
        if len(global_ort.meeples) > 0:
            self.update_besitzer()

        # den hinzugefuegten ort loeschen
        alle_orte.remove(global_ort)

    def check_if_fertig(self):
        t = True
        for koordinaten in self.koordinaten_plus_oeffnungen:
            # wenn es an den koords noch offene kanten gibt
            if self.koordinaten_plus_oeffnungen[koordinaten]:
                t = False
        self.fertig = t

    def update_meeples(self, player):
        """ nimmt player an, welcher ein meeple auf diese landschaft setzt"""

        # wenn dieser spieler schon meeple in ort hat
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

    def evaluate(self):
        """um nachdem geupdated wurde, ob die landschaft fertig ist, falls dem so ist alles richtig aufzuloesen"""
        if self.fertig:

            # Punktevergabe

            # wenn es einen eindeutigen Besitzer gibt
            if self.besitzer is not None:
                self.besitzer.punkte += self.wert
            elif len(self.meeples) > 0:
                for pl in self.meeples:
                    pl.punkte += self.wert

            # Meeplerueckgabe
            for pl in self.meeples:
                pl.meeples += self.meeples[pl]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        a = hash(repr(self))
        return hash(repr(self))

