import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal, print_undirected_edges, get_total_weight


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

        # Expanding station index assignment for clarity
        sorted_stations = sorted(self.stations)  # Sort stations first
        for index, station in enumerate(sorted_stations):
            self.station_index[station] = index

        self.num_of_stations = len(self.stations)

        # Initialize the adjacency list graph with weighted edges
        self.graph = AdjacencyListGraph(self.num_of_stations, weighted=True, directed=False)

        # Insert edges into the graph and sort them
        for row_index, row in self.cleaned_data.iterrows():
            start_key = self.station_index[row['Starting Station']]
            end_index = self.station_index[row['Destination']]
            weight = row['Journey Time']
            if not self.graph.has_edge(start_key, end_index):
                self.graph.insert_edge(start_key, end_index, weight)
                self.edges.append((start_key, end_index, weight))


class Minimizing_line_sections:
    def __init__(self, graph_data):
        self.graph_data = graph_data

    # Run Kruskal's algorithm to get the Minimum Spanning Tree
    def close_lines(self):
        mst = kruskal(self.graph_data.graph)

        # Find edges that are not part of the MST
        closed_edges = []
        for start, destination, weight in self.graph_data.edges:
            if not mst.has_edge(start, destination):
                closed_edges.append((self.graph_data.stations[start], self.graph_data.stations[destination]))

        return closed_edges, mst


if __name__ == "__main__":
    file = 'London Underground data.xlsx'

    # Load and format the data
    formatter = FormatData(file)
    formatter.load_and_clean_data()
    formatter.build_graph()

    # Minimize line sections using Kruskal's MST
    minimizer = Minimizing_line_sections(formatter)
    closed_routes, mst = minimizer.close_lines()

    # Output the closed line sections
    print("Closed Line Sections:")
    for start, destination in sorted(closed_routes):
        print(f"{start} - {destination}")

    # Print MST edges and total weight
    # print("\nEdges:")
    # print_undirected_edges(mst, formatter.stations)
    # total_weight = get_total_weight(mst)
    # print(f"\nTotal Weight of MST: {total_weight}")
