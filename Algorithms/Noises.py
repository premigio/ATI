import os
import random

from PIL import Image, ImageDraw, ImageChops
import numpy as np
from matplotlib import pyplot as plt

from TP0.image import MyImage, normalization


def salt_n_pepper(image: MyImage, density: float):
    w, h = image.image.size
    pixel_array = np.array(image.image)
    p0 = np.random.uniform()
    p1 = 1 - p0
    number_of_pixels = np.floor(density*w*h)
    number_of_pixels = int(number_of_pixels)
    for n in range(number_of_pixels):
        i = random.randint(0, w - 1)
        j = random.randint(0, h - 1)
        x = np.random.uniform()
        if x <= p0:
            pixel_array[i][j] = 0
        elif x >= p1:
            pixel_array[i][j] = 255

    pixel_array = normalization(pixel_array)
    fin_image = MyImage.numpy_to_image(pixel_array, image.mode)
    return MyImage.from_image(fin_image, image.dimensions)


def noise_apply(image: MyImage, percentage: float, add_multiply, noise_function):
    w, h = image.image.size
    pixel_array = np.array(image.image, dtype=np.int64)

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


def exponential_multiplicative(image: MyImage, percentage: float, lambda_param: float):
    return noise_apply(image, percentage, lambda x, y: x * y, lambda: exponential_number_gen(lambda_param))


# Generators

def gaussian_number_gen(mean, deviation):
    return np.random.normal(mean, deviation)


def rayleigh_number_gen(epsilon):
    return np.random.rayleigh(epsilon)


def exponential_number_gen(lambda_param):
    return np.random.exponential(scale=(1 / lambda_param))
