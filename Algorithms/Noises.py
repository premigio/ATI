import random

import numpy as np
from PIL import Image

from Algorithms.Classes.MyImage import MyImage, normalization


def salt_n_pepper(image: MyImage, density: float, p0: float):
    w, h = image.image.size
    pixel_array = np.array(image.image)
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

    layers = image.image.split()
    w, h = image.image.size

    pixel_array = []

    for im in layers:
        pixel_array.append(np.array(im, dtype=np.float64))

    pixel_array2 = pixel_array.copy()

    for i in range(h):
        for j in range(w):
            for k in range(len(layers)):
                random_value = random.random()
                if random_value < percentage:  # asi puedo cambiar el siguiente porcentaje apenas de los pixeles.
                    pixel_array2[k][i][j] = add_multiply(pixel_array2[k][i][j], noise_function())

    final_image = []
    for band in range(len(layers)):
        pixel_array_layer = normalization(pixel_array2[band])
        final_image.append(MyImage.numpy_to_image(pixel_array_layer, layers[band].mode))

    final = Image.merge(image.mode, final_image)
    return MyImage.from_image(final, image.dimensions)


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
