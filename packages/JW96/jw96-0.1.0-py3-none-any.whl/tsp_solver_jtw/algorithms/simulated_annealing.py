# Simulated Annealing Algorithm
import math
import random

from tsp_solver_jtw.utils import calculate_distance


def simulated_annealing(cities, temp=1000, cooling_rate=0.995):
    current_route = list(range(len(cities)))
    random.shuffle(current_route)
    current_distance = calculate_distance(current_route, cities)

    while temp > 1:
        new_route = current_route[:]
        i, j = random.sample(range(len(cities)), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        new_distance = calculate_distance(new_route, cities)

        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temp):
            current_route, current_distance = new_route, new_distance
        temp *= cooling_rate

    return current_route, current_distance