from time import perf_counter
from collections import deque
import campus_navigation.Buildings as B
def solve_dfs(start, end, names=False):
    grid = B.buildings_list
    stack = deque()
    previous = deque()
    found = False
    visited_count = 0
    current = None
    #start counting time and search for path to end
    start_time = perf_counter()
    paths = {start:start}
    explore_order = []
    stack.append(start)
    previous.append(start)
    while stack and not found:
        
        current = stack.pop()
        explore_order.append((previous.pop(), current))
        visited_count += 1
        if current == end:
            found == True
            return gen_path(current, paths, start, names), visited_count, explore_order, perf_counter()-start_time
        add_to_stack(grid, current, stack, previous, paths)
    return None, visited_count, explore_order, perf_counter()-start_time

#traces and returns path using the dictionary
def gen_path(current, paths, start, names):
    result = []
    while not current == start:
        if names:
            result.append(B.Buildings(current+1).name)
        else:
            result.append(current)
        current = paths[current]
    result.append(start)
    return result

#adds new coordinates to queue and defines them in the dictionary
def add_to_stack(grid, current, stack, previous, paths):
    for building, x in grid[current]:
        if not building in paths:
            stack.append(building)
            print(B.Buildings(building+1).name)
            previous.append(current)
            paths[building] = current