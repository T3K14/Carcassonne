import multiprocessing
import time
from functools import reduce


def calculate_tree_from_startnode(x):
    print('starting tree calculation')
    time.sleep(1)
    print('t_end erreicht')
    return 1

def add_two_trees(node1, node2):
    return 1


start = time.time()

x = 1
trees = [calculate_tree_from_startnode(x) for i in range(10)]

end = time.time()

print(f'This took {end - start:.2f} seconds.')

start = time.time()
pool = multiprocessing.Pool()
trees = pool.map(calculate_tree_from_startnode, [x for i in range(10)])

end = time.time()
print(f'This took {end - start:.2f} seconds.')

reduce(add_two_trees, trees)

print(map.__doc__)
