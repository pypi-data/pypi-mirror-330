import unittest
from tsp_solver.algorithms import hill_climbing

print(hill_climbing)

class TestHillClimbing(unittest.TestCase):
    def test_hill_climbing(self):
        cities = [(0, 0), (2, 3), (5, 4), (6, 1), (8, 3), (1, 6)]
        route, distance = hill_climbing.solve_tsp(cities)
        self.assertIsInstance(route, list)
        self.assertGreater(distance, 0)

if __name__ == '__main__':
    unittest.main()
