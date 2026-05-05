import heapq
import campus_navigation.Buildings as B
def solve_dijkstra(source, goal):
    graph = B.buildings_list
    n = len(graph)
    dist = [float('inf')]*n
    dist[source] = 0
    pq = [(0, source)]
    path = {}
    out_path = []
    while pq:
        current_dist, u = heapq.heappop(pq)
        if current_dist > dist[u]:
            continue
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                path[v] = u
                heapq.heappush(pq, (dist[v], v))
    i = goal
    while not i == source:
        out_path.append(i)
        i = path[i]
    out_path.append(source)
    return dist[goal], out_path