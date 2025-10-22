from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
from print_path import print_path

# Define the station names and map them to indices
station_names = ["A", "B", "C", "D", "E", "F"]  # A=0, B=1, C=2, D=3, E=4, F=5
station_to_index = {}

for index, name in enumerate(station_names):
    station_to_index[name] = index
# Array to define the edges: (start station, end station, duration)
edges = [
    ("A", "B", 5), ("A", "C", 8), ("B", "C", 10),
    ("B", "D", 6), ("C", "D", 7), ("D", "E", 3),
    ("D", "F", 9), ("E", "F", 2)
]

# Initialize the graph with n nodes (n being the size of the network/vertices)
stations_graph = AdjacencyListGraph(len(station_names), directed=False, weighted=True)

# Insert edges from the array into an adjacency list graph
for start, end, duration in edges:
    start_index = station_to_index[start]
    end_index = station_to_index[end]
    stations_graph.insert_edge(start_index, end_index, duration)

# Get user input for starting and destination station in upper/lowercase removing space
starting_station = input("Enter the starting station (A, B, C, D, E, F): ").strip().upper()
destination_station = input("Enter the destination station (A, B, C, D, E, F): ").strip().upper()

# Checks if the station is valid, one of the options
if starting_station not in station_to_index or destination_station not in station_to_index:
    print("Invalid station. Please enter a valid station (A, B, C, D, E, F).")
else:
    # Get the indices for the source and destination stations
    starting_in = station_to_index[starting_station]
    destination_in = station_to_index[destination_station]

    # Utilize Dijkstra's Algorithm to find the shortest route from starting index(station)
    duration, predecessors = dijkstra(stations_graph, starting_in)

    if duration[destination_in] == float('inf'):
        print(f"No path from {starting_station} to {destination_station}.")
    else:
        # Call print_path function to display the route (converts station indices to names)
        path = print_path(predecessors, starting_in, destination_in, lambda x: station_names[x])
        print(f"Shortest path from {starting_station} to {destination_station}: {' -> '.join(path)}")
        print(f"Duration of Journey: {duration[destination_in]} minutes")
