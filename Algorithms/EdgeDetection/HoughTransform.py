import numpy as np
from PIL import Image
import seaborn as sb
import matplotlib.pyplot as plt

from Algorithms.Classes.MyImage import MyImage, normalization
from Algorithms.Thresholding import otsu_thresholding
from Algorithms.EdgeDetection.EdgeDetection import prewitt_sobel_filters


def sobel(image):
    return prewitt_sobel_filters(image, False)


def prewitt(image):
    return prewitt_sobel_filters(image, True)


def graph_accumulated2d(accumulator, x_label, y_label):
    sb.heatmap(accumulator, cmap="Blues"
               # , xticklabels=np.array(r_range),
               # yticklabels=np.array(t_range)
               )
    plt.title("Hough Space")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def graph_accumulated3d(accumulator, x_label, y_label, z_label):
    sb.heatmap(accumulator, cmap="Blues"
               # , xticklabels=np.array(r_range),
               # yticklabels=np.array(t_range)
               )
    plt.title("Hough Space")
    ax = plt.axes(projection="3d")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.zlabel(z_label)
    plt.show()


EPSILON_SINE_COSINE = 0.01


# https://towardsdatascience.com/lines-detection-with-hough-transform-84020b3b1549
def hough_line_transform(image: MyImage, min_rho: float, max_rho: float, size_rho: int = 1,
                         min_theta: float = -90.0, max_theta: float = 90.0, size_theta: int = 1,
                         threshold_function=otsu_thresholding, border_detection_function=sobel,
                         epsilon: float = 1.0,  # el epsilon lo necesito para encajar en la posicion especifica
                         threshold_value=200, graph_accum=False, graph_lines=False):
    if image is None:
        return

    image = border_detection_function(image)  # Busco los bordes
    image, _ = threshold_function(image)  # Umbral para dejar los valores con 0s y 255s

    pixel_array = np.array(image.image, dtype=np.float64)
    w, h = image.image.size

    t_range = np.linspace(min_theta, max_theta, size_theta)
    r_range = np.linspace(min_rho, max_rho, size_rho)
    accumulator = np.zeros(shape=(r_range.shape[0], t_range.shape[0]))  # inicio el accumulator con 0s

    for pixel_x in range(w):
        for pixel_y in range(h):
            if pixel_array[pixel_y][pixel_x] == 255:  # si es un punto blanco
                for j, theta in enumerate(t_range):
                    calculated_rho = pixel_x * np.cos(np.deg2rad(theta)) + pixel_y * np.sin(np.deg2rad(theta))
                    for i, rho in enumerate(r_range):
                        if np.abs(rho - calculated_rho) <= epsilon:
                            accumulator[i][j] += 1

    if graph_accum:
        graph_accumulated2d(accumulator, "ρ", "θ")

    final_points = []  # en el formato (ρ, θ)

    for j, theta in enumerate(t_range):
        for i, rho in enumerate(r_range):
            if accumulator[i][j] >= threshold_value:
                final_points.append((rho, theta))

    if graph_lines:
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
            plt.plot(x, y)
        plt.imshow(pixel_array, cmap="Greys")
        # plt.axis('off')
        plt.title("Detected Lines")
        plt.show()

    return final_points


def hough_circle_transform(image: MyImage, min_x: float, max_x: float, size_x: int,
                           min_y: float, max_y: float, size_y: int,
                           min_r: float, max_r: float, size_r: int,
                           threshold_function=otsu_thresholding, border_detection_function=sobel,
                           epsilon: float = 1.0,  # el epsilon lo necesito para encajar en la posicion especifica
                           threshold_value=200, graph_lines=False):
    if image is None:
        return

    image = border_detection_function(image)  # Busco los bordes
    image, _ = threshold_function(image)  # Umbral para dejar los valores con 0s y 255s

    pixel_array = np.array(image.image, dtype=np.float64)
    w, h = image.image.size

    x_range = np.linspace(min_x, max_x, size_x)
    y_range = np.linspace(min_y, max_y, size_y)
    r_range = np.linspace(min_r, max_r, size_r)
    accumulator = np.zeros(shape=(x_range.shape[0], y_range.shape[0], r_range.shape[0]))  # inicio el accumulator con 0s

    for pixel_x in range(w):
        for pixel_y in range(h):
            if pixel_array[pixel_y][pixel_x] == 255:  # si es un punto blanco
                for i, x in enumerate(x_range):
                    for j, y in enumerate(y_range):
                        for k, r in enumerate(r_range):
                            circle = (pixel_x - x) ** 2 + (pixel_y - y) ** 2 - r ** 2
                            if np.abs(circle) <= epsilon:
                                accumulator[i][j][k] += 1

    final_points = []  # en el formato (x, y, r)

    for i, x in enumerate(x_range):
        for j, y in enumerate(y_range):
            for k, r in enumerate(r_range):
                if accumulator[i][j][k] >= threshold_value:
                    final_points.append((x, y, r))

    if graph_lines:
        axis = plt.gca()
        for x, y, r in final_points:
            c = plt.Circle((x, y), r, color='r', fill=False)
            axis.add_artist(c)
        plt.title("Detected Circles")
        plt.imshow(pixel_array, cmap="Greys")
        plt.show()

    return final_points
