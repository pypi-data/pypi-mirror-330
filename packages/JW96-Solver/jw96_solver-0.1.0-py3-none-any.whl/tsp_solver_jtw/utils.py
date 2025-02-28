# utils.py
import math
import random

def calculate_distance(route, cities):
    return sum(math.dist(cities[route[i]], cities[route[i + 1]]) for i in range(len(route) - 1)) + math.dist(cities[route[-1]], cities[route[0]])


def generate_random_cities(n, x_range=(0, 10), y_range=(0, 10)):
    return [(random.uniform(*x_range), random.uniform(*y_range)) for _ in range(n)]

