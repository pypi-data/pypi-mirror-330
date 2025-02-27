import pickle
import os
import torch

MODEL_PATH = os.path.join(os.path.dirname(__file__), "trained_model.pkl")

def load_model():
    """Load the trained model from the file."""
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)
    model.eval()  # Ensure the model is in evaluation mode
    return model
