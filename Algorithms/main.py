from TP0.image import MyImage
from Algorithms.Functions import *
from Algorithms.Noises import *
from Algorithms.Filters import *


sizeDict = {
    'LENA': (256, 256),
    'GIRL': (389, 164),
    'GIRL2': (256, 256),
    'BARCO': (290, 207),
    'FRACTAL': (389, 164),
}

if __name__ == '__main__':
    lena_photo = MyImage('../Photos/LENA.RAW', sizeDict['LENA'])
    # lena_photo.image.show()
    noise_photo = salt_n_pepper(lena_photo)
    noise_photo.image.show()
