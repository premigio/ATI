from Algorithms.Filters import *
from Algorithms.Functions import *
from Algorithms.Noises import *
from Algorithms.BorderDetection import *
from Algorithms.DiffusionFilters import *
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
    #lena_photo.image.show()
    # lena_photo.show()
    # Para imagenes color. TODO ver que onda umbralizar pq ndeah
    # photos = photo.image.split()
    # final_image = []
    # for window in range(len(photos)):
    #     final_image.append(prewitt_sobel_filters(MyImage.from_image(photos[window]), False).image)
    # final = Image.merge(photo.mode, final_image)
    # final.show()
    # prewitt_sobel_filters(lena_photo, True).image.show()
    fin = anisotropic(lena_photo, FunctionDiff.LECLERC, 5.0, 50)
    histogram(fin, True)
    fin.image.show()

    # a = bilateral_filter(photo, 7, 2, 30)
    # a.image.show()
