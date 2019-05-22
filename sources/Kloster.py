class Kloster():
    def __init__(self, koords, besitzer, cards_set):
        self.counter = 1
        self.besitzer = besitzer
        self.fertig = False
        self.umgebungs_koordinaten = [(koords[0] - 1, koords[1] + 1), (koords[0], koords[1] + 1), (koords[0] + 1, koords[1] + 1),
                  (koords[0] + 1, koords[1]), (koords[0] + 1, koords[1] - 1), (koords[0], koords[1] - 1),
                  (koords[0] - 1, koords[1] - 1), (koords[0] - 1, koords[1])]

        for k in self.umgebungs_koordinaten:
            if k in cards_set:
                self.counter += 1
        self.check_if_fertig()

    def check_if_fertig(self):
        if self.counter == 9:
            self.besitzer.punkte += 9
            self.besitzer.meeples += 1
            self.fertig = True
