from TP0.image import MyImage
from Algorithms.Functions import *
from Algorithms.Noises import *
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

photo = MyImage('../Photos/LENA.RAW', sizeDict['LENA'])
photo2 = MyImage('../Photos/Lenaclor.pbm', sizeDict['LENA'])

photo.image.show()
eq_photo = rayleigh_multiplicative(photo, 0.2, 0.5)
eq_photo.image.show()
