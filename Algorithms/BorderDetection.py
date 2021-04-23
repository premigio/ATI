import math

import numpy as np
from PIL import Image

from Algorithms.Filters import get_pixels_around
from Classes.MyImage import MyImage, normalization


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


# noinspection PyUnresolvedReferences,PyTypeChecker
def prewitt_sobel_filters(image: MyImage, prewitt: bool):
    if image is None:
        return

    mask_h = [[-1, -1, -1],
              [0, 0, 0],
              [1, 1, 1]]

    mask_v = [[-1, 0, 1],
              [-1, 0, 1],
              [-1, 0, 1]]

    if not prewitt:
        mask_h[0][1] *= 2
        mask_h[2][1] *= 2
        mask_v[1][0] *= 2
        mask_v[1][2] *= 2

    mask_h = np.array(mask_h)
    mask_v = np.array(mask_v)

    pixel_array = np.array(image.image, dtype=np.float64)
    pixel_array2 = pixel_array.copy()
    w, h = image.image.size

    for i in range(w):
        for j in range(h):
            dx = get_pixels_around(pixel_array, j, i, mask_h)
            dy = get_pixels_around(pixel_array, j, i, mask_v)
            pixel_array2[j][i] = (np.sum(dx) ** 2 + np.sum(dy) ** 2) ** 0.5

    normalization(pixel_array2)
    fin_image = MyImage.numpy_to_image(pixel_array2, image.mode)
    return MyImage.from_image(fin_image, image.dimensions)


def all_directions(image: MyImage):
    if image is None:
        return

    mask_h = [[1, 1, 1],
              [1, -2, 1],
              [-1, -1, -1]]

    mask_v = [[-1, 1, 1],
              [-1, -2, 1],
              [-1, 1, 1]]

    mask_45 = [[1, 1, 1],
               [-1, -2, 1],
               [-1, -1, 1]]

    mask_135 = [[-1, -1, 1],
                [-1, -2, 1],
                [1, 1, 1]]

    mask_h = np.array(mask_h)
    mask_v = np.array(mask_v)
    mask_45 = np.array(mask_45)
    mask_135 = np.array(mask_135)

    pixel_array = np.array(image.image, dtype=np.float64)
    pixel_array2 = pixel_array.copy()
    w, h = image.image.size

    for i in range(w):
        for j in range(h):
            dx = get_pixels_around(pixel_array, j, i, mask_h)
            dy = get_pixels_around(pixel_array, j, i, mask_v)
            dx5 = get_pixels_around(pixel_array, j, i, mask_45)
            dy5 = get_pixels_around(pixel_array, j, i, mask_135)
            pixel_array2[j][i] = (np.sum(dy5) ** 2 + np.sum(dx5) ** 2 + np.sum(dx) ** 2 + np.sum(dy) ** 2) ** 0.5

    normalization(pixel_array2)
    fin_image = MyImage.numpy_to_image(pixel_array2, image.mode)
    return MyImage.from_image(fin_image, image.dimensions)


# Laplacian edge detector
def laplacian_edge_detector(my_image: MyImage, laplacian_mask, threshold: int = 0):
    if my_image is None:
        return

    layers = my_image.image.split()
    pixel_array = []
    for im in layers:
        pixel_array.append(np.array(im, dtype=np.float))

    width, height = my_image.image.size
    laplacian_op = []

    for k in range(len(layers)):
        laplacian_op.append(pixel_array[k].copy())

    for i in range(height):
        for j in range(width):
            for k in range(len(layers)):
                laplacian_op[k][i][j] = np.sum(get_pixels_around(pixel_array[k], i, j, laplacian_mask))

    final_images = []
    for k in range(len(layers)):
        result_cross = crosses_by_zero(laplacian_op[k], width, height, threshold)
        final_images.append(MyImage.numpy_to_image(result_cross, layers[k].mode))

    final = Image.merge(my_image.mode, final_images)
    return MyImage.from_image(final, my_image.dimensions)


def crosses_by_zero(laplacian_op, width, height, threshold: int = 0):
    normalization(laplacian_op)

    result_cross = np.zeros(shape=(height, width), dtype=np.uint8)

    for i in range(height - 1):
        for j in range(width):
            if laplacian_op[i][j] == 0:
                if i - 1 >= 0 and np.sign(laplacian_op[i - 1][j]) != np.sign(laplacian_op[i + 1][j]):
                    if abs(laplacian_op[i - 1][j]) + abs(laplacian_op[i + 1][j]) >= threshold:
                        result_cross[i][j] = 255
            else:
                if np.sign(laplacian_op[i][j]) != np.sign(laplacian_op[i + 1][j]):
                    if abs(laplacian_op[i][j]) + abs(laplacian_op[i + 1][j]) >= threshold:
                        result_cross[i][j] = 255

    for i in range(height):
        for j in range(width - 1):
            if laplacian_op[i][j] == 0:
                if j - 1 >= 0 and np.sign(laplacian_op[i][j - 1]) != np.sign(laplacian_op[i][j + 1]):
                    if abs(laplacian_op[i][j - 1]) + abs(laplacian_op[i][j + 1]) >= threshold:
                        result_cross[i][j] = 255
            else:
                if np.sign(laplacian_op[i][j]) != np.sign(laplacian_op[i][j + 1]):
                    if abs(laplacian_op[i][j]) + abs(laplacian_op[i][j + 1]) >= threshold:
                        result_cross[i][j] = 255

    return result_cross
