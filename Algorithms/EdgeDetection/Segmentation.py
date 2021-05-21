# Modelos de Intercambio de Pixels
# Por cada iteración:
#   1.  Indicar la región inicial con un rectángulo dentro del objeto de interés y definir Lin y Lout.
#   2.  Para cada x en Lout, si Fd (x) > 0 entonces, borrar x de Lout y agregarlo a Lin.
#       Luego, para cada y vecino de x, con φ(y) = 3, agregar y a Lout y poner φ(y) = 1.
#   3.  Después del paso 2, algunos pixels x en Lin pudieron transformarse en interiores, entonces se borrran de Lin y
#       se asigna φ (x) = −3.
#   4.  Para cada x en Lin, si Fd (x) < 0 entonces, borrar x de Lin y agregarlo a Lout.
#       Luego, para cada y vecino de x, con φ(y) = -3, agregar y a Lin y poner φ(y) = 1.
#   5.  Después del paso 3, algunos pixels x en Lout pudieron transformarse en exteriores, entonces se borrran de Lout
#       y se asigna φ (x) = −3.
# Seguimiento en video:
# En el primer cuadro se elige el objeto a seguir con un rectángulo, ese rectángulo es la curva inicial.
# En los cuadros siguientes, la curva inicial está dada por la curva resultante del cuadro anterior.
from typing import Tuple, List

import numpy as np
from PIL.Image import Image

from Algorithms.Classes.MyImage import MyImage


class Segmentation:
    def __init__(self, my_image: MyImage, crop_area: ((int, int), (int, int)), iterations: int, epsilon: float):
        self.curr_image = my_image
        self.layers = my_image.image.split()
        self.crop_area: ((int, int), (int, int)) = crop_area
        self.iterations = iterations
        self.epsilon = epsilon
        self.lin: List[Tuple[int, int]] = []
        self.lout: List[Tuple[int, int]] = []
        self.theta_obj: Tuple[int, int, int]

        self.std_area()
        self.init_curve()
        self.theta_obj = self.theta()
        self.all_images = [self.get_image_edges()]
        self.segment()

    def std_area(self):
        crop_from, crop_to = self.crop_area
        crop_from_x, crop_from_y = crop_from
        crop_to_x, crop_to_y = crop_to
        if crop_from_x > crop_to_x:
            lower_x = crop_to_x
            higher_x = crop_from_x
        else:
            lower_x = crop_from_x
            higher_x = crop_to_x
        if crop_from_y > crop_to_y:
            lower_y = crop_to_y
            higher_y = crop_from_y
        else:
            lower_y = crop_from_y
            higher_y = crop_to_y
        self.crop_area = ((lower_x, lower_y), (higher_x, higher_y))

    def init_curve(self):

        crop_from, crop_to = self.crop_area

        for i in range(crop_from[0], crop_to[0] + 1):
            self.lout.append((i, crop_from[1]))
            self.lin.append((i, crop_from[1] + 1))
            self.lout.append((i, crop_to[1]))
            self.lin.append((i, crop_to[1] - 1))

        for j in range(crop_from[1], crop_to[1] + 1):
            self.lout.append((crop_from[0], j))
            self.lin.append((crop_from[0] + 1, j))
            self.lout.append((crop_to[0], j))
            self.lin.append((crop_to[0] - 1, j))

    def change_image(self, my_image: MyImage):
        self.curr_image = my_image
        self.layers = my_image.image.split()
        self.segment()

    def get_image_edges(self) -> MyImage:

        image = self.curr_image.image.copy()
        width, height = image.size

        for pixel in self.lin:
            new_pixel = (245, 0, 135)
            image.putpixel(pixel, new_pixel)

        for pixel in self.lout:
            new_pixel = (255, 255, 0)
            image.putpixel(pixel, new_pixel)

        return MyImage.from_image(image, (width, height))

    def get_iterations(self):
        return self.all_images

    def segment(self):

        condition = True
        iterations = 0
        while iterations < self.iterations and condition:

            condition = False

            # Step 3: Scan through the two lists Lout and Lin and update:
            new_lin = self.lin.copy()
            new_lout = self.lout.copy()

            # Outward evolution. Scan through Lout. For each point x ∈ Lout, switch_in(x) if Fˆ(x) > 0.
            for x in self.lout:
                if self.Fd(x) > 0:
                    condition = True
                    new_lout.remove(x)
                    new_lin.append(x)
                    neighbours = self.neighbours(x)
                    for y in neighbours:
                        if self.phi(y, new_lin, new_lout) == 3:
                            new_lout.append(y)

            self.lin = new_lin.copy()

            # Eliminate redundant points in Lin. Scan through Lin.
            # For each point x ∈ Lin, if ∀y ∈ N(x), φˆ(y) < 0, delete x from Lin, and set φˆ(x) = −3.
            for x in self.lin:
                any_lout = False
                for y in self.neighbours(x):
                    y_phi = self.phi(y, new_lin, new_lout)
                    if y_phi == -1:
                        any_lout = True
                        break
                if not any_lout:
                    new_lin.remove(x)

            self.lin = new_lin.copy()

            # Inward evolution. Scan through Lin. For each point x ∈ Lin, switch_out(x) if Fˆ(x) < 0.
            for x in self.lin:
                if self.Fd(x) < 0:
                    condition = True
                    new_lin.remove(x)
                    new_lout.append(x)
                    neighbours = self.neighbours(x)
                    for y in neighbours:
                        if self.phi(y, new_lin, new_lout) == -3:
                            new_lin.append(y)

            self.lout = new_lout.copy()

            # Eliminate redundant points in Lout. Scan through Lout.
            # For each point x ∈ Lout, if ∀y ∈ N(x), φˆ(y) > 0, delete x from Lout, and set φˆ(x) = 3.
            for x in self.lout:
                any_lout = False
                for y in self.neighbours(x):
                    y_phi = self.phi(y, new_lin, new_lout)
                    if y_phi == 1:
                        any_lout = True
                        break
                if not any_lout:
                    new_lout.remove(x)

            self.lout = new_lout
            self.lin = new_lin
            iterations += 1
            self.all_images.append(self.get_image_edges())

    def phi(self, pixel: Tuple[int, int], lin: List[Tuple[int, int]], lout: List[Tuple[int, int]]):

        if pixel in lin:
            return 1
        if pixel in lout:
            return -1

        fd = self.Fd(pixel)
        if fd < 0:
            return -3
        if fd >= 0:
            return 3

    def Fd(self, pixel: Tuple[int, int]):

        color = np.array([layer.getpixel((pixel[0], pixel[1])) for layer in self.layers])
        theta_norm = np.linalg.norm(color - self.theta_obj)

        if theta_norm < self.epsilon:
            return 1
        else:
            return -1

    def theta(self):

        crop_from, crop_to = self.crop_area
        colors_accum = np.zeros(len(self.layers))

        for i in range(crop_from[0], crop_to[0]):
            for j in range(crop_from[1], crop_to[1]):
                for k in range(len(self.layers)):
                    colors_accum[k] += self.layers[k].getpixel((i, j))

        x = crop_to[0] - crop_from[0]
        y = crop_to[1] - crop_from[1]

        return np.array([float(color) / (x * y) for color in colors_accum])

    def neighbours(self, pixel: Tuple[int, int]):
        w, h = self.curr_image.dimensions

        neighbours = []

        if pixel[0] - 1 >= 0:
            neighbours.append((pixel[0] - 1, pixel[1]))
        if pixel[0] + 1 < w:
            neighbours.append((pixel[0] + 1, pixel[1]))
        if pixel[1] - 1 >= 0:
            neighbours.append((pixel[0], pixel[1] - 1))
        if pixel[1] + 1 < h:
            neighbours.append((pixel[0], pixel[1] + 1))

        return neighbours
