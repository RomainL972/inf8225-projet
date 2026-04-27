import data_utils
import argparse

from tqdm import tqdm
import networkx as nx
import numpy as np


def generate_random_graphs(n, c):
    graphs = []
    for _ in tqdm(range(n)):
        g = nx.Graph()
        g.add_nodes_from(range(64))
        while g.number_of_edges() < c:
            u, v = np.random.choice(64, 2, replace=False)
            g.add_edge(u, v)
        graphs.append(g)
    return graphs


def greedyColoring(graph) -> int:
    V = graph.number_of_nodes()
    adj = [list(graph.neighbors(i)) for i in range(graph.number_of_nodes())]

    result = [-1] * V

    # Assign the first color to first vertex
    result[0] = 0
    # A temporary array to store the available colors.
    # True value of available[cr] would mean that the
    # color cr is assigned to one of its adjacent vertices
    available = [False] * V

    # Assign colors to remaining V-1 vertices
    for u in range(1, V):
        # Process all adjacent vertices and
        # flag their colors as unavailable
        for i in adj[u]:
            if result[i] != -1:
                available[result[i]] = True

        # Find the first available color
        cr = 0
        while cr < V:
            if not available[cr]:
                break

            cr += 1

        # Assign the found color
        result[u] = cr

        # Reset the values back to false
        # for the next iteration
        for i in adj[u]:
            if result[i] != -1:
                available[result[i]] = False

    return len(set(result))


def main():
    print("loading graphs...")
    graphs = generate_random_graphs(100, 512)

    success_count = 0
    for graph in tqdm(graphs):
        n_colors = greedyColoring(graph)
        success_count += n_colors <= 8

    print(f"Greedy coloring solved {success_count} out of {len(graphs)} problems")

    data_utils.save_graphs(
        graphs, [f"graph_{i}.dimacs" for i in range(len(graphs))], "saved_graphs/random"
    )


if __name__ == "__main__":
    main()
