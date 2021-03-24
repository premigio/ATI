import numpy as np

from TP0.image import MyImage, normalization
from PIL import Image


# mascaras son impares!
def get_pixels_around(pixel_array, r, c, mask, circular_border=False):
    mask_size, _ = mask.shape
    m, n = pixel_array.shape
    coord = []
    half_mask = int((mask_size - 1) / 2)
    my_range = np.arange(start=- 1 * half_mask, stop=half_mask + 1, step=1)
    for i in my_range:
        for j in my_range:
            if circular_border:
                if r + i < m and c + j < n:
                    coord.append(pixel_array[r + i, c + j] * mask[i][j])
                elif r + i < m:
                    coord.append(pixel_array[r + i, 0] * mask[i][j])
                elif c + j < n:
                    coord.append(pixel_array[0, c + j] * mask[i][j])
                else:
                    coord.append(pixel_array[0, 0] * mask[i][j])
            else:
                if 0 <= r + i < m and 0 <= c + j < n:
                    coord.append(pixel_array[r + i, c + j] * mask[i][j])
                else:
                    coord.append(0)

    return coord


def mean_filter(image: MyImage, mask: int):
    if image is None:
        return
    wei = 1.0 / (mask ** 2)
    pixel_array = np.array(image.image)
    pixel_array2 = pixel_array.copy()
    w, h = image.image.size

    for i in range(w):
        for j in range(h):
            pixel_array2[j][i] = wei * np.sum(get_pixels_around(pixel_array, j, i, np.ones(shape=(mask, mask))))

    fin_image = MyImage.numpy_to_image(pixel_array2, image.mode)
    return MyImage.from_image(fin_image, image.dimensions)


def median_filter(image: Image, mask: int):
    if image is None:
        return
    pixel_array = np.array(image.image)
    pixel_array2 = pixel_array.copy()
    w, h = image.image.size

    for i in range(w):
        for j in range(h):
            pixels_around = get_pixels_around(pixel_array, j, i, np.ones(shape=(mask, mask)))
            pixels_around = np.array(pixels_around)
            pixels_around.sort()
            pixel_array2[j][i] = np.median(pixels_around)

    fin_image = MyImage.numpy_to_image(pixel_array2, image.mode)
    return MyImage.from_image(fin_image, image.dimensions)


def weighted_median_filter(image: Image):
    if image is None:
        return
    pixel_array = np.array(image.image)
    pixel_array2 = pixel_array.copy()
    w, h = image.image.size
    mask = [1, 2, 1, 2, 4, 2, 1, 2, 1]

    for i in range(w):
        for j in range(h):
            pixels_around = get_pixels_around(pixel_array, j, i, np.ones(shape=(3, 3)))
            weighted_pixels_around = []
            for n in range(len(pixels_around)):
                for m in range(mask[n]):
                    weighted_pixels_around.append(pixels_around[n])
            weighted_pixels_around = np.array(weighted_pixels_around)
            weighted_pixels_around.sort()
            pixel_array2[j][i] = np.median(weighted_pixels_around)

    fin_image = MyImage.numpy_to_image(pixel_array2, image.mode)
    return MyImage.from_image(fin_image, image.dimensions)


def gaussian_filter(image: MyImage, sigma: int):
    # para color, haces split y dsps Image.merge(img_cpy.image_element.mode, channels)
    # eso antes de llamar esto en el front

    mask = 2 * sigma + 1
    pixel_array = np.array(image.image)
    pixel_array2 = pixel_array.copy()
    w, h = image.image.size

    full_mask = np.zeros(shape=(mask, mask))

    for x in range(mask):
        for y in range(mask):
            full_mask[x][y] = np.exp(-(x ** 2 + y ** 2) / (sigma ** 2)) / (
                    2 * np.pi * (sigma ** 2))

    full_mask = np.divide(full_mask, np.sum(full_mask))

    for i in range(w):
        for j in range(h):
            pixel_array2[j][i] = np.sum(get_pixels_around(pixel_array, j, i, full_mask))

    fin_image = MyImage.numpy_to_image(pixel_array2, image.mode)
    return MyImage.from_image(fin_image, image.dimensions)


def border_enhancement(image: MyImage, mask: int):
    if image is None:
        return
    wei = 1.0 / (mask ** 2)
    pixel_array = np.array(image.image, dtype=np.int64)
    pixel_array2 = pixel_array.copy()
    w, h = image.image.size

    mask_matrix = np.ones(shape=(mask, mask)) * -1
    half_mask = int((mask - 1) / 2)
    mask_matrix[half_mask][half_mask] = mask_matrix[half_mask][half_mask] * (- (mask ** 2 - 1))

    for i in range(w):
        for j in range(h):
            pixel_array2[j][i] = wei * np.sum(get_pixels_around(pixel_array, j, i, mask_matrix))
    normalization(pixel_array2)
    fin_image = MyImage.numpy_to_image(pixel_array2, image.mode)
    return MyImage.from_image(fin_image, image.dimensions)
