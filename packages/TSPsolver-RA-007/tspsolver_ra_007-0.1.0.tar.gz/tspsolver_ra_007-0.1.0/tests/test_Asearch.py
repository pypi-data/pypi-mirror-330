import unittest
from tsp_solver.algorithms import Asearch

class TestAStarSearch(unittest.TestCase):
    def test_Asearch(self):
        cities = [(0, 0), (2, 3), (5, 4), (6, 1), (8, 3), (1, 6)]
        route, distance = Asearch.solve_tsp(cities)
        self.assertIsInstance(route, tuple)
        self.assertGreater(distance, 0)

if __name__ == '__main__':
    unittest.main()
