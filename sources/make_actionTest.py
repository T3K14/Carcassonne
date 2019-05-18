import Spiel_class
import card_class
import Player_Class
import unittest
from Strasse import Strasse
from Ort import Ort

class MakeActionTest(unittest.TestCase):

    def test_1(self):
        spiel = Spiel_class.Spiel(card_class.Kartenliste)

        # alle_orte nach Zug
        goal = [spiel.alle_orte[0]]
        # alle strassen nach Zug
        goal2 = [spiel.alle_strassen[0], Strasse((1, 0), [1, 2])]

        k = card_class.Card("O", "S", 'S', 'O', 'O')
        spiel.make_action(k, (1, 0), 0, Player_Class.Player(1), None)

        self.assertEqual(len(spiel.alle_orte), len(goal))
        #self.assertEqual(len(goal2), len(spiel.alle_strassen))
        self.assertEqual(sorted(k.kanten), sorted({0: spiel.cards_set[(0, 0)].kanten[1], 1: k.kanten[1], 2: k.kanten[2], 3: spiel.cards_set[(0, 0)].kanten[1]}))

        for o in spiel.alle_orte:
            self.assertTrue(o in goal)
        for s in spiel.alle_strassen:
            self.assertTrue(s in goal2)


if __name__ == '__main__':
    unittest.main()