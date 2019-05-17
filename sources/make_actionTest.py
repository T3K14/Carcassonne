import Spiel_class
import card_class
import unittest

class MakeActionTest(unittest.TestCase):

    def test_1(self):
        spiel = Spiel_class.Spiel(card_class.Kartenliste)

        # alle_orte nach Zug
        goal = []
        # alle strassen nach Zug
        goal2 = []

        spiel.make_action(card_class.Card("O", "S", 'S', 'O', 'O'), (1, 0), 0, None)

        self.assertEqual(len(goal), len(spiel.alle_orte))
        self.assertEqual(len(goal2), len(spiel.alle_strassen))

        for o in spiel.alle_orte:
            self.assertTrue(o in goal)
        for s in spiel.alle_strassen:
            self.assertTrue(s in goal2)


if __name__ == '__main__':
    unittest.main()