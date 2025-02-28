import math
import random

from tsp_solver_jtw.utils import calculate_distance


def random_search(cities, iterations=1000):
    best_route = None
    best_distance = float('inf')
    for _ in range(iterations):
        route = list(range(len(cities)))
        random.shuffle(route)
        distance = calculate_distance(route, cities)
        if distance < best_distance:
            best_route, best_distance = route, distance
    return best_route, best_distance