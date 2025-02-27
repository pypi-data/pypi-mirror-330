import torch
import networkx as nx
from torch_geometric.data import Data
from .model import load_model

def sort_edge_index(edge_index):
    """Sort edges to maintain order."""
    pairs = list(zip(edge_index[0].tolist(), edge_index[1].tolist()))
    sorted_pairs = sorted(pairs)
    sorted_edge_0, sorted_edge_1 = zip(*sorted_pairs)
    return torch.tensor([list(sorted_edge_0), list(sorted_edge_1)])

# J is a Ising graph
def predict_and_merge(J, h, reduction_rate=0.1):
    """
    Predicts and merges edges in an Ising graph using the trained model.
    
    Args:
        J (dict): Edge weights dictionary.
        h (dict): Node biases dictionary.
        reduction_rate (float): Percentage of edges to reduce.

    Returns:
        tuple: Compressed J, h, and compression stats.
    """
    model = load_model()
    
    # Convert J to Hamiltonian form
    for key in J:
        J[key] = -J[key]

    G = nx.Graph()
    G.add_edges_from(J.keys())
    G.add_nodes_from(h.keys())
    for u, v in J:
        G[u][v]['weight'] = J[(u, v)]
    
    original_J = J.copy()
    original_h = h.copy()
    num_edges_initial = len(J)
    
    edge_rate_reduced = 0
    while edge_rate_reduced < reduction_rate:
        node_features, edge_features, edge_index = extract_features(G, J, h)

        data = Data(
            x=torch.tensor(node_features, dtype=torch.float),
            edge_index=sort_edge_index(edge_index),
            edge_attr=torch.tensor(edge_features, dtype=torch.float)
        )

        model.eval()
        with torch.no_grad():
            output = model(data.x, data.edge_index, data.edge_attr)

        min_index = torch.argmin(torch.min(torch.abs(output), torch.abs(1 - output))).item()
        action = "merge" if output[min_index] <= 0.5 else "flip_and_merge"

        edge_list = list(J.keys())
        u, v = edge_list[min_index]

        if action == "merge":
            J, h = merge_edges(J, h, u, v)
        else:
            J, h = flip_and_merge(J, h, u, v)

        G.clear()
        G.add_edges_from(J.keys())
        G.add_nodes_from(h.keys())

        num_edges_reduced = num_edges_initial - len(J)
        edge_rate_reduced = num_edges_reduced / num_edges_initial

    return J, h, edge_rate_reduced * 100

def extract_features(G, J, h):
    """Extracts node and edge features for model input."""
    node_features = []
    edge_features = []
    edge_index = []

    abs_weights = {u: sum(abs(J[(u, v)]) for v in G.neighbors(u)) for u in G.nodes()}

    for u in G.nodes():
        node_features.append([G.degree[u], 1 / G.degree[u] if G.degree[u] != 0 else 0])

    for (u, v) in J:
        edge_features.append([J[(u, v)], abs(J[(u, v)])])
        edge_index.append([u, v])

    return node_features, edge_features, torch.tensor(edge_index).t()

def merge_edges(J, h, u, v):
    """Merges edge (u, v) in the Ising model."""
    new_J = {}
    new_h = h.copy()

    new_h[u] += new_h[v] + J.get((u, v), 0)
    new_h[v] = 0

    for (a, b) in J:
        if a == v:
            a = u
        elif b == v:
            b = u
        if a != b:
            new_J.setdefault((a, b), 0)
            new_J[(a, b)] += J[(a, b)]

    new_J.pop((u, u), None)
    return new_J, new_h

def flip_and_merge(J, h, u, v):
    """Flips edge weights for u and merges (u, v)."""
    flipped_J = {key: -value if u in key else value for key, value in J.items()}
    return merge_edges(flipped_J, h, u, v)
