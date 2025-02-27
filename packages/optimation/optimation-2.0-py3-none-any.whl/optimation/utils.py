# Utility functions for Optimation

def normalize_weights(weight_A, weight_B):
    """ Normalize weights so they sum to 1 """
    total = weight_A + weight_B
    return weight_A / total, weight_B / total
