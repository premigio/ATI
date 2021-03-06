import numpy as np
from PIL import Image

from Algorithms.Filters.Filters import get_pixels_around
from Algorithms.Classes.MyImage import MyImage, normalization


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
    gx, gy = get_directional_derivatives(pixel_array, w, h, mask_h, mask_v)

    for i in range(w):
        for j in range(h):
            dx = gx[j, i]
            dy = gy[j, i]
            pixel_array2[j][i] = (dx ** 2 + dy ** 2) ** 0.5

    normalization(pixel_array2)
    fin_image = MyImage.numpy_to_image(pixel_array2, image.mode)
    return MyImage.from_image(fin_image, image.dimensions)


def get_directional_derivatives(pixel_array, width, height, mask_x, mask_y):

    gx = np.ndarray(shape=(width, height))
    gy = np.ndarray(shape=(width, height))

    for i in range(height):
        for j in range(width):
            dx = np.sum(get_pixels_around(pixel_array, i, j, mask_x))
            dy = np.sum(get_pixels_around(pixel_array, i, j, mask_y))
            gx[i, j] = dx
            gy[i, j] = dy

    return gx, gy


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
