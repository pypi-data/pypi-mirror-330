import torch
import pickle
import numpy as np
import os
import neal
import networkx as nx
from predict import predict_and_merge, sort_edge_index, merge_edges, flip_and_merge
from .model import Solver, NodeEdgeGNNLayerWithDualAggregation

# Define the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Function to calculate energy using simulated annealing
def cal_energy(J, h):
    # without linear biases
    sa = neal.SimulatedAnnealingSampler()
    linear_terms = {i: 0 for i in range(len(h))}
    sample_set_sa = sa.sample_ising(linear_terms, J, num_reads=1000)
    return sample_set_sa.first.energy + sum(h.values())

# Load the model
def load_model(model_path='trained_model.pkl'):
    """Load the saved model using pickle"""
    print(f"Loading model from: {model_path}")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    model.to(device)  # Make sure model is on the correct device
    model.eval()      # Set to evaluation mode
    return model

# Test with a sample problem
def test_predict_and_merge():
    print("Loading model...")
    model = load_model()
    print("Model loaded successfully!")
    
    print("\nTesting with a 25-node example...")
    
    # Example: ws - 25
    h = {i: 0 for i in range(25)}
    J = {(0, 1): 2, (0, 24): 4, (0, 2): -2, (0, 23): -2, (0, 3): -1, (0, 22): 3, (0, 4): -5, (0, 21): -1, (1, 2): -2, (1, 3): 1, (1, 24): 3, (1, 23): 4, (1, 5): 2, (1, 22): -3, (1, 9): 1, (2, 3): -1, (2, 4): 3, (2, 5): 2, (2, 24): -1, (2, 6): -3, (2, 23): 2, (3, 5): 4, (3, 6): -5, (3, 7): 4, (3, 24): 4, (3, 9): 3, (3, 19): 3, (4, 5): 2, (4, 6): -3, (4, 7): 3, (4, 8): 5, (5, 6): -3, (5, 7): -4, (5, 8): 4, (5, 20): -5, (6, 7): 4, (6, 8): -1, (6, 9): 4, (6, 10): 0, (7, 8): -3, (7, 9): 4, (7, 10): 2, (7, 11): -3, (8, 9): -1, (8, 10): -1, (8, 11): 4, (8, 12): -1, (8, 20): 0, (9, 10): 3, (9, 12): 3, (9, 13): -1, (9, 23): 1, (10, 11): -4, (10, 12): 0, (10, 13): -2, (10, 14): -2, (11, 12): -2, (11, 13): 3, (11, 14): 3, (11, 15): -2, (12, 13): -5, (12, 14): 0, (12, 15): -2, (12, 16): -1, (13, 14): 0, (13, 15): 2, (13, 16): 3, (13, 17): -1, (14, 15): 4, (14, 16): 1, (14, 17): 0, (14, 18): -5, (15, 16): -1, (15, 17): 0, (15, 18): 5, (15, 19): 1, (16, 17): 2, (16, 18): -1, (16, 19): -5, (16, 20): 1, (17, 18): -3, (17, 19): 4, (17, 20): 0, (17, 21): 1, (18, 19): 2, (18, 20): 5, (18, 21): 5, (18, 22): 1, (19, 21): 5, (19, 22): 4, (19, 23): 0, (20, 21): -2, (20, 23): 2, (20, 24): 2, (21, 22): 3, (21, 23): -3, (21, 24): 0, (22, 23): 3, (22, 24): -3, (23, 24): 4}

    print(f"Number of nodes: {len(h)}")
    print(f"Number of edges: {len(J)}")
    
    # Calculate initial energy
    initial_energy = cal_energy(J, h)
    print(f"Initial energy: {initial_energy}")
    
    # Set reduction rate
    reduction_rate = 0.1
    print(f"Reduction rate: {reduction_rate}")

    # Run predict_and_merge
    edge_reduction_percent, off_set_sum, compressed_J = predict_and_merge(model, J, h, reduction_rate)
    
    print("\nResults:")
    print(f"Edge reduction percentage: {edge_reduction_percent:.2f}%")
    print(f"Offset sum: {off_set_sum:.2f}")
    print(f"Number of edges after compression: {len(compressed_J)}")
    
    # Calculate compressed energy (using compressed_J instead of original J)
    compressed_energy = cal_energy(compressed_J, h) + off_set_sum
    print(f"Compressed energy: {compressed_energy:.2f}")
    print(f"Optimality: {compressed_energy/initial_energy * 100:.2f}%")

if __name__ == "__main__":
    test_predict_and_merge()