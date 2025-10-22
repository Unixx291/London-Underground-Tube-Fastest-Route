import time
import random
import matplotlib.pyplot as plt
import math
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra

# Function to measure execution time and print journey paths for Dijkstra's algorithm
def measure_avg_time(graph, trials):
    total_time = 0
    journey_info = []

    for run in range(trials):
        start = random.randint(0, graph.get_card_V() - 1)
        destination = start
        while start == destination:
            destination = random.randint(0, graph.get_card_V() - 1)

        start_time = time.time()
        distances, _ = dijkstra(graph, start)
        journey_stops = distances[destination]
        end_time = time.time()

        total_time += (end_time - start_time) * 1000  # Convert to milliseconds

        # Store journey information for display
        journey_info.append((start, destination, journey_stops))

    average_execution_time = total_time / trials

    # Display each journey
    for start, destination, stops in journey_info:
        print(f"Shortest Journey based on stops between"
              f" Station {start} and Station {destination}: {stops} stops")

    return average_execution_time

# Function to generate a random network with a spanning tree and measure Dijkstra's performance
def generate_and_measure_network(network_size, edge_probability=0.01, trials=10):
    # Create a graph object
    network = AdjacencyListGraph(network_size, directed=False, weighted=True)
    # Ensure connectivity by creating a spanning tree
    for i in range(network_size - 1):
        if not network.has_edge(i, i + 1):
            network.insert_edge(i, i + 1, weight=1)

    # Add extra random edges based on edge probability
    for u in range(network_size):
        for v in range(u + 1, network_size):
            if random.random() <= edge_probability and not network.has_edge(u, v):
                network.insert_edge(u, v, weight=1)

    edge_count = network.get_card_E()
    print(f"Total edges in the graph: {edge_count}")

    # Measure average execution time and display journey info
    avg_time = measure_avg_time(network, trials=trials)
    return avg_time, edge_count

# Test different network sizes from 100 to 1000 incrementally in steps of 100
network_sizes = range(1100, 2100, 100)
average_times = []
edge_counts = []

for network_size in network_sizes:
    print(f"\nNetwork size: {network_size} stations")
    edge_probability = 0.01 / network_size  # Dynamically adjust edge probability
    avg_time, edges = generate_and_measure_network(network_size, edge_probability=edge_probability, trials=10)
    average_times.append(avg_time)
    edge_counts.append(edges)
    print(f"Average execution time for {network_size} stations: {avg_time:.2f} ms")

# Generate theoretical O(n log n) times for comparison
theoretical_times = [n * math.log2(n) for n in network_sizes]
scaling_factor = max(average_times) / max(theoretical_times)
theoretical_times = [t * scaling_factor for t in theoretical_times]

# Plotting results
plt.plot(network_sizes, average_times, marker='o', label="Empirical Average Time")
plt.plot(network_sizes, theoretical_times, linestyle="--", color="red", label="Theoretical O(n log n) Time")
plt.xlabel('Network Size (n)')
plt.ylabel('Average Execution Time (ms)')
plt.title('Empirical vs Theoretical Execution Time of Dijkstra\'s Algorithm (Number of Stops)',size=10)
plt.legend()
plt.grid()
plt.show()
