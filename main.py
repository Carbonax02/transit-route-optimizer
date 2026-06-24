from parser import load_data, build_edges
from graph import build_graph_static
from algorithms import dijkstra, bfs, dijkstra_fewest_transfers

def search_stop(stops, query):
    query = query.lower().strip()
    matches = stops[stops['stop_name'].str.lower().str.contains(query)]
    return matches[['stop_id', 'stop_name', 'stop_lat', 'stop_lon']]

def pick_stop(stops, prompt):
    while True:
        query = input(prompt)
        matches = search_stop(stops, query)
        
        if matches.empty:
            print("  No stops found. Try a different name.\n")
            continue
        
        print("\n  Matches found:")
        for i, row in enumerate(matches.itertuples()):
            print(f"  {i+1}. {row.stop_name} (ID: {row.stop_id})")
        
        choice = input("\n  Enter number to select: ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(matches):
            print("  Invalid choice.\n")
            continue
        
        selected = matches.iloc[int(choice) - 1]
        print(f"  Selected: {selected['stop_name']}\n")
        return selected['stop_id']

def print_route(path, cost, stops, routes):
    stop_lookup = stops.set_index('stop_id')['stop_name']
    route_lookup = routes.set_index('route_id')['route_short_name']

    print(f"\n{'='*50}")

    if cost is None:
        print(f"Total stops: {len(path)} (fewest stops mode — time not calculated)")
    else:
        print(f"Total travel time: {cost // 60} mins {cost % 60} secs")
        print(f"Total stops: {len(path)}")

    print(f"{'='*50}\n")

    current_route = None
    for i, (stop_id, route_id) in enumerate(path):
        name = stop_lookup.get(stop_id, 'Unknown')

        if i == 0:
            print(f"  START → {name}")
            continue

        # route change = transfer
        if route_id != current_route and current_route is not None:
            route_name = route_lookup.get(route_id, str(route_id))
            print(f"\n  ** TRANSFER — Board route {route_name} **\n")

        if i == len(path) - 1:
            print(f"  END   → {name}")
        else:
            print(f"  {i:2}.    {name}")

        current_route = route_id


if __name__ == '__main__':
    print("Loading data...")
    stops, stop_times, trips, routes = load_data()
    edges = build_edges(stop_times, trips)
    graph = build_graph_static(edges)
    print("Ready.\n")


    while True:
        print("="*50)
        source = pick_stop(stops, "Enter source stop name: ")
        target = pick_stop(stops, "Enter destination stop name: ")


        print("\nOptimization mode:")
        print("  1. Fastest route")
        print("  2. Fewest stops")
        print("  3. Fewest transfers")
        mode = input("Select mode (1/2/3): ").strip()

        print("Finding route...")

        if mode == '1':
            cost, path = dijkstra(graph, source, target)
        elif mode == '2':
            cost, path = bfs(graph, source, target)
            # calculate actual travel time separately for display
            cost = None
        elif mode == '3':
            cost, path = dijkstra_fewest_transfers(graph, source, target)
        else:
            print("Invalid mode, using fastest route")
            cost, path = dijkstra(graph, source, target)

        if path:
            print_route(path, cost, stops, routes)
        else:
            print("No route found between these stops.")

        again = input("\n\nSearch again? (y/n): ").strip().lower()
        if again != 'y':
            break