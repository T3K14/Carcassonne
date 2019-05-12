import unittest

import rotate2

class RoatationTest(unittest.TestCase):

    def test_rotate_infos_right(self):
        self.assertEqual(rotate2.rotate_info_right(["O", "S", "S", "W"]), ["W", "O", "S", "S"])

    def test_rotate_lists_right(self):
        self.assertEqual(rotate2.rotate_lists_right([1, 2]), [2, 3])



if __name__ == "__main__":
    unittest.main()