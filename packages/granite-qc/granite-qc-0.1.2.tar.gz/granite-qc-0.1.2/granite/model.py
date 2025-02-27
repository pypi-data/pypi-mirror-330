import pickle
import os

# Dynamically locate the model path within the installed package
MODEL_PATH = os.path.join(os.path.dirname(__file__), "trained_model.pkl")

def load_model():
    """Load the trained model from the installed package directory."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Ensure it is included in the package.")
    
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)
    
    model.eval()
    return model
