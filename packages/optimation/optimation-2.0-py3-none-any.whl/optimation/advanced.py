# Advanced optimation techniques

def weighted_tradeoff(A, B, weight_A, factor=1.0):
    """ Adjust weights with a trade-off factor """
    weight_B = 100 - weight_A
    normalized_A = (weight_A / 100) * factor
    normalized_B = (weight_B / 100) * factor
    return (A * normalized_A) + (B * normalized_B)
