import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal
from dijkstra import dijkstra
from print_path import print_path


class FormatData:
    def __init__(self, file):
        self.file = file
        self.cleaned_data = None
        self.stations = None
        self.station_index = {}
        self.graph = None
        self.num_of_stations = 0
        self.edges = []

    def load_and_clean_data(self):
        # Load and clean the Excel data
        underground_data = pd.read_excel(self.file)
        underground_data.columns = ['Line', 'Starting Station', 'Destination', 'Journey Time']
        self.cleaned_data = underground_data.dropna(subset=['Line', 'Starting Station', 'Destination', 'Journey Time'])

    def build_graph(self):
        # Sort and index stations deterministically
        self.stations = sorted(set(self.cleaned_data['Starting Station']).union(set(self.cleaned_data['Destination'])))

        # Assigning indices to stations
        for index, station in enumerate(self.stations):
            self.station_index[station] = index

        self.num_of_stations = len(self.stations)

        # Initialize the adjacency list graph with weighted edges
        self.graph = AdjacencyListGraph(self.num_of_stations, weighted=True, directed=False)

        # Insert edges into the graph and sort them
        for row_index, row in self.cleaned_data.iterrows():
            start_key = self.station_index[row['Starting Station']]
            end_key = self.station_index[row['Destination']]
            weight = row['Journey Time']
            if not self.graph.has_edge(start_key, end_key):
                self.graph.insert_edge(start_key, end_key, weight)
                self.edges.append((start_key, end_key, weight))


class MinimizingLineSections:
    def __init__(self, graph_data):
        self.graph_data = graph_data

    # Run Kruskal's algorithm to get the Minimum Spanning Tree
    def close_lines(self):
        mst = kruskal(self.graph_data.graph)
        closed_edges = []
        for start, destination, weight in self.graph_data.edges:
            if not mst.has_edge(start, destination):
                closed_edges.append((self.graph_data.stations[start], self.graph_data.stations[destination], weight))
        return closed_edges, mst


class PathFinder:
    def __init__(self, graph, stations):
        self.graph = graph
        self.stations = stations

    def find_all_journey_durations(self):
        all_durations = []
        for start in range(len(self.stations)):
            distances, predecessors = dijkstra(self.graph, start)
            for end in range(start + 1, len(self.stations)):
                if distances[end] != float('inf'):
                    all_durations.append(distances[end])
        return all_durations

    def find_longest_journey(self):
        max_duration = -1
        longest_path = None
        for start in range(len(self.stations)):
            distances, predecessors = dijkstra(self.graph, start)
            for end, duration in enumerate(distances):
                if duration > max_duration and duration != float('inf'):
                    max_duration = duration
                    longest_path = print_path(predecessors, start, end, lambda x: self.stations[x])
        return max_duration, longest_path


def plot_histogram(all_durations):
    plt.figure(figsize=(10, 6))
    plt.hist(all_durations, bins=range(0, int(max(all_durations)) + 1), edgecolor='black', align='left')
    plt.title('Histogram of Journey Times')
    plt.xlabel('Journey Duration (Minutes)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()


def main(file):
    formatter = FormatData(file)
    formatter.load_and_clean_data()
    formatter.build_graph()

    # Generate MST and get closed sections
    minimizer = MinimizingLineSections(formatter)
    closed_routes, mst = minimizer.close_lines()

    # Output closed line sections
    print("Closed Line Sections:")
    for start, destination, weight in sorted(closed_routes):
        print(f"{start} - {destination} (Duration: {weight} minutes)")

    # Use MST to find journey durations and longest path
    path_finder = PathFinder(mst, formatter.stations)

    # Find and print longest journey on MST
    max_duration, longest_path = path_finder.find_longest_journey()
    print(f"\nLongest Journey Duration on MST: {max_duration} minutes")
    print(f"Path: {' → '.join(longest_path)}")


if __name__ == "__main__":
    file = 'London Underground data.xlsx'
    main(file)
