from collections import defaultdict
from parser import load_data, build_edges

def build_graph(edges):
    graph = defaultdict(list)
    for u, v, travel_time, depart, arrive, trip_id, route_id in edges:
        graph[u].append({
            'to': v,
            'travel_time': travel_time,
            'depart': depart,
            'arrive': arrive,
            'trip_id': trip_id,
            'route_id': route_id
        })
    return graph




def build_graph_static(edges):
    best = {}

    for u, v, travel_time, depart, arrive, trip_id, route_id in edges:
        key = (u, v, route_id)
        if key not in best or best[key]['travel_time'] > travel_time:
            best[key] = {
                'to': v,
                'travel_time': travel_time,
                'route_id': route_id
            }
    graph = defaultdict(list)
    for (u, v, route_id), data in best.items():
        graph[u].append(data)

    return graph




if __name__ == "__main__":
    stops, stop_times, trips = load_data()
    edges = build_edges(stop_times, trips)
    graph = build_graph(edges)

    print(f"Number of Nodes in graph: {len(graph)}")
    
    sample_stop = list(graph.keys())[0]
    print(f"Sample stop {sample_stop} has {len(graph[sample_stop])} outgoing connections:")
    for conn in graph[sample_stop][:3]:
        print(conn)


