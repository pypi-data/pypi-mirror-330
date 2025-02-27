def optimate(A, B, weight_A):
    """ Perform optimation balancing between A and B """
    weight_B = 100 - weight_A
    normalized_A = weight_A / 100
    normalized_B = weight_B / 100
    return (A * normalized_A) + (B * normalized_B)
