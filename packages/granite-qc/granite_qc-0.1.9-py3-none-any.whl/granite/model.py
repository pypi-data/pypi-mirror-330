import pickle
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import MessagePassing

# Define the necessary classes before loading the model
class NodeEdgeGNNLayerWithDualAggregation(MessagePassing):
    def __init__(self, node_in_channels, edge_in_channels, node_out_channels, edge_out_channels):
        super(NodeEdgeGNNLayerWithDualAggregation, self).__init__(aggr='add')  # Use sum aggregation
        self.node_self_linear = torch.nn.Linear(node_in_channels, node_out_channels)
        self.node_neighbor_linear = torch.nn.Linear(node_in_channels, node_out_channels)
        self.edge_to_node_linear = torch.nn.Linear(edge_in_channels, node_out_channels)
        
        # Weight matrix for edge update
        self.edge_update_linear = torch.nn.Linear(2 * node_in_channels + edge_in_channels, edge_out_channels)

        # Initialize learnable scalar parameters
        self.node_scalar = torch.nn.Parameter(torch.randn(1) / 2.576) 
        self.edge_scalar = torch.nn.Parameter(torch.randn(1) / 2.576)

    def forward(self, x, edge_index, edge_attr):
        # Propagate messages, undirected edges
        node_out = self.propagate(edge_index, x=x, edge_attr=edge_attr)

        # Update edge embeddings (excluding self-loops and reversed edges)
        num_original_edges = edge_attr.size(0)
        
        edge_concat = torch.cat([x[edge_index[0, :num_original_edges]], 
                                 x[edge_index[1, :num_original_edges]], 
                                 edge_attr], dim=-1)
        edge_out = self.edge_update_linear(edge_concat)
        edge_out = F.relu(edge_out + self.edge_scalar)
        
        return node_out, edge_out

    def message(self, x_j, edge_attr, index: torch.Tensor, size_i: int):
        # Handle messages differently for original edges and self-loops
        num_original_edges = edge_attr.size(0)
        
        # For original edges
        orig_messages = self.node_neighbor_linear(x_j[:num_original_edges]) + self.edge_to_node_linear(edge_attr)
        
        # For self-loops (only use node features)
        self_messages = self.node_neighbor_linear(x_j[num_original_edges:])
        
        # Combine messages
        all_messages = torch.cat([orig_messages, self_messages], dim=0)
        
        return all_messages

    def update(self, aggr_out, x):
        # Combine the node's own previous representation with the aggregated information
        out = aggr_out + self.node_self_linear(x) + self.node_scalar
        return F.relu(out)

class Solver(torch.nn.Module):
    def __init__(self, node_in_channels, edge_in_channels, node_out_channels, edge_out_channels, num_layers, mlp_hidden_dim = 64):
        super(Solver, self).__init__()
        self.layers = torch.nn.ModuleList()
        self.num_layers = num_layers
        for i in range(num_layers):
            node_in = node_in_channels if i == 0 else node_out_channels
            edge_in = edge_in_channels if i == 0 else edge_out_channels
            self.layers.append(NodeEdgeGNNLayerWithDualAggregation(node_in, edge_in, node_out_channels, edge_out_channels))

        # phase 2: Logistic regression
        self.feature_dim = 2 * node_out_channels + edge_out_channels 
        concat_dim = self.feature_dim
        
        # Use MLP for the final layer
        self.mlp = nn.Sequential(
            nn.Linear(concat_dim, mlp_hidden_dim),
            nn.ReLU(),
            nn.Linear(mlp_hidden_dim, mlp_hidden_dim),
            nn.ReLU(),
            nn.Linear(mlp_hidden_dim, 1)
        )
        self.final_layer = nn.Linear(concat_dim, 1)

    def forward(self, x, edge_index, edge_attr):
        from copy import deepcopy
        original_edge_attr = deepcopy(edge_attr)
        for i in range(self.num_layers - 1):
            layer = self.layers[i]
            x, edge_attr = layer(x, edge_index, edge_attr)

        # Handle last layer separately 
        # Concatenate node and edge embeddings from the last layer
        u = x[edge_index[0]]
        v = x[edge_index[1]]
        # add original edge_attr
        edge_concat = torch.cat([u, v, edge_attr], dim=1)

        # Add a MLP to compute the final edge score
        edge_emb = self.mlp(edge_concat)          # E * 1
        
        output = torch.sigmoid(edge_emb)
        return output.squeeze()

# Path to the model file
MODEL_PATH = os.path.join(os.path.dirname(__file__), "trained_model.pkl")

def load_model():
    """Load the trained model from the file."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Ensure it is included in the package.")
        
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)
    
    model.eval()  # Ensure model is in evaluation mode
    return model

# Example usage:
if __name__ == "__main__":
    # Load the model
    model = load_model("trained_model.pkl")
    print("Model loaded successfully!")
    
    # You can now use the model for inference
    # For example:
    # predictions = model(x, edge_index, edge_attr)