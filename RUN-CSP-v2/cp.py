import networkx as nx
from ortools.sat.python import cp_model
import argparse
import data_utils
from tqdm import tqdm


def solve_with_cp(graph: nx.Graph, n_colors: int) -> bool:
    model = cp_model.CpModel()

    n = graph.number_of_nodes()
    edge_vars = [model.new_int_var(0, n_colors - 1, f"edge_{i}") for i in range(n)]

    for u, v in graph.edges():
        model.add(edge_vars[u] != edge_vars[v])

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    #     print("Vertex assignments:")
    #     for v in sorted(graph.nodes()):
    #         print(f"  vertex {v}: color {solver.Value(edge_vars[v])}")

    return status == cp_model.OPTIMAL or status == cp_model.FEASIBLE


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--data_path",
        default=None,
        help="Path to the evaluation data. Expects a directory with graphs in dimacs format.",
    )
    parser.add_argument(
        "-i",
        "--n_instances",
        type=int,
        default=100,
        help="Number of instances for evaluation.",
    )
    args = parser.parse_args()

    names, graphs = data_utils.load_graphs(args.data_path, limit=args.n_instances)

    success_count = 0
    for graph in tqdm(graphs):
        success_count += solve_with_cp(graph, 8)

    print(f"CP solved {success_count} out of {len(graphs)} problems")
