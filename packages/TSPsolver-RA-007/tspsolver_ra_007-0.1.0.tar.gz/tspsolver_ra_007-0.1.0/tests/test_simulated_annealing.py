import unittest
from tsp_solver.algorithms import simulated_annealing

class TestSimulatedAnnealing(unittest.TestCase):
    def test_simulated_annealing(self):
        cities = [(0, 0), (2, 3), (5, 4), (6, 1), (8, 3), (1, 6)]
        route, distance = simulated_annealing.solve_tsp(cities, temp=1000, cooling_rate=0.995)
        self.assertIsInstance(route, list)
        self.assertGreater(distance, 0)

if __name__ == '__main__':
    unittest.main()
