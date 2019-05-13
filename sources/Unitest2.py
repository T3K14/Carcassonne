import unittest
import numpy as np

import rotate2
from card_class import Card

class RoatationTest(unittest.TestCase):

    def test_rotate_infos_right(self):
        self.assertEqual(rotate2.rotate_info_right(["O", "S", "S", "W"]), ["W", "O", "S", "S"])

    def test_rotate_lists_right(self):
        self.assertEqual(rotate2.rotate_list_right([1, 2]), [2, 3])

    def test_rotate_matrix_right(self):
        k = Card("W", "O", "W", "O", "O")
        k.rotate_right()

        self.assertTrue((k.matrix == np.array([[1, 1, 1, 1, 1, 1, 1],
                                               [0, 0, 1, 1, 1, 0, 0],
                                               [0, 0, 1, 1, 1, 0, 0],
                                               [0, 0, 1, 1, 1, 0, 0],
                                               [0, 0, 1, 1, 1, 0, 0],
                                               [0, 0, 1, 1, 1, 0, 0],
                                               [1, 1, 1, 1, 1, 1, 1]])).all(), msg="{}".format(k.matrix))
        k.rotate_right()
        self.assertTrue((k.matrix == np.array([[1, 0, 0, 0, 0, 0, 1],
                                               [1, 0, 0, 0, 0, 0, 1],
                                               [1, 1, 1, 1, 1, 1, 1],
                                               [1, 1, 1, 1, 1, 1, 1],
                                               [1, 1, 1, 1, 1, 1, 1],
                                               [1, 0, 0, 0, 0, 0, 1],
                                               [1, 0, 0, 0, 0, 0, 1]])).all(), msg="{}".format(k.matrix))


if __name__ == "__main__":
    unittest.main()