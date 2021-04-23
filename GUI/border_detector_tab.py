import math

import numpy as np

from Algorithms.BorderDetection import laplacian_edge_detector
from Classes.MyImage import MyImage


# mask_size should be at least 4 * sigma + 1
def log_mask(sigma: float, mask_size: int):
    mask = np.zeros(shape=(mask_size, mask_size), dtype=float)
    margin = math.floor(mask_size / 2)
    range_log = range(-margin, margin + 1)

    for x in range_log:
        for y in range_log:
            mask[x + margin][y + margin] = -(1 / (math.sqrt(2 * math.pi) * sigma ** 3)) * \
                                           (2 - (x ** 2 + y ** 2) / sigma ** 2) * \
                                           math.exp(- (x ** 2 + y ** 2) / (2 * sigma ** 2))

    return mask


def show_laplacian_detector(my_image: MyImage, window):
    laplacian_mask = [[0, -1, 0],
                      [-1, 4, -1],
                      [0, -1, 0]]

    laplacian_mask = np.array(laplacian_mask)

    image = laplacian_edge_detector(my_image, laplacian_mask)
    image.image.show()
    return image


def show_laplacian_slope_detector(my_image: MyImage, window):
    laplacian_mask = [[0, -1, 0],
                      [-1, 4, -1],
                      [0, -1, 0]]

    laplacian_mask = np.array(laplacian_mask)

    threshold = window.ask_for_float('Choose a threshold value',
                                     default=30.0, min_value=0.0, text='Threshold')

    image = laplacian_edge_detector(my_image, laplacian_mask, threshold=threshold)
    image.image.show()
    return image


def show_laplacian_gauss_detector(my_image: MyImage, window):

    sigma = window.ask_for_int('Choose a sigma value',
                                 default=1, min_value=1, text='Sigma')

    mask = log_mask(sigma, sigma * 6 + 1)
    image = laplacian_edge_detector(my_image, mask)
    image.image.show()
    return image
