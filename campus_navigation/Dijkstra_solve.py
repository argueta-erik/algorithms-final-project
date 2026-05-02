import heapq
import campus_navigation.Buildings as B
def solve_dijkstra(graph, source, goal):
    n = len(graph)
    dist = [float('inf')]*n
    dist[source-1] = 0
    pq = [(0, source-1)]
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        if current_dist > dist[u]:
            continue
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))
    return dist[goal-1]