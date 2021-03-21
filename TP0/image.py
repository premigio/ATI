import os
from typing import List

from PIL import Image, ImageDraw, ImageChops
import numpy as np
from enum import Enum


class Mode(Enum):
    ONE = '1'
    L = 'L'
    P = 'P'
    RGB = 'RGB'
    HSV = 'HSV'
    LAB = 'LAB'
    RGBA = 'RGBA'


def normalization(arr):
    macs = np.max(arr)
    mim = np.min(arr)

    if macs - mim == 0:
        return arr
    m = 255 / (macs - mim)
    c = - m * mim

    return arr * m + c


def photo_combination(image1: Image, image2: Image, function):
    i1array = np.array(image1)
    i2array = np.array(image2)

    i1af = i1array.astype('float')
    i2af = i2array.astype('float')

    addition = function(i1af, i2af)

    return Image.fromarray(normalization(addition).astype('uint8'))


class MyImage:

    def __init__(self, path: str, raw_prop: (int, int) = None):
        self.path = path
        if path is not None:
            self.file_name = os.path.basename(path)
            self.extension = path.split('.')[-1]
            self.image = self.my_load_image(raw_prop)
            self.pixels = self.image.load()
            self.mode = self.image.mode
            # self.image_array = np.array(self.image)

        if raw_prop is not None:
            self.dimensions = raw_prop
        else:
            self.dimensions = self.image.size

    def my_load_image(self, raw_prop: (int, int) = (256, 256)):
        if self.extension.lower() == 'raw':
            file = open(self.path, "rb")
            img = Image.frombytes(mode="L", size=raw_prop, data=file.read())  # mode=L es 8-bit pixels, black and white
        else:
            img = Image.open(self.path)
        return img

    @staticmethod
    def load_image(path: str, raw_prop: (int, int) = (256, 256)):
        if path is None:
            return
        extension = path.split('.')[-1]
        if extension.lower() == 'raw':
            file = open(path, "rb")
            img = Image.frombytes(mode="L", size=raw_prop, data=file.read())  # mode=L es 8-bit pixels, black and white
        else:
            img = Image.open(path)
        return img

    def my_save_image(self, path: str):
        self.image.save(path)

    @staticmethod
    def save_image(image: Image, path: str):
        if image is None:
            print("image is None")
            return
        image.save(path)

    @staticmethod
    def get_pixel(image: Image, pos: (int, int)):
        return image.getpixel(pos)

    @staticmethod
    def is_grey_scale(image: Image):
        img = image.copy().convert('RGB')
        w, h = img.size
        for i in range(w):
            for j in range(h):
                r, g, b = img.getpixel((i, j))
                if r != g != b:
                    return False
        return True

    def my_get_pixel(self, pos: (int, int)):
        return self.image.getpixel(pos)

    def modify_pixel(self, pos: (int, ...), new_pixel):
        self.pixels[pos] = new_pixel

    def copy(self, image_to_copy, box, mask=None):
        new_image = self.image.copy()
        new_image.paste(image_to_copy, box, mask)
        return new_image

    @staticmethod
    def add_photos(image1: Image, image2: Image):
        return photo_combination(image1, image2, lambda x, y: x + y)

    @staticmethod
    def subtract_photos(image1: Image, image2: Image):
        return photo_combination(image1, image2, lambda x, y: x - y)

    @staticmethod
    def multiply_photos(image1: Image, image2: Image):
        return photo_combination(image1, image2, lambda x, y: x * y)

    @staticmethod
    def add_photos_lib(image1: Image, image2: Image):
        return Image.blend(image1, image2, 0.5)

    @staticmethod
    def type_conversion(image, mode: Mode = Mode.HSV):
        return image.convert(mode.value)

    @staticmethod
    def create_square_image(size: (int, int) = (200, 200), mode: str = "L"):
        image = Image.new(mode, size)
        draw = ImageDraw.Draw(image)
        draw.rectangle(((size[0] / 2) - (size[0] / 4),
                        (size[1] / 2) - (size[1] / 4),
                        (size[0] / 2) + (size[0] / 4),
                        (size[1] / 2) + (size[1] / 4)), fill=255)
        return image

    @staticmethod
    def create_circle_image(size: (int, int) = (200, 200), mode: str = "L"):
        image = Image.new(mode, size)
        draw = ImageDraw.Draw(image)
        draw.ellipse(((size[0] / 2) - (size[0] / 4),
                      (size[1] / 2) - (size[1] / 4),
                      (size[0] / 2) + (size[0] / 4),
                      (size[1] / 2) + (size[1] / 4)), fill=255)
        return image

    @staticmethod
    def numpy_to_image(array: List[List[tuple]], mode: str = "RGB"):
        w = len(array)
        h = len(array[0])

        image = Image.new(mode, (w, h))
        pix = image.load()
        for i in range(len(array)):
            for j in range(len(array[i])):
                pix[(i, j)] = int(array[j][i]) if array[j][i].shape == () else tuple(array[j][i])

        return image
