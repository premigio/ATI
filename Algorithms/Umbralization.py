# a) Umbralizaci ́on Global
# b) M ́etodo de umbralizaci ́on de Otsu.
# c) M ́etodo de umbralizaci ́on multinivel de Otsu aplicado a ima ́genes en color (RGB).
import numpy as np
from PIL import Image

from Algorithms import Utils

from Classes.MyImage import MyImage


def global_thresholding(my_image: MyImage, delta_t: float):
    if my_image is None:
        return

    iterations = 0
    prev_t = float('inf')

    width, height = my_image.dimensions
    array_img = []

    for i in range(height):
        for j in range(width):
            array_img.append(my_image.image.getpixel((i, j)))

    curr_t = get_mean(array_img, height * width)

    while abs(prev_t - curr_t) > delta_t:
        prev_t = curr_t
        curr_t = get_threshold(my_image.image, curr_t)
        iterations += 1

    img_thr = MyImage.threshold(my_image.image, int(curr_t))
    image = MyImage.from_image(img_thr, my_image.dimensions)

    return image, int(curr_t), iterations


def get_groups(image: Image, threshold: float):
    width, height = image.size
    pixel_array_lower = []
    pixel_array_higher = []

    for i in range(height):
        for j in range(width):
            if image.getpixel((i, j)) < threshold:
                pixel_array_lower.append(image.getpixel((i, j)))
            else:
                pixel_array_higher.append(image.getpixel((i, j)))

    return pixel_array_higher, pixel_array_lower


def get_threshold(image: Image, threshold: float):
    g1, g2 = get_groups(image, threshold)
    n_g1 = len(g1)
    n_g2 = len(g2)

    m1 = get_mean(g1, n_g1)
    m2 = get_mean(g2, n_g2)

    return 0.5 * (m1 + m2)


def get_mean(array: [], size: int):
    m = 0
    for i in range(size):
        m += array[i]

    return m / size


def otsu_thresholding(my_image: MyImage):
    if my_image is None:
        return

    layers = my_image.image.split()

    final_images = []
    final_ts = []

    for im in layers:
        img, t = get_otsu_threshold(im)
        final_images.append(img)
        final_ts.append(t)

    final = Image.merge(my_image.mode, final_images)

    return MyImage.from_image(final, my_image.dimensions), final_ts


def get_otsu_threshold(image):
    my_image = MyImage.from_image(image, image.size)

    acum_hist, hist = get_acum_histogram(my_image)
    acum_media = get_acum_media(hist)
    global_media = acum_media[-1]

    var = []
    # para cada valor posible de umbral t en [0, ..., 255]
    for t in range(256):
        if not np.isclose((acum_hist[t] * (1 - acum_hist[t])), 0):
            var_t = ((global_media * acum_hist[t] - acum_media[t]) ** 2) / (acum_hist[t] * (1 - acum_hist[t]))
            var.append(var_t)

    variance = np.array(var)
    arg_max = np.argwhere(variance == max(variance))
    t = sum(arg_max) / len(arg_max)

    img_thr = MyImage.threshold(image, int(t[0]))

    return img_thr, t[0]


def get_acum_histogram(my_image: MyImage):
    histogram = Utils.histogram(my_image)

    acum_histogram = np.zeros(len(histogram), dtype=float)

    for i in range(len(histogram)):
        for j in range(i + 1):
            acum_histogram[i] += histogram[j]

    return acum_histogram, histogram


def get_acum_media(prob_dist: []):
    acum_media = np.zeros(len(prob_dist), dtype=float)
    for i in range(256):
        for j in range(i + 1):
            acum_media[i] += j * prob_dist[j]

    return acum_media
