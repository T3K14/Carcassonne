class Kloster():
    def __init__(self, koords, besitzer):
        self.counter = 1
        self.besitzer = besitzer
        self.fertig = False
        self.umgebungs_koordinaten = [(koords[0] - 1, koords[1] + 1), (koords[0], koords[1] + 1), (koords[0] + 1, koords[1] + 1),
                  (koords[0] + 1, koords[1]), (koords[0] + 1, koords[1] - 1), (koords[0], koords[1] - 1),
                  (koords[0] - 1, koords[1] - 1), (koords[0] - 1, koords[1])]

        # fuer mcts-spielkopie ww
        self.id = 'k'
        self.name = 1


    def calculate_if_fertig(self):
        if self.counter == 9:
            self.besitzer.punkte += 9

            # Punkte, die der Spieler mit Kloestern verdient hat updaten
            self.besitzer.kloster_points += 9

            self.besitzer.meeples += 1
            self.fertig = True

