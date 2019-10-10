import unittest
import numpy as np
from card_class import Card as Karte


class CardTest(unittest.TestCase):
    def testGeneration(self):
        c = Karte("O", "W", "S", "S")
        #print(" HI")
        self.assertIsInstance(c, Karte)

    def test_matrix_creation(self):
        c = Karte("W", "O", "W", "O", "O")

        self.assertTrue((c.matrix == np.array([[1,0,0,0,0,0,1],
                            [1,0,0,0,0,0,1],
                            [1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1],
                            [1,0,0,0,0,0,1],
                            [1,0,0,0,0,0,1]])).all(), msg="{}".format(c.matrix))







if __name__ == "__main__":
    unittest.main()
