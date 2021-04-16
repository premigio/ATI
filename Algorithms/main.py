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
    photo = MyImage('../Photos/TEST.pbm')
    # lena_photo.image.show()
    noise_photo = prewitt_sobel_filters(lena_photo, False)
    noise_photo.image.show()
