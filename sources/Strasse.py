class StasseAufKarte:
    def __init__(self, kanten, name):
        self.kanten = kanten
        self.wert = 1
        self.name = name

        # fuer mcts-spielkopie ww
        self.id = 's'


class Strasse:
    def __init__(self, koordinaten, kanten, wert=1):
        self.koordinaten_plus_oeffnungen = {koordinaten: kanten}
        self.wert = 1
        self.besitzer = None
        self.fertig = False
        self.name = None  # zum debuggen
        self.meeples = {}

    def update_kanten(self, koordinaten_kanten):
        """ nimmt liste mit koordinaten und kanten an, die an den koordinaten geloescht werden sollen"""

        #for kante in koordinaten_kanten[1]:
        #    self.koordinaten_plus_oeffnungen[koordinaten_kanten[0]].remove(kante)
        for koordinaten, kante in koordinaten_kanten:
            self.koordinaten_plus_oeffnungen[koordinaten].remove(kante)

    def add_part(self, koordinaten, strasse):
        """ nimmt ortsteil, koordinaten des neuen teils und wo dieses teil den aktuellen ort beruehrt"""

        self.koordinaten_plus_oeffnungen.update({(koordinaten[0], koordinaten[1]): strasse.kanten})
        self.wert += strasse.wert

    def add_global(self, global_strasse, alle_strassen):
        """ fuegt sich selbst die orte in dictionary bei und loescht diese aus alle orte"""

        self.koordinaten_plus_oeffnungen.update(global_strasse.koordinaten_plus_oeffnungen)
        self.wert += global_strasse.wert

        # update meeples:
        for pl in global_strasse.meeples:
            if pl in self.meeples:
                self.meeples[pl] += global_strasse.meeples[pl]
            else:
                self.meeples.update({pl: global_strasse.meeples[pl]})
        if len(global_strasse.meeples) > 0:
            self.update_besitzer()

        # den hinzugefuegten ort loeschen
        alle_strassen.remove(global_strasse)

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
        return hash(repr(self))


