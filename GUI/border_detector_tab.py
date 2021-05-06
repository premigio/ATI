import math

from Algorithms.EdgeDetection.Canny import canny_edge_detector
from Algorithms.EdgeDetection.EdgeDetection import *
from Algorithms.Classes.MyImage import MyImage

# mask_size should be at least 6 * sigma + 1
from Algorithms.EdgeDetection.Susan import susan_detector


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


def show_laplacian_detector(my_image: MyImage, window):
    laplacian_mask = [[0, -1, 0],
                      [-1, 4, -1],
                      [0, -1, 0]]

    laplacian_mask = np.array(laplacian_mask)

    image = laplacian_edge_detector(my_image, laplacian_mask)
    image.image.show()
    return image


def show_laplacian_slope_detector(my_image: MyImage, window):
    laplacian_mask = [[0, -1, 0],
                      [-1, 4, -1],
                      [0, -1, 0]]

    laplacian_mask = np.array(laplacian_mask)

    threshold = window.ask_for_int('Choose a threshold value',
                                   default=30, min_value=0.0, text='Threshold')

    image = laplacian_edge_detector(my_image, laplacian_mask, threshold=threshold)
    image.image.show()
    return image


def show_laplacian_gauss_detector(my_image: MyImage, window):
    sigma = window.ask_for_int('Choose a sigma value',
                               default=1, min_value=1, text='Sigma')

    threshold = window.ask_for_int('Choose a threshold value',
                                   default=30, min_value=0, text='Threshold')

    mask = log_mask(sigma, sigma * 6 + 1)
    image = laplacian_edge_detector(my_image, mask, threshold)
    image.image.show()
    return image


def __prewit_sobel_aux(my_image: MyImage, prewitt):
    if my_image is None:
        return
    photos = my_image.image.split()
    final_image = []
    for window in range(len(photos)):
        if prewitt is not None:
            final_image.append(prewitt_sobel_filters(MyImage.from_image(photos[window]), prewitt).image)
        else:
            final_image.append(all_directions(MyImage.from_image(photos[window])).image)
    final = Image.merge(my_image.mode, final_image)
    final.show()
    return MyImage.from_image(final)


def show_prewitt_detector(my_image: MyImage, window):
    return __prewit_sobel_aux(my_image, True)


def show_sobel_detector(my_image: MyImage, window):
    return __prewit_sobel_aux(my_image, False)


def show_directional_border(my_image: MyImage, window):
    return __prewit_sobel_aux(my_image, None)


def show_susan_detector(my_image: MyImage, window):
    threshold = window.ask_for_int('Choose a threshold value',
                                   default=15, min_value=0, text='Threshold')
    edge_value = window.ask_for_int('Choose an edge value',
                                    default=50, min_value=0, max_value=100, text='Edge')
    corner_value = window.ask_for_int('Choose a corner value',
                                      default=75, min_value=0, max_value=100, text='Corner')
    epsilon = window.ask_for_int('Choose an epsilon value',
                                      default=10, min_value=0, max_value=100, text='Corner')
    image = susan_detector(my_image, threshold, edge_value/100, corner_value/100, epsilon/100)
    image.image.show()
    return image


def show_canny_detector(my_image: MyImage, window):
    sigma = window.ask_for_int('Choose a sigma value',
                               default=1, min_value=1, text='Sigma')

    threshold1 = window.ask_for_int('Choose a threshold value',
                                    default=30, min_value=0, text='Threshold 1')

    threshold2 = window.ask_for_int('Choose a threshold value',
                                    default=100, min_value=0, text='Threshold 2')

    image = canny_edge_detector(my_image, sigma, threshold1, threshold2)
    image.image.show()
    return image
