from Algorithms.ObjectDetection.Kaze import akaze
from Algorithms.ObjectDetection.Sift import *
from Algorithms.Classes.MyImage import *

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
    arc0 = MyImage('../Photos/similar_photos/arc/arc0.png')
    arc1 = MyImage('../Photos/similar_photos/arc/arc1.png')

    imtest1 = MyImage('../Photos/similar_photos/test_image/imagenPrueba.png')
    imtest2 = MyImage('../Photos/similar_photos/test_image/imagenPruebaBlur.png')
    imtest3 = MyImage('../Photos/similar_photos/test_image/imagenPruebaLight.png')
    imtest4 = MyImage('../Photos/similar_photos/test_image/imagenPruebaRotada.png')

    alonso1 = MyImage('../Photos/similar_photos/Alonso/Alonso_ElPintorCaminante.jpg')
    alonso2 = MyImage('../Photos/similar_photos/Alonso/ElCaminanteAlonso.jpg')
    alonso3 = MyImage('../Photos/similar_photos/Alonso/ElCaminanteAlonso2.jpg')
    alonso4 = MyImage('../Photos/similar_photos/Alonso/ElCaminanteAlonso3.jpg')

    square = MyImage('../Photos/cuadrado.png')

    # harris = harris_detector(test_photo, 2, 0.04, 97.0)
    # harris.image.show()
    _, equal = akaze(arc0, arc1, show_detected_keypoints=True)
    print(equal)
