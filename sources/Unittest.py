import unittest
from KarteMod import Karte


class CardTest(unittest.TestCase):
    def testGeneration(self):
        c = Karte("O", "W", "S", "S")
        #print(" HI")
        self.assertIsInstance(c, Karte)







if __name__ == "__main__":
    unittest.main()
