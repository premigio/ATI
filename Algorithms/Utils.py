import numpy as np
from matplotlib import pyplot as plt

from Algorithms.Classes.MyImage import MyImage


def power(image: MyImage, gamma: float):
    c = 255 ** (1 - gamma)
    pixel_array = np.array(image.image)

    pixel_array = np.power(pixel_array, gamma) * c

    pixel_array = pixel_array.astype(int)

    return MyImage.numpy_to_image(pixel_array, image.mode)


def histogram(image: MyImage, draw: bool = False):  # solo para color gris
    hist = [0] * 256

    width, height = image.image.size
    for i in range(width):
        for j in range(height):
            pixel = image.my_get_pixel((i, j))
            hist[pixel] += 1

    hist = [value / (height * width) for value in hist]

    if draw:
        draw_histogram(hist)

    return hist


def equalized_histogram(my_image: MyImage, draw_hist: bool = False, draw_image: bool = False):
    # int[255(sk - smin)/(1 - smin) + 0.5]
    image = MyImage.from_image(my_image.image.copy())
    hist = histogram(image, draw_hist)
    cdf = np.cumsum(hist)
    height, width = image.image.size
    for i in range(width):
        for j in range(height):
            image.modify_pixel((i, j),
                               int(0.5 + (cdf[image.my_get_pixel((i, j))] - min(cdf)) * 255.0 / (1 - min(cdf))))
    if draw_image:
        image.image.show()
    return image


def equalized_histogram2(image: MyImage, draw_hist: bool = False, draw_image: bool = False):
    # int[255(sk - smin)/(1 - smin) + 0.5]
    pixel_array = np.array(image.image)
    hist = histogram(image, draw_hist)
    cdf = np.cumsum(hist)
    height, width = image.image.size
    for i in range(width):
        for j in range(height):
            pixel_array[i][j] = 0.5 + (cdf[pixel_array[i][j]] - min(cdf)) * 255.0 / (1 - min(cdf))
    final_image = MyImage.numpy_to_image(pixel_array.astype(int), image.mode)
    if draw_image:
        final_image.show()
    return MyImage.from_image(final_image, image.dimensions)


def draw_histogram(hist):
    plt.bar(range(256), hist, width=1.0, align="edge")
    plt.show()