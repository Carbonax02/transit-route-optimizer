# Bangalore Transit Route Optimizer

A city-scale transit routing engine built on live BMTC (Bangalore Metropolitan Transport Corporation) GTFS data, covering 9,600+ stops and 1.4M+ edges across Bangalore's bus network.

## What it does

Given a source and destination bus stop, the router finds the optimal route across Bangalore's bus network using three different optimization strategies:

- **Fastest route** — minimizes total travel time (Dijkstra)
- **Fewest stops** — minimizes number of stops visited (BFS)
- **Fewest transfers** — minimizes bus changes with a configurable transfer penalty (transfer-penalized Dijkstra)

Output includes stop-by-stop directions with transfer points and boarding route clearly marked.

## Project Structure

```
├── data/                  # Raw BMTC GTFS files
│   ├── stops.txt          # All bus stops with coordinates
│   ├── routes.txt         # Bus route definitions
│   ├── trips.txt          # Individual scheduled runs per route
│   ├── stop_times.txt     # Arrival/departure times at each stop per trip
│   ├── calendar.txt       # Service schedules by day
│   ├── shapes.txt         # GPS path geometry per route
│   ├── fare_attributes.txt
│   ├── fare_rules.txt
│   └── feed_info.txt
├── parser.py              # Loads and parses GTFS files, builds edge list
├── graph.py               # Constructs adjacency list from edge list
├── algorithms.py          # Dijkstra, BFS, transfer-penalized Dijkstra
└── main.py                # Interactive CLI
```

## How it works

### Data pipeline
Raw GTFS files are parsed and joined across `stop_times.txt`, `trips.txt`, and `routes.txt` to extract 1.5M stop-time entries. These are collapsed into a per-route adjacency list where each edge stores travel time, departure/arrival time, and route ID.

### Graph
- **Nodes** — 9,600+ bus stops
- **Edges** — directed connections between consecutive stops on the same route, weighted by travel time in seconds
- **Graph type** — directed weighted graph (one edge per route per stop pair)

### Algorithms
| Mode | Algorithm | Optimizes |
|------|-----------|-----------|
| Fastest route | Dijkstra | Total travel time |
| Fewest stops | BFS | Number of stops |
| Fewest transfers | Dijkstra + transfer penalty | Route changes (900s penalty per transfer) |

## Setup

### Requirements
```
pip install pandas
```

### Data
Download BMTC GTFS data from [Transitfeeds](https://transitfeeds.com/p/bmtc/1089) and place the extracted files inside the `data/` folder.

### Run
```
python main.py
```

## Example output

```
Enter source stop name: majestic
Enter destination stop name: electronic city

Optimization mode:
  1. Fastest route
  2. Fewest stops
  3. Fewest transfers
Select mode (1/2/3): 1

==================================================
Total travel time: 38 mins 47 secs
Total stops: 37
==================================================

  START → Kempegowda Bus Station(Majestic/KBS)
   1.    Ananda Rao Circle
   ...
  ** TRANSFER — Board route KBS-3A **
   ...
  END   → Electronic City Wipro Main Gate
```

## Dataset
- **Source** — BMTC GTFS open data via Transitfeeds
- **Stops** — 9,682
- **Trips** — 55,930
- **Stop-time entries** — 1,505,517
- **Graph edges** — 1,449,587
