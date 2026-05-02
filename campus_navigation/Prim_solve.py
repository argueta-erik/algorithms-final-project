import heapq
import campus_navigation.Buildings as B
def prim_mst(start=None, names=False, trace=False):
    adj = B.buildings_list
    if start is None:
        start = 0
    
    visited = set()
    min_heap = []
    mst_edges = []
    total_weight = 0
    
    def add_edges_from(vertex):
        for neighbor, weight in adj[vertex]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (weight, vertex, neighbor))
                if trace:
                    print(f"  Pushed edge {vertex} -- {neighbor} weight = {weight}")
    if trace:
        print("\n[Prim Trace]")
        print("Starting Vertex:", start)
        
    visited.add(start)
    add_edges_from(start)
    
    while min_heap and len(visited) < B.Buildings.SRC:
        weight, u, v = heapq.heappop(min_heap)
        if trace:
            print(f"\nPopped edge {u} -- {v} weight={weight}")
            
        if v in visited:
            if trace:
                print("   Skipped (destination already visited")
            continue
        visited.add(v)
        if names:
            mst_edges.append((B.Buildings(u+1).name, B.Buildings(v+1).name, weight))
        else:
            mst_edges.append((u,v,weight))
        total_weight += weight
        
        if trace:
            print("  Accepted")
            print("  Visited Now:", visited)
        add_edges_from(v)
        
    is_connected = (len(visited) == B.Buildings.SRC)
    
    return mst_edges, total_weight, is_connected