class Player:

    def __init__(self, nr, art='human'):
        self.nummer = nr
        self.meeples = 7
        self.punkte = 0
        self.art = art

        self.meeples_per_kloster = 0
        self.meeples_per_ort = 0
        self.meeples_per_strasse = 0
        self.meeples_per_wiese = 0

        self.kloster_points = 0
        self.ort_points = 0
        self.strassen_points = 0
        self.wiesen_points = 0


