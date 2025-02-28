import heapq
import math



def a_star_search(cities):
    num_cities = len(cities)
    pq = [(0, [0])]
    best_distance = float('inf')
    best_route = []

    while pq:
        cost, path = heapq.heappop(pq)
        if len(path) == num_cities:
            total_cost = cost + math.dist(cities[path[-1]], cities[path[0]])
            if total_cost < best_distance:
                best_distance, best_route = total_cost, path
        else:
            for i in range(num_cities):
                if i not in path:
                    new_cost = cost + math.dist(cities[path[-1]], cities[i])
                    heapq.heappush(pq, (new_cost, path + [i]))

    return best_route, best_distance
