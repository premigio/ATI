# Se implementa en etapas:
# 1. Suavizamiento y diferenciación: Convolución con una gaussiana.
#   El primer paso es suavizar la imagen antes de realizar cualquier detección de bordes.
#   El éxito del método depende de el tamaño del filtro que se usa en este paso, en el sentido de que será más o menos
#   sensible al ruido.
# 2. Obtener la dirección perpendicular al borde.
#   En este paso se aplica el método de Sobel para encontrar las aproximaciones de las derivadas.
#   Y luego la imagen Magnitud de borde |G| = |Gx| + |Gy|
# 3. Se calcula el ángulo del gradiente, con lo cual podemos estimar la dirección ortogonal al borde.
#   φ = arctan(Gy/Gx) si Gx no es 0, φ = 0 si Gx = 0
#   Este ángulo nos indica la dirección perpendicular al borde, pero en una imagen los ángulos pueden ser:
#   0°, 45°, 90°, 135°
#   Entonces tenemos que ubicar cuál es φ entre estas posibilidades.
# 4. Supresión de no máximos
#   Para cada pixel con magnitud de borde no cero, inspeccionar los pixels adyacentes indicados en la dirección
#   ortogonal al su borde. Si la magnitud de cualquiera de los dos pixels adyacentes es mayor que la del pixel en
#   cuestión, entonces borrarlo como borde.
# 5. Umbralización con histéresis: Elimina Bordes Falsos
#   1. Elegir dos umbrales t1,t2.
#   2. Marcar todos los pixels con magnitud mayor que t2 como correctos (sí pertenecen al borde)
#   y los menores que t1 como incorrectos.
#   3. Los pixels cuya magnitud de borde está entre t1 y t2 y están conectados con un borde,
#   se marcan también como borde. La conectitud puede ser 4- conexo u 8 –conexo.
from enum import Enum

import numpy as np
from PIL import Image

from Algorithms.Classes.MyImage import MyImage, normalization
from Algorithms.EdgeDetection.EdgeDetection import get_directional_derivatives
from Algorithms.Filters.Filters import gaussian_filter

mask_h = [
    [-1, -1, -1],
    [0, 0, 0],
    [1, 1, 1]
]
mask_h = np.array(mask_h)

mask_v = [
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1]
]
mask_v = np.array(mask_v)


class Slope(Enum):
    # grado = 0 --> pend horizontal --> avanzamos en el eje x pero no en el eje y
    horizontal = [1, 0]
    # grado = 45 --> pend positiva --> avanzamos en el eje x y en el eje y
    positive = [1, 1]
    # grado = 90 --> pend vertical --> avanzamos en el eje y pero no en el eje x
    vertical = [0, 1]
    # grado = 135 --> pend negativa --> retrocedemos en el eje x y en el eje x
    negative = [-1, -1]


def canny_edge_detector(my_image: MyImage, sigma: int, threshold1: int, threshold2: int):
    if my_image is None:
        return

    # 1. Suavizamiento y diferenciación: Convolución con una gaussiana.
    filtered_img = gaussian_filter(my_image, sigma)

    # 2. Obtener la dirección perpendicular al borde. Y luego la imagen Magnitud de borde |G| = |Gx| + |Gy|
    pixel_array = np.array(my_image.image, dtype=np.float64)
    w, h = my_image.image.size
    gx, gy = get_directional_derivatives(pixel_array, w, h, mask_h, mask_v)
    g = np.hypot(gx, gy)
    g = normalization(g)

    # 3. Se calcula el ángulo del gradiente, con lo cual podemos estimar la dirección ortogonal al borde.
    # gradiente = pendiente = slope
    grad = [rad * 180 / np.pi for rad in np.arctan2(gy, gx)]
    grad = np.array(grad)
    slopes = classify_grad(grad)

    # 4. Supresión de no máximos
    no_max = max_suppression(g, slopes)

    # 5. Umbralización con histéresis
    result = threshold_edges(no_max, threshold1, threshold2)

    img2 = get_img(my_image, result)
    image = MyImage.from_image(img2, my_image.dimensions)
    return image


def classify_grad(slope: np.ndarray):
    # grados entre [-180, 180]
    classified = np.ndarray(shape=slope.shape, dtype=list)
    x, y = slope.shape

    for i in range(x):
        for j in range(y):
            grad = slope[i, j]

            # grados entre [0, 180]
            if grad < 0:
                grad += 180

            # los clasificamos en los cambios en las posiciones de píxeles que tenemos que mirar
            if grad < 22.5 or grad >= 157.5:
                classified[i, j] = Slope.horizontal

            if 22.5 <= grad < 67.5:
                classified[i, j] = Slope.positive

            if 67.5 <= grad < 112.5:
                classified[i, j] = Slope.vertical

            if 112.5 <= grad < 157.5:
                classified[i, j] = Slope.negative

    return classified


def max_suppression(g: np.ndarray, slopes: np.ndarray):
    max_suppressed = g.copy()
    w, h = g.shape

    for i in range(w):
        for j in range(h):

            slope = slopes[i, j]
            pixel0 = g[i, j]

            pos_1_x = i + slope.value[0]
            pos_1_y = j + slope.value[1]
            if 0 <= pos_1_x < w and 0 <= pos_1_y < h:
                pixel1 = g[pos_1_x, pos_1_y]
                if pixel1 > pixel0:
                    max_suppressed[i, j] = 0

            pos_2_x = i - slope.value[0]
            pos_2_y = j - slope.value[1]
            if 0 <= pos_2_x < w and 0 <= pos_2_y < h:
                pixel1 = g[pos_2_x, pos_2_y]
                if pixel1 > pixel0:
                    max_suppressed[i, j] = 0

    return max_suppressed


def threshold_edges(g: np.ndarray, threshold1: int, threshold2: int):
    edges_before = np.zeros(shape=g.shape)
    width, height = g.shape

    # sólo marco a los bordes que son mayores a t2
    for i in range(width):
        for j in range(height):
            if g[i, j] >= threshold2:
                edges_before[i, j] = 255

    edges_after = edges_before.copy()
    # sólo marco a los bordes que están conectados entre t1 y t2
    for i in range(width):
        for j in range(height):
            if threshold1 <= g[i, j] < threshold2 and is_edge_connected(edges_before, i, j):
                edges_after[i, j] = 255

    return edges_after


def is_edge_connected(edges: np.ndarray, x, y):
    # lo hago 4 conexo
    range_x = range(x - 1, x + 2)
    range_y = range(y - 1, y + 2)
    width, height = edges.shape

    for i in range_x:
        for j in range_y:
            if 0 <= i < width and 0 <= j < height and i != x and j != y:
                return edges[i, j] == 255

    return False


def get_img(my_image: MyImage, pixels: np.array):
    image = Image.new(my_image.image.mode, pixels.shape)
    width, height = pixels.shape

    for i in range(height):
        for j in range(width):
            pixel = int(pixels[i, j])
            image.putpixel((j, i), pixel)

    return image
