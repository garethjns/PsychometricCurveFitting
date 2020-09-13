import numpy as np


def logit(x: np.array, mean: float, var: float) -> np.array:
    return 1 / (1 + np.exp(-var * (x - mean)))
