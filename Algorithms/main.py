from Algorithms.EdgeDetection.Harris import harris_detector
from Algorithms.EdgeDetection.HoughTransform import *

sizeDict = {
    'LENA': (256, 256),
    'GIRL': (389, 164),
    'GIRL2': (256, 256),
    'BARCO': (290, 207),
    'FRACTAL': (389, 164),
}

# Explicar Canny, Susan, Hough <-- probar parametros menores, y con ruido. Que se vea el video

if __name__ == '__main__':
    lena_photo = MyImage('../Photos/LENA.RAW', sizeDict['LENA'])
    photo = MyImage('../Photos/Lenaclor.pbm')
    test_photo = MyImage('../Photos/TEST.pbm')
    square = MyImage('../Photos/cuadrado.png')

    harris = harris_detector(test_photo, 2, 0.04, 97.0)
    harris.image.show()
