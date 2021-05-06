import numpy as np

from Algorithms.Classes.MyImage import MyImage, normalization
from PIL import Image


# mascaras son impares!
def get_pixels_around(pixel_array, r, c, mask, circular_border=False, no_count_border=True):
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
                    coord.append(pixel_array[r + i, c + j] * mask[i + half_mask][j + half_mask])
                elif no_count_border:
                    coord.append(0)

    return coord


# noinspection PyUnresolvedReferences,PyTypeChecker
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


# noinspection PyUnresolvedReferences,PyTypeChecker
def median_filter(image: MyImage, mask: int):
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


# noinspection PyUnresolvedReferences,PyTypeChecker
def weighted_median_filter(image: MyImage):
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


# noinspection PyUnresolvedReferences,PyTypeChecker
def gaussian_filter(image: MyImage, sigma: int):
    # para color, haces split y dsps Image.merge(image.mode, channels)
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


# noinspection PyUnresolvedReferences,PyTypeChecker
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


def calculate_bi_fil_w(image, i, j, k, l, o_s, o_r):
    return np.exp(-((((i - k) ** 2 + (j - l) ** 2) / (2.0 * o_s ** 2)) +
                    ((np.linalg.norm(image[j][i] - image[l][k]) ** 2) / (2.0 * o_r ** 2))))


# Primera vez que hago lo de colores aca, pasasr a las otras funciones de a poco
def calculate_bi_filter(pixel_array, i, j, mask, o_s, o_r):
    h, w = pixel_array.shape

    half_mask = int((mask - 1) / 2)
    my_range = np.arange(start=- 1 * half_mask, stop=half_mask + 1, step=1)

    sum_nom = 0.0
    sum_den = 0.0

    for l in my_range:
        for k in my_range:
            if 0 <= k + i < w and 0 <= l + j < h:
                wei = calculate_bi_fil_w(pixel_array, i, j, i + k, j + l, o_s, o_r)
                sum_den += wei
                sum_nom += pixel_array[j + l][i + k] * wei

    return sum_nom / sum_den


# noinspection PyUnresolvedReferences,PyTypeChecker
def bilateral_filter(image: MyImage, mask: int, o_s: float, o_r: float):
    if image is None or mask % 2 == 0:
        return

    layers = image.image.split()
    w, h = image.image.size

    pixel_array = []

    for im in layers:
        pixel_array.append(np.array(im, dtype=np.float64))

    pixel_array2 = pixel_array.copy()
    for i in range(w):
        for j in range(h):
            for k in range(len(layers)):
                pixel_array2[k][j][i] = calculate_bi_filter(pixel_array[k], i, j, mask, o_s, o_r)

    final_image = []
    for band in range(len(layers)):
        final_image.append(MyImage.numpy_to_image(pixel_array2[band], layers[band].mode))

    final = Image.merge(image.mode, final_image)
    return MyImage.from_image(final, image.dimensions)
