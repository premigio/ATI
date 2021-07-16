import time

from Algorithms.ObjectDetection.Kaze import akaze, kaze
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

    boat1 = MyImage('../Photos/boat/img1.jpg')
    boat2 = MyImage('../Photos/boat/img2.jpg')
    boat3 = MyImage('../Photos/boat/img3.jpg')
    boat4 = MyImage('../Photos/boat/img4.jpg')
    boat5 = MyImage('../Photos/boat/img5.jpg')
    boat6 = MyImage('../Photos/boat/img6.jpg')

    boat_dataset = [boat1, boat2, boat3, boat4, boat5, boat6]

    iguazu1 = MyImage('../Photos/iguazu/img1.jpg')
    iguazu2 = MyImage('../Photos/iguazu/img2.jpg')
    iguazu3 = MyImage('../Photos/iguazu/img3.jpg')
    iguazu4 = MyImage('../Photos/iguazu/img4.jpg')
    iguazu5 = MyImage('../Photos/iguazu/img5.jpg')
    iguazu6 = MyImage('../Photos/iguazu/img6.jpg')

    iguazu_dataset = [iguazu1, iguazu2, iguazu3, iguazu4, iguazu5, iguazu6]

    for i in range(5):
        img1 = iguazu_dataset[0]
        img2 = iguazu_dataset[i+1]

        print("Iguazu dataset img1 vs. img" + str(i+2))

        startTime = time.time()
        _, equal = kaze(img1, img2, show_detected_keypoints=True)
        finishTime = round(time.time() - startTime, 2)
        print("Time: " + str(finishTime))
        print("Equal: " + str(equal))
