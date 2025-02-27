import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data
import networkx as nx
import time
import pickle
import os
from copy import deepcopy
import numpy as np

# Make sure you have the proper device set up
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#%%
def sort_edge_index(edge_index):
    # Step 1: Create pairs for edge[0][i], edge[1][i]
    pairs = list(zip(edge_index[0].tolist(), edge_index[1].tolist()))
    
    # Step 2: Sort these pairs
    sorted_pairs = sorted(pairs)
    
    # Step 3: Separate pairs again
    sorted_edge_0, sorted_edge_1 = zip(*sorted_pairs)
    
    # Convert back to tensor
    sorted_edge_index = torch.tensor([list(sorted_edge_0), list(sorted_edge_1)])
    
    return sorted_edge_index



def merge_edges(J, h, u, v):
    """
    Merge the edge (u, v) in the Ising model.
    """
    new_J = {}
    new_h = h.copy()

    # Update node weights
    new_h[u] += new_h[v] + J.get((u, v), 0)
    new_h[v] = 0

    # Update edge weights
    for (a, b) in J:
        old_a = a
        old_b = b
        if a == v:
            a = u
        elif b == v:
            b = u
        if a != b:
            if a > b:
                a, b = b, a
            if (a, b) in new_J:
                new_J[(a, b)] += J[(old_a, old_b)]
            else:
                new_J[(a, b)] = J[(old_a, old_b)]

    # Remove self-loops
    if (u, u) in new_J:
        del new_J[(u, u)]

    return new_J, new_h


def flip_and_merge(J, h, u, v):
    """
    Flip the sign of weights connected to node u and then merge the edge (u, v). (u will be the represented)
    """
    # Step 2.1: Flip the sign of weights connected to node u
    flipped_J = {key: -value if u in key else value for key, value in J.items()}

    # Step 2.2: Merge the edge (u, v)
    if (u > v): u, v = v, u
    return merge_edges(flipped_J, h, u, v)

# J is a Ising graph
def predict_and_merge(model, J, h, reduction_rate):
    original_J = J.copy()
    original_h = h.copy()
    # Initialize Graph
    G = nx.Graph()
    G.add_edges_from(J.keys())
    G.add_nodes_from(h.keys())
    for u, v in J.keys():
        G[u][v]['weight'] = J[(u, v)]

    edge_rate_reduced = 0
    num_node_reduced = 0
    while edge_rate_reduced < reduction_rate:

        for key,value in J.items():
            J[key] = -J[key]

        G = nx.Graph()
        G.add_edges_from(J.keys())
        G.add_nodes_from(h.keys())
        for u, v in J:
            G[u][v]['weight'] = J[(u, v)]
        
        node_features = []

        edge_features = []

        edge_index = []
        edges = list(J.keys())
        edge_index = torch.tensor(edges).t().contiguous()

        #=============== Weight features ===============
        node_features = []
        abs_weight_list = []
        weight_sum_list = []
        for node in sorted(G.nodes()):
            connected_weights = [G[node][nbr]['weight'] for nbr in G[node]]
            weight_sum = sum(connected_weights)
            abs_weight_sum = sum(abs(w) for w in connected_weights)
            degree = G.degree(node)
            node_features.append([degree, 1/degree if degree != 0 else 0])
            abs_weight_list.append(abs_weight_sum)
            weight_sum_list.append(weight_sum)

        # Calculate edge features (weights) 

        fast_score_list = []
        sim_score_list = []
        sign_list = []
        edge_weight_list = []
        edge_abs_weight_list = []
        min_2_ends = []
        sum_2_ends = []
        small_sim_score_list = []
        for (u, v) in J.keys():
            fast_score = 2 * abs(J[(u, v)]) - min(abs_weight_list[u], abs_weight_list[v])
            min_2_ends.append(min(abs_weight_list[u], abs_weight_list[v]))
            sum_2_ends.append(abs_weight_list[u] + abs_weight_list[v])
            sim_score = 2 * abs(J[(u, v)])
            if (J[(u, v)] >= 0):
                sim_score = sim_score - 0.5 * abs(weight_sum_list[u] - weight_sum_list[v])
            else: 
                sim_score = sim_score - 0.5 * abs(weight_sum_list[u] + weight_sum_list[v])
            
            if (J[(u, v)] >= 0):
                small_sim_score_list.append(0.5 * abs(weight_sum_list[u] - weight_sum_list[v]))
            else: 
                small_sim_score_list.append(abs(weight_sum_list[u] + weight_sum_list[v]))

            sign = 1
            if (J[(u, v)] < 0):
                sign = -1
            if (J[(u, v)] == 0):
                sign = 0
            fast_score_list.append(fast_score)
            sim_score_list.append(sim_score)
            sign_list.append(sign)
            edge_weight_list.append(J[(u, v)])
            edge_abs_weight_list.append(abs(J[(u, v)]))
            # edge_features.append([max(fast_score, sim_score), fast_score, sim_score])
        
        edge_features = list(zip(edge_weight_list, edge_abs_weight_list))
        x = torch.tensor(node_features, dtype=torch.float).to(device)
        
        edge_attr = torch.tensor(edge_features, dtype=torch.float).view(-1, 2).to(device)        # 2 features


        edge_index = sort_edge_index(edge_index).to(device)
        data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr)
        data.edge_inference_weight = torch.tensor([edge for edge in edge_weight_list], dtype=torch.float).to(device)
        data.positive_weight = torch.tensor(data.edge_inference_weight>=0, dtype=torch.float).to(device)
        data.edge_inference_abs_weight = torch.tensor([edge for edge in edge_abs_weight_list], dtype=torch.float).to(device)
        data.edge_inference_fast_score = torch.tensor([edge for edge in fast_score_list], dtype=torch.float).to(device)
        data.edge_inference_sim_score = torch.tensor([edge for edge in sim_score_list], dtype=torch.float).to(device)
        data.min_2_ends = torch.tensor([edge for edge in min_2_ends], dtype=torch.float).to(device)
        data.sum_2_ends = torch.tensor([edge for edge in sum_2_ends], dtype=torch.float).to(device)
        data.small_sim_score = torch.tensor([edge for edge in small_sim_score_list], dtype=torch.float).to(device)

        data.max_score = torch.max(data.edge_inference_fast_score,data.edge_inference_sim_score)
        data.positive_score = torch.tensor(data.max_score>0, dtype=torch.float)
        data.fasthare_predict = data.positive_score * data.positive_weight

        model.eval()

        with torch.no_grad():
            output = model(data.x, data.edge_index, data.edge_attr)
        
        # Find the edge with minimim of: 
        # mininum(abs(output[i] - 0), abs(1 - output[i]))
        min_change_index = torch.argmin(torch.min(torch.abs(output), torch.abs(1 - output))).item()
        try:
            output = output[min_change_index].item()
        except:
            # in case 1 number only
            output = output.item()
        
        if (output > 0.5):
            min_change_index = min_change_index + len(J) # flip

        # conver J back to Ising model
        for key,value in J.items():
            J[key] = -J[key]

        flip = True
        # Merge or flip and merge based on the predicted energy change
        if min_change_index < len(J):
            u, v = list(J.keys())[min_change_index]
            J, h = merge_edges(J, h, u, v)
            flip = False
        else:
            u, v = list(J.keys())[min_change_index % len(J)]
            J, h = flip_and_merge(J, h, u, v)
        # if flip:
        #     s = "flip"
        # else:
        #     s = "merge"
        # print(f"{s} u, v: ", u, v)
        # print("J after action: ", J)
        # print("h after action: ", h)
        # Update graph G
        num_node_reduced += 1
        num_edges_reduced = len(original_J) - len(J)
        edge_rate_reduced = (num_edges_reduced / len(original_J)) 
        # node_rate_reduced = num_node_reduced / len(original_h)
        # if debug:
        #     print(f"Edge rate reduce: {edge_rate_reduced}")
        G.clear()
        G.add_edges_from(J.keys())
        G.add_nodes_from(h.keys())
        for u, v in J.keys():
            G[u][v]['weight'] = J[(u, v)]
        # print("J: ", J)
        if nx.is_empty(G):
            break
    
    end_time = time.time()
    # Final energy calculation after all merges
    # final_energy = cal_energy(J, h)
    # if debug:
    #     print(f"Final energy after merging: {final_energy}")
    #     print(f"Initial energy: {min_energy}")
    #     print(f"Final J: {J}")
    #     print(f"Final h: {h}")
    # if final_energy < min_energy:
    #     assert False, "[predict and merge] Check the model!"
    return ((len(original_J) - len(J))/ len(original_J)) * 100, sum(h.values()), J
