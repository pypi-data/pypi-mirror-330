# example_usage.py

from tsp_solver_jtw.utils import generate_random_cities
from tsp_solver_jtw.algorithms.random_search import random_search
from tsp_solver_jtw.algorithms.hill_climbing import hill_climbing
from tsp_solver_jtw.algorithms.simulated_annealing import simulated_annealing
from tsp_solver_jtw.algorithms.Asearch import a_star_search

if __name__ == "__main__":

    cities = [(0, 0), (2, 3), (5, 4), (6, 1), (8, 3), (1, 6)]

    print("Random Search:", random_search(cities, iterations=1000))
    print("Hill Climbing:", hill_climbing(cities))
    print("Simulated Annealing:", simulated_annealing(cities, temp=1000, cooling_rate=0.995))

    print('''Example Usage\n
    cities = [(0, 0), (2, 3), (5, 4), (6, 1), (8, 3), (1, 6)]\n

    print("Random Search:", random_search(cities, iterations=1000))\n
    print("Hill Climbing:", hill_climbing(cities))\n
    print("Simulated Annealing:", simulated_annealing(cities, temp=1000, cooling_rate=0.995))\n
    ''')
