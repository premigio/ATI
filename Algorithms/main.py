from Algorithms.Filters import *
from Algorithms.Functions import *
from Algorithms.Noises import *
from Algorithms.BorderDetection import *
from TP0.image import MyImage

sizeDict = {
    'LENA': (256, 256),
    'GIRL': (389, 164),
    'GIRL2': (256, 256),
    'BARCO': (290, 207),
    'FRACTAL': (389, 164),
}

if __name__ == '__main__':
    lena_photo = MyImage('../Photos/LENA.RAW', sizeDict['LENA'])
    photo = MyImage('../Photos/Lenaclor.pbm')
    # lena_photo.image.show()

    # Para imagenes. TODO ver que onda umbralizar pq ndeah
    # photos = photo.image.split()
    # final_image = []
    # for window in range(len(photos)):
    #     final_image.append(prewitt_sobel_filters(MyImage.from_image(photos[window]), False).image)
    # final = Image.merge(photo.mode, final_image)
    prewitt_sobel_filters(lena_photo, True).image.show()
