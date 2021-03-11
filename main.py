from PIL import Image
import numpy as np


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

    def copy(self, image1, image2):
        pass

    @staticmethod
    def create_square_image(size: (int, int) = (200, 200), mode: str = "L"):
        image = Image.new(mode, size)
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

photo = MyImage('/Users/pedroremigiopingarilho/Desktop/ITBA/ATI/ATI/Photos/Lenaclor.pbm', sizeDict['LENA'])
photo.modify_pixel((2, 2), (0, 0, 0))
photo.image.show()

# MyImage.create_square_image().show()