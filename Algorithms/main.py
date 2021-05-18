import numpy as np

from Algorithms.Classes.MyImage import MyImage
from Algorithms.EdgeDetection.Canny import canny_edge_detector
from Algorithms.EdgeDetection.Susan import susan_detector
from Algorithms.EdgeDetection.HoughTransform import *

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
    test_photo = MyImage('../Photos/TEST.pbm')

    # img = canny_edge_detector(lena_photo, 1, 0, 100)
    # img.show()

    # susan = susan_detector(test_photo, 15)
    # susan.show()
    D = max(test_photo.image.size)
    hough_line_transform(test_photo, -(2 ** 0.5) * D, (2 ** 0.5) * D, 200, size_theta=200, epsilon=2,
                         threshold_value=250, graph_accum=True,
                         graph_lines=True)
