import os
import random

from PIL import Image, ImageDraw, ImageChops
import numpy as np
from matplotlib import pyplot as plt

from TP0.image import MyImage, normalization


def noise_apply(image: MyImage, percentage: float, add_multiply, noise_function):
    w, h = image.image.size
    pixel_array = np.array(image.image)

    for i in range(h):
        for j in range(w):
            random_value = random.random()
            if random_value < percentage:  # asi puedo cambiar el siguiente porcentaje apenas de los pixeles.
                pixel_array[i][j] = add_multiply(pixel_array[i][j], noise_function())

    pixel_array = normalization(pixel_array)
    fin_image = MyImage.numpy_to_image(pixel_array, image.mode)
    return MyImage.from_image(fin_image, image.dimensions)


def gaussian_additive(image: MyImage, percentage: float, mean: float, deviation: float):
    return noise_apply(image, percentage, lambda x, y: x + y, lambda: gaussian_number_gen(mean, deviation))


def rayleigh_multiplicative(image: MyImage, percentage: float, epsilon: float):
    # 1 - np.exp(-(x ** 2)/(2 * phi ** 2))
    return noise_apply(image, percentage, lambda x, y: x * y, lambda: rayleigh_number_gen(epsilon))


def gaussian_number_gen(mean, deviation):
    return np.random.normal(mean, deviation)


def rayleigh_number_gen(epsilon):
    return np.random.rayleigh(epsilon)
