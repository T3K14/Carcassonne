import unittest

import rotate2

class RoatationTest(unittest.TestCase):

    def test_rotate_card_right(self):
        self.assertEqual(rotate2.rotate_card_right(["O", "S", "S", "W"]), ["W", "O", "S", "S"])

if __name__ == "__main__":
    unittest.main()