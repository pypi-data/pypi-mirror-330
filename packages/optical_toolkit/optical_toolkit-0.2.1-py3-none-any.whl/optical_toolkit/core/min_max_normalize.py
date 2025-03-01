import numpy as np


def min_max_normalize(image):
    min_val = np.min(image)
    max_val = np.max(image)

    normalized_image = (image - min_val) / (max_val - min_val)

    return normalized_image
