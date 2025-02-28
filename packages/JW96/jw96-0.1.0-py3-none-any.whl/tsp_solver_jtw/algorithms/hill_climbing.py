import random

from tsp_solver_jtw.utils import calculate_distance


def hill_climbing(cities, iterations=1000):
    current_route = list(range(len(cities)))
    random.shuffle(current_route)
    current_distance = calculate_distance(current_route, cities)

    for _ in range(iterations):
        new_route = current_route[:]
        i, j = random.sample(range(len(cities)), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        new_distance = calculate_distance(new_route, cities)
        if new_distance < current_distance:
            current_route, current_distance = new_route, new_distance

    return current_route, current_distance
