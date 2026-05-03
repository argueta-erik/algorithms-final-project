from time import perf_counter
import campus_navigation.Buildings as B
def solve_dfs(start, end, names=False):
    grid = B.buildings_list
    stack = []
    found = False
    visited_count = 0
    current = None
    #start counting time and search for path to end
    start_time = perf_counter()
    paths = {start:start}
    stack.append(start)
    while stack and not found:
        current = stack.pop()
        visited_count += 1
        if current == end:
            found == True
            return gen_path(current, paths, start, names), visited_count, perf_counter()-start_time
        add_to_queue(grid, current, stack, paths)
    return None, visited_count, perf_counter()-start_time

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
def add_to_queue(grid, current, queue, paths):
    for building, x in grid[current]:
        if not building in paths:
            queue.append(building)
            paths[building] = current