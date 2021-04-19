import numpy as np
from Algorithms.Filters import get_pixels_around
from TP0.image import MyImage, normalization
from PIL import Image


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

    pixel_array = np.array(image.image)
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

    pixel_array = np.array(image.image)
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
