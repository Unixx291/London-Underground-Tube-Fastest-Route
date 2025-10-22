import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
from print_path import print_path


def load_data(file):  # Loads the data from the Excel file, labeling the columns and clearing empty rows
    underground_data = pd.read_excel(file, sheet_name='Sheet1')
    underground_data.columns = ["Line", "Start", "Destination", "Duration"]
    underground_data = underground_data.dropna(subset=["Duration", "Start", "Destination"])
    return underground_data.drop_duplicates(subset=["Start", "Destination"])


def build_graph(underground_data):  # Build the graph using unique stations and set edge weights to 1 for counting stops
    stations = pd.concat([underground_data["Start"], underground_data["Destination"]]).unique()
    station_index = {}
    num_stations = len(stations)
    for index, station in enumerate(stations):
        station_index[station] = index

    graph = AdjacencyListGraph(num_stations, directed=False, weighted=True)
    added_edges = set()  # To track unique edges

    for row_index, row in underground_data.iterrows():
        start_key = station_index[row["Start"]]
        end_key = station_index[row["Destination"]]

        # Ensure each unique edge is only inserted once, regardless of direction
        edge = (min(start_key, end_key), max(start_key, end_key))
        if edge not in added_edges:
            graph.insert_edge(start_key, end_key, weight=1)  # Set weight to 1 for counting stops
            added_edges.add(edge)

    return graph, station_index, stations


def calculate_all_journey_stops(graph, num_stations):
    all_journey_stops = []
    for start in range(num_stations):
        distances, predecessors = dijkstra(graph, start)
        for end in range(start + 1, num_stations):  # Only count each journey once by ensuring start < end
            if distances[end] != float('inf'):
                all_journey_stops.append(distances[end])
    return all_journey_stops


def plot_histogram(all_journey_stops):
    plt.figure(figsize=(10, 6))
    plt.hist(all_journey_stops, bins=range(0, int(max(all_journey_stops)) + 1), edgecolor='black', align='left')
    plt.title('Histogram of Possible Journey Stops')
    plt.xlabel('Number of Stops')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()


def find_longest_journey(graph, num_stations, stations):  # Finds the longest journey by stops
    max_stops = -1
    longest_path = None
    for start in range(num_stations):
        distances, predecessors = dijkstra(graph, start)
        for end in range(num_stations):
            if distances[end] > max_stops and distances[end] != float('inf'):
                max_stops = distances[end]
                longest_path = print_path(predecessors, start, end, lambda x: stations[x])
    return max_stops, longest_path


def main(file):
    # Load and clean data
    underground_data = load_data(file)

    # Build the graph with unique edges
    graph, station_index, stations = build_graph(underground_data)
    num_stations = len(stations)

    # Calculate journey stops
    all_journey_stops = calculate_all_journey_stops(graph, num_stations)
    print(f"Total possible journeys calculated (in terms of stops): {len(all_journey_stops)}")

    # Plot histogram of journey stops
    plot_histogram(all_journey_stops)

    # Find the longest journey in terms of stops
    max_stops, longest_path = find_longest_journey(graph, num_stations, stations)

    print(f"Longest Journey: {max_stops} stops")
    print(f"Path: {' → '.join(longest_path)}")


if __name__ == "__main__":
    file = 'London Underground data.xlsx'
    main(file)
