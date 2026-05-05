from time import perf_counter
from collections import deque
from campus_navigation.Buildings import buildings_list as grid
import campus_navigation.Buildings as B
def solve_bfs(start, end, names=False):
    Q = deque()
    found = False
    visited_count = 0
    current = None
    #start counting time and search for path to end
    start_time = perf_counter()
    paths = {start:start}
    Q.append(start)
    while Q and not found:
        current = Q.popleft()
        visited_count += 1
        if current == end:
            found == True
            return gen_path(current, paths, start, names), visited_count, perf_counter()-start_time
        add_to_queue(grid, current, Q, paths)
    return None, visited_count, perf_counter()-start_time

#traces and returns path using the dictionary
def gen_path(current, paths, start, names):
    result = []
    if names:
        while not current == start:
            result.append(B.Buildings(current+1).name)
            current = paths[current]
        result.append(B.Buildings(start+1).name)
        return result
    while not current == start:
        result.append(current)
        current = paths[current]
    result.append(start)
    return result

#adds new coordinates to queue and defines them in the dictionary
def add_to_queue(grid, current, queue, paths):
    for building, x in grid[current]:
        if not building in paths:
            queue.append(building)
            paths[building] = current