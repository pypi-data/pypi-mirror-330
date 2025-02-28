import numpy as np

def normalize_probabilities(probabilities):
    total = np.sum(probabilities)
    return probabilities / total if total > 0 else probabilities
