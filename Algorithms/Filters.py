import numpy as np

from TP0.image import MyImage


def median_filter(image: MyImage, mask: int):
    if image is None:
        return
    w = 1 / (mask ** 2)
    pixel_array = np.array(image.image)
    h, w = image.dimensions

    for i in range(h):
        for j in range(w):
            pixel_array[i][j]


def mean_filter():
    pass


def gaussian_filter():
    pass