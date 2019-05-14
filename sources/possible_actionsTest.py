import unittest
from KarteMod import Karte
from Rotate import Rotate

def calculate_possible_actions(card, possible_coordinates, cards_set):
        """checkt, ob und wie karte an jede freie stelle gelegt werden kann,
            returned liste mit tupel bestehend aus moeglicher anlegestelle und anzahl von rotationen die dafür noetig sind
            nimmt eine Karte an, sowie liste möglicher anlegestellen und dictionary von gelegten Karten
            """

        possible_actions = []

        # ich will hier nicht wirklich was an der Karte rotieren, nur um zu schauen, wo was passt
        info = card.info[:]

        d = {0: 2, 1: 3, 2: 0, 3: 1}

        for x, y in possible_coordinates:

            # zuerst alle nachbarkarten finden und speichern wo sie relatativ zu eigener Karte liegen
            # das sollte woanders gemacht werden, da man sonst fuer jede neu gezogene Karte immer wieder die umgebung
            # untersucht, obwohl man das schon x mal davor gemacht hat
            nachbar_koordinaten = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
            nachbar_karten = []

            for relative_pos, nkoo in enumerate(nachbar_koordinaten):
                for koord_von_karte in cards_set:
                    if koord_von_karte == nkoo:
                        nachbar_karten.append((relative_pos, cards_set[koord_von_karte].info[d[relative_pos]]))

                        # nicht 100 pro sicher, aber da dann schon karte an nkoo gefunden wurde, kann da ja keine weitere mehr sein
                        continue

            for i in range(4):

                # wenn pro Rotation nach allen Ueberpruefungen immer noch True, dann hinzufuegen
                b = True
                for n in nachbar_karten:
                    if b:
                        b = b and info[n[0]] == n[1]
                    else:
                        break

                if b:
                    possible_actions.append((x, y, i))

                # eins weiter rotieren
                info = Rotate.rotate_card_right(info)

        # jetzt Meeples
        #if player.meeples > 0:
        #    pass

        return possible_actions

class possible_actionsTest(unittest.TestCase):


    def test_1(self):
        cards_set = {(0, 0): Karte("S", "O", "S", "W"), (1, 1): Karte("W", "O", "O", "W","O")}
        possible_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 2), (2, 1)]

        k = Karte("S", "O", "O", "S", "O")

        goal = [(0, -1, 0), (0, -1, 1), (2, 1, 1), (2, 1, 2), (1, 0, 2)]
        # self.assertEqual(calculate_possible_actions(Karte("S", "O", "O", "S", "O"), possible_coordinates, cards_set), [(0, -1, 0), (0, -1, 1), (2, 1, 1), (2, 1, 2), (1, 0, 2)])
        self.assertEqual(len(goal), len(calculate_possible_actions(k, possible_coordinates, cards_set)))
        for a in calculate_possible_actions(Karte("S", "O", "O", "S", "O"), possible_coordinates, cards_set):
            self.assertIn(a, goal)



if __name__ == "__main__":
    unittest.main()
