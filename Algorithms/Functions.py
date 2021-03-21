import os

from PIL import Image, ImageDraw, ImageChops
import numpy as np
from TP0.image import MyImage


def power(image: MyImage, gamma: float):
    c = 255 ** (1 - gamma)
    pixel_array = np.array(image.image)

    pixel_array = np.power(pixel_array, gamma) * c

    pixel_array = pixel_array.astype(int)

    return MyImage.numpy_to_image(pixel_array, image.mode)


def histogram(image: MyImage):
    pass
