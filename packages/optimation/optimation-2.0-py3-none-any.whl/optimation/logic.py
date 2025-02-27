# Core Optimation Logic

def balance_variables(A, B, weight_A):
    """ Balances two variables using a weighted approach """
    weight_B = 100 - weight_A
    normalized_A = weight_A / 100
    normalized_B = weight_B / 100
    return (A * normalized_A) + (B * normalized_B)

def exponential_weighting(A, B, weight_A):
    """ Applies an exponential weighting function to variables """
    weight_B = 100 - weight_A
    return (A ** (weight_A / 100)) + (B ** (weight_B / 100))
