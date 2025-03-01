Objective
Create a Python library (tsp_solver) that implements various algorithms to solve the Traveling Salesperson Problem (TSP). The library should include the following algorithms:  One of the example is https://github.com/dmishin/tsp-solverLinks to an external site. 

Random Search
Hill Climbing
Simulated Annealing
A* search
Requirements
Name your github repositiory TSPsolver_firstcharofyourname_lastcharofyourname_anydigitwhichmake the name availble
Implement each algorithm as a separate module.
Provide a unified interface for solving TSP with different methods.
Ensure modular, well-documented, and optimized code.
Include unit tests for each algorithm.

Project Structure
        tsp_solver/
        │── __init__.py
        │── algorithms/
        │   ├── __init__.py
        │   ├── Asearch.py
        │   ├── random_search.py
        │   ├── hill_climbing.py
        │   ├── simulated_annealing.py
        │── utils.py
        │── example_usage.py
        │── tests/
        │   ├── test_Asearch.py
        │   ├── test_random_search.py
        │   ├── test_hill_climbing.py
        │   ├── test_simulated_annealing.py
        
 

Example Usage
        from tsp_solver.algorithms import bruteforce, random_search, hill_climbing, simulated_annealing
        
        cities = [(0, 0), (2, 3), (5, 4), (6, 1), (8, 3), (1, 6)]
        
        print("Random Search:", random_search.solve_tsp(cities, iterations=1000))
        print("Hill Climbing:", hill_climbing.solve_tsp(cities))
        print("Simulated Annealing:", simulated_annealing.solve_tsp(cities, temp=1000, cooling_rate=0.995))
        
Publish in Python
Use the tutorial https://www.serviceobjects.com/blog/step-by-step-guide-to-publishing-python-libraries-to-pypi/
I should be able to install your library in my colab using pip install
Deliverables
GitHub repository with structured code link
your library install name
