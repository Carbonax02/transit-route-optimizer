import heapq
from collections import deque



def dijkstra(graph, source, target):
    counter = 0
    pq = []
    heapq.heappush(pq, (0, counter, source, [(source, None)]))
    visited = set()

    while pq:
        cost, _, current, path = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == target:
            return cost, path

        for edge in graph[current]:
            neighbor = edge['to']
            if neighbor not in visited:
                new_cost = cost + edge['travel_time']
                counter += 1
                new_path = path + [(neighbor, edge['route_id'])]
                heapq.heappush(pq, (new_cost, counter, neighbor, new_path))

    return None, []
# This bfs is for minimizing the number of stops, not the travel time. 
# It can be used to find a path with the least number of stops between two points in the graph.
def bfs(graph, source, target):
    queue = deque()
    queue.append((source, [(source, None)]))
    visited = set()
    visited.add(source)

    while queue:
        current, path = queue.popleft()

        if current == target:
            return len(path) - 1, path

        for edge in graph[current]:
            neighbor = edge['to']
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [(neighbor, edge['route_id'])]))

    return None, []

# This dijkstra is for minimizing the number of transfers, not the travel time.
def dijkstra_fewest_transfers(graph, source, target, transfer_penalty=900):
    counter = 0
    pq = []
    heapq.heappush(pq, (0, counter, source, [(source, None)], None))
    visited = set()

    while pq:
        cost, _, current, path, current_route = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == target:
            return cost, path

        for edge in graph[current]:
            neighbor = edge['to']
            if neighbor not in visited:
                new_cost = cost + edge['travel_time']
                if current_route is not None and edge['route_id'] != current_route:
                    new_cost += transfer_penalty
                counter += 1
                new_path = path + [(neighbor, edge['route_id'])]
                heapq.heappush(pq, (new_cost, counter, neighbor, new_path, edge['route_id']))

    return None, []



if __name__ == '__main__':
    from parser import load_data, build_edges
    from graph import build_graph_static
    from collections import defaultdict

    stops, stop_times, trips = load_data()
    edges = build_edges(stop_times, trips)
    graph = build_graph_static(edges)

    source = 21629
    target = 20639

    cost, path = dijkstra(graph, source, target)

    if path:
        stop_lookup = stops.set_index('stop_id')['stop_name']
        
        print(f"\nFrom: {stop_lookup[source]}")
        print(f"To:   {stop_lookup[target]}")
        print(f"Total travel time: {cost // 60} mins {cost % 60} secs")
        print(f"Total stops: {len(path)}")
        print(f"\n{'='*50}")
        print("Route:")
        for i, stop_id in enumerate(path):
            name = stop_lookup.get(stop_id, 'Unknown')
            if i == 0:
                print(f"  START → {name}")
            elif i == len(path) - 1:
                print(f"  END   → {name}")
            else:
                print(f"  {i:2}.    {name}")
    else:
        print("No path found")