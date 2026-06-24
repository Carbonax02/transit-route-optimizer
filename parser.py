import pandas as pd

def load_data():
    stops = pd.read_csv('data/stops.txt')
    stop_times = pd.read_csv('data/stop_times.txt') 
    trips = pd.read_csv('data/trips.txt')
    routes = pd.read_csv('data/routes.txt')
    return stops, stop_times, trips, routes

def parse_time(t):
    h,m,s = map(int, t.split(':'))
    return h * 3600 + m * 60 + s

def build_edges(stop_times, trips):
    stop_times = stop_times.merge(trips[['trip_id', 'route_id']], on='trip_id')

    stop_times['arr_sec'] = stop_times['arrival_time'].apply(parse_time)
    stop_times['dep_sec'] = stop_times['departure_time'].apply(parse_time)

    stop_times = stop_times.sort_values(by=['trip_id', 'stop_sequence'])

    edges = []
    for trip_id, group in stop_times.groupby('trip_id'):
        group = group.reset_index(drop=True)
        for i in range(len(group) - 1):
            u = group.loc[i, 'stop_id']
            v = group.loc[i+1, 'stop_id']
            depart = group.loc[i, 'dep_sec']
            arrive = group.loc[i+1, 'arr_sec']
            route = group.loc[i, 'route_id']
            travel_time = arrive - depart
            edges.append((u, v, travel_time, depart, arrive, trip_id, route))
    
    return edges

if __name__ == "__main__":
    stops, stop_times, trips = load_data()
    print("Building edges...")
    edges = build_edges(stop_times, trips)
    print(f"Number of edges: {len(edges)}")
    print("Sample edge:", edges[0])
    