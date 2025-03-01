import unittest
from tsp_solver.algorithms import random_search

class TestRandomSearch(unittest.TestCase):
    def test_random_search(self):
        cities = [(0, 0), (2, 3), (5, 4), (6, 1), (8, 3), (1, 6)]
        route, distance = random_search.solve_tsp(cities, iterations=100)
        self.assertIsInstance(route, list)
        self.assertGreater(distance, 0)

if __name__ == '__main__':
    unittest.main()
