import math
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from GUI.graph_window import GraphWindow
from PyQt5 import QtWidgets

from Algorithms.EdgeDetection.Canny import canny_edge_detector
from Algorithms.EdgeDetection.EdgeDetection import *
from Algorithms.EdgeDetection.HoughTransform import *
from Algorithms.Classes.MyImage import MyImage

# mask_size should be at least 6 * sigma + 1
from Algorithms.EdgeDetection.Segmentation import Segmentation
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
    image = susan_detector(my_image, threshold, edge_value / 100, corner_value / 100, epsilon / 100)
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


def __graph_accumulated(accumulator, x_label, y_label, window):
    sc = GraphWindow(window, width=5, height=4, dpi=100)

    sc.axes.set_xlabel(x_label)
    sc.axes.set_ylabel(y_label)

    toolbar = NavigationToolbar(sc, window)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(toolbar)
    layout.addWidget(sc)

    sb.heatmap(accumulator, cmap="Blues")

    widget = QtWidgets.QWidget()
    widget.setLayout(layout)
    widget.setWindowTitle("Hough Space")
    return widget


def __graph_final_points(pixel_array, final_points, window):
    w, h = pixel_array.shape

    sc = GraphWindow(window, width=5, height=4, dpi=100)

    for rho, theta in final_points:
        sine = np.sin(np.deg2rad(theta))
        cosine = np.cos(np.deg2rad(theta))

        if np.abs(sine) > EPSILON_SINE_COSINE and np.abs(cosine) > EPSILON_SINE_COSINE:
            x = np.array(range(0, w))
            y = (rho - x * cosine) / sine
        elif np.abs(sine) <= EPSILON_SINE_COSINE:
            x = np.full((h,), rho)
            y = np.array(range(0, h))
        else:
            x = np.array(range(0, w))
            y = np.full((w,), rho)
        sc.axes.plot(x, y)
    sc.axes.imshow(pixel_array, cmap="Greys")
    # plt.axis('off')

    toolbar = NavigationToolbar(sc, window)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(toolbar)
    layout.addWidget(sc)

    widget = QtWidgets.QWidget()
    widget.setLayout(layout)
    widget.setWindowTitle("Detected Lines")

    return widget


def show_hough_line_detector(my_image: MyImage, window):
    if my_image is None or my_image.image is None:
        return
    D = max(my_image.image.size)

    min_rho = window.ask_for_float('Choose min ρ value', default=(-(2 ** 0.5) * D), min_value=(-9999999.0), text="min ρ")
    max_rho = window.ask_for_float('Choose max ρ value', default=((2 ** 0.5) * D), text="max ρ")
    size_rho = window.ask_for_int('Choose number of ρ values', default=200, text="number of ρ")
    min_theta = window.ask_for_float('Choose min θ value', default=(-90.0), min_value=(-180.0), text="min θ")
    max_theta = window.ask_for_float('Choose max θ value', default=90.0, text="max θ")
    size_theta = window.ask_for_int('Choose number of θ values', default=200, text="number of θ")
    epsilon = window.ask_for_float('Choose a value for epsilon', default=2, text="epsilon")
    threshold_value = window.ask_for_int('Choose a value for the threshold', default=250, text="threshold")

    final_points, accumulator, pixel_array = hough_line_transform(my_image, min_rho, max_rho, size_rho, min_theta,
                                                                  max_theta,
                                                                  size_theta, epsilon=epsilon,
                                                                  threshold_value=threshold_value, graph_accum=True,
                                                                  graph_lines=False)

    # w1 = __graph_accumulated(accumulator, "ρ", "θ", window)
    w2 = __graph_final_points(pixel_array, final_points, window)

    return w2  # w1


def show_hough_circle_detector(my_image: MyImage, window):
    if my_image is None or my_image.image is None:
        return

    min_x = window.ask_for_float('Choose min x value', default=0.0, text="min x")
    max_x = window.ask_for_float('Choose max x value', default=255.0, text="max x")
    size_x = window.ask_for_int('Choose number of x values', default=64, text="number of x")
    min_y = window.ask_for_float('Choose min y value', default=0.0, text="min y")
    max_y = window.ask_for_float('Choose max y value', default=255.0, text="max y")
    size_y = window.ask_for_int('Choose number of y values', default=64, text="number of y")
    min_r = window.ask_for_float('Choose min r value', default=0.0, text="min r")
    max_r = window.ask_for_float('Choose max r value', default=180.0, text="max r")
    size_r = window.ask_for_int('Choose number of r values', default=50, text="number of r")
    epsilon = window.ask_for_float('Choose a value for epsilon', default=1, text="epsilon")
    threshold_value = window.ask_for_int('Choose a value for the threshold', default=5, text="threshold")

    hough_circle_transform(my_image, min_x, max_x, size_x, min_y, max_y, size_y, min_r, max_r, size_r, epsilon=epsilon,
                           threshold_value=threshold_value, graph_lines=True)

    return
