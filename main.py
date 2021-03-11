from PIL import Image, ImageDraw
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


class MyImage:

    def __init__(self, path: str, raw_prop: (int, int) = None):
        self.path = path
        if path is not None:
            self.extension = path.split('.')[-1]
            self.image = self.my_load_image(raw_prop)
            self.pixels = self.image.load()
            # self.image_array = np.array(self.image)

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

    def my_get_pixel(self, pos: (int, int)):
        return self.image.getpixel(pos)

    def modify_pixel(self, pos: (int, ...), new_pixel):
        self.pixels[pos] = new_pixel

    def copy(self, image_to_copy, box, mask=None):
        new_image = self.image.copy()
        new_image.paste(image_to_copy, box, mask)
        return new_image

    @staticmethod
    def type_conversion(image, mode=Mode):
        return image.convert(mode)

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


sizeDict = {
    'LENA': (256, 256),
    'GIRL': (389, 164),
    'GIRL2': (256, 256),
    'BARCO': (290, 207),
    'FRACTAL': (389, 164),
}

# lena = MyImage.load_image('/Users/pedroremigiopingarilho/Desktop/ITBA/ATI/ATI/Photos/LENA.RAW', sizeDict['LENA'])
# lena2 = MyImage.load_image('/Users/pedroremigiopingarilho/Desktop/ITBA/ATI/ATI/Photos/Lenaclor.pbm')  # .show()
#
# print(MyImage.get_pixel(lena2, (100, 200)))

photo = MyImage('/Users/pedroremigiopingarilho/Desktop/ITBA/ATI/ATI/Photos/LENA.RAW', sizeDict['LENA'])
photo2 = MyImage('/Users/pedroremigiopingarilho/Desktop/ITBA/ATI/ATI/Photos/GIRL.RAW', sizeDict['GIRL'])

a = MyImage.create_circle_image(sizeDict['GIRL'])

photo.copy(photo2.image, (0, 0), a.resize(sizeDict['GIRL'])).show()
