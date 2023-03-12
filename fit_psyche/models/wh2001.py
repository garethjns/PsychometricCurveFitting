import numpy as np
from scipy import special


def wh2001(
    x: np.array, mean: float, var: float, guess_rate: float, lapse_rate: float
) -> np.ndarray:
    return guess_rate + (1.0 - guess_rate - lapse_rate) * 0.5 * (
        1.0 + special.erf((x - mean) / np.sqrt(2.0 * var**2.0))
    )
