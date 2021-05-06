# 1. Ubicar una máscara circular alrededor de cada pixel.
# 2. Calcular la cantidad de pixels dentro de la máscara que tienen el mismo nivel de gris que el núcleo,
#   salvo un umbral.
#   r0 pixel central
#   r otro pixel dentro de la máscara.
#   c (r, r0) = 1 si |I(r) - I(r0)| < threshold, 0 en otro caso
from enum import Enum

import numpy as np
from PIL import Image

from Algorithms.Classes.MyImage import MyImage

susan_mask = [
    [0, 0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 0, 0]
]
susan_mask = np.array(susan_mask)

susan_mask_length = 37


# antes probaban con t = 27, t = 15 queda mejor
def susan_detector(my_image: MyImage, threshold: int, edge_value=0.50, corner_value=0.75, epsilon=0.1):
    if my_image is None:
        return

    width, height = my_image.image.size
    pixels_array = np.array(my_image.image, dtype=np.float64)

    corners_pixels = np.zeros(shape=pixels_array.shape)
    edges_pixels = np.zeros(shape=pixels_array.shape)

    for i in range(height):
        for j in range(width):
            s_r0 = s(i, j, pixels_array, threshold)
            if edge_value - epsilon <= s_r0 <= edge_value + epsilon:
                edges_pixels[i, j] = 255
            if corner_value - epsilon <= s_r0:
                corners_pixels[i, j] = 255

    img = get_img(pixels_array, edges_pixels, corners_pixels)
    return MyImage.from_image(img, my_image.dimensions)


def get_img(pixels: np.array, edges: np.array, corners: np.array) -> MyImage:
    image = Image.new('RGB', pixels.shape)
    width, height = pixels.shape

    for i in range(height):
        for j in range(width):
            pixel = int(pixels[i, j])
            edge = edges[i, j]
            corner = corners[i, j]

            if corner == 255:
                pixel = (255, 0, 0)
                image.putpixel((j, i), pixel)
            elif edge == 255:
                pixel = (0, 0, 255)
                image.putpixel((j, i), pixel)
            else:
                pixel = (pixel, pixel, pixel)
                image.putpixel((j, i), pixel)

    return image


def c(other_pixel, core_pixel, threshold: int):
    if abs(other_pixel - core_pixel) < threshold:
        return 1
    return 0


def s(x: int, y: int, pixels_array: np.array, threshold: int):
    core_pixel = pixels_array[x, y]
    circular_pixels = get_pixels_around(pixels_array, x, y, susan_mask)
    n_core_pixel = sum([c(other_pixel, core_pixel, threshold) for other_pixel in circular_pixels])
    return 1.0 - float(n_core_pixel) / len(circular_pixels)


def get_pixels_around(pixels_array, x, y, mask):
    mask_size, _ = mask.shape
    m, n = pixels_array.shape
    coord = []
    half_mask = int((mask_size - 1) / 2)
    my_range = np.arange(start=- 1 * half_mask, stop=half_mask + 1, step=1)
    for i in my_range:
        for j in my_range:
            if m > x + i >= 0 and 0 != mask[i + half_mask][j + half_mask] and 0 <= y + j < n:
                coord.append(pixels_array[x + i, y + j])

    return coord
