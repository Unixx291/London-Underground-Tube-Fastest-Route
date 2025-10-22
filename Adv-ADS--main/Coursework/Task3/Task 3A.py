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


def build_graph(underground_data):  # Parse the data from the Excel to build an Adjacency List graph
    stations = pd.concat([underground_data["Start"], underground_data["Destination"]]).unique()
    station_index = {}
    num_stations = len(stations)
    for index, station in enumerate(stations):  # Map stations to indices
        station_index[station] = index

    graph = AdjacencyListGraph(num_stations, directed=False, weighted=True)
    added_edges = set()  # To keep track of unique edges

    # Traverse each row and add each unique edge only once
    for row_index, row in underground_data.iterrows():
        start = station_index[row["Start"]]
        end = station_index[row["Destination"]]
        journey_duration = row["Duration"]

        # Use sorted tuple to ensure each pair is added in one direction only
        edge = (min(start, end), max(start, end))

        # Insert edge if it hasn't been added before
        if edge not in added_edges:
            graph.insert_edge(start, end, weight=journey_duration)
            added_edges.add(edge)

    return graph, station_index, stations


def calculate_all_durations(graph, num_stations):  # Calculates all the possible journey durations uniquely
    all_durations = []
    for start in range(num_stations):
        distances, predecessors = dijkstra(graph, start)
        for end in range(start + 1, num_stations):  # Only count journeys where start < end to avoid duplication
            if distances[end] != float('inf'):
                all_durations.append(distances[end])
    return all_durations


def find_longest_journey(graph, num_stations, stations):  # Finds the longest journey
    max_duration = -1
    longest_path = None
    for start in range(num_stations):
        distances, predecessors = dijkstra(graph, start)
        for end in range(num_stations):
            if distances[end] > max_duration and distances[end] != float('inf'):
                max_duration = distances[end]
                longest_path = print_path(predecessors, start, end, lambda x: stations[x])
    return max_duration, longest_path


def plot_histogram(all_durations):  # Plots the histogram of the duration of possible journeys
    plt.figure(figsize=(10, 6))
    plt.hist(all_durations, bins=range(0, int(max(all_durations)) + 1), edgecolor='black', align='left')
    plt.title('Histogram of Possible Journey Durations by Minutes')
    plt.xlabel('Journey Duration (Minutes)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()


def main(file):
    # Load and clean data
    underground_data = load_data(file)

    # Build the graph with unique edges
    graph, station_index, stations = build_graph(underground_data)
    num_stations = len(stations)

    # Calculate all journey durations
    all_durations = calculate_all_durations(graph, num_stations)
    print(f"Total journey durations calculated: {len(all_durations)}")

    # Plot histogram of the journey durations
    plot_histogram(all_durations)

    # Find the longest journey and print it
    max_duration, longest_path = find_longest_journey(graph, num_stations, stations)
    print(f"Longest Journey Duration: {max_duration} minutes")
    print(f"Path: {' → '.join(longest_path)}")


if __name__ == "__main__":
    file = 'London Underground data.xlsx'
    main(file)
