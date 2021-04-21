import numpy as np
from TP0.image import MyImage, normalization
from PIL import Image
from enum import Enum


def leclerc(sigma):
    return lambda i: (np.exp(-(i ** 2)) / (sigma ** 2))


def lorentz(sigma):
    return lambda i: (1 / (1 + (i ** 2) / (sigma ** 2)))


def iso_function(sigma):
    return lambda i: 1


class FunctionDiff(Enum):
    LECLERC = leclerc
    LORENTZ = lorentz
    ISOTROPIC = iso_function


# lambda = 0.25
def add_directions(arr, x, y, border_function, w, h):
    total = 0
    for direction in ['N', 'W', 'E', 'S']:
        val = 0
        if direction == 'N':
            if y + 1 < h:
                val = arr[y + 1][x]
        elif direction == 'W':
            if x - 1 >= 0:
                val = arr[y][x - 1]
        elif direction == 'E':
            if x + 1 < w:
                val = arr[y][x + 1]
        else:  # S
            if y - 1 >= 0:
                val = arr[y - 1][x]
        val -= arr[y][x]
        total += val * border_function(val)
    return total


def anisotropic(image: MyImage, border_function: FunctionDiff, sigma: float, iterations: int = 1):
    if image is None:
        return
    pixel_array = np.array(image.image, dtype=np.int64)
    pixel_array2 = pixel_array.copy()
    w, h = image.image.size

    for _ in range(iterations):
        pixel_array = pixel_array2
        for x in range(w):
            for y in range(h):
                pixel_array2[y][x] = pixel_array2[y][x] + 0.25 * (
                    add_directions(pixel_array, x, y, border_function(sigma), w, h))

    normalization(pixel_array2)
    fin_image = MyImage.numpy_to_image(pixel_array2, image.mode)
    return MyImage.from_image(fin_image, image.dimensions)


def isotropic(image: MyImage, iterations: int):
    anisotropic(image, FunctionDiff.ISOTROPIC, iterations)
