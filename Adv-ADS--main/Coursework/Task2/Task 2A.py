from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
from print_path import print_path

# Define the station names and map them to indices
station_names = ["A", "B", "C", "D", "E", "F"]  # A=0, B=1, C=2, D=3, E=4, F=5
station_to_index = {name: index for index, name in enumerate(station_names)}

# Array to define the edges: (start station, end station, number of stops)
# All edge weights are set to 1, representing one stop between each station.
edges = [
    ("A", "B", 1), ("A", "C", 1), ("B", "C", 1),
    ("B", "D", 1), ("C", "D", 1), ("D", "E", 1),
    ("D", "F", 1), ("E", "F", 1)
]

# Initialize the graph with 6 nodes
stations_graph = AdjacencyListGraph(len(station_names), directed=False, weighted=True)

# Insert edges from the array, using "1" as the weight for each edge (representing one stop)
for start, end, stops in edges:
    start_index = station_to_index[start]
    end_index = station_to_index[end]
    stations_graph.insert_edge(start_index, end_index, stops)

# Get user input for starting and destination station
starting_station = input("Enter the starting station (A, B, C, D, E, F): ").strip().upper()
destination_station = input("Enter the destination station (A, B, C, D, E, F): ").strip().upper()

# Station validation checker
if starting_station not in station_to_index or destination_station not in station_to_index:
    print("Invalid station. Please enter a valid station (A, B, C, D, E, F).")
else:
    # Get the indices for the source and destination stations
    starting_in = station_to_index[starting_station]
    destination_in = station_to_index[destination_station]

    # Use Dijkstra's Algorithm to find the shortest route (in terms of stops)
    stops, predecessors = dijkstra(stations_graph, starting_in)

    # Prints the shortest path and the number of stops using the print_path function
    if stops[destination_in] == float('inf'):
        print(f"No path from {starting_station} to {destination_station}.")
    else:
        # Call print_path function to display the route (converts station indices to names)
        path = print_path(predecessors, starting_in, destination_in, lambda x: station_names[x])
        print(f"Shortest path from {starting_station} to {destination_station}: {' -> '.join(path)}")
        print(f"Number of Stops: {stops[destination_in]}")
