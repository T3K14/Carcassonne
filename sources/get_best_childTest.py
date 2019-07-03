from mcts2 import Node
from mcts_parallelized import get_best_child
import unittest


class get_best_childTest(unittest.TestCase):

    def test1(self):
        nodes1 = [Node(i, i) for i in range(20)]
        for i in range(20):
            nodes1[i].visits = i

        nodes2 = [Node(i, i) for i in range(20)]
        for i, j in enumerate(range(0, 40, 2)):
            nodes2[i].visits = j

        root1 = Node('root', 'root')
        root1.children = nodes1

        root2 = Node('root', 'root')
        root2.children = nodes2

        self.assertEqual(19, get_best_child((root1, root2)).status)

    def test2(self):
        nodes1 = [Node(i, i) for i in range(20)]
        for i in range(20):
            nodes1[i].visits = i

        nodes2 = [Node(i, i) for i in range(20)]
        for i, j in enumerate(range(0, 40, 2)):
            nodes2[i].visits = j

        root1 = Node('root', 'root')
        root1.children = nodes1

        root2 = Node('root', 'root')
        root2.children = nodes2

        root1.children[14].visits = 100

        self.assertEqual(14, get_best_child((root1, root2)).status)


if __name__ == '__main__':
    unittest.main()
